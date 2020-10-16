
a = (n + 1, 6)
x = np.zeros(a, float)

mpar = 70 / 1000
dcan = 94 / 100
mpay = 300 / 1000
decent = 3.7
Apar = math.pi * dcan ** 2 / 4
rogr = 1.225
Cd0 = 2 * 9.81 * (mpar + mpay) / (Apar * rogr * decent ** 2)
Cd0 = 1.22 / 2
dt = 1

x[0, 0] = y[iend, 0]
x[0, 1] = y[iend, 1]
x[0, 2] = y[iend, 2]
x[0, 3] = y[iend, 3]
x[0, 4] = y[iend, 4]
x[0, 5] = y[iend, 5]
h = x[0, 2]
k = 0
while abs(h) > 40:
    (lat, lon, h) = pm.ned2geodetic(x[k, 0], x[k, 1], x[k, 2], lat0, lon0, h0)
    if (k - 1) % 100 == 0:
        resp = windapi.ned(lat, lon, h, 0, 0)
        resp = ast.literal_eval(resp)
        vxw = resp[0]
        vyw = resp[1]
        tamb = resp[2]
        pamb = resp[3]
        print(-x[k, 2])
    else:
        pamb = Pold
        tamb = Told
        vxw = vxwold
        vyw = vywold

    Ramb = 287
    roamb = pamb / (Ramb * tamb)

    k = k + 1
    vz = (2 * 9.81 * (mpar + mpay) / (Apar * roamb * Cd0)) ** 0.5
    x[k, 0] = x[k - 1, 0] + vxw * dt
    x[k, 1] = x[k - 1, 1] + vyw * dt
    x[k, 2] = x[k - 1, 2] + vz * dt
    x[k, 3] = vxw
    x[k, 4] = vyw
    x[k, 5] = vz
    Pold = pamb
    Told = tamb
    vxwold = vxw
    vywold = vyw

plt.plot(-x[0:k, 2], x[0:k, 5], 'r.')
plt.show()


def makeKML():
    f = open("kml.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://earth.google.com/kml/2.1">\n')
    f.write('<Document>\n    <name>Balloon Trajectory </name>\n')
    f.write('<Style id="track">\n      <LineStyle>\n        <color>7f00ff00</color>\n      </LineStyle>\n     '
            ' <PolyStyle>\n        <color>7f00ff00</color>\n      </PolyStyle>\n    </Style>\n')
    f.write('<Style id="place">\n      <IconStyle>\n        <scale>1</scale>\n        <Icon>\n          '
            '<href>http://weather.uwyo.edu/icons/purple.gif</href>\n        </Icon>\n      </IconStyle>\n    '
            '</Style>')
    (lat, lon, h) = pm.ned2geodetic(y[iend // 2, 0], y[iend // 2, 1], y[iend // 2, 2], lat0, lon0, h0)

    f.write(
        f'    <LookAt>\n      <longitude>{lon:.5f}</longitude>\n      <latitude>{lat:.5f}</latitude>\n      <range>200000.000</range>\n      <tilt>50.0</tilt>\n      <heading>10.9920856305692</heading>\n    </LookAt>\n')
    f.write(
        '<Placemark>\n      <name>Flight Path</name>\n      <styleUrl>#track</styleUrl>\n      <LineString>\n        '
        '<tessellate>1</tessellate>\n        <extrude>1</extrude>\n        <altitudeMode>absolute</altitudeMode>\n    '
        '    <coordinates>\n')
    for i in range(0, iend, 100):
        (lat, lon, h) = pm.ned2geodetic(y[i, 0], y[i, 1], y[i, 2], lat0, lon0, h0)
        f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

    (latb, lonb, hb) = pm.ned2geodetic(y[iend, 0], y[iend, 1], y[iend, 2], lat0, lon0, h0)
    f.write(F'{lonb:.6f},{latb:.6f},{hb:.6f}\n')

    for i in range(0, k, 100):
        (lat, lon, h) = pm.ned2geodetic(x[i, 0], x[i, 1], x[i, 2], lat0, lon0, h0)
        f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

    (lat, lon, h) = pm.ned2geodetic(x[k, 0], x[i, 1], x[i, 2], lat0, lon0, h0)
    f.write(F'{lon:.6f},{lat:.6f},{h:.6f}\n')

    f.write('        </coordinates>\n      </LineString>\n    </Placemark>\n')

    f.write(
        F'<Placemark>\n<name>Balloon Launch</name>\n<description>Balloon Launch at {lat0:.6f}, '
        F'{lon0:.6f}</description>\n<Point><coordinates> {lon0:.6f},{lat0:.6f},{h0:.6f}</coordinates></Point>\n'
        F'</Placemark>\n ')
    f.write(
        F'<Placemark>\n<name>Balloon Burst</name>\n<description>Balloon Burst at {latb:.6f}, '
        F'{lonb:.6f}</description>\n<Point><coordinates> {lonb:.6f},{latb:.6f},{hb:.6f}</coordinates></Point>\n'
        F'</Placemark>\n ')
    f.write(
        F'<Placemark>\n<name>Balloon Landing</name>\n<description>Balloon Landing at {lat:.6f}, '
        F'{lon:.6f}</description>\n<Point><coordinates> {lon:.6f},{lat:.6f},{h:.6f}</coordinates></Point>\n'
        F'</Placemark>\n ')
    f.write('  </Document>\n</kml>\n')

    f.close()


makeKML()

import subprocess

subprocess.run(["start kml.kml"])
