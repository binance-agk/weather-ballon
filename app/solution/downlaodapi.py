import requests


class Dl(object):
    def __init__(self, year, month, day, hour):
        self.hour = hour
        self.month = month
        self.year = year
        self.day = day

    def reforecastdl(self, progressEmitter, errorEmitter, doneEmitter):
        params = {
            'time': '{0}-{1}-{2}T{3}:00:00Z'.format(self.year, self.month, self.day, self.hour),
            'var': ['Geopotential_height_isobaric', 'Temperature_isobaric', 'u-component_of_wind_isobaric',
                    'v-component_of_wind_isobaric'],
            'accept': 'netcdf'
        }
        url = "https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg/best"

        resp = requests.get(url, params=params, stream=True)

        if resp.status_code == 404:
            errorEmitter('data not found try other time')
            print(resp.status_code)
            return
        elif resp.status_code == 400:
            errorEmitter(str(resp.content.decode("utf-8")))
            return
        elif resp.status_code != 200:
            errorEmitter('something is wrong... try again ')
            return

        rem = 0
        size = 0
        print(resp.url)

        with open('data/GFS_Global_0p5deg_best_{0}{1}{2}_{3}00.grib2.nc'.format(self.year, self.month, self.day,
                                                                                self.hour), 'wb') as f:
            try:
                for block in resp.iter_content(3020):
                    f.write(block)
                    f.flush()
                    size = size + 3020
                    if rem % 50 == 0:
                        # progressEmitter(f'{size // 1024} KB receiving ...')
                        progressEmitter(size // 1024)  # KB receiving
                        # print(, "KB receiving ...")
                    rem = rem + 1
            except Exception:
                errorEmitter(Exception.__str__())
                pass

        doneEmitter('done')
        print('done ')

        pass

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

        try:
            resp = requests.get(url, params=params, stream=True)
        except Exception as e:
            errorEmitter(e.__str__())
            return
        if resp.status_code == 404:
            errorEmitter('data not found try other time')
            print(resp.status_code)
            return
        elif resp.status_code != 200:
            errorEmitter('something is wrong... try again ')
            return

        rem = 0
        size = 0
        print(resp.url)

        with open('data/GFS_Global_0p5deg_ana_{0}{1}{2}_{3}00.grib2.nc'.format(self.year, self.month, self.day,
                                                                               self.hour), 'wb') as f:
            try:
                for block in resp.iter_content(3020):
                    f.write(block)
                    f.flush()
                    size = size + 3020
                    if rem % 50 == 0:
                        # progressEmitter(f'{size // 1024} KB receiving ...')
                        progressEmitter(size // 1024)  # KB receiving
                        # print(, "KB receiving ...")
                    rem = rem + 1
            except Exception:
                errorEmitter(Exception.__str__())
                pass

        doneEmitter('done')
        print('done ')


if __name__ == '__main__':
    def emmiter(msg): return print(msg)


    Dl(2020, 11, '16', '06').reforecastdl(emmiter, emmiter, emmiter)
