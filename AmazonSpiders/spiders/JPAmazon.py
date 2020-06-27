# -*- coding: utf-8 -*-
import scrapy
from AmazonSpiders.items import AmazonspidersItem
from urllib.request import unquote


class JpamazonSpider(scrapy.Spider):
    name = 'JPAmazon'
    allowed_domains = ['amazon.co.jp']

    def __init__(self, search_key=None, Q=None, *args, **kwargs):
        super(JpamazonSpider, self).__init__(*args, **kwargs)
        self.Q = Q
        self.start_urls = []
        for i in range(1, 11, 1):
            self.start_urls.append(
                'https://www.amazon.co.jp/s?k={}&page={}&__mk_ja_JP=カタカナ&ref=sr_pg_1'.format(search_key, i))
        # https://www.amazon.co.jp/s?k=iPhone&page=2&__mk_ja_JP=カタカナ&ref=sr_pg_1
        # self.start_urls = [
        #     'https://www.amazon.co.jp/s?k={}&__mk_ja_JP=カタカナ&ref=nb_sb_noss_2'.format(search_key)]

    def parse(self, response):
        self.Q.put('\n开始爬取网址：{}'.format(unquote(response.url, 'utf-8')))
        commodity_list = response.xpath(
            "//div[@class='a-section a-spacing-medium']")
        page_index = response.xpath(
            "//li[@class='a-selected']/a/text()").get()
        next_url = response.xpath(
            "//li[@class='a-last']/a/@href").get()
        results = []
        for commodity in commodity_list:
            item = AmazonspidersItem()
            item['name'] = commodity.xpath(
                "./div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a/span/text()").get()
            item['page_index'] = page_index
            item['page_link'] = response.url
            item['commodity_link'] = response.urljoin(
                commodity.xpath("./span/a/@href").get())
            results.append(item)
            # yield item
        self.Q.put('成功爬取网址：{}'.format(unquote(response.url, 'utf-8')))
        return results
        # if not next_url or int(page_index) > 10:
        #     if (next_url is None or next_url == '') and int(page_index) != 10:
        #         self.Q.put('下一页链接获取失败，程序退出')
        #     elif page_index is None or page_index == '':
        #         self.Q.put('当前页数获取失败，程序退出')
        #     return
        # else:
        #     yield scrapy.Request(response.urljoin(next_url),
        #                          callback=self.parse, dont_filter=True)

    @staticmethod
    def close(spider, reason):
        spider.Q.put('\n')
        spider.Q.put('爬取结束,请切换至结果页查看结果')
        spider.Q.put('OVER')
