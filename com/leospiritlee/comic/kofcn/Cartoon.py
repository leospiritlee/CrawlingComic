#coding:utf-8

from CrawlingUtil import *
from Chapter import *

class Cartoon:

    def __init__(self, comic_url, comic_title, save_path):
        comic_content = CrawlingUtil.get_content(comic_url)
        if not comic_content:
            print(comic_title + "Cartoon init failed.")
            return

        #漫画保存父目录
        self.save_path = save_path

        # 漫画标题
        self.comic_title = comic_title

        # 分集URL
        self.comic_chapter_url_arr = self.get_comic_chapter_url_arr(comic_content)
        if not self.comic_chapter_url_arr:
            print(comic_title + "Cartoon init failed.")
            return

        # 获取总集数
        self.comic_chapter_url_total = len(self.comic_chapter_url_arr)

        # 标记每次下载图片时,是否先检查本地已存在对应图片
        self.need_check_pic = False


    # 获取每部漫画的分集的URL
    def get_comic_chapter_url_arr(self, comic_content):
        chapter_li = str(comic_content.find_all('li', class_='col-md-3'))
        urls = re.findall(CrawlingUtil.pattern, chapter_li)
        return urls;




    def save(self, path, chapter_title):
        dir_path = path + "/" + chapter_title
        self.create_dir_path(dir_path)

        # 判断是否已经下载过
        list = os.listdir(dir_path)
        if len(list) >= len(self.page_url_arr):
            print(self.title + " has been downloaded.")
            return

        # 获取图片时会偶尔出现请求超时的情况,会导致一部漫画存在部分缺失,此时文件夹中已存在大部分图片
        # 当前已存在图片大于一定数量时判定为存在少数缺页情况,这时候通过判断只对未存在图片进行请求
        if len(list) >= (len(self.page_url_arr) / 2):
            print("每张图片下载前先检查本地是否已存在.")
            self.need_check_pic = True

        for i in range(0, len(self.page_url_arr)):
            page_url = self.page_url_arr[i]
            pic_url = self.get_pic_url(page_url)
            if pic_url == None:
                continue

            pic_path = dir_path + "/" + str(i + 1) + ".jpg"
            if (self.need_check_pic):
                exists = os.path.exists(pic_path)
                if exists:
                    print("pic: " + pic_url + " exists.")
                    continue

            self.save_pic(pic_url, pic_path)

        print(self.title + " fetch finished.")


    def start(self):
        print(self.comic_title + ' has comic no. :' + str(self.comic_chapter_url_total))

        for i in range(0, len(self.comic_chapter_url_arr)):
            comic_chapter_url = self.comic_chapter_url_arr[i]

            print(self.comic_title + ' visit webPage :' + comic_chapter_url)

            chapter = Chapter(comic_chapter_url,i ,self.save_path, self.comic_title)
            chapter.start()
