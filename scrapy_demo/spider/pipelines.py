# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import openpyxl
import pymysql


class DbPipeline:
    # 批处理
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database="spider",
            charset="utf8"
        )
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write2db()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get("title", "")
        rank = item.get("rank", 0)
        subject = item.get("subject", "")
        self.data.append((title, rank, subject))
        if len(self.data) == 100:
            self._write2db()
            self.data.clear()

        return item

    def _write2db(self):
        self.cursor.executemany(
            'insert into db_top_movie (title, rating, subject) values (%s, %s, %s)',
            self.data
        )
        self.conn.commit()


# class DbPipeline:
#     # 每爬取到一条数据写入一次
#     def __init__(self):
#         self.conn = pymysql.connect(
#             host="localhost",
#             port=3306,
#             user="root",
#             password="1234",
#             database="spider",
#             charset="utf8"
#         )
#         self.cursor = self.conn.cursor()
#
#     def close_spider(self, spider):
#         self.conn.commit()
#         self.conn.close()
#
#     def process_item(self, item, spider):
#         title = item.get("title", "")
#         rank = item.get("rank", 0)
#         subject = item.get("subject", "")
#         self.cursor.execute(
#             'insert into db_top_movie (title, rating, subject) values (%s, %s, %s)',
#             (title, rank, subject)
#         )
#         return item


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()  # 创建工作簿
        self.ws = self.wb.active  # 拿到默认工作表
        # sheet = wb.create_sheet()  # 创建新的工作表
        self.ws.title = "Top250"
        self.ws.append(("标题", "评分", "主题"))

    def close_spider(self, spider):
        self.wb.save("豆瓣电影Top250.xlsx")

    def process_item(self, item, spider):
        title = item.get("title", "")
        rank = item.get("rank", "")
        subject = item.get("subject", "")
        self.ws.append((title, rank, subject))
        return item
