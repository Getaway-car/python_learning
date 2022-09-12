# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 爬虫获取到的数据需要组装成Item对象
class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 电影名
    rank = scrapy.Field()  # 评分
    subject = scrapy.Field()  # 中心思想
