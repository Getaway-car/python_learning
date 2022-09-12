import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        '''
        提供一组要爬取的url给引擎
        :return:
        '''
        for page in range(10):
            yield Request(
                url=f'https://movie.douban.com/top250?start={page * 25}&filter='
            )

    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            moive_item = MovieItem()
            # .extract_first()用于抽取选择器对象中的第一条数据
            moive_item['title'] = list_item.css('span.title::text').extract_first()  # 电影名
            moive_item['rank'] = list_item.css('span.rating_num::text').extract_first()  # 评分
            moive_item['subject'] = list_item.css('span.inq::text').extract_first()  # 中心思想
            yield moive_item  # 使用yield关键字（生成器），将movie_item交给引擎，再由引擎交给数据管道进行后续操作

