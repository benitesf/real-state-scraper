import re
import common

def get_postings(page):
	"""
	Returns all the postings that can be found on the page in a list
	"""
	return page.find_all("div", {"class": "postingCard"})

def get_post_link(post):
	"""
	Finds the a tag and extract the href field
	"""
	tag = post.find("a", {"class": "go-to-posting"})
	if tag is None:
		return None
	return tag["href"]


def extract_title(post):
	"""
	Extracts title from article container

	Returns
	-------
	title: string.
	"""
	art = post.find("div", {"id": "article-container"})
	tit = art.find("hgroup", {"class": "title-container"})

	title = tit.find("h2", class_="title-type-sup").text
	return title

def extract_date(post):
	"""
	Extracts date from section container

	Returns
	-------
	date: string
	"""
	section = post.find("section", class_="article-section article-section-description")
	date = section.find("span", class_="section-date").text.strip()

	return date

def extract_operation(post):
	"""
	Extracts operation type from js

	Returns
	-------
	operation: string
	"""
	script = post.find_all("script")
	operation_pattern = re.compile(r"'operationType'\s*:\s*(.*?),")
	operation = common.search_pattern(operation_pattern, script)

	return operation

def extract_property(post):
	"""
	Extracts property type from js

	Returns
	-------
	property: string
	"""
	script = post.find_all("script")
	property_pattern = re.compile(r"'propertyType'\s*:\s*(.*?),")
	property_ = common.search_pattern(property_pattern, script)

	return property_

def extract_property_features(post):
	"""
	Extracts the property features from js

	Returns
	-------
	features: dict
	"""
	features = {}

	icons = post.find_all("li", class_="icon-feature")
	if len(icons) == 0:
		return features

	for i in icons:
		label = i.i["class"][0]
		text = i.text.strip()
		features[label] = text
		
	return features

def extract_general_features(post):
	"""
	Extracts the general features from js

	Returns
	-------
	features: string 
	"""
	script = post.find_all("script")
	feature_pattern = re.compile(r"'generalFeatures'\s*:\s*({.*\d?}),")
	feature = common.search_pattern(feature_pattern, script)

	if feature == "":
		feature = "{}"

	return feature

def extract_description(post):
	"""
	Extracts the description from js
	
	Returns
	-------
	description: string
	"""
	script = post.find_all("script")
	desc_pattern = re.compile(r"'description'\s*:\s*\"(.*?)\",")
	desc = common.search_pattern(desc_pattern, script)

	return desc

def extract_location(post):
	"""
	Extracts the location info from js

	Returns
	-------
	province: string
	city: string
	neighborhood: string
	address: string
	"""
	script = post.find_all("script")
	province_pattern = re.compile(r"'province'\s*:\s*(.*?),")
	city_pattern = re.compile(r"'city'\s*:\s*(.*?),")
	neighborhood_pattern = re.compile(r"'neighborhood'\s*:\s*(.*?),")
	address_pattern = re.compile(r"'address'\s*:\s*{\"name\":\"(.*?)\",")

	province = common.search_pattern(province_pattern, script)
	city = common.search_pattern(city_pattern, script)
	neighborhood = common.search_pattern(neighborhood_pattern, script)
	address = common.search_pattern(address_pattern, script)

	return province, city, neighborhood, address

def extract_location_id(post):
	"""
	Extracts the location id info from js

	Returns
	-------
	province_id: string
	city_id: string
	neighborhood_id: string
	"""
	script = post.find_all("script")
	prov_id_patt = re.compile(r"'provinceId'\s*:\s*(.*?),")
	city_id_patt = re.compile(r"'cityId'\s*:\s*(.*?),")
	neig_id_patt = re.compile(r"'neighborhoodId'\s*:\s*(.*?),")

	prov_id = common.search_pattern(prov_id_patt, script)
	city_id = common.search_pattern(city_id_patt, script)
	neig_id = common.search_pattern(neig_id_patt, script)

	return prov_id, city_id, neig_id

def extract_publisher_data(post):
	"""
	Extracts publisher data from js

	Returns
	-------

	id_urbania: string
	id_publisher: string
	"""
	script = post.find_all("script")
	
	id_urbania_pattern = re.compile(r"'idAviso'\s*:\s*(.*?),")
	id_urbania = common.search_pattern(id_urbania_pattern, script)

	id_publisher_pattern = re.compile(r"'postingCode'\s*:\s*(.*?),")
	id_publisher = common.search_pattern(id_publisher_pattern, script)

	return id_urbania, id_publisher


def extract_sell_price(post):
	"""
	Extracts sell price data from js

	Returns
	-------
	price: string
	"""
	script = post.find_all("script")
	price_pattern = re.compile(r"'sellPrice'\s*:\s*(.*\d?),")
	price = common.search_pattern(price_pattern, script)

	return price

def extract_rental_price(post):
	"""
	Extracts rental price data from js

	Returns
	-------
	rental_price: string
	"""
	script = post.find_all("script")
	price_pattern = re.compile(r"'rentalPrice'\s*:\s*(.*\d?),")
	price = common.search_pattern(price_pattern, script)

	return price
