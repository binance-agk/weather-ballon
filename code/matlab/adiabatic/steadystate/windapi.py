import sys

import netCDF4
import numpy as np
from scipy.interpolate import Rbf
import os


files=[]

for file in os.listdir("./"):
    # print(file)
    if file.endswith(".nc"):
        print(len(files), file)
        files.append(os.path.abspath(file))
if len(files)>0:
    test2word = input("select index of your desired file(0|1|2|...) ")
    ind = int(test2word)
    print(ind)

filename = files[ind]
f = netCDF4.Dataset(str(filename))
MAXLAYERNUMBER = 31

href = [48165.21, 42772.97, 39671.37, 35876.543, 33472.727, 31007.893, 26436.203, 23853.016, 20643.412, 18544.133,
        16327.822, 13822.03, 12068.036, 10653.013, 9439.774, 8373.583, 7419.694, 6556.828, 5765.28, 5031.6753,
        4349.6113, 3713.6584, 3117.0637, 2554.485, 2022.0889, 1520.427, 1050.7377, 823.6616, 601.1975, 310.89972,
        80.58687]
pref = [100., 200., 300., 500., 700., 1000., 2000., 3000., 5000.,
        7000., 10000., 15000., 20000., 25000., 30000., 35000., 40000., 45000.,
        50000., 55000., 60000., 65000., 70000., 75000., 80000., 85000., 90000.,
        92500., 95000., 97500., 100000.]



def getclosest_ij(lats, lons, latpt, lonpt):
    # find squared distance of every point on grid
    dist_sq_lat = (lats - latpt) ** 2
    dist_sq_lon = (lons - lonpt) ** 2
    # 1D index of minimum dist_sq element
    minindex_flattened_lat = dist_sq_lat.argmin()
    minindex_flattened_lon = dist_sq_lon.argmin()
    # Get 2D index for latvals and lonvals arrays from 1D index
    return (minindex_flattened_lat, minindex_flattened_lon)


def closest_isobariclevels_to(f, lats, lons, lat0, lon0, h):
    hi = []
    for gi in range(MAXLAYERNUMBER):
        hi.append((href[gi] - h) ** 2)
    hi = np.array(hi)
    bestLayer = hi.argmin()
    return bestLayer


def upanddownofthislayer(index, limit):
    if (limit + index) > MAXLAYERNUMBER:
        return (index - limit, MAXLAYERNUMBER - 1)
    elif (index - limit) < 0:
        return (0, limit + index)
    else:
        return (index - limit, limit + index)


# //get properties of atmosphere in interpolated levels for lat lon height point of the world
def getVariableRbf(f, varkey, lat0, lon0, h0, limitangle, limitinterpolateforlayer):
    # Temperature_isobaric(time, isobaric6, latitude, longitude)
    lat, lon = f.variables['lat'], f.variables['lon']
    lats = lat[:]
    lons = lon[:]
    iTR, jTR = getclosest_ij(lats, lons, lat0, lon0)
    # print(iTR, jTR)
    # broad cast grid
    # creating (x,y)->z for interpolating
    x = []
    y = []
    h = []
    target = []
    bestlevel = closest_isobariclevels_to(f, lats, lons, lat0, lon0, h0)

    if limitinterpolateforlayer == 0:
        variable = f.variables[varkey][0][bestlevel]
        return variable[iTR][jTR]

    down, up = upanddownofthislayer(bestlevel, limit=limitinterpolateforlayer)
    if limitinterpolateforlayer == 0:
        down = bestlevel
        up = bestlevel + 1
    down = bestlevel

    print('do up levels', bestlevel, down, up)

    # for ih in range(bestlevel, bestlevel + 1):
    for ih in range(down, up):
        variable = f.variables[varkey][0][ih]
        geo = f.variables['Geopotential_height_isobaric'][0][ih]
        for i in range(-limitangle, limitangle + 1):
            for j in range(-limitangle, limitangle + 1):
                x.append(lats[iTR + i])
                y.append(lons[jTR + j])
                h.append(geo[iTR + i][jTR + j])
                target.append(variable[iTR + i][jTR + j])
    if len(target) == 1:
        return target[0]
    rbf = Rbf(x, y, h, target, epsilon=1)
    val = rbf(lat0, lon0, h0)
    return val


