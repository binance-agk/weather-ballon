import ast
import math
from math import sqrt
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pymap3d as pm
import solution.windapi as windapi

"""solution class for categorize 
and gather all parameters related"""


class Solution(object):
    densities = [0.082, 0.164]

    def __init__(self, anyerroremmiter, balloonemmiter, parachuteemmiter, flightdoneemmiter, lat0, lon0, day, month,
                 year, hour, minute,
                 filename, gasType, balloontype, mpay, chutetype, nozzlelift, iternumber, endtime):
        self.anyerroremmiter = anyerroremmiter
        self.flightdoneemmiter = flightdoneemmiter
        self.parachuteemmiter = parachuteemmiter
        self.balloonemmiter = balloonemmiter
        self.iternumber = iternumber
        self.endtime = endtime
        self.hnext = -1
        self.windapi = windapi
        self.lat0 = lat0
        self.lon0 = lon0
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        try:
            self.netcfd4 = netCDF4.Dataset(filename)
        except OSError as e:
            anyerroremmiter(e.__str__())
        self.minute = minute
        self.gasType = gasType
        self.mpay = mpay
        self.chutetype = chutetype
        self.nozzlelift = nozzlelift
        self.balloontype = balloontype

        self.getinit()

    def getinit(self):
        bname = (
            'TA200', 'TA300', 'TA350', 'TA450', 'TA500', 'TA600', 'TA700', 'TA800', 'TA1000', 'TA1200', 'TA1500',
            'TA2000', 'TA3000', 'TX800', 'TX1000', 'TX1200', 'TX2000', 'TX3000')
        self.balloontypeindex = bname.index(self.balloontype)

        mbs = [200, 300, 350, 450, 500, 600, 700, 800, 1000, 1200, 1500, 2000, 3000, 800, 1000, 1200, 2000, 3000]
        mbs = list(map(lambda x: x / 1000.0, mbs))
        mps = [250, 250, 250, 250, 250, 250, 250, 250, 250, 1050, 1050, 1050, 1050, 250, 250, 1050, 1050, 1050]
        mps = list(map(lambda x: x / 1000.0, mps))
        vol0s = [.83, .97, 1.03, 1.16, 1.22, 1.5, 1.63, .76, 2.01, 2.99, 3.33, 3.89, 4.97, 1.76, 2.01, 2.99, 3.89, 4.97]
        dbs = [300, 378, 412, 472, 499, 605, 653, 700, 786, 863, 944, 1054, 1300, 738, 828, 910, 1079, 1331]
        dbs = list(map(lambda x: x / 100.0, dbs))

        print(bname[self.balloontypeindex])
        i = self.balloontypeindex
        self.mbalon = mbs[i]
        # self.mpay = mps[i]
        self.Vol0 = vol0s[i]
        self.Vold = self.Vol0
        self.DBurst = dbs[i]
        self.Vburst = math.pi * self.DBurst ** 3 / 6
        self.rogas = self.densities[self.gasType]
        self.mgas = self.rogas * self.Vol0
        self.Mtot = self.mgas + self.mbalon + self.mpay
        self.Mgros = self.mbalon + self.mpay
        self.vywold, self.vxwold = 0, 0
        self.h0 = 0
        self.terminate = False
        self.Pold = 100e3
        self.Told = 100

    def dXdt(self, t, x):
        (lat, lon, h) = pm.ned2geodetic(x[0], x[1], x[2], self.lat0, self.lon0, self.h0)
        # print((lat,lon,h))
        if abs(h) >= self.hnext:
            resp = self.windapi.ned(self.netcfd4, lat, lon, h, 0, 0)
            resp = ast.literal_eval(resp)
            vxw = resp[0]
            vyw = resp[1]
            tamb = resp[2]
            pamb = resp[3]
            self.hnext = 1000 + self.hnext
            # print(x[2])
            self.balloonemmiter(f" {h:.2f}m :ارتفاع بالن ")
        else:
            pamb = self.Pold
            tamb = self.Told
            vxw = self.vxwold
            vyw = self.vywold

        Ramb = 287
        roamb = pamb / (Ramb * tamb)
        Rhel = 2077.1

        vx = x[3]
        vy = x[4]
        vz = x[5]

        Vrel = sqrt((vxw - vx) ** 2 + (vyw - vy) ** 2 + (vz) ** 2)
        vrelz = 0 - vz
        vrelx = vxw - vx
        vrely = vyw - vy
        ro = roamb
        rogasvir = pamb * 1.15 / (Rhel * tamb)
        # mgas = self.rogas * self.Vol0
        gama = 1.06
        Vol = (self.Pold / pamb) ** (1 / gama) * self.Vold
        self.rogas = self.mgas / Vol
        g = 9.81
        B = (ro - self.rogas) * g * Vol
        L = (Vol * 3 / 4 / math.pi) ** (1 / 3)
        A = math.pi * L ** 2
        visco = 1.81 * 10 ** -5
        Re = roamb * Vrel * L / visco  # specific definition by radius no diameter
        cd = 4.808 * (math.log(Re)) ** 2 / 100 - 1.406 * math.log(Re) + 10.490
        if cd > 0.9:
            cd = 0.9

        Drag = 0.5 * ro * (Vrel) ** 2 * cd * A
        dxdt = [0, 0, 0, 0, 0, 0]
        dxdt[0] = vx
        dxdt[1] = vy
        dxdt[2] = vz
        dxdt[3] = Drag * (vrelx) / Vrel / self.Mtot
        dxdt[4] = Drag * vrely / Vrel / self.Mtot
        dxdt[5] = (self.Mgros * 9.81 - B + Drag * vrelz / Vrel) / self.Mtot

        self.Pold = pamb
        self.Vold = Vol
        self.Told = tamb
        self.vxwold = vxw
        self.vywold = vyw

        if Vol >= self.Vburst:
            print('Vol ', Vol)
            self.balloonemmiter(f"{h:.1f}ترکیدن بالن در ارتفاع ")
            self.terminate = True
            return np.array([dxdt[0], dxdt[1], dxdt[2], dxdt[3], dxdt[4], dxdt[5]])

        if abs(x[2]) > 49e3:
            self.terminate = True
            return np.array([dxdt[0], dxdt[1], dxdt[2], dxdt[3], dxdt[4], dxdt[5]])
        if vz > 0:
            print("vz iw positive")
            self.terminate = True
            return np.array([dxdt[0], dxdt[1], dxdt[2], dxdt[3], dxdt[4], dxdt[5]])

        return np.array([dxdt[0], dxdt[1], dxdt[2], dxdt[3], dxdt[4], dxdt[5]])

    def rk4(self, dfdt, t0, tend, y0, n):
        self.T = [0] * (n + 1)
        a = (n + 1, len(y0))
        self.Y = np.zeros(a, float)
        h = (tend - t0) / float(n)
        self.T[0] = x = t0
        self.Y[0][:] = y0
        for i in range(1, n + 1):
            y = self.Y[i - 1][:]
            k1 = h * dfdt(x, y)
            k2 = h * dfdt(x + 0.5 * h, y + 0.5 * k1)
            k3 = h * dfdt(x + 0.5 * h, y + 0.5 * k2)
            k4 = h * dfdt(x + h, y + k3)
            self.T[i] = x = t0 + i * h
            self.Y[i, :] = y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
            if self.terminate:
                self.iend = i
                return self.T, self.Y
        return self.T, self.Y

    def solveparachutepart(self):
        a = (self.iternumber + 1, 6)
        x = np.zeros(a, float)
        self.Tpar = [0] * (self.iternumber + 1)

        chutetypes = ('TX160', 'TX5012')
        chuteweights = (70 / 1000.0, 180 / 1000.0)
        # self.chutetypeindex = chutetypes.index(self.chutetype)

        mpar = 70 / 1000
        dcan = 94 / 100
        mpay = 300 / 1000
        mpay = self.mpay
        decent = 3.7
        Apar = math.pi * dcan ** 2 / 4
        rogr = 1.225
        Cd0 = 2 * 9.81 * (mpar + mpay) / (Apar * rogr * decent ** 2)
        # Cd0 = 1.22 / 2
        dt = 1
        iend = self.iend
        x[0, 0] = self.Y[iend, 0]
        x[0, 1] = self.Y[iend, 1]
        x[0, 2] = self.Y[iend, 2]
        x[0, 3] = self.Y[iend, 3]
        x[0, 4] = self.Y[iend, 4]
        x[0, 5] = self.Y[iend, 5]
        h = x[0, 2]
        t0 = self.T[iend]
        k = 0
        while abs(h) > 40:
            (lat, lon, h) = pm.ned2geodetic(x[k, 0], x[k, 1], x[k, 2], self.lat0, self.lon0, self.h0)
            if (k - 1) % 100 == 0:
                resp = self.windapi.ned(self.netcfd4, lat, lon, h, 0, 0)
                resp = ast.literal_eval(resp)
                vxw = resp[0]
                vyw = resp[1]
                tamb = resp[2]
                pamb = resp[3]
                self.parachuteemmiter(f"{h:.1f}")
            else:
                pamb = self.Pold
                tamb = self.Told
                vxw = self.vxwold
                vyw = self.vywold

            Ramb = 287.0
            roamb = pamb / (Ramb * tamb)

            k = k + 1
            vz = (2 * 9.81 * (mpar + mpay) / (Apar * roamb * Cd0)) ** 0.5
            x[k, 0] = x[k - 1, 0] + vxw * dt
            x[k, 1] = x[k - 1, 1] + vyw * dt
            x[k, 2] = x[k - 1, 2] + vz * dt
            x[k, 3] = vxw
            x[k, 4] = vyw
            x[k, 5] = vz
            self.Tpar[k] = k * dt + t0
            self.Pold = pamb
            self.Told = tamb
            self.vxwold = vxw
            self.vywold = vyw

        self.flightdoneemmiter('فرود و پایان پرواز...')
        self.kend = k
        self.Xpar = x
        return self.Tpar, self.Xpar

    def solveballoonpart(self):
        h0 = 0
        x0 = 0
        y0 = 0
        z0 = 0
        t, y = self.rk4(self.dXdt, 0, self.endtime, [x0, y0, z0, 0, 0, 0], self.iternumber)
        return t, y

    def exportKML(self):
        f = open("lmk.kml", "w")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://earth.google.com/kml/2.1">\n')
        f.write('<Document>\n    <name>Balloon Trajectory </name>\n')
        f.write('<Style id="track">\n      <LineStyle>\n        <color>7fff00aa</color>\n      </LineStyle>\n     '
                ' <PolyStyle>\n        <color>7f00ff00</color>\n      </PolyStyle>\n    </Style>\n')
        f.write('<Style id="place">\n      <IconStyle>\n        <scale>1</scale>\n        <Icon>\n          '
                '<href>http://weather.uwyo.edu/icons/purple.gif</href>\n        </Icon>\n      </IconStyle>\n    '
                '</Style>')
        (lat, lon, h) = pm.ned2geodetic(self.Y[self.iend // 2, 0], self.Y[self.iend // 2, 1], self.Y[self.iend // 2, 2],
                                        self.lat0, self.lon0, self.h0)

        f.write(
            f'    <LookAt>\n      <longitude>{lon:.5f}</longitude>\n      <latitude>{lat:.5f}</latitude>\n      <range>200000.000</range>\n      <tilt>50.0</tilt>\n      <heading>10.9920856305692</heading>\n    </LookAt>\n')
        f.write(
            '<Placemark>\n      <name>Flight Path</name>\n      <styleUrl>#track</styleUrl>\n      <LineString>\n        '
            '<tessellate>1</tessellate>\n        <extrude>1</extrude>\n        <altitudeMode>absolute</altitudeMode>\n    '
            '    <coordinates>\n')
        for i in range(0, self.iend, 100):
            (lat, lon, h) = pm.ned2geodetic(self.Y[i, 0], self.Y[i, 1], self.Y[i, 2], self.lat0, self.lon0, self.h0)
            f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

        (latb, lonb, hb) = pm.ned2geodetic(self.Y[self.iend, 0], self.Y[self.iend, 1], self.Y[self.iend, 2], self.lat0,
                                           self.lon0, self.h0)
        f.write(F'{lonb:.6f},{latb:.6f},{hb:.6f}\n')

        for i in range(0, self.kend, 100):
            (lat, lon, h) = pm.ned2geodetic(self.Xpar[i, 0], self.Xpar[i, 1], self.Xpar[i, 2], self.lat0, self.lon0,
                                            self.h0)
            f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

        (lat, lon, h) = pm.ned2geodetic(self.Xpar[self.kend, 0], self.Xpar[self.kend, 1],
                                        self.Xpar[self.kend, 2], self.lat0, self.lon0, self.h0)
        f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

        f.write('        </coordinates>\n      </LineString>\n    </Placemark>\n')

        f.write(
            F'<Placemark>\n<name>Balloon Launch</name>\n<description>Balloon Launch at {self.lat0 :.6f}, '
            F'{self.lon0 :.6f}</description>\n<Point><coordinates> {self.lon0 :.6f},{self.lat0 :.6f},{self.h0 :.6f}</coordinates></Point>\n'
            F'</Placemark>\n ')
        f.write(
            F'<Placemark>\n<name>Balloon Burst</name>\n<description>Balloon Burst at {latb:.6f}, '
            F'{lonb:.6f} at {hb:.1f}m</description>\n<Point><coordinates> {lonb:.6f},{latb:.6f},{hb:.6f}</coordinates></Point>\n'
            F'</Placemark>\n ')
        f.write(
            F'<Placemark>\n<name>Balloon Landing</name>\n<description>Landing at {lat:.6f}, '
            F'{lon:.6f}</description>\n<Point><coordinates> {lon:.6f},{lat:.6f},{h:.6f}</coordinates></Point>\n'
            F'</Placemark>\n ')
        f.write('  </Document>\n</kml>\n')

        f.close()


# # t, y = rk4(f, 0, 11, [x0, 2], 1111)
def anyerroremmiter(args):
    pass


def balloonemmiter(args):
    pass


def parachuteemmiter(args):
    pass


def flightdoneemmiter(args):
    pass


if __name__ == '__main__':
    year = 2020
    month = 10
    day = 15
    hour = 12
    lat0 = 12
    lon0 = 122

    filename = "GFS_Global_0p5deg_best_{0}{1}{2:0=2d}_{3:0=2d}00.grib2.nc" \
        .format(year, month, day, hour)
    print(filename)
    solution = Solution(anyerroremmiter, balloonemmiter, parachuteemmiter, flightdoneemmiter, lat0, lon0, day, month,
                        year, hour, 0, filename, 1, 10, 0.2, None, 0, 22000, 15000)
    t, y = solution.solveballoonpart()
    iend = solution.iend
    plt.plot(t[0:iend], -y[0:iend, 2], 'g.')
    plt.show()
    plt.plot(t[0:iend], -y[0:iend, 5], 'g.')
    plt.show()

    solution.solveparachutepart()
    k = solution.kend
    plt.plot(solution.Tpar[0:k], -solution.Xpar[0:k, 2], 'r.')
    plt.show()
    plt.plot(solution.Tpar[0:k], -solution.Xpar[0:k, 5], 'r.')
    plt.show()
