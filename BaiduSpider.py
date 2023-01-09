# author:jianbang666
import requests
import re
import os

class Spider(object):
    def __init__(self,pn,word,queryWord):
        self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                     'Connection': 'keep-alive',
                      "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsNiw0LDUsNyw4LDIsOQ%3D%3D&word=%E8%A3%B8%E5%9C%9F%E5%9B%BE%E7%89%87"
                     }
        self.pn=pn
        self.word=word
        self.queryWord=queryWord
        self.base_url="https://image.baidu.com/search/acjson?"
        self.paras={
            "tn":"resultjson_com",
            "logid":"8969753192566552047",
            "ipn":"rj",
            "ct":"201326592",
            "is":"",
            "fp":"result",
            "fr":"",
            "word":self.word,
            "queryWord":self.queryWord,
            "cl":"2",
            "lm":"-1",
            "ie":"utf-8",
            "oe":"utf-8",
            "adpicid":"",
            "st":"",
            "z":"",
            "ic":"",
            "hd":"",
            "latest":"",
            "copyright":"",
            "s":"",
            "se":"",
            "tab":"",
            "width":"",
            "height":"",
            "face":"",
            "istype":"",
            "qc":"",
            "nc":"1",
            "expermode":"",
            "nojc":"",
            "isAsync":"",
            "pn":self.pn,
            "rn":"30",
            "gsm":"1e"
        }

        self.url=self.getResponse()


    def getResponse(self):
        response = requests.get(self.base_url, headers=self.headers,params=self.paras)
        response.encoding = 'utf-8'
        return response.text,response.status_code

    def matchUrl(self,string):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        url = re.findall(pattern, string)
        return list(set(url))

    def saveUrl(sel,name,url_li,outpath):
        with open(os.path.join(outpath,"img_url.txt"),encoding="utf-8",mode="a+") as f:
            for i,url in enumerate(url_li):
                f.write(name+"_"+str(i)+"\t"+url+"\n")



class GetImg(object):
    def __init__(self,filePath):
        self.img_file=filePath
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }

    def Url2Img(self):
        with open(self.img_file,"r") as freader:
            li=freader.readlines()
            for data in li:
                print(data)
                fileName,url=data.split()
                r = requests.get(url, headers=self.headers)
                f = open("./data/"+str(fileName)+".jpg",'wb')
                f.write(r.content)
                f.close()















if __name__=="__main__":
    # pn=1
    # spider = Spider(pn=pn)
    # content,status=spider.getResponse()
    # print(content)
    # # print(type(content))
    # url_list=spider.matchUrl(content)
    # print(len(url_list))
    # print(url_list)
    # spider.saveUrl(url_list,"./")

    query_list=["裸露土地照片","裸土照片","建筑工地裸土照片","城市裸土照片","白天裸土照片","晚上裸土照片","农村裸土照片","城郊裸土照片","冬天裸土照片","春天裸土照片","夏天裸土照片","秋天裸土照片","红色裸土照片","褐色裸土照片","黄色裸土照片","高清裸土照片","模糊裸土照片","摄像头裸土照片","手机拍照裸土照片"]
    pn = 1
    page = 20
    for key,query in enumerate(query_list):
        print(query)
        for i in range(1,page+1):
            word=query
            spider = Spider(pn=pn,word=word,queryWord=query)
            content,_=spider.getResponse()
            print(content)
            url_list=spider.matchUrl(content)
            if len(url_list)==0:
                break
            print(url_list)
            name=str(key)+"_"+str(pn)+"_"+str(i)
            spider.saveUrl(name,url_list,"./")
            pn+=29

    getimg=GetImg("./img_url.txt")
    getimg.Url2Img()






