#coding:utf-8
from Cartoon import *

class Gentleman:

    def __init__(self, url, path):
        exists = os.path.exists(path)
        if not exists:
            print('file path is not valid')
            exit(0)

        self.base_url = url
        self.path = path
        content = CrawlingUtil.get_content(url)
        self.page_url_arr = self.get_page_url_arr(content)


    #读取指定URL 渲染网页内容
    # def get_content(self, url):
    #     try:
    #         response = requests.get(url)
    #         htmlContent = BeautifulSoup(response.content.decode('gbk','ignore'), 'html.parser')
    #         return htmlContent
    #     except Exception as e:
    #         print('Content Rendering failed!')
    #         print(e)
    #         print('Open the webPage url:' + url + ' failed!')
    #         return None


    #获取每一部的URL访问地址
    def get_page_url_arr(self, content):
        target_b = str(content.find_all('b'))
        urls = re.findall(CrawlingUtil.pattern, target_b)
        return urls


    def start(self):
        # 遍历每一页的内容
        print(self.page_url_arr)
        for i in range(0, len(self.page_url_arr)):
            # 获取每一页漫画的url
            name = str(self.page_url_arr[i]).split('/')[5]
            comic_url = str(self.page_url_arr[i])
            print("page " + str(i + 1) + ":" + name)
            path = self.path + '/' + name
            CrawlingUtil.create_dir_path(path)

            cartoon = Cartoon(comic_url, name, self.path)
            cartoon.start()

            print("======= page " + str(i + 1) + " fetch finished =======")