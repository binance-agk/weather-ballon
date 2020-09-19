import requests

test2word = input("select day ")
day = int(test2word)
test2word = input("select month ")
month = int(test2word)
test2word = input("select year ")
year = int(test2word)
test2word = input("select hour(0 , 6 , 12 , 18)")
hour = int(test2word)
from datetime import time
from datetime import date

mydate = date(year, month, day)
mytime = time(hour, 0)

if (month) < 10:
    month = '0' + str(month)

if (hour) < 10:
    hour = '0' + str(hour)

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
url = "https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2" \
    .format(year, month, day, hour)

r = requests.get(url, params=params, stream=True)
print("-----------------------------------------------------------------")
print(r.request.url)
print("-----------------------------------------------------------------")

size = 0
rem = 0

if r.status_code!=200:
    print('something is wrong... try again ')

with open('GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc'.format(year, month, day, hour), 'wb') as f:
    try:
        for block in r.iter_content(3020):
            r.status_code
            f.write(block)
            f.flush()
            size = size + 3020
            if rem % 32000:
                print(f'{size//1024} KB receiving ...\r', end="")
                # print(, "KB receiving ...")
            rem = rem + 1
    except KeyboardInterrupt:
        print(KeyboardInterrupt.__str__())
        pass
print('done')