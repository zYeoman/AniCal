#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Parser : Parser for AniCal. Return anime list.
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2017-01-11
Last Modified : 2017-01-15
'''

import re
import datetime
import dateutil.parser
import requests
from bs4 import BeautifulSoup

_SEASON = ['冬', '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋']
_SEASON_N = ['01', '01', '01', '04', '04', '04', '07', '07', '07', '10', '10', '10']


class ParserBase():
    """Spider, get html content"""

    def __init__(self, root, proxy=None):
        """Init
        :root: root url
        :proxy: proxy {'http':'127.0.0.1:1080'}
        """
        self._root = root
        self._animes = None
        self._session = requests.session()
        self._session.proxies = proxy
        self._session.headers = {'User-Agent': 'Magic Browser'}

    def geturl(self, url):
        '''通过代理、模拟Magic
        :url: url without root
        :return: BeautirulSoup response
        '''
        seq = self._session.get(self._root + url)
        seq.encoding = 'utf-8'
        return BeautifulSoup(seq.content, 'lxml')

    def getjson(self, url):
        '''返回字典
        :url: url without root
        :return: dict
        '''
        seq = self._session.get(self._root + url)
        seq.encoding = 'utf-8'
        return seq.json()

    @property
    def animes(self):
        if self._animes is None:
            self.parse()
        return self._animes

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
                jpTV = content_list[2].text
            else:
                jpTV = ''
            if len(content_list) == 4:
                zhTV = content_list[3].text
            else:
                zhTV = ''
            content_dict = {
                'title': anime.text,
                'datetime': self.parse_time(timetype),
                'jpTV': jpTV,
                'zhTV': zhTV,
                'intro': intro
            }
            self._animes.append(content_dict)

    def parse_time(self, string):
        """parse moegirl time format yyyy年mm月dd日起 每周wHH:MM
        Notice that HH may be bigger than 24
        :string: input time string.
        :returns: dict
                   start: datetime.datetime
                   end: datetime.datetime
                   g: bool whether 隔周
        """
        fmt = '%Y年%m月%d日起%z'
        try:
            (date_str, delta_str) = string.split(' ')[:2]
        except:
            return {'start': datetime.datetime.now(), 'end': datetime.datetime.now(), 'g': False}
        try:
            (hours, mins) = re.findall('[0-9]+', delta_str)[:2]
        except:
            (hours, mins) = ('0','0')
        start = datetime.datetime.strptime(date_str + '+0900', fmt)
        seconds = 60 * (60 * int(hours) + int(mins[:2]))
        delta = datetime.timedelta(seconds=seconds)
        start += delta
        return {'start': start, 'g': '隔周' in string}

class WikiParser(ParserBase):
    """Parser to parse zh.wikipedia"""

    def __init__(self, proxy=None):
        """init
        :proxy: User proxy {'http': '127.0.0.1:1080'}
        """
        self.root  = 'https://zh.wikipedia.org'
        self.url   = '/zh-cn/%E6%97%A5%E6%9C%AC%E5%8B%95%E7%95%AB%E5%88%97%E8%A1%A8_({}%E5%B9%B4)'
        # /zh-cn/日本动画列表(2016年)
        ParserBase.__init__(self, self.root, proxy)
        year = datetime.datetime.now().year
        self._page = self.geturl(self.url.format(year))
        self._dict_wiki = ['date','title_zh','title','intro','extra']

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

class BangumiParser(ParserBase):

    """Parser to parse bangumi-data/bangumi-data"""

    def __init__(self, proxy=None):
        """init
        :proxy: User proxy {'http': '127.0.0.1:1080'}
        """
        self.root  = 'https://cdn.rawgit.com'
        self.url   = '/bangumi-data/bangumi-data/master/data/items/{}/{}.json'
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
            date = {'start': start, 'g': False}
            content_dict = {
                'title': anime['titleTranslate']['zh-Hans'][0],
                'datetime': date,
                'jpTV': '',
                'zhTV': anime['sites'][0]['site'],
                'intro': anime['title']
            }
            self._animes.append(content_dict)

