# -*- coding = utf-8 -*-
# @Time: 2022/9/12 9:57
# @Author: Haoea

import os
from concurrent.futures import ThreadPoolExecutor

import requests


def download_picture(url):
    NETWORK_STATUS = True  # 判断状态变量
    filename = url[url.rfind('/') + 1:]
    try:
        resp = requests.get(url=url, timeout=5)
        if resp.status_code == 200:
            with open(f'./images/multi_beauty/{filename}', 'wb') as file:
                file.write(resp.content)
    except requests.exceptions.Timeout:
        NETWORK_STATUS = False
        print("请求超时")

    return NETWORK_STATUS

def main():
    count = 0
    if not os.path.exists('./images/multi_beauty'):
        os.makedirs('./images/multi_beauty')
    with ThreadPoolExecutor(max_workers=16) as pool:
        try:
            for page in range(6, 9):
                resp = requests.get(url=f'https://image.so.com/zjl?ch=beauty&sn={page * 30}', timeout=5)
                if resp.status_code == 200:
                    pic_dict_list = resp.json()['list']
                    for pic_dict in pic_dict_list:
                        status = pool.submit(download_picture, pic_dict['qhimg_url'])
                        if status:
                            count += 1
        except requests.exceptions.Timeout:
            pass
    print(f"成功下载：{count}")

if __name__ == '__main__':
    main()
