# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImobItem(scrapy.Item):
    # define the fields for your item here like:
    _id: scrapy.Field()
    code = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    common_price = scrapy.Field()
    url = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    total_area = scrapy.Field()
    util_area = scrapy.Field()
    bathrooms = scrapy.Field()
    suites = scrapy.Field()
    age = scrapy.Field()
    parking = scrapy.Field()
    price_changed = scrapy.Field()