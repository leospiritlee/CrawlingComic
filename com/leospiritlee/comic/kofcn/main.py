#coding:utf-8
from Gentleman import *

url = 'http://www.kofcn.org/kof/comic/'

save_path = '\comic\kof'

gentleman = Gentleman(url, save_path)
gentleman.start()