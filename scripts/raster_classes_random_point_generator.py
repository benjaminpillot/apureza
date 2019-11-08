# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

import numpy as np

from gistools.raster import RasterMap

# raster = RasterMap("/home/ird/Documents/apureza/data/sansseb_iota2_S2_2019.tif", no_data_value=0)
raster = RasterMap("/home/ird/Documents/apureza/data/sanseb_spot7_aout2018.tif", no_data_value=0)

# for value in np.unique(raster.raster_array[~np.isnan(raster.raster_array)]):
for value in [11, 12, 13, 14]:
    class_lat = raster.geo_grid.latitude[raster.raster_array == value].reshape(-1, 1)
    class_lon = raster.geo_grid.longitude[raster.raster_array == value].reshape(-1, 1)
    points = np.random.choice(len(class_lat), 50, replace=False)

    lat_lon = np.concatenate([class_lon[points], class_lat[points]], axis=1)
    np.savetxt("/home/ird/Desktop/random_points/class_%d.csv" % value, lat_lon, delimiter=",")
