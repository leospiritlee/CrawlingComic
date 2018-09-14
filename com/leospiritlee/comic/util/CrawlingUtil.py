#coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import os

class CrawlingUtil:

    # 提取标题的URL
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # 提取href中的URL
    pattern_href = '<a.*?href="(.+)".*?>(.*?)</a>'

    # 提取字符串中的数字
    pattern_num =re.compile(r"\d+\.?\d*")

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
