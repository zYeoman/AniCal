#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
WikiParser ：Parser for AniCal. Return anime list.
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2017-01-22
Last Modified : 2017-01-22
'''

import re
import datetime

from .ParserBase import ParserBase

_SEASON = [
    '冬', '冬', '冬',
    '春', '春', '春',
    '夏', '夏', '夏',
    '秋', '秋', '秋'
]


class MoeParser(ParserBase):
    """Parser to parse moegirl"""

    def __init__(self, proxy=None):
        """init
        :proxy: User proxy {'http': '127.0.0.1:1080'}
        """
        # /zh-cn/日本动画列表(2016年)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        self.root = 'https://zh.moegirl.org'
        self.url = '/zh/日本{}年{}季动画'.format(year, _SEASON[month])
        ParserBase.__init__(self, self.root, proxy)
        self._page = self.geturl(self.url)

    def parse(self):
        """parse moegirl page. Generate self._animes
        :returns: None
        """
        # 前两个是目录和导航, 后两个是参见和导航菜单
        animes = self._page('h2')[2:-2]
        self._animes = []
        for anime in animes:
            content_list = anime.find_next('dl')('dd')
            content_intro = anime.find_next('h3')
            timetype = content_list[1].text
            if content_intro.text == '简介':
                intro = content_intro.next_sibling.next_sibling.text.strip(
                    '\n')
            else:
                intro = ''
            if len(content_list) == 3:
                site_jp = content_list[2].text
            else:
                site_jp = ''
            if len(content_list) == 4:
                site_zh = content_list[3].text
            else:
                site_zh = ''
            content_dict = {
                'title': anime.text,
                'datetime': parse_time(timetype),
                'site': '\n'.join([site_jp, site_zh]),
                'intro': intro
            }
            self._animes.append(content_dict)

def parse_time(string):
    """parse moegirl time format yyyy年mm月dd日起 每周wHH:MM
    Notice that HH may be bigger than 24
    :string: input time string.
    :returns: dict
               start: datetime.datetime
               interval: int
    """
    fmt = '%Y年%m月%d日起%z'
    try:
        (date_str, delta_str) = string.split(' ')[:2]
    except:
        return {'start': datetime.datetime.now(), 'interval': 1}
    try:
        (hours, mins) = re.findall('[0-9]+', delta_str)[:2]
    except:
        (hours, mins) = ('0', '0')
    start = datetime.datetime.strptime(date_str + '+0900', fmt)
    seconds = 60 * (60 * int(hours) + int(mins[:2]))
    delta = datetime.timedelta(seconds=seconds)
    start += delta
    interval = 2 if '隔周' in string else 1
    return {'start': start, 'interval': interval}
