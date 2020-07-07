# -*- coding: utf-8 -*-
import scrapy
from AmazonSpiders.items import AmazonspidersItem


class UsamazonSpider(scrapy.Spider):
    name = 'USAmazon'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?k=iphone&page=1&ref=nb_sb_noss']

    # http://localhost:9080/crawl.json?spider_name=USAmazon&start_requests=true

    def parse(self, response):
        commodity_xpath = '//div[@data-index]//div[@class="sg-col-inner"]/div[@class="a-section a-spacing-none"]//a[@class="a-link-normal a-text-normal"]'
        commodity_list = response.xpath(commodity_xpath)
        page_index = response.xpath(
            "//li[@class='a-selected']/a/text()").get()
        next_url = response.xpath(
            "//li[@class='a-last']/a/@href").get()
        for commodity in commodity_list:
            item = AmazonspidersItem()
            item['name'] = commodity.xpath('./span/text()').get()
            item['page_index'] = page_index
            item['page_link'] = response.url
            item['commodity_link'] = response.urljoin(
                commodity.xpath("./@href").get())
            yield item
        if not next_url or not page_index or int(page_index) > 10:
            return
        else:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True)
        pass
