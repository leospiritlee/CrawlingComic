#coding:utf-8

from CrawlingUtil import *

class Chapter:

    def __init__(self, comic_chapter_url, chapter_no, save_path, comic_title):
        # 定义保存路径
        self.save_path = save_path + '/' + comic_title + '/' + str(chapter_no + 1)
        print(self.save_path)

        chapter_content = CrawlingUtil.get_content(comic_chapter_url)

        if not chapter_content:
            print(chapter_no + "chapter init failed.")
            return

        # 漫画名称
        self.comic_title = comic_title

        # 漫画第 集
        self.chapter_no = chapter_no

        # 漫画章节编号
        self.comic_no = str(comic_chapter_url).split('/')[6]

        # 定义访问地址前缀
        self.self_downLoadBase_url = CrawlingUtil.base_url  + comic_title + '/' +self.comic_no + "/"

        # 获取每章中图片所在的页面url
        self.comic_chapter_content_pic_url_arr = self.get_comic_chapter_pic_url_arr(comic_chapter_url, chapter_content)

        # 生成每张图片的数组
        self.pic_url_arr = self.get_pic_url_arr()

    # 获取每一集图片所在的URL
    def get_comic_chapter_pic_url_arr(self, comic_chapter_url, chapter_content):
        chapter_div = str(chapter_content.find_all('div', class_='post-page'))
        soup = BeautifulSoup(chapter_div, 'html.parser')

        list = soup.find_all('a')

        list.pop()

        page_url = []

        for k in list:
            result = re.findall(CrawlingUtil.pattern_href, str(k))
            if len(result) == 0:
                continue

            url = result[0][0]
            if url =='#':
                url = comic_chapter_url
            else:
                url = self.self_downLoadBase_url+url
            page_url.append(url)

        return page_url


    def get_pic_url_arr(self):

        print('has ' + str(len(self.comic_chapter_content_pic_url_arr)) + ' pic')

        pic_url_arr = []

        for i in range(0, len(self.comic_chapter_content_pic_url_arr)):
            url = self.comic_chapter_content_pic_url_arr[i]
            page_content = CrawlingUtil.get_content(url)
            pic_url = self.get_pic_url(page_content)
            pic_url_arr.append(pic_url)

        return pic_url_arr

    def get_pic_url(self, page_content):
        page_div = str(page_content.find_all('div',class_='picbox'))

        pic_url = re.findall(CrawlingUtil.pattern_src, page_div)[0][0]
        return  CrawlingUtil.prefix_down_url + '' + pic_url

    def start(self):
        print('start down pic')
        CrawlingUtil.save(self.save_path, self.pic_url_arr)