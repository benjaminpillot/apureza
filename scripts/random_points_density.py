# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
import numpy as np
from gistools.layer import PolygonLayer

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


density_type = ["dense", "tresdense", "diffus"]

for dtype in density_type:
    density = PolygonLayer("/home/ird/Desktop/densite/grille_edif_100_%s.shp" % dtype)
    points = np.random.choice(len(density), 50, replace=False)
    density_random = density[points].centroid()
    lon = density_random.geometry.x.to_numpy().reshape(-1, 1)
    lat = density_random.geometry.y.to_numpy().reshape(-1, 1)

    lon_lat = np.concatenate([lon, lat], axis=1)
    np.savetxt("/home/ird/Desktop/Density random points/density_%s.csv" % dtype, lon_lat, delimiter=",")
