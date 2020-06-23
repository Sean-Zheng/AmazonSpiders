# -*- coding: utf-8 -*-
import scrapy
from AmazonSpiders.items import AmazonspidersItem
from urllib.request import unquote


class UsamazonSpider(scrapy.Spider):
    name = 'USAmazon'
    allowed_domains = ['amazon.com']

    def __init__(self, search_key=None, Q=None, *args, **kwargs):
        super(UsamazonSpider, self).__init__(*args, **kwargs)
        self.Q = Q
        self.start_urls = [
            'https://www.amazon.com/s?k={}&ref=nb_sb_noss'.format(search_key)]

    def parse(self, response):
        self.Q.put('开始爬取网址：{}'.format(unquote(response.url, 'utf-8')))
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
        if not next_url or int(page_index) > 10:
            if (next_url is None or next_url == '') and int(page_index) != 10:
                self.Q.put('下一页链接获取失败，程序退出')
            elif page_index is None or page_index == '':
                self.Q.put('当前页数获取失败，程序退出')
            return
        else:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True)
        pass

    @staticmethod
    def close(spider, reason):
        spider.Q.put('爬取结束')
