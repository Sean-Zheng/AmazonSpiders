# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonspidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    page_index = scrapy.Field()
    page_link = scrapy.Field()
    commodity_img = scrapy.Field()
    commodity_link = scrapy.Field()
    pass
