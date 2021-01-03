#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 14:40:54 2020

@author: joker
"""

import os
import datetime
import pandas as pd
import _pickle as pkl
import seaborn as sns

import filter
import macros

data = []
filename = os.path.join(os.getcwd(), "data", "raw", "sale_31-12-2020.data")
with open(filename, 'rb') as fr:
    try:
        while True:
            data.append(pkl.load(fr))
    except EOFError:
        pass
    

cols = ["id_urbania", "id_publisher", "date", "title", "description",
        "sell_price", "rental_price", "operation", "property",
        "province_id", "province", "city_id", "city", "neighborhood_id",
        "neighborhood", "address", "antiquity", "bathroom", "toilet",
        "bedroom", "covered_area", "total_area", "garage", "url"]
df = pd.DataFrame()


for chunk in data:
    for row in chunk:
        id_urbania = row["id"]["id_urb"]
        id_publisher = row["id"]["id_pub"]
        date = row["date"]
        title = row["title"]
        description = row["desc"]
        sell_price = row["price"]["sell_price"]
        rental_price = row["price"]["rental_price"]
        operation = row["oper"]
        property_ = row["prop"]
        province_id = row["loc"]["prov"]["id"]
        province = row["loc"]["prov"]["value"]
        city_id = row["loc"]["city"]["id"]
        city = row["loc"]["city"]["value"]
        neighborhood_id = row["loc"]["neigh"]["id"]
        neighborhood = row["loc"]["neigh"]["value"]
        address = row["loc"]["addr"]
        url = row["url"]
        
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

        s = pd.Series([id_urbania, id_publisher, date, title, description,
                       sell_price, rental_price, operation, property_,
                       province_id, province, city_id, city, neighborhood_id,
                       neighborhood, address, antiquity, bathroom, toilet, 
                       bedroom, covered_area, total_area, garage, url])
        row_df = pd.DataFrame([s])
        df = pd.concat([row_df, df], ignore_index=True)


df.columns = cols
now = datetime.datetime.now()
#df_f = df.copy()

# Clean and filter data
df = filter.clean_single_quote(df)
df = filter.clean_double_quote(df)
df = filter.strip(df)
df["date"] = df["date"].apply(filter.calculate_date, args=(now,))
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
df = df.astype({"id_urbania": str, "id_publisher": str, "date": str,
                "title": str, "description": str, "sell_price": int,
                "rental_price": int, "operation": str, "property": str,
                "province_id": str, "province": str, "city_id": str,
                "city": str, "neighborhood_id": str, "neighborhood": str,
                "address": str, "antiquity": int, "bathroom": int,
                "toilet": int, "bedroom": int, "covered_area": int,
                "total_area": int, "garage": int, "url": str
                })

to_filename = os.path.join(os.getcwd(), "data", "extracted", "sale_extracted_31-12-2020.data")
df.to_pickle(to_filename)

"""
lima_df = df[df["province"] == "Lima"][["date", "sell_price", "antiquity",
                                        "bathroom", "toilet", "bedroom",
                                        "covered_area", "total_area", "garage"]]
"""