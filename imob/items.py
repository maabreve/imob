# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImobItem(scrapy.Item):
    # define the fields for your item here like:
    _id: scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    common_price = scrapy.Field()
    url = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    area_total = scrapy.Field()
    area_util = scrapy.Field()
    banheiros = scrapy.Field()
    suites = scrapy.Field()
    idade = scrapy.Field()
    vagas = scrapy.Field()