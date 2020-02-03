# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import geopandas as gpd
import re

##########Ouverture de la base des cas de dengue 2010##########
an=["2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014"]
base=pd.DataFrame()
for y in an :
    excl= "Dengue"+y+".xlsx"
    onglet="dengue"+y
    basey = pd.read_excel(excl, onglet)
    basey = basey[(basey.RA == "SAO SEBASTIAO")|(basey.RA == "S�O SEBASTI�O")|(basey.RA == "S�O SEBASTIAO")]
    #creation d'un index
    basey["index"] = basey.index.values.tolist()
    basey["index"] = basey["index"].astype(int)+1
    basey["index"] = y+"_"+basey["index"].astype(str)
    base = pd.concat([base, basey])

base.set_index("index", inplace=True)
base=base.reset_index()
    
    #Ouverture du fichier Level.xlsx qui va permettre de formater les noms de rue et de quartier selon plusieur niveaux :
L11 = pd.read_excel("Level.xlsx","L11")    #Niveau L11 = niveau quartiers
L12 = pd.read_excel("Level.xlsx","L12")    #Niveau L12 = niveau quadras
L13 = pd.read_excel("Level.xlsx","L13")    #Niveau L13 = niveau conjuntos
L14 = pd.read_excel("Level.xlsx","L14")    #Niveau L14 = niveau rues
L15 = pd.read_excel("Level.xlsx","L15")    #Niveau L15 = niveau casas
L16 = pd.read_excel("Level.xlsx","L16")    #Niveau L16 = niveau appartements
L11bis = pd.read_excel("Level.xlsx","L11bis")    #Niveau L11bis = quartiers et rues avec des noms compos�s
L11ter = pd.read_excel("Level.xlsx","L11ter")    #Niveau L11ter = quartiers avec des noms compos�s

    #creation d'un tableau adresse1 avec la colonne index et les 4 colonnes de la base Dengue contenant des informations d'adresse
adresse1 = pd.concat([base["index"], base["NM_LOGRADO"], base["NM_COMPLEM"], base["NU_NUMERO"], base["NM_REFEREN"]], axis = 1)
    #convertion des cellules Nan en cellules vides
adresse1 = adresse1.fillna("")
    
    #creation de la colonne adresse comprenant la valeur LOGRADO si elle existe ou la valeur COMPLEM si LOGRADO n'existe pas
adresse1.loc[adresse1.NM_LOGRADO == "", "adresse"] = adresse1["NM_COMPLEM"]
adresse1.loc[adresse1.NM_LOGRADO != "", "adresse"] = adresse1["NM_LOGRADO"]
    #creation de la colonne complement pour mettre les valeurs de COMPLEM qui n'ont pas �t� apport�es a LOGRADO (en general un nom de quartier)
adresse1.loc[adresse1.NM_LOGRADO != "", "complement"] = adresse1["NM_COMPLEM"]
    #comblement de la colonne complement avec les valeurs de REFEREN
adresse1.loc[adresse1.NM_REFEREN != "", "complement"] = adresse1["NM_REFEREN"]

    #formatage de la partie complement en fonction des quartier decrits dans Niveau L11
adresse1 = pd.merge(adresse1, L11, how = 'left' , left_on = "complement", right_on = "oldad", sort = False)
del adresse1['complement']
del adresse1["oldad"]

    #remplacement des caracteres ".", "_", "�", ",", "-", "]" par " "
adresse1["adresse"] = adresse1.adresse.str.replace("."," ")
adresse1["adresse"] = adresse1.adresse.str.replace("'"," ")
adresse1["adresse"] = adresse1.adresse.str.replace("CJ"," CJ")
adresse1["adresse"] = adresse1.adresse.str.replace("CONJ"," CONJ")
adresse1["adresse"] = adresse1.adresse.str.replace("_"," ")
adresse1["adresse"] = adresse1.adresse.str.replace("-"," ")
adresse1["adresse"] = adresse1.adresse.str.replace("�"," ")
adresse1["adresse"] = adresse1.adresse.str.replace(","," ")
adresse1["adresse"] = adresse1.adresse.str.replace("]"," ")
adresse1["adresse"] = adresse1.adresse.str.replace("  "," ")
adresse1["adresse"] = adresse1.adresse.str.replace("("," ")
adresse1["adresse"] = adresse1.adresse.str.replace("  "," ")
adresse1["adresse"] = adresse1.adresse.str.replace("+","A")
adresse1["adresse"] = adresse1.adresse.str.replace("+","E")

    #Formatage des nom de rue ou de quartier comprenant plusieurs mots dans LOGRADO
myList = L11bis.oldad.values.tolist()
for l in [L11bis] :
    for q in l['oldad'].values.tolist() :
        a = myList.index(q)
        r = l.iloc[a,1]
        adresse1["adresse"] = adresse1.adresse.str.replace(str(q),str(r))

    #convertion des cellules Nan en cellules vides
