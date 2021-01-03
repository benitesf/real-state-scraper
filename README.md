# Scraper for real-state information
Extract information from real-state web pages with the purpose of getting insights.

## Stages

* Scrape web page information
* Save information
* Visualize information

## Scraping

1. Select **mode** and **location**.
2. Find paging object.
3. Iterate over pages to get all postings.
4. Iterate over posts to extract the info.
5. Save information.

## Database schema
We consider 2 tables *Province* and *Mode*.
The table mode is a generalization from different tables:
- sale
- rental
- temporal
- project
	- pre-sale-plan
	- pre-sale-building
	- pre-sale-premiere

There is a relation 1 to * between Pronvince and Mode tables.

Sale(id_urbania, id_publisher, date, title, price_id, operation, property, location_id, prop_feat_id, gen_feat_id, description)
Price()
Location(cod, name)
PropertyFeatures()
GeneralFeatures()
