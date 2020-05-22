import requests

stream_url = 'https://thredds-test.unidata.ucar.edu/thredds/ncss/grid/grib/NCEP/' \
             'GFS/Global_0p5deg_ana/GFS_Global_0p5deg_ana_20200508_1800.grib2' \
             '?var=Geopotential_height_isobaric&var=Temperature_isobaric&var=u-component_of_wind_isobaric&var=v-component_of_wind_isobaric&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2020-05-08T18%3A00%3A00Z&time_end=2020-05-08T18%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'


local_filename = 'nc.nc'
# NOTE the stream=Tr
