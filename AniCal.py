#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider import Spider
import time

class AniCal(Spider):

    """AniCal: Dump anime info from wiki and serve iCal"""

    def __init__(self, proxy=None):
        """TODO: to be defined1. """
        self.root  = 'https://zh.wikipedia.org'
        self.url   = '/zh-cn/%E6%97%A5%E6%9C%AC%E5%8B%95%E7%95%AB%E5%88%97%E8%A1%A8_({}%E5%B9%B4)'
        self._dict = ['date','title_zh','title','company','extra']
        # /zh-cn/日本动画列表(2016年)
        Spider.__init__(self, self.root, proxy)
        thisyear = time.localtime().tm_year
        self._main_page = self.geturl(self.url.format(thisyear))

    def parse_main(self):
        """parse main page, get anime list.
        :returns: TODO

        """
        tables = self._main_page.find_all('table', class_='wikitable')
        self._animes = self.parse_table(tables[:-2])
        self._ovaoads = self.parse_table([tables[-2]])
        self._movies = self.parse_table([tables[-1]])

    def parse_table(self, tables):
        """parse tables of animes

        :tables: TODO
        :returns: TODO

        """
        contents = []
        for table in tables:
            for line in table.find_all('tr')[1:]:
                content = [x.text for x in line.find_all('td')]
                if len(content) < 4:
                    continue
                content_dict = dict(zip(self._dict, content))
                content_dict['url'] = line.find_all('td')[1].a['href']
                contents.append(content_dict)
        return contents

if __name__ == '__main__':
    proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    ani = AniCal(proxy)
    ani.parse_main()
    print(str(ani._animes))