# //get properties of atmosphere in interpolated levels for lat lon height point of the world
def getTVPVariableRbf(f, lat0, lon0, h0, limitangle, limitinterpolateforlayer):
    # Temperature_isobaric(time, isobaric6, latitude, longitude)
    lat, lon = f.variables['lat'], f.variables['lon']
    lats = lat[:]
    lons = lon[:]
    iTR, jTR = getclosest_ij(lats, lons, lat0, lon0)
    # print(iTR, jTR)
    # broad cast grid
    # creating (x,y)->z for interpolating
    x = []
    y = []
    h = []
    t = []
    p = []
    vv = []
    vu = []
    bestlevel = closest_isobariclevels_to(f, lats, lons, lat0, lon0, h0)

    if limitinterpolateforlayer == 0:
        T = f.variables['Temperature_isobaric'][0][bestlevel]
        Vu = f.variables['u-component_of_wind_isobaric'][0][bestlevel]
        Vv = f.variables['v-component_of_wind_isobaric'][0][bestlevel]
        P = pref[bestlevel]
        hnex=f.variables["Geopotential_height_isobaric"][0][bestlevel - 1][iTR][jTR];
        if hnex<0:
            hnex=0.0
        print([Vv[iTR][jTR], Vu[iTR][jTR], T[iTR][jTR], P,hnex])
        return [Vv[iTR][jTR], Vu[iTR][jTR], T[iTR][jTR], P,hnex+200]

    down, up = upanddownofthislayer(bestlevel, limit=limitinterpolateforlayer)
    if limitinterpolateforlayer == 0:
        down = bestlevel
        up = bestlevel + 1
    down = bestlevel

    print('do up levels', bestlevel, down, up)

    # for ih in range(bestlevel, bestlevel + 1):
    for ih in range(down, up):
        T = f.variables['Temperature_isobaric'][0][ih]
        Vu = f.variables['u-component_of_wind_isobaric'][0][ih]
        Vv = f.variables['v-component_of_wind_isobaric'][0][ih]
        P = pref[ih]
        geo = f.variables['Geopotential_height_isobaric'][0][ih]
        for i in range(-limitangle, limitangle + 1):
            for j in range(-limitangle, limitangle + 1):
                x.append(lats[iTR + i])
                y.append(lons[jTR + j])
                h.append(geo[iTR + i][jTR + j])
                t.append(T[iTR + i][jTR + j])
                vv.append(Vu[iTR + i][jTR + j])
                vu.append(Vv[iTR + i][jTR + j])
                p.append(P)

    rbft = Rbf(x, y, h, t, epsilon=1)
    rbfvv = Rbf(x, y, h, vv, epsilon=1)
    rbfvu = Rbf(x, y, h, vu, epsilon=1)
    rbfp = Rbf(x, y, h, p, epsilon=1)
    val = [rbfvv(lat0, lon0, h0).min(), rbfvu(lat0, lon0, h0).min(), rbft(lat0, lon0, h0).min(),
           rbfp(lat0, lon0, h0).min()]
    print(val)
    return val


from bottle import route, run


@route("/value/<var>/<lat0>/<lon0>/<h0>/<limitangle>/<limitinterpolateforlayer>")
def d9(var, lat0, lon0, h0, limitangle, limitinterpolateforlayer):
    try:
        lat0, lon0, h0, limitangle, limitinterpolateforlayer = float(lat0), float(lon0), float(h0), int(
            limitangle), int(limitinterpolateforlayer)
        if lon0 < 0:
            lon0 = 360 + lon0
        rbf = getVariableRbf(f, var, lat0, lon0, h0, limitangle, limitinterpolateforlayer)

        return str(rbf)
    except MemoryError as err:
        return err.__str__()


@route("/allvalue/<lat0>/<lon0>/<h0>/<limitangle>/<limitinterpolateforlayer>")
def ned(lat0, lon0, h0, limitangle, limitinterpolateforlayer):
    try:
        lat0, lon0, h0, limitangle, limitinterpolateforlayer = float(lat0), float(lon0), float(h0), int(
            limitangle), int(limitinterpolateforlayer)
        if lon0 < 0:
            lon0 = 360 + lon0
        rbf = getTVPVariableRbf(f, lat0, lon0, h0, limitangle, limitinterpolateforlayer)

        return str(rbf)
    except MemoryError as err:
        return err.__str__()


@route("/ned/<var>/<xn>/<ye>/<zd>/<limitangle>/<limitinterpolateforlayer>")
def d9(var, lat0, lon0, h0, limitangle, limitinterpolateforlayer):
    try:
        lat0, lon0, h0, limitangle, limitinterpolateforlayer = float(lat0), float(lon0), float(h0), int(
            limitangle), int(limitinterpolateforlayer)
        if lon0 < 0:
            lon0 = 360 + lon0
        rbf = getVariableRbf(f, var, lat0, lon0, h0, limitangle, limitinterpolateforlayer)

        return str(rbf)
    except Exception as err:
        return err.__str__()


# getVariableRbf(f, 'v-component_of_wind_isobaric', lat0, lon0, 3000, 0,1)

run(host='localhost', port=8080 ,quiet=True)