adresse1 = adresse1.fillna("")

    #suppression des colonnes LOGRADO et COMPLEM
del adresse1['NM_LOGRADO']
del adresse1["NM_COMPLEM"]
del adresse1["NM_REFEREN"]

    #renommer la premiere colonne numero
adresse1.columns = ["index", "numero", "adresse", "complement"]


    #creation d'une table adresseSplit avec 15 colonnes issues du d�coupage des chaines de caracteres de la colonne adresse s�par�s par " "
adresseSplit = adresse1.adresse.str.split(pat = " ", expand=True)
adresseSplit.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
adresseSplit["index"] = adresse1["index"]

    #convertir les cellules Nan en cellules vides
for j in adresseSplit.columns :
    adresseSplit[j] = adresseSplit[j].fillna("")

    #R�organisation de la table adresse1
del adresse1['adresse']                                    #suppression de la colonne adresse
adresse1["numero"] = adresse1["numero"].apply(str)         #conversion de la colonne numero en str
adresse1["complement"] = adresse1["complement"].apply(str) #conversion de la colonne complement en str
adresse1["complement"] = adresse1.complement.fillna("")    #convertir les cellules Nan en cellules vides dans la colonne complement

    #creation des niveaux d'adressage
s = [L12,L13,L14,L15,L16,L11ter]  
LevTemp2=pd.DataFrame()
for i in s :
    LevTemp = adresseSplit.copy()
    for j in LevTemp.drop(['index'], axis=1).columns :
        LevTemp=pd.merge(LevTemp, i, how = 'left', left_on = j, right_on = "oldad", sort = False)
        del LevTemp[j]
        del LevTemp["oldad"]
        LevTemp = LevTemp.fillna("")
        LevTemp.loc[LevTemp.level != "", "temp"] = LevTemp["level"]
        del LevTemp["level"]
        LevTemp2[i.iloc[0, 1]] = LevTemp["temp"]

adresse1.loc[LevTemp2.L11ter != "", "complement"] = LevTemp2["L11ter"]
LevTemp2["index"] = LevTemp["index"]
LevTemp2["L11quater"] = adresse1["complement"]

    #remplissage des valeurs d'adressage
# pour chaque ligne on cherche la colonne "m" ou il y a une valeur de la liste de niveau "l" pris dans les listes L12, L13,...

for l in s :
    adresse3 = adresseSplit.copy()
    for m in adresse3.drop(['index'], axis=1).columns:
        for q in l['oldad'].values.tolist() :
            adresse3.loc[adresse3[m] == q, "ValQ"] = adresse3.iloc[:,int(m)]
            adresse3 = adresse3.fillna("")
            liste = adresse3["ValQ"]
            for cel in range(0, len(liste)) :
                txt = liste[cel]
                x = re.search("^[1-9][a-zA-Z]", txt)
                y = re.search("^[1-9]$", txt)
                if (x or y):
                    liste[cel] = "0"+txt
            adresse3["ValQ"] = adresse3.ValQ.str.replace("_"," ")
    LevTemp2["val"+l.iloc[0, 1]]= adresse3["ValQ"]
    
LevTemp2.loc[LevTemp2.valL12 == "CASA", "L12"] = ""
LevTemp2.loc[LevTemp2.valL12 == "CASA", "valL12"] = ""
    
        #convertion des cellules Nan en cellules vides
for j in LevTemp2.columns :
    LevTemp2[j] = LevTemp2[j].fillna("")
    
    #Cr�ation du fichier CSV "adresseDef" 
adresseDef=pd.DataFrame()
adresseDef["index"] = LevTemp2["index"]
adresseDef.loc[LevTemp2.L14 == "", "L14"] = ""
adresseDef.loc[LevTemp2.L14 != "", "L14"] = LevTemp2["L14"]+ " " + LevTemp2["valL14"]
adresseDef.loc[LevTemp2.L13 == "", "L13"] = ""
adresseDef.loc[LevTemp2.L13 != "", "L13"] = LevTemp2["L13"]+ " " + LevTemp2["valL13"]
adresseDef.loc[LevTemp2.L12 == "", "L12"] = ""
adresseDef.loc[LevTemp2.L12 != "", "L12"] = LevTemp2["L12"]+ " " + LevTemp2["valL12"]
adresseDef.loc[LevTemp2.L15 != "CDP", "Habitat"] = LevTemp2["L15"]
adresseDef.loc[LevTemp2.L16 == "Apartement", "Habitat"] = "Apartement"
adresseDef["adresse"] =  adresseDef['L14'] + "," + adresseDef['L13'] + "," + adresseDef['L12'] + "," + adresse1["complement"]
 
