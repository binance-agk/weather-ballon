import netCDF4

# f = netCDF4.Dataset('GFS_Global_0p5deg_ana_20200508_1800.grib23.nc')
from scipy.interpolate import Rbf

f = netCDF4.Dataset('stream_1111.nc')
import matplotlib.pyplot as plt

plt.plot(f.variables['u-component_of_wind_isobaric'][0][0][111])
plt.show()
plt.plot(f.variables['Temperature_isobaric'][0][0][111])
plt.show()

lat, lon = f.variables['lat'], f.variables['lon']
lats = lat[:]
lons = lon[:]


def getclosest_ij(lats, lons, latpt, lonpt):
    # find squared distance of every point on grid
    dist_sq_lat = (lats - latpt) ** 2
    dist_sq_lon = (lons - lonpt) ** 2
    # 1D index of minimum dist_sq element
    minindex_flattened_lat = dist_sq_lat.argmin()
    minindex_flattened_lon = dist_sq_lon.argmin()
    # Get 2D index for latvals and lonvals arrays from 1D index
    return (minindex_flattened_lat, minindex_flattened_lon)


MAXLAYERNUMBER = 31


def closest_isobariclevels_to(f, lats, lons, lat0, lon0, h):
    i, j = getclosest_ij(lats, lons, lat0, lon0)
    hi = []
    for gi in range(MAXLAYERNUMBER):
        geo = f.variables['Geopotential_height_isobaric'][0][gi]
        hi.append((geo[i][j] - h) ** 2)
    import numpy
    hi = numpy.array(hi)
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
    lat, lon = f.variables['latitude'], f.variables['longitude']
    lats = lat[:]
    lons = lon[:]
    iTR, jTR = getclosest_ij(lats, lons, lat0, lon0)
    # broad cast grid
    # creating (x,y)->z for interpolating
    x = []
    y = []
    h = []
    target = []
    bestlevel = closest_isobariclevels_to(f, lats, lons, lat0, lon0, h0)
    down, up = upanddownofthislayer(bestlevel, limit=limitinterpolateforlayer)
    for ih in range(down, up):
        variable = f.variables[varkey][0][ih]
        geo = f.variables['Geopotential_height_isobaric'][0][ih]
        for i in range(-limitangle, limitangle + 1):
            for j in range(-limitangle, limitangle + 1):
                x.append(lats[iTR + i])
                y.append(lons[jTR + j])
                h.append(geo[iTR + i][jTR + j])
                target.append(variable[iTR + i][jTR + j])

    rbf = Rbf(x, y, h, target, epsilon=1)
    return rbf


# creating a grid for interpolating
# top right
lat0 = 35
lon0 = -50

iTR, jTR = getclosest_ij(lats, lons, lat0, lon0)
radiusAngle = 0
# broad cast grid
# creating (x,y)->z for interpolating
x = []
y = []
h = []
target = []

# Temperature_isobaric(time, isobaric6, latitude, longitude)

for ih in range(25, 28):
    variable = f.variables['v-component_of_wind_isobaric'][0][ih]
    geo = f.variables['Geopotential_height_isobaric'][0][ih]
    for i in range(-radiusAngle, radiusAngle + 1):
        for j in range(-radiusAngle, radiusAngle+1):
            x.append(lats[iTR + i])
            y.append(lons[jTR + j])
            h.append(geo[iTR + i][jTR + j])
            target.append(variable[iTR + i][jTR + j])

rbf = Rbf(x, y, h, target, epsilon=1)

plt.plot(target, 'bo')
plt.plot(rbf(x, y, h), 'r+')
plt.show()

plt.plot(x, target, 'bo')
plt.plot(x, rbf(x, y, h), 'r+')
plt.show()
plt.plot(y, target, 'yo')
plt.plot(y, rbf(x, y, h), 'r+')
plt.show()
plt.plot(h, target, 'go')
plt.plot(h, rbf(x, y, h), 'r+')
plt.show()
