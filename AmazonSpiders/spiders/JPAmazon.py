# -*- coding: utf-8 -*-
import scrapy
from AmazonSpiders.items import AmazonspidersItem
from AmazonSpiders.log import write_log, remove_log


class JpamazonSpider(scrapy.Spider):
    name = 'JPAmazon'
    allowed_domains = ['amazon.co.jp']

    def __init__(self, search_key=None, *args, **kwargs):
        super(JpamazonSpider, self).__init__(*args, **kwargs)
        remove_log()
        self.start_urls = [
            'https://www.amazon.co.jp/s?k={}&__mk_ja_JP=カタカナ&ref=nb_sb_noss_2'.format(search_key)]

    def parse(self, response):
        commodity_list = response.xpath(
            "//div[@class='a-section a-spacing-medium']")
        for commodity in commodity_list:
            item = AmazonspidersItem()
            item['name'] = commodity.xpath(
                "./div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a/span/text()").extract_first()
            item['url'] = response.urljoin(
                commodity.xpath("./span/a/@href").extract_first())
            yield item
        current_page = response.xpath(
            "//li[@class='a-selected']/a/text()")
        print("*"*50)
        print(current_page)
        next_url = response.xpath(
            "//li[@class='a-last']/a/@href").extract_first()

        print('current page is page {}'.format(current_page.get()))
        print('{}'.format(response.urljoin(next_url)))
        print('#'*50)
        write_log('current page is page {}'.format(current_page.get()))
        if not next_url or int(current_page.get()) > 10:
            return
        else:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True)
        pass
