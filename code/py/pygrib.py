# ==============================================================================
# GNC-A Blog Python Tutorial: Part I
# ==============================================================================

import matplotlib.pyplot as plt  # Import the Matplotlib package
from osgeo import gdal  # Import the GDAL library

# Read the GRIB file
grib = gdal.Open('E:\\VLAB\\Python\\GFS Samples\\gfs_sam_0p50_00.f0000')

# Read an specific band
band = grib.GetRasterBand(142)

# Read the band as a Python array
data = band.ReadAsArray()

# Show the image
plt.imshow(data, cmap='jet')