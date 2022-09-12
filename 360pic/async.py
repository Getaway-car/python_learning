# -*- coding = utf-8 -*-
# @Time: 2022/9/12 10:39
# @Author: Haoea

"""
异步I/O版本爬虫
"""
import asyncio
import json
import os

import aiofile
import aiohttp


async def download_picture(session, url):
    filename = url[url.rfind('/') + 1:]
    try:
        async with session.get(url, ssl=False) as resp:
            if resp.status == 200:
                data = await resp.read()
                async with aiofile.async_open(f'./images/async_beauty/{filename}', 'wb') as file:
                    await file.write(data)
    except BaseException:
        print("爬取失败")

async def fetch_json():
    async with aiohttp.ClientSession() as session:
        for page in range(11, 15):
            try:
                async with session.get(
                    url=f'https://image.so.com/zjl?ch=beauty&sn={page * 30}',
                    ssl=False
                ) as resp:
                    if resp.status == 200:
                        json_str = await resp.text()
                        result = json.loads(json_str)
                        for pic_dict in result['list']:
                            await download_picture(session, pic_dict['qhimg_url'])
            except BaseException:
                pass


def main():
    if not os.path.exists('./images/async_beauty'):
        os.makedirs('./images/async_beauty')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_json())
    loop.close()


if __name__ == '__main__':
    main()