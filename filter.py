import datetime
import re
import pandas as pd

def clean_single_quote(df):
	return df.applymap(lambda x: x.replace("'", ""))

def clean_double_quote(df):
	return df.applymap(lambda x: x.replace("\"", ""))

def strip(df):
	return df.applymap(lambda x: x.strip())

def calculate_date(x, now):
	"""
	Acts as lambda function to calculate the date from current one
	"""
	#now = datetime.datetime.now()
	n = int(extract_only_number(x))
	if n > 0:
		return (now - datetime.timedelta(n)).strftime("%d-%m-%Y")
	return now.strftime("%d-%m-%Y")
	
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
	now = datetime.datetime.now().year
	m = re.match(r'^A estrenar$', x)
	if m:
		return now

	n = int(extract_only_number(x))
	if n > 0:
		return now - n
	return -1
