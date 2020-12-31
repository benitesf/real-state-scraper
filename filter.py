import datetime
import re
import pandas as pd

def clean_single_quote(df):
	return df.applymap(lambda x: x.replace("'", ""))

def strip(df):
	return df.applymap(lambda x: x.strip())

def calculate_date(x):
	"""
	Acts as lambda function to calculate the date from current one
	"""
	now = datetime.datetime.now()
	n = extract_only_number(x)
	if n == 0:
		return now.strftime("%d-%m-%Y")
	
	return (now - datetime.timedelta(int(n))).strftime("%d-%m-%Y")
	

def extract_only_number(x):
	"""
	Acts as a lambda to filtering only numbers
	"""
	r = re.findall(r'\d+', x)
	if len(r) > 0:
		return r[0]
	return 0

def clean_antiquity(x):
	"""
	Acts as a lambda to filtering antiquity column
	"""
	m = re.match(r'^A estrenar$', x)
	if m:
		return 0
	
	r = re.findall(r'\d+', x)
	if len(r) > 0:
		return r[0]
	return -1
