import ast
from math import sqrt
import numpy as np
from matplotlib import markers

hnext=0
#  test rk4
def f(t, y):
    p = (1 - y[0] ** 2) * y[1] - y[0]
    return np.array([y[1], p])


import matplotlib.pyplot as plt
import math
import pymap3d as pm
import requests

def rk4(f, t0, tend, y0, n):
    global terminate,iend
    T = [0] * (n + 1)
    a = (n + 1, len(y0))
    Y = np.zeros(a, float)
    h = (tend - t0) / float(n)
    T[0] = x = t0
    Y[0][:] = y0
    for i in range(1, n + 1):
        y = Y[i - 1][:]
        k1 = h * f(x, y)
        k2 = h * f(x + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(x + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(x + h, y + k3)
        T[i] = x = t0 + i * h
        Y[i, :] = y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
        if terminate:
            iend = i
            return T, Y
    return T, Y

vywold,vxwold=0,0
h0 = 0
terminate = False
Pold = 100e3
Told = 100




h0 = 0
kt = 0
x0 = 0
y0 = 0
z0 = 0

bname = (
    'TA 200', 'TA 300', 'TA 350', 'TA 450', 'TA 500', 'TA 600', 'TA 700', 'TA 800', 'TA 1000', 'TA 1200', 'TA 1500',
    'TA 2000', 'TA 3000', 'TX 800', 'TX 1000', 'TX 1200', 'TX 2000', 'TX 3000')

mbs = [200, 300, 350, 450, 500, 600, 700, 800, 1000, 1200, 1500, 2000, 3000, 800, 1000, 1200, 2000, 3000]
mbs = list(map(lambda x: x / 1000.0, mbs))
mps = [250, 250, 250, 250, 250, 250, 250, 250, 250, 1050, 1050, 1050, 1050, 250, 250, 1050, 1050, 1050]
mps = list(map(lambda x: x / 1000.0, mps))
vol0s = [.83, .97, 1.03, 1.16, 1.22, 1.5, 1.63, .76, 2.01, 2.99, 3.33, 3.89, 4.97, 1.76, 2.01, 2.99, 3.89, 4.97]
dbs = [300, 378, 412, 472, 499, 605, 653, 700, 786, 863, 944, 1054, 1300, 738, 828, 910, 1079, 1331]
dbs = list(map(lambda x: x / 100.0, dbs))

i = len(dbs) - 1
mbalon = mbs[i]
mpay = mps[i]
Vol0 = vol0s[i]
Vold = Vol0
DBurst = dbs[i]
Vburst = math.pi * DBurst ** 3 / 6
rogas = 0.164
mgas = rogas * Vol0
Mtot = mgas + mbalon + mpay
Mgros = mbalon + mpay
hnext = 0
lat0 = 36
lon0 = 52


n = 10000;
iend = n;
endtime = 15000;
import timeit
import windapi

#  test rk4
def dXdt(t, x):
    (lat, lon, h) = pm.ned2geodetic(x[0], x[1], x[2], lat0, lon0, h0)
    global hnext ,Pold ,Told,vywold,vxwold,Vold,terminate
    # print((lat,lon,h))
    if abs(h) >= hnext:
        # start_time = timeit.default_timer()
        # url = 'http://localhost:8080/allvalue/' + str(lat) + '/' + str(lon) + '/' + str(h) + '/0/0';
        # r = requests.get(url=url)
        # resp = ast.literal_eval(r.text)
        resp=windapi.ned(lat,lon,h,0,0)
        resp = ast.literal_eval(resp)
        # elapsed = timeit.default_timer() - start_time
        # print(resp)
        vxw = resp[0]
        vyw = resp[1]
        tamb = resp[2]
        pamb = resp[3]
        hnext = 1000 + hnext
        print(x[2])
    else:
        pamb = Pold
        tamb = Told
        vxw = vxwold
        vyw = vywold
    
    Ramb = 287
    roamb = pamb / (Ramb * tamb)
    Rhel = 2077.1
    
    vx = x[3]
    vy = x[4]
    vz = x[5]

    Vrel = sqrt((vxw - vx) ** 2 + (vyw - vy) **2 + (vz) **2)
    vrelz = 0 - vz
    vrelx = vxw - vx
    vrely = vyw - vy
    ro = roamb
    rogas = 0.164
    rogasvir = pamb * 1.15 / (Rhel * tamb)
    rogasold = rogasvir
    mgas = rogas * Vol0
    gama = 1.06
    Vol = (Pold / pamb) ** (1 / gama) * Vold
    rogasvir = mgas / Vol
    g = 9.81
    B = (ro - rogasvir) * g * Vol
    L = (Vol * 3 / 4 / math.pi) **(1 / 3)
    A = math.pi * L ** 2
    visco = 1.81 * 10 ** -5
    Re = roamb * Vrel * L / visco
    cd = 4.808 * (math.log(Re)) ** 2 / 100 - 1.406 * math.log(Re) + 10.490
    Drag = 0.5 * ro * (Vrel) ** 2 * cd * A
    if cd > 0.9:
        cd = 0.85

    dxdt = [0,0,0,0,0,0]
    dxdt[0] = vx
    dxdt[1] = vy
    dxdt[2] = vz
    dxdt[3] = Drag * (vrelx) / Vrel / Mtot
    dxdt[4] = Drag * vrely / Vrel / Mtot
    dxdt[5] = (Mgros * 9.81 - B + Drag * vrelz / Vrel) / Mtot

    if Vol >= Vburst:
        dxdt = dxdt
        print(Vol)
        terminate = True
        return np.array([dxdt[0],dxdt[1],dxdt[2],dxdt[3],dxdt[4],dxdt[5]])

    if abs(x[2] )> 49e3:
        terminate = True
        return np.array([dxdt[0],dxdt[1],dxdt[2],dxdt[3],dxdt[4],dxdt[5]])
    if vz > 0:
        print("vz iw positive")
        terminate = True
        return np.array([dxdt[0], dxdt[1], dxdt[2], dxdt[3], dxdt[4], dxdt[5]])

    Pold = pamb
    Vold = Vol
    Told = tamb
    vxwold = vxw
    vywold = vyw

    return np.array([dxdt[0],dxdt[1],dxdt[2],dxdt[3],dxdt[4],dxdt[5]])



# t, y = rk4(f, 0, 11, [x0, 2], 1111)


t, y = rk4(dXdt, 0, endtime, [x0, y0, z0, 0, 0, 0], n)

plt.plot(t, -y[:, 2], 'g.')
plt.show()

plt.plot(t, -y[:, 5], 'g.')
plt.show()
