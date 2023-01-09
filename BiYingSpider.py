# -*- coding：utf-8 -*-
# author:https://github.com/taojianglong/python-crawler
import requests
import json
import os
from lxml import etree
import re
import random
import socket
# 设置请求超时时间，防止长时间停留在同一个请求
socket.setdefaulttimeout(10)

def biying_pic_url(num, keyword):
    pic_url= []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    for i in range((num // 35) + 1):
        page_url = 'https://cn.bing.com/images/async?q={}&first={}&count=35&relo=4&relp=5&cw=1117&ch=689&scenario=ImageBasicHover&datsrc=N_I&layout=ColumnBased&mmasync=1&dgState=c*6_y*1582s1599s1589s1660s1720s1704_i*40_w*172&IG=B3C2B933EAED48A4A82330EC1E7A638B&SFX=2&iid=images.5659'.format(keyword, i*35)
        print(page_url)
        html = requests.get(page_url, headers=headers).text
        html = etree.HTML(html)
        conda_list = html.xpath('//a[@class="iusc"]/@m')
        for j in conda_list:
            img_url = re.search('"murl":"(.*?)"', j).group(1)
            pic_url.append(img_url)
    print(len(pic_url))
    return pic_url

def down_img(num, keyword):
    pic_url  = biying_pic_url(num, keyword)

    if os.path.exists('./data1/'+keyword):
        pass
    else:
        os.makedirs('./data1/'+keyword)

    path = './data1/'
    for index,i in enumerate(pic_url):
        try:
            filename = path + keyword + '/' + str(index) + '.jpg'
            print(filename)
            with open(filename, 'wb+') as f:
                f.write(requests.get(i).content)
        except:
            continue
if __name__ == '__main__':
    keyword = '裸土'
    num = int(input('请输入爬取图片数目：'))
    down_img(num, keyword)