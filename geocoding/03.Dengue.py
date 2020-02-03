##########IMPORT##########

import pandas as pd
import numpy as np
import geopandas as gpd
import re

##########Creation des polygones Cas##########
AMerger = pd.read_csv("AMerger.csv")
Impossible = pd.read_csv("Impossible.csv")
base = pd.read_csv("base.csv")
LevTemp2 = pd.read_csv("LevTemp2.csv")
adresseDef = pd.read_csv("adresseDef.csv")
AMerger = AMerger.set_index("index")
AMerger = AMerger.drop(Impossible["index"])
AMerger = AMerger.reset_index()

GeoConcat = gpd.read_file("GeoConcat.shp", header = None, index_col = 0)

MergeCas = pd.DataFrame()           
MergeCas = pd.merge(AMerger, GeoConcat, how = 'inner', left_on = "adresse", right_on = "adresse", sort = False)            
CasDengue = gpd.GeoDataFrame(MergeCas,geometry="geometry")

DengueDissolve = CasDengue.dissolve(by='index', as_index=False)
Dengue = pd.DataFrame()
Dengue["index"]=DengueDissolve["index"]
Dengue["DT_SIN_PRI"]=DengueDissolve["DT_SIN_PRI"]
Dengue['adresse']=DengueDissolve['adresse']
Dengue["SOROTIPO"] = DengueDissolve["SOROTIPO"].apply(str)  
Dengue["geometry"]=DengueDissolve["geometry"]
Dengue["Habitat"]=DengueDissolve["Habitat"]
Dengue = gpd.GeoDataFrame(Dengue,geometry="geometry")

Dengue.to_file("Dengue.shp")

##########Cas non placés##########
PosUndone=AMerger.copy()
PosUndone=PosUndone.set_index("index")
PosUndone=PosUndone.drop(DengueDissolve["index"])
PosUndone=PosUndone.reset_index()

PosUndone = PosUndone.reindex(columns = ["index"])
Undone3 = pd.merge(PosUndone, base, how = 'left' , left_on = "index", right_on = "index", sort = False)
Undone4 = pd.merge(Undone3, LevTemp2, how = 'left' , left_on = "index", right_on = "index", sort = False)
Undone5 = Undone4.reindex(columns = ["index", 'L11quater', "L12", "valL12", "L13", "valL13", "L14", "valL14", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM", "NM_REFEREN"])
Undone = pd.merge(Undone5, adresseDef, how = 'left' , left_on = "index", right_on = "index", sort = False)
Undone = Undone.reindex(columns = ["index", 'L11quater', "L12", "valL12", "L13", "valL13", "L14", "valL14", "adresse", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM", "NM_REFEREN"])

Undone.to_csv("Undone.csv", encoding = "utf-8")