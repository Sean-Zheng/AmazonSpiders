# -*- coding: utf-8 -*-
import scrapy


class UsamazonSpider(scrapy.Spider):
    name = 'USAmazon'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    def parse(self, response):
        pass
