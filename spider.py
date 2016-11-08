#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib.request as urllib
import time
import sys
from bs4 import BeautifulSoup

'''
spider with proxy
'''

class Spider():

    """Spider, get articles from sis"""

    def __init__(self, root, proxy=None):
        self.root = root
        self.proxy = proxy
        self.size = 0
        self.starttime = time.time()

    def geturl(self, url):
        '''通过代理、模拟Magic'''
        seq = urllib.Request(self.root+url, headers={'User-Agent': 'Magic Browser'})
        if self.proxy:
            proxy = urllib.ProxyHandler(self.proxy)
            opener = urllib.build_opener(proxy)
            urllib.install_opener(opener)
        response = urllib.urlopen(seq)
        res = response.read()
        self.size += sys.getsizeof(res) / 1000.0
        now = time.time()
        rate = self.size / (now - self.starttime)
        print(str(self.size/1000) + 'MB\t' + str(rate) + 'KB/s\r')
        return BeautifulSoup(res, 'lxml')

