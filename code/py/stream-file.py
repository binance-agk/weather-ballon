import requests

stream_url0 = 'https://thredds-test.unidata.ucar.edu/thredds/ncss/grid/grib/NCEP/' \
             'GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_20200508_1800.grib2' \
             '?var=Geopotential_height_isobaric&var=Temperature_isobaric&var=u-component_of_wind_isobaric&var=v-component_of_wind_isobaric&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2020-05-08T18%3A00%3A00Z&time_end=2020-05-08T18%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'

stream_url = 'https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_20200508_1800.grib2?var=Geopotential_height_isobaric&var=Temperature_isobaric&var=u-component_of_wind_isobaric&var=v-component_of_wind_isobaric&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2020-05-08T18%3A00%3A00Z&time_end=2020-05-08T18%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'


stream_url = 'https://thredds.ucar.edu/thredds/ncss/grib/NCEP/GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_20200518_0600.grib2?var=Geopotential_height_isobaric&var=Temperature_isobaric&var=u-component_of_wind_isobaric&var=v-component_of_wind_isobaric&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2020-05-18T06%3A00%3A00Z&time_end=2020-05-18T06%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'

print(stream_url)

r = requests.get(stream_url, stream=True)

with open('GFS_Global_0p5deg_ana_20200518_0600.grib2.nc', 'wb') as f:
    try:
        for block in r.iter_content(3020):
            f.write(block)
    except KeyboardInterrupt:
        pass

