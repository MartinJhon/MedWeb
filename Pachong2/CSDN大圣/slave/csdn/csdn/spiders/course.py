# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from csdn.items import CourseItem


class CourseSpider(RedisSpider):
    name = 'course'
    redis_key = "coursespider:start_urls"

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(CourseSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):
        #print(response.status)
            item = CourseItem()
            item['title'] = response.css("h1::text").extract_first().strip()
            item['lessons'] = response.css("span.pinfo::text").extract_first().split('/')[1]
            item['teacher'] = response.css("div.professor_name a::text").extract_first()
            item['group'] = response.css("span.for::text").extract_first()
            item['number'] = response.css("span.num::text").extract_first()
            item['price'] = response.css("span.money::text").extract_first().strip()
            lists = response.css("div.outL_box dl")
            item['guideline'] = ''
            for list in lists:
                item['guideline'] += list.css("dt.clearfix span::text").extract_first().strip() + "   "
                item['guideline'] += " ".join(list.css("span.ellipsis::text").extract()).strip()+ "   "
            item['guideline'] = item['guideline'].strip()
            #print(item)
            yield item
        #pass