adresseDef=pd.merge(adresseDef, base, how = 'left', left_on = "index", right_on = "index", sort = False)
adresseDef = adresseDef.reindex(columns = ["index", "DT_SIN_PRI", "SEM_PRI", 'adresse', "SOROTIPO", "Habitat"])

##########################################################################################################################
                            ##########Ajout de la date de premier symptome (format dd/mm/yyyy)##########
    
adresseDef["DT_SIN_PRI"] = adresseDef["DT_SIN_PRI"].astype(str)
adresseDef["DT_SIN_PRI"] = pd.to_datetime(adresseDef["DT_SIN_PRI"])
adresseDef['yyyyww'] = adresseDef["DT_SIN_PRI"].dt.strftime('%Y%V')
adresseDef["yyyyww"] = adresseDef["yyyyww"].astype(int)
adresseDef["SEM_PRI"] = adresseDef["SEM_PRI"].astype(int)

adresseDef["compare"] = (adresseDef["yyyyww"]-adresseDef["SEM_PRI"])

adresseDef["year"] = adresseDef["DT_SIN_PRI"].dt.year
adresseDef["year"] = adresseDef["year"].astype(str)

adresseDef["day"] = adresseDef["DT_SIN_PRI"].dt.day
adresseDef["day"] = adresseDef["day"].astype(str)
liste = adresseDef["day"]
for cel in range(0, len(liste)) :
    txt = liste[cel]
    x = re.search("^[1-9]$", txt)
    if x:
        liste[cel] = "0"+txt

adresseDef["month"] = adresseDef["DT_SIN_PRI"].dt.month
adresseDef["month"] = adresseDef["month"].astype(str)
liste = adresseDef["month"]
for cel in range(0, len(liste)) :
    txt = liste[cel]
    x = re.search("^[1-9]$", txt)
    if x:
        liste[cel] = "0"+txt

adresseDef["Date1"]= adresseDef["month"] + "/" + adresseDef["day"] + "/" + adresseDef["year"] 
adresseDef["Date2"]= adresseDef["day"] + "/" + adresseDef["month"] + "/" + adresseDef["year"] 

adresseDef.loc[(adresseDef["compare"] <= 1) & (adresseDef["compare"] >= -1), "Date"] = adresseDef["Date1"]
adresseDef.loc[(adresseDef["compare"] > 1) | (adresseDef["compare"] < -1), "Date"] = adresseDef["Date2"]
adresseDef["DT_SIN_PRI"]=adresseDef["Date"]
adresseDef["SEM_PRI"] = adresseDef["SEM_PRI"].astype(str)

AMerger = adresseDef.reindex(columns = ["index", "DT_SIN_PRI", 'adresse', "SOROTIPO", "Habitat"])
AMerger.to_csv("AMerger.csv", encoding = "utf-8")

##########Determination des adresses impossibles a placer##########

adresseIMP=LevTemp2.copy()

adresseIMP.loc[(adresseIMP.valL13 < "D")& (adresseIMP.valL12 != '')& (adresseIMP.valL13 != ''), "VALID"] = "OK"
adresseIMP.loc[adresseIMP.valL12 >= "26", "VALID"] = "OK"
adresseIMP.loc[(adresseIMP.valL12 > "10")& (adresseIMP.valL12 < '11'), "VALID"] = "OK"
adresseIMP.loc[(adresseIMP.valL12 > "20")& (adresseIMP.valL12 < '21'), "VALID"] = "OK"
adresseIMP.loc[adresseIMP.valL13 > "C", "VALID"] = "OK"
adresseIMP.loc[adresseIMP.valL14 >= "100", "VALID"] = "OK"
adresseIMP.loc[adresseIMP.L11quater != "", "VALID"] = "OK"
adresseIMP.loc[(adresseIMP.valL14 < "A")& (adresseIMP.L11quater == '')& (adresseIMP.valL12 == '')& (adresseIMP.valL13 == ''), "VALID"] = ""

adresseIMP = adresseIMP.reindex(columns = ["index", 'L11quater', "L12", "valL12", "L13", "valL13", "L14", "valL14", "VALID"])
Imp2=adresseIMP.loc[adresseIMP["VALID"]!="OK",:]
Imp3 = pd.merge(Imp2, base, how = 'left' , left_on = "index", right_on = "index", sort = False)
Imp4 = pd.merge(Imp3, adresseDef, how = 'left' , left_on = "index", right_on = "index", sort = False)
Impossible = Imp4.reindex(columns = ["index", 'L11quater', "L12", "valL12", "L13", "valL13", "L14", "valL14", "adresse", "NM_LOGRADO", "NU_NUMERO", "NM_COMPLEM", "NM_REFEREN"])

Impossible.to_csv("Impossible.csv", encoding = "utf-8")
base.to_csv("base.csv", encoding = "utf-8")
LevTemp2.to_csv("LevTemp2.csv", encoding = "utf-8")
adresseDef.to_csv("adresseDef.csv", encoding = "utf-8")