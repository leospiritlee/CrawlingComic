#coding:utf-8

from Gentleman import *
import platform

url = 'http://www.kofcn.org/kof/comic/'

save_path = '\comic\kof'
if platform.system() == 'Darwin':
    save_path = '/Users/leospiritlee/Documents/comic/kof'


gentleman = Gentleman(url, save_path)
gentleman.start()