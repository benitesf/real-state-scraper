import cloudscraper
import re
import random
import time
from bs4 import BeautifulSoup

def get_page(url):
  scr = cloudscraper.create_scraper().get(url)
  cnt = scr.content
  return BeautifulSoup(cnt, 'lxml')

def get_n_pages(src_url, number):
	"""
	Returns n pages from url
	"""
	base = src_url
	last = False
	n = 1

	for i in range(0, number):
		if last:
			break
		url = base + "?page=" + str(n)
		page = get_page(url)
		last = is_last_page(page)
		yield page
		n += 1
	

def get_next_page(src_url):
	"""
	Finds the next page postings if exists
	"""
	base = src_url
	n = 1
	last = False

	while True:
		if last:
			break
		url = base + "?page=" + str(n)
		page = get_page(url)
		last = is_last_page(page)
		yield page
		n += 1

def is_last_page(page):
	"""
	Check if the current page contains lastPage: true
	"""
	links = page.find_all("script")
	last_page_patt = re.compile(r"'lastPage': (.*?),")
	no_res_patt = re.compile(r"const\s+noResults\s+=\s+(.*?);")

	"""for s in links:
		data = s.string
		if type(data) is type(None):
			continue
		m = re.search(p, data)
		if m:
			if m.group(1) == 'true':
				return True"""

	lp = search_pattern(last_page_patt, links)
	nr = search_pattern(no_res_patt, links)

	if lp.strip() == 'true' or nr.strip() == 'true':
		return True

	return False

def search_pattern(pattern, resultSet):
	"""
	Iterates over a resultset to find a pattern
	"""
	value = ""
	for s in resultSet:
		data = s.string
		if type(data) is type(None):
			continue
		m = re.search(pattern, data)
		if m:
			value = m.group(1)
			break
	return value

def sleep_random_between(start, stop):
	"""
	Sleeps random between start and stop seconds to prevent been blocked
	"""
	time.sleep(random.randint(start, stop))
