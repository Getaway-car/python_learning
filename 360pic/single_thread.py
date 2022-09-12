# -*- coding = utf-8 -*-
# @Time: 2022/9/12 9:52
# @Author: Haoea

import os
import requests


def download_picture(url):
    filename = url[url.rfind('/') + 1:]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f'./images/single_beauty/{filename}', 'wb') as file:
            file.write(resp.content)

def main():
    num = 0
    if not os.path.exists('./images/single_beauty'):
        os.makedirs('./images/single_beauty')
    for page in range(3):
        resp = requests.get(url=f'https://image.so.com/zjl?ch=beauty&sn={page * 30}', timeout=(3, 7))
        if resp.status_code == 200:
            pic_dict_list = resp.json()['list']
            for pic_dict in pic_dict_list:
                download_picture(pic_dict['qhimg_url'])

    print("成功下载" + num)

if __name__ == '__main__':
    main()