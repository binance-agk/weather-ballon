import requests
import csv, io, json
from bottle import route, run


@route('/wind/<lat>/<lng>/<year>/<month>/<day>/<hh>')
def index(lat, lng, year, month, day, hh):
    params = {
        'var': ['Geopotential_height_isobaric', 'Temperature_isobaric', 'u-component_of_wind_isobaric',
                'v-component_of_wind_isobaric', ],
        'latitude': lat,
        'longitude': lng,
        'time_start': '{0}-{1}-{2}T{3}:00:00Z'.format(year, month, day, hh),
        'time_end': '{0}-{1}-{2}T{3}:00:00Z'.format(year, month, day, hh),
        'accept': 'csv'
        # more key=value pairs as appeared in your query string
    }
    url = "https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2" \
        .format(year, month, day, hh)

    resp = requests.get(url,
                        params=params)

    cot = resp.content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(cot))
    king = list(reader)
    vV = []
    uV = []
    p = []
    h = []
    t = []
    print(resp.status_code)

    for ki in king:
        p.append(ki['vertCoord[unit="Pa"]'])
        h.append(ki['Geopotential_height_isobaric[unit="gpm"]'])
        t.append(ki['Temperature_isobaric[unit="K"]'])
        uV.append(ki['u-component_of_wind_isobaric[unit="m/s"]'])
        vV.append(ki['v-component_of_wind_isobaric[unit="m/s"]'])

    return {'p': p, 'h': h, 't': t, 'uv': uV, 'vv': vV}


# print(king[0])
# json_data = json.dumps(list(reader))
# print(json_data)
# print(king)

run(host='localhost', port=8080)
