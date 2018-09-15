#coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import os
import urllib.request

class CrawlingUtil:

    # 提取标题的URL
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # 提取href中的URL
    pattern_href = '<a.*?href="(.+)".*?>(.*?)</a>'

    # 提取字符串中的数字
    pattern_num =re.compile(r"\d+\.?\d*")

    # 提取src中的URL
    pattern_src = '<img.*?src="(.+)".*?>(.*?)</img>'

    #标准URL
    base_url = 'http://www.kofcn.org/kof/comic/'

    #下载URL前缀
    prefix_down_url = 'http://www.kofcn.org'

    # 读取指定URL 渲染网页内容
    def get_content(url):
        try:
            response = requests.get(url)
            htmlContent = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')
            return htmlContent
        except Exception as e:
            print('Content Rendering failed!')
            print(e)
            print('Open the webPage url:' + url + ' failed!')
            return None

    def create_dir_path(path):
        # 以漫画名创建文件夹
        exists = os.path.exists(path)
        if not exists:
            print("create folder "+ path +" success")
            os.makedirs(path)
        else:
            print("folder "+ path +" exist")

    def save(path, pic_url_arr):
        # 是否进行下载检查
        need_check_pic = False
        print('savePath is ', path)
        CrawlingUtil.create_dir_path(path)

        list = os.listdir(path)
        if len(list) >= len(pic_url_arr):
            print(" has been downloaded.")
            return

        # 获取图片时会偶尔出现请求超时的情况,会导致一部漫画存在部分缺失,此时文件夹中已存在大部分图片
        # 当前已存在图片大于一定数量时判定为存在少数缺页情况,这时候通过判断只对未存在图片进行请求
        if len(list) >= (len(pic_url_arr) / 2):
            print("每张图片下载前先检查本地是否已存在.")
            need_check_pic = True

        # print(need_check_pic)
        # print(len(list), len(pic_url_arr))

        for i in range(0, len(pic_url_arr)):
            pic_url = pic_url_arr[i]
            if pic_url == None:
                continue

            pic_path = path + "/" + str(i + 1) + ".jpg"
            if (need_check_pic):
                exists = os.path.exists(pic_path)
                if exists:
                    print("pic: " + pic_url + " exists.")
                    continue

            CrawlingUtil.save_pic(pic_url, pic_path)

        print(" fetch finished.")

    def save_pic(pic_url, path):
        # 将图片保存到指定文件夹中
        req = urllib.request.Request(pic_url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
        req.add_header('GET', pic_url)

        try:
            print("save pic url:" + pic_url)
            resp = urllib.request.urlopen(req)
            data = resp.read()
            # print data

            fp = open(path, "wb")
            fp.write(data)
            fp.close
            print("save pic finished.")
        except Exception as e:
            print(e)
            print("save pic: " + pic_url + " failed.")
