##########IMPORT##########

import pandas as pd
import numpy as np
import geopandas as gpd
import re
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

Dengue = gpd.read_file("Dengue.shp", header = None, index_col = 0)

DengueCentroid = pd.DataFrame()
DengueCentroid["Location ID"]=Dengue["index"]
DengueCentroid["Number of Cases"]="1"
DengueCentroid["Date/Time"]=Dengue["DT_SIN_PRI"]
DengueCentroid["Habitat"]=Dengue["Habitat"]
DengueCentroid['geometry'] = Dengue.geometry.centroid
DengueCentroid = gpd.GeoDataFrame(DengueCentroid,geometry="geometry")


outdf = gpd.GeoDataFrame(columns=Dengue.columns)
for idx, row in Dengue.iterrows():
    if type(row.geometry) == Polygon:
        outdf = outdf.append(row,ignore_index=True)
    if type(row.geometry) == MultiPolygon:
        multdf = gpd.GeoDataFrame(columns=Dengue.columns)
        recs = len(row.geometry)
        multdf = multdf.append([row]*recs,ignore_index=True)
        for geom in range(recs):
            multdf.loc[geom,'geometry'] = row.geometry[geom]
        outdf = outdf.append(multdf,ignore_index=True)

from shapely.geometry import Point

col = outdf.columns.tolist()

nodes = gpd.GeoDataFrame(columns=col)

for index, row in outdf.iterrows():
    for j in list(row['geometry'].exterior.coords): 
        nodes = nodes.append({'index': row['index'], 'DT_SIN_PRI':row['DT_SIN_PRI'],'adresse':row['adresse'],'SOROTIPO':row['SOROTIPO'],'Habitat':row['Habitat'], 'geometry':Point(j) },ignore_index=True)

nodes['x'] = nodes['geometry'].apply(lambda p: p.x)
nodes['y'] = nodes['geometry'].apply(lambda p: p.y)
del nodes["DT_SIN_PRI"]
del nodes["adresse"]
del nodes["SOROTIPO"]
del nodes["geometry"]
del nodes["Habitat"]

MergeDistance = pd.merge(nodes, DengueCentroid, how = 'inner', left_on = "index", right_on = "Location ID", sort = False)

MergeDistance['x_cent'] = MergeDistance['geometry'].apply(lambda p: p.x)
MergeDistance['y_cent'] = MergeDistance['geometry'].apply(lambda p: p.y)
del MergeDistance["Date/Time"]
del MergeDistance["Number of Cases"]
del MergeDistance["Location ID"]
del MergeDistance["geometry"]

MergeDistance['Imprecision'] = np.sqrt( (MergeDistance.x-MergeDistance.x_cent)**2 + (MergeDistance.y-MergeDistance.y_cent)**2 )* 100000

del MergeDistance["x"]
del MergeDistance["y"]
del MergeDistance["x_cent"]
del MergeDistance["y_cent"]
del MergeDistance["Habitat"]

MergeDistance.set_index("index", inplace=True)

MergeDistance = MergeDistance.min(level='index')

MergeDistance=MergeDistance.reset_index()


DengueCentroid = pd.merge(DengueCentroid, MergeDistance, how = 'inner', left_on = "Location ID", right_on = "index", sort = False)

del DengueCentroid["index"]

DengueCentroid.to_file("DengueCentroid.shp")

DengueCentroid