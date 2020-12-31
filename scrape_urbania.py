#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:49:26 2020

@author: joker
"""


import os
import datetime
import json
import logging
import _pickle as pkl

import common
import sale
import macros

logging.basicConfig(level=logging.INFO)

def scrape_sell(base_url, action, mode, locs, fp):
    logging.info("Scraping sale mode")
    batch = 32
    data = []
    
    for k in locs:
        logging.info(f'location: {locs[k]}')
        url = base_url + "/" + action + "/" + mode + locs[k]        
        #pages = [p for p in common.get_n_pages(url, 2)]
        
        for page in common.get_next_page(url):
            posts = sale.get_postings(page)
            if posts is None:
                logging.warning("Posts is None, avoiding")
                continue
            for post in posts:
                p_link = sale.get_post_link(post)
                if p_link is None:
                    logging.warning("Post link is None, avoiding")
                    continue
                if 'proyecto' in p_link:
                    continue
                common.sleep_random_between(2, 4)
                p_link = base_url + p_link
                post_page = common.get_page(p_link)
                try:
                    row = extract_sale_info(post_page)
                    row["url"] = p_link
                    data.append(row)
                    
                    if len(data) % batch == 0:
                        pkl.dump(data, fp)
                        del data[:]
                except Exception as e:
                    logging.error("While extracting sale info", exc_info=True)
    
    if len(data) > 0:
        pkl.dump(data, fp)
        del data[:]
                
def extract_sale_info(post_page):
    id_urbania, id_publisher = sale.extract_publisher_data(post_page)
    date = sale.extract_date(post_page)
    title = sale.extract_title(post_page)
    sell_price = sale.extract_sell_price(post_page)
    rental_price = sale.extract_rental_price(post_page)
    operation = sale.extract_operation(post_page)
    property_ = sale.extract_property(post_page)
    province, city, neighborhood, address = sale.extract_location(post_page)
    prov_id, city_id, neig_id = sale.extract_location_id(post_page)
    property_features = sale.extract_property_features(post_page)
    general_features = sale.extract_general_features(post_page)
    description = sale.extract_description(post_page)
    
    jsonData = json.loads(general_features)

    genfeats = []
    for k in jsonData:
        serv = jsonData[k]
        for ks in serv:
            feat = serv[ks]
            row = {
                "id" : feat["featureId"],
                "label": feat["label"],
                "measure": feat["measure"],
                "value": feat["value"]
                }
            genfeats.append(row)
    
    row = {
        "id": {
            "id_urb": id_urbania,
            "id_pub": id_publisher
            },
        "date": date,
        "title": title,
        "price": {
            "sell_price":  sell_price,
            "rental_price": rental_price
            },
        "oper": operation,
        "prop": property_,
        "loc": {
            "prov": {
                "id": prov_id,
                "value": province
                },
            "city": {
                "id": city_id,
                "value": city
                },
            "neigh": {
                "id": neig_id,
                "value": neighborhood
                },
            "addr": address,
            },
        "prop_feat": property_features,
        "gen_feat": genfeats,
        "desc": description
        }
    return row
           

if __name__ == "__main__":
    outdir = "data"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    # Scraper sale mode and save as pickle
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    filename = os.path.join(outdir, f"sale_{date}.data")
    
    with open(filename, 'ab+') as fp:
        scrape_sell(macros.BASE_URL, macros.ACTION["find"], 
                    macros.MODE["sale"], macros.LOCATION, fp)
    