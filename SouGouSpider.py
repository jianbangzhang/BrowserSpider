import requests, time, os
from multiprocessing.pool import Pool
from urllib.parse import urlencode


class sogoupic():
    def __init__(self, keyword, mode=1):
        # mode=1默认爬取全部，可通过更改mode的值爬取其他类型的图片
        self.keyword = keyword
        self.mode = mode  # 以便后续函数调用
        self.header = {
            'Host': 'pic.sogou.com',
            'Referer': 'https://pic.sogou.com/pics?query=%s&mode=%s' % (keyword.encode('gbk'), str(mode)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }  # 伪装请求头


    def get_json(self, url):
        # 传入参数url
        try:
            res = requests.get(url=url, headers=self.header)
            if res.status_code == 200:
                return res.json()  # 返回json格式的数据
        except requests.ConnectionError:
            return None  # 如果访问失败返回None

    def get_img(self, page):
        # 传入参数page控制爬取页数
        params = {
            'mode': self.mode,
            'start': page,
            'xml_len': 48,
            'query': self.keyword
        }
        url = 'https://pic.sogou.com/napi/pc/searchList?' + urlencode(params)
        # 拼接网址 使用urlencode()将params编码为我们在浏览器地址栏看得到的那样
        json = self.get_json(url)
        if json:
            imgurls = json['data']['items']
            # json数据就像python中的字典，同时里面嵌套了字典和列表
            # 也可使用pythonjson模块解析 可参考https://blog.csdn.net/suipingsp/article/details/39480341
            for img in imgurls:
                picurl = img['picUrl']  # 图片网址
                name = img['name']  # 图片名称.后面用作图片保存的path
                yield {'name': name,'picurl': picurl}  # 相当于返回了一个生成器，以节约内存

        else:
            return None  # 若获取json数据失败则返回none

    def down_pic(self, name, url):
        if not os.path.exists(r'D:\pyfiles\picture'):
            os.makedirs(r'D:\pyfiles\picture')  # 如果不存在,就创建文件夹
        path = r'D:\pyfiles\picture\%s' % name
        try:
            res = requests.get(url=url)
            if res.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(res.content)
                    print('下载成功！')
        except requests.ConnectionError:
            print('下载失败!')


crawler = sogoupic('裸土')  # 实例化对象，传入所需要的爬取图片的关键字


def main(page):
    imgs = crawler.get_img(page)  # 调用get_img()方法，获取图片网址和名称
    if imgs:
        for img in imgs:
            crawler.down_pic(img['name'], img['picurl'])  # 传入名称和网址
        # 调用爬取图片并保存
    else:
        print('爬取失败!')


if __name__ == '__main__':
    # page = int(input('请输入爬取页数:'))
    page=3000
    pool = Pool()  # 调用mutiprocessing 中的进程池方法进行多进程下载
    groups = range(page + 1)
    pool.map(main, groups)
    # 用map()获取结果，在map()中需要放入函数和需要迭代运算的值，然后它会自动分配给CPU核，返回结果
    pool.close()
    pool.join()

