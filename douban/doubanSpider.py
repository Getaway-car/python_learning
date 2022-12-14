# -*- coding = utf-8 -*-
# @Time: 2022/8/28 22:48
# @Author: Haoea

"""

"""
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re   # 正则表达式，进行文字匹配
import urllib.request, urllib.error   # 指定url，获取网页数据
import xlwt  # 进行excel操作
import sqlite3   # 进行SQLite数据库操作
import os


def douban_spider():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣Top250.xls"
    dbpath = "movie.db"
    # 3.保存数据
    saveData(datalist, savepath)
    saveDate2DB(datalist, dbpath)



# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)   # re.S 让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

head = { # 模拟浏览器头部信息，向豆瓣服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
    }
saveDir = "./movie_poster/"


def getData(baseurl):
    """
    爬取网页
    :param baseurl:
    :return:
    """
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('div', class_ = "item"):  # 查找符合要求的字符串，形成列表
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle, item)
            if(len(titles) == 2):
                ctitle = titles[0]   # 中文片名
                data.append(ctitle)
                otitle = titles[1].replace("/", "").replace(u'\xa0', u'')  # 外国片名
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append('')  # 外文片名留空

            rating = re.findall(findRating, item)[0]  # 评分
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]  # 评价人数
            data.append(judgeNum)

            inq = re.findall(findInq, item)  # 概述
            if(len(inq) != 0):
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist

    return datalist

def askURL(url):
    """
    得到一个指定url的网络内容
    :param url:
    :return:
    """


    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

def saveData(datalist, dbpath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        # print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])

    book.save(dbpath)

def saveDate2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250
            (info_link, pic_link, cname, ename, score, rated, introduction, info)
            values (%s)
            '''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()


# 爬取并解析图片的路径，直接保存图片
def save1File():
    saveDir = "./movie_poster/"
    img_src = "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p988260245.jpg"
    path_list = img_src.split("/")
    objPath = saveDir + path_list[-1]

    isExists = os.path.exists(saveDir)
    if not isExists:
        os.mkdir(saveDir)

    img = urllib.request.urlopen(img_src)

    with open(objPath, "ab") as f:
        f.write(img.read())

# 读取数据库中的图片路径和电影名称
def saveFiles(dbpath):
    isExists = os.path.exists(saveDir)
    if not isExists:
        os.mkdir(saveDir)

    # 从数据库读取图片路径和电影名称
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    sql = "select pic_link, cname from movie250"
    records = cur.execute(sql)
    res = records.fetchall()
    print(res)
    cur.close()
    conn.close()


    # 逐一爬取并保存图片
    for movie in res:
        img_src = movie[0]
        objPath = saveDir + movie[1] + ".jpg"

        try:
            req = urllib.request.Request(url=img_src, headers=head)
            img = urllib.request.urlopen(req)
            with open(objPath, "ab") as f:
                f.write(img.read())
        except BaseException as e:
            print(e.args)



def init_db(dbpath):
    sql1 = "drop table if exists movie250"
    sql = '''
            create table movie250
            (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar ,
            ename varchar ,
            score numeric ,
            rated numeric ,
            introduction text,
            info text
            )
        '''  # 创建数据库
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql1)
    cursor.execute(sql)
    conn.commit()
    conn.close()




if __name__ == "__main__":
    douban_spider()
    # save1File
    saveFiles("movie.db")
    # print("爬取完毕！")

