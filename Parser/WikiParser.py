#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WikiParser ：Parser for AniCal. Return anime list.
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2017-01-22
Last Modified : 2017-01-23
"""

import datetime

from .ParserBase import ParserBase


class WikiParser(ParserBase):
    """Parser to parse zh.wikipedia"""
    def __init__(self, proxy=None):
        """init
        :proxy: User proxy {'http': '127.0.0.1:1080'}
        """
        self.root = 'https://zh.wikipedia.org'
        self.url = '/zh-cn/日本動畫列表_({}年)'
        # /zh-cn/日本动画列表(2016年)
        ParserBase.__init__(self, self.root, proxy)
        year = datetime.datetime.now().year
        self._page = self.geturl(self.url.format(year))
        print(self._page)
        self._dict_wiki = ['date', 'title_zh', 'title', 'intro', 'extra']
        self._ovaoads = None
        self._movies = None

    def parse(self):
        """parse wiki page, generate anime list.
        :returns: None
        """
        tables = self._page.find_all('table', class_='wikitable')
        self._animes = self.parse_table(tables[:-2])
        self._ovaoads = self.parse_table([tables[-2]])
        self._movies = self.parse_table([tables[-1]])

    def parse_table(self, tables):
        """parse tables of animes
        :tables: tables from wiki page
        :returns: contents of tables
        """
        contents = []
        for table in tables:
            for line in table.find_all('tr')[1:]:
                content = [x.text for x in line.find_all('td')]
                if len(content) < 4:
                    continue
                content_dict = dict(zip(self._dict_wiki, content))
                content_dict['url'] = line.find_all('td')[1].a['href']
                contents.append(content_dict)
        return contents
