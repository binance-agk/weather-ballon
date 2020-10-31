import requests


def code(year, month, day, hour):
    params = {
        'var': ['Geopotential_height_isobaric', 'Temperature_isobaric', 'u-component_of_wind_isobaric',
                'v-component_of_wind_isobaric'],
        'time_start': '{0}-{1}-{2}T{3}:00:00Z'.format(year, month, day, hour),
        'time_end': '{0}-{1}-{2}T{3}:00:00Z'.format(year, month, day, hour),
        'disableLLSubset': 'on',
        'disableProjSubset': 'on',
        'horizStride': '1',
        'vertCoord': '',
        'timeStride': '1',
        'accept': 'netcdf'
    }
    url = "https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana" \
          "/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2" \
        .format(year, month, day, hour)

    try:
        resp = requests.head(url, params=params)
        print(resp.url)
        return resp.status_code
    except Exception as e:
        print(e.__str__())
        return 400


print(code(2020, 10, 30, '18'))
