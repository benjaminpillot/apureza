# -*- coding: utf-8 -*-
##########Construction de GeoConcat : shapefile contenant l'ensemble des adresses possibles#########

import pandas as pd
import numpy as np
import geopandas as gpd
import re

    #Creation du shp de niveau d'adressage L11 constitu� des QUARTIERS et agregeant les admin_level 10 et 11 et la prison

# Charger les shapes L11
admin_level_10 = gpd.read_file("admin_level_10.shp", header = None, index_col = 0)
admin_level_11 = gpd.read_file("admin_level_11.shp", header = None, index_col = 0)
amenity_prison = gpd.read_file("amenity_prison.shp", header = None, index_col = 0)

# Combiner les shapes pour former GeoL11
GeoL11_v1 = gpd.overlay(admin_level_10, admin_level_11, how='union')
GeoL11_v1 = GeoL11_v1.fillna("")
GeoL11_v1.loc[GeoL11_v1.name_1 != "", "L11"] = GeoL11_v1["name_1"]
GeoL11_v1.loc[GeoL11_v1.name_2 != "", "L11"] = GeoL11_v1["name_2"]
GeoL11_v2 = gpd.overlay(GeoL11_v1, amenity_prison, how='union')
GeoL11_v2 = GeoL11_v2.fillna("")
GeoL11_v2.loc[GeoL11_v2.name != "", "L11"] = GeoL11_v2["name"]
GeoL11_v3 = GeoL11_v2.reindex(columns = ["L11", "geometry"])
GeoL11 = gpd.GeoDataFrame(GeoL11_v3,geometry="geometry")
GeoL11["L11"] = GeoL11.L11.str.replace("ã","�")
GeoL11["L11"] = GeoL11.L11.str.replace("â","�")

    #Creation du shp de niveau d'adressage L12 constitu� des QUADRA et agregeant les place "quarter"
#Charger les shapes L12
place_quarter = gpd.read_file("place_quarter.shp", header = None, index_col = 0)
#Combiner les shapes pour former GeoL12
place_quarter["L12"] = place_quarter["name"]
GeoL12_v1 = place_quarter.reindex(columns = ["L12", "geometry"])
GeoL12 = gpd.GeoDataFrame(GeoL12_v1,geometry="geometry")

    #Creation du shp de niveau d'adressage L13 constitu� des CONJUNTOS et agregeant les place "city_block"
#Charger les shapes L13
place_city_block = gpd.read_file("place_city_block.shp", header = None, index_col = 0)
#combiner les shapes pour former GeoL13
place_city_block["L13"] = place_city_block["name"]
GeoL13_v1 = place_city_block.reindex(columns = ["L13", "geometry"])
GeoL13 = gpd.GeoDataFrame(GeoL13_v1,geometry="geometry")

    #Creation du shp de niveau d'adressage L14 constitu� des RUES et agregeant les buffers de 25m autour des "highway"
#Charger les shapes L14
highway = gpd.read_file("highway.shp", header = None, index_col = 0)
#combiner les shapes pour former GeoL14
highway = highway.fillna("")
highway.loc[highway.name != "", "L14"] = highway["name"]
highway.loc[highway.name == "", "L14"] = highway["ref"]
highway["L14"] = highway.L14.str.replace("DF-140;DF-436","DF 140") 
highway['geometry'] = highway.geometry.buffer(0.00025)
GeoL14_v1 = highway.reindex(columns = ["L14", "geometry"])
GeoL14 = gpd.GeoDataFrame(GeoL14_v1,geometry="geometry")
GeoL14 = GeoL14.fillna("")
GeoL14 = GeoL14.loc[GeoL14["L14"]!="",:]
GeoL14["L14"] = GeoL14.L14.str.replace("ã","�")
GeoL14["L14"] = GeoL14.L14.str.replace("â","�")

#Charger le shape enveloppe Sao Sebastiao
loc_name_RA14 = gpd.read_file("loc_name_RA14.shp", header = None, index_col = 0)

GeoL11_GeoL12 = gpd.overlay(GeoL11, GeoL12, how='intersection')
GeoL11_GeoL13 = gpd.overlay(GeoL11, GeoL13, how='intersection')
GeoL11_GeoL14 = gpd.overlay(GeoL11, GeoL14, how='intersection')
GeoL12_GeoL13 = gpd.overlay(GeoL12, GeoL13, how='intersection')
GeoL12_GeoL14 = gpd.overlay(GeoL12, GeoL14, how='intersection')
GeoL13_GeoL14 = gpd.overlay(GeoL13, GeoL14, how='intersection')
GeoL11_GeoL12_GeoL13 = gpd.overlay(GeoL11_GeoL12, GeoL13, how='intersection')
GeoL11_GeoL12_GeoL14 = gpd.overlay(GeoL11_GeoL12, GeoL14, how='intersection')
GeoL12_GeoL13_GeoL14 = gpd.overlay(GeoL13_GeoL14, GeoL12, how='intersection')
GeoL11_GeoL13_GeoL14 = gpd.overlay(GeoL13_GeoL14, GeoL11, how='intersection')
GeoL11_GeoL12_GeoL13_GeoL14 = gpd.overlay(GeoL11_GeoL12, GeoL13_GeoL14, how='intersection')

GeoConcat = pd.concat([GeoL11, GeoL12, GeoL13, GeoL14, GeoL11_GeoL12, GeoL11_GeoL13, GeoL11_GeoL14, GeoL12_GeoL13, GeoL12_GeoL14, GeoL13_GeoL14, GeoL11_GeoL12_GeoL13, GeoL11_GeoL12_GeoL14, GeoL12_GeoL13_GeoL14, GeoL11_GeoL13_GeoL14, GeoL11_GeoL12_GeoL13_GeoL14], sort=False)
GeoConcat = gpd.overlay(GeoConcat, loc_name_RA14, how='intersection')
GeoConcat = GeoConcat.fillna("")

GeoConcat["adresse"] = GeoConcat['L14'] + "," + GeoConcat['L13'] + "," + GeoConcat['L12'] + "," + GeoConcat["L11"]

GeoConcat = GeoConcat.dissolve(by="adresse", as_index=False)

GeoConcat.to_file("GeoConcat.shp")