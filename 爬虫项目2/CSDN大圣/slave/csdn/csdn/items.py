# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    #课程标题，课时、讲师、适合人群、学习人数、价格、课程大纲
    collection = "Courses"

    title = scrapy.Field()
    lessons = scrapy.Field()
    teacher = scrapy.Field()
    group = scrapy.Field()
    number = scrapy.Field()
    price = scrapy.Field()
    guideline = scrapy.Field()
