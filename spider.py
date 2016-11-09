#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib.request
import urllib.parse
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
        url = urllib.parse.quote(url)
        seq = urllib.request.Request(self.root+url, headers={'User-Agent': 'Magic Browser'})
        if self.proxy:
            proxy = urllib.request.ProxyHandler(self.proxy)
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
        response = urllib.request.urlopen(seq)
        res = response.read()
        self.size += sys.getsizeof(res) / 1000.0
        now = time.time()
        rate = self.size / (now - self.starttime)
        print(str(self.size/1000) + 'MB\t' + str(rate) + 'KB/s\r')
        return BeautifulSoup(res, 'lxml')

