# -*- coding: utf-8 -*-
import scrapy
from AmazonSpiders.items import AmazonspidersItem
from urllib.request import unquote


class JpamazonSpider(scrapy.Spider):
    name = 'JPAmazon'
    allowed_domains = ['amazon.co.jp']
    start_urls = [
        'https://www.amazon.co.jp/s?k=iPhone&page=1&__mk_ja_JP=カタカナ&ref=sr_pg_1']

    def parse(self, response):
        commodity_list = response.xpath(
            "//div[@class='a-section a-spacing-medium']")
        page_index = response.xpath(
            "//li[@class='a-selected']/a/text()").get()
        next_url = response.xpath(
            "//li[@class='a-last']/a/@href").get()
        for commodity in commodity_list:
            item = AmazonspidersItem()
            item['name'] = commodity.xpath(
                "./div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a/span/text()").get()
            item['page_index'] = page_index
            item['page_link'] = response.url
            item['commodity_link'] = response.urljoin(
                commodity.xpath("./span/a/@href").get())
            yield item
        if not next_url or not page_index or int(page_index) > 10:
            return
        else:
            yield scrapy.Request(response.urljoin(next_url),
                                 callback=self.parse, dont_filter=True)
