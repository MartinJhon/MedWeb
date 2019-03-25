# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule  
from scrapy.linkextractors import LinkExtractor  
from csdn.items import MasterItem 


class CourseSpider(CrawlSpider):
    name = 'course'
    allowed_domains = ['edu.csdn.net']
    start_urls = ['https://edu.csdn.net/courses/k']
    
    #Rule是在定义抽取链接的规则
    rules = (  
        Rule(LinkExtractor(allow=('https://edu.csdn.net/courses/k/p[0-9]+',)), callback='parse_item', follow=True),  
    ) 

    def parse_item(self, response):
        lists = response.selector.css("div.course_dl_list")
        for list in lists:
            item = MasterItem()
            item['url'] = list.css("div a::attr(href)").extract_first() 
            yield item
            #print(item)
