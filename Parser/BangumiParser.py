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
import dateutil.parser

from .ParserBase import ParserBase

_SEASON_N = [
    '01', '01', '01',
    '04', '04', '04',
    '07', '07', '07',
    '10', '10', '10'
]


class BangumiParser(ParserBase):
    """Parser to parse bangumi-data/bangumi-data"""

    def __init__(self, proxy=None):
        """init
        :proxy: User proxy {'http': '127.0.0.1:1080'}
        """
        self.root = 'https://cdn.rawgit.com'
        self.url = '/bangumi-data/bangumi-data/master/data/items/{}/{}.json'
        ParserBase.__init__(self, self.root, proxy)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        self._page = self.getjson(self.url.format(year, _SEASON_N[month]))

    def parse(self):
        """parse bangumi-data, generate anime list.
        :return: None
        """
        self._animes = []
        for anime in self._page:
            if anime['begin'] == '':
                continue
            start = dateutil.parser.parse(anime['begin'])
            date = {'start': start, 'interval': 1}
            anime_title = anime['titleTranslate'].get(
                'zh-Hans', [anime['title']])
            try:
                zhtv = anime['sites'][0]['site']
            except IndexError:
                zhtv = ''
            content_dict = {
                'title': anime_title[0],
                'datetime': date,
                'site': zhtv,
                'intro': anime['title']
            }
            self._animes.append(content_dict)
