#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 14:40:54 2020

@author: joker
"""

import pandas as pd
import _pickle as pkl

import filter
from variables import *

data = []
filename = "sale.data"
with open(filename, 'rb') as fr:
    try:
        while True:
            data.append(pkl.load(fr))
    except EOFError:
        pass
    

cols = ["id_urbania", "date", "sell_price",
        "rental_price", "operation", "property",
        "province", "city", "neighborhood",
        "antiquity", "bathroom", "toilet", "bedroom",
        "covered_area", "total_area", "garage"]
df = pd.DataFrame()


for chunk in data:
    for row in chunk:
        id_urbania = row["id"]["id_urb"]
        date = row["date"]
        sell_price = row["price"]["sell_price"]
        rental_price = row["price"]["rental_price"]
        operation = row["oper"]
        property_ = row["prop"]
        province = row["loc"]["prov"]["value"]
        city = row["loc"]["city"]["value"]
        neighborhood = row["loc"]["neigh"]["value"]
        
        antiquity = ''
        bathroom = ''
        toilet = ''
        bedroom = ''
        covered_area = ''
        total_area = ''
        garage = ''
        
        feats = row["prop_feat"]
        if "icon-antiguedad" in feats:
            antiquity = feats["icon-antiguedad"]
        if "icon-bano" in feats:
            bathroom = feats["icon-bano"]
        if "icon-toilete" in feats:
            toilet = feats["icon-toilete"]
        if "icon-dormitorio" in feats:
            bedroom = feats["icon-dormitorio"]
        if "icon-scubierta" in feats:
            covered_area = feats["icon-scubierta"]
        if "icon-stotal" in feats:
            total_area = feats["icon-stotal"]
        if "icon-cochera" in feats:
            garage = feats["icon-cochera"]

        s = pd.Series([id_urbania, date, sell_price, rental_price, operation,
                       property_, province, city, neighborhood, antiquity,
                       bathroom, toilet, bedroom, covered_area, total_area, garage])
        row_df = pd.DataFrame([s])
        df = pd.concat([row_df, df], ignore_index=True)

df.columns = cols

df_f = df.copy()

# Filter Data
df = filter.clean_single_quote(df)
df = filter.strip(df)
df["date"] = df["date"].apply(filter.calculate_date)
df["sell_price"] = df["sell_price"].apply(filter.extract_only_number)
df["rental_price"] = df["rental_price"].apply(filter.extract_only_number)
df["antiquity"] = df["antiquity"].apply(filter.clean_antiquity)
df["bathroom"] = df["bathroom"].apply(filter.extract_only_number)
df["toilet"] = df["toilet"].apply(filter.extract_only_number)
df["bedroom"] = df["bedroom"].apply(filter.extract_only_number)
df["covered_area"] = df["covered_area"].apply(filter.extract_only_number)
df["total_area"] = df["total_area"].apply(filter.extract_only_number)
df["garage"] = df["garage"].apply(filter.extract_only_number)

# Set types
df = df.astype({"id_urbania": str, "date": str, "sell_price": int,
                "rental_price": int, "operation": str, "property": str,
                "province": str, "city": str, "neighborhood": str,
                "antiquity": int, "bathroom": int, "toilet": int,
                "bedroom": int, "covered_area": int, "total_area": int,
                "garage": int
                })
