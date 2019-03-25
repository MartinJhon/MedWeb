# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
from urllib.parse import quote
from jd.items import ProductItem
from datetime import datetime, timedelta


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['search.jd.com']
    start_urls = 'https://search.jd.com/Search?enc=utf-8&qrst=1&rt=1&stop=1&vt=2&s=1&click=0&keyword='

    def start_requests(self):
        input_keyword = input("请输入要查询的关键字：")
        begin = datetime.now()
        if input_keyword == '':
            for keyword in self.settings.get('DEFAULT_KEYWORDS'):
                print("系统将从默认配置中读取关键字...")
                print("查询关键字 '{0}' 中...".format(keyword))
                for page in range(1, 2 * self.settings.get('MAX_PAGE') + 1, 2):
                    url = self.start_urls + quote(keyword)
                    yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
        else:
            print("查询关键字 '{0}' 中...".format(input_keyword))
            for page in range(1, 2 * self.settings.get('MAX_PAGE') + 1, 2):
                url = self.start_urls + quote(input_keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
        span = datetime.now() - begin
        print("爬取结束, 耗时(%d 秒)."%(span.total_seconds()))

    def parse(self, response):
        products = response.selector.css('li.gl-item')
        for product in products:
            item = ProductItem()
            item['price'] = product.css('div.p-price i::text').extract_first()
            item['title'] =  product.css('i.promo-words::text').extract_first()
            item['comments'] =  product.css('div.p-commit strong a::text').extract_first()          
            item['shop'] = product.css("div.p-shop a::attr('title')").extract_first()  
            item['icon'] = '、'.join(product.css("div.p-icons i::attr('data-tips')").extract())
            yield item
            #print(item)

