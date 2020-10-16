import requests


class Dl(object):
    def __init__(self, year, month, day, hour):
        self.hour = hour
        self.month = month
        self.year = year
        self.day = day

    def dl(self, progressEmitter, errorEmitter, doneEmitter):
        params = {
            'var': ['Geopotential_height_isobaric', 'Temperature_isobaric', 'u-component_of_wind_isobaric',
                    'v-component_of_wind_isobaric'],
            'time_start': '{0}-{1}-{2}T{3}:00:00Z'.format(self.year, self.month, self.day, self.hour),
            'time_end': '{0}-{1}-{2}T{3}:00:00Z'.format(self.year, self.month, self.day, self.hour),
            'disableLLSubset': 'on',
            'disableProjSubset': 'on',
            'horizStride': '1',
            'vertCoord': '',
            'timeStride': '1',
            'accept': 'netcdf'
        }
        url = "https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana" \
              "/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2" \
            .format(self.year, self.month, self.day, self.hour)

        r = requests.get(url, params=params, stream=True)

        if r.status_code != 200:
            errorEmitter('something is wrong... try again ')

        rem = 0
        size = 0

        with open('data/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc'.format(self.year, self.month, self.day,
                                                                               self.hour), 'wb') as f:
            try:
                for block in r.iter_content(3020):
                    f.write(block)
                    f.flush()
                    size = size + 3020
                    if rem % 50 == 0:
                        # progressEmitter(f'{size // 1024} KB receiving ...')
                        progressEmitter(size // 1024)  # KB receiving
                        # print(, "KB receiving ...")
                    rem = rem + 1
            except KeyboardInterrupt:
                errorEmitter(KeyboardInterrupt.__str__())
                pass

        doneEmitter('done')
        print('done ')


if __name__ == '__main__':
    def emmiter(msg): return print(msg)
    Dl(2020, 10, '01', '06').dl(emmiter, emmiter, emmiter)
