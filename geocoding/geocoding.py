# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

from geopy.geocoders import Nominatim
import csv
import time
import pandas as pd
import geopandas as gpd

geocoder = Nominatim(domain="193.48.189.24/nominatim", scheme="http", timeout=3)
inputFile = open('Cas.csv', "rt", encoding="utf-8")
outputFile = open("resultat.csv", "w")
try:
    outputData = csv.writer(outputFile, delimiter=";", lineterminator="\n")
    outputData.writerow(("adresse", "latitude", "longitude"))
    inputData = csv.reader(inputFile, delimiter=";")
    for ligne in inputData:
        adresse = ligne[6] + ", Distrito Federal, Região Centro-Oeste, BRASIL"
        adresse2 = ligne[1]
        try:
            location = geocoder.geocode(adresse, True, 30)
            outputData.writerow((adresse2, location.latitude, location.longitude))
        except Exception as inst:
            print(inst)
finally:
    inputFile.close()
    outputFile.close()

resultat = pd.read_csv("resultat.csv", sep=";")
GeoResult = gpd.GeoDataFrame(resultat, geometry=gpd.points_from_xy(resultat.longitude, resultat.latitude))
GeoResult.to_file("GeoResult.shp")
