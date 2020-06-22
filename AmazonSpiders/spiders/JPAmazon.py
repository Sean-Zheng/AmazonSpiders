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
        write_log('开始爬取网址：{}'.format(response.url))
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
        if not next_url or int(page_index) > 10:
            if next_url is None and int(page_index) != 10:
                write_log('下一页链接获取失败，程序退出')
            elif page_index is None or page_index == '':
                write_log('当前页数获取失败，程序退出')
            else:
                write_log('未知错误')
            return
        else:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True)
        pass
