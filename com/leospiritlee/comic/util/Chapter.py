#coding:utf-8

from CrawlingUtil import *

class Chapter:

    def __init__(self, comic_chapter_url, chapter_no, save_path):
        # 定义保存路径
        self.save_path = save_path

        chapter_content = CrawlingUtil.get_content(comic_chapter_url)

        if not chapter_content:
            print(chapter_no + "chapter init failed.")
            return

        # 获取每章中图片所在的页面url
        self.comic_chapter_content_pic_url_arr = self.get_comic_chapter_pic_url_arr(comic_chapter_url, chapter_content)

        # print(self.comic_chapter_content_pic_url_arr)

    # 获取每一集图片所在的URL
    def get_comic_chapter_pic_url_arr(self, comic_chapter_url, chapter_content):
        chapter_div = str(chapter_content.find_all('div', class_='post-page'))
        soup = BeautifulSoup(chapter_div, 'html.parser')

        list = soup.find_all('a').pop(0)

        for k in list:
            print(re.findall(CrawlingUtil.pattern_num, k))

        # for k in soup.find_all('a'):
        #     print(k['href'])  # 查a标签的href值
