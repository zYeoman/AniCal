#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AniCal : Generate anime iCal format file for calendar app(for example:Google Calendar)
Copyright (C) 2016 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2016-11-08
Last Modified : 2017-01-09
'''
import re
import datetime
import icalendar
import requests
from bs4 import BeautifulSoup

_SEASON = ['冬', '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋']


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
        self._dict_wiki = ['date', 'title_zh', 'title', 'company', 'extra']
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
        dur = 10 if '泡面番' in string else 30
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
        end = start + datetime.timedelta(seconds=dur * 60)
        return {'start': start, 'end': end, 'g': '隔周' in string}

class AniCal():
    """AniCal: Dump anime info from wiki and serve iCal"""

    def __init__(self):
        """init AniCal
        """
        pass

    def event_c(self, anime):
        """create event of anime
        :anime: detail of anime in self._animes
        :returns: event of iCal
        """
        event = icalendar.Event()
        event['summary'] = anime['title']
        event.add('dtstart', anime['datetime']['start'])
        event.add('dtend', anime['datetime']['end'])
        event['description'] = anime['intro']
        event['location'] = anime['zhTV']
        # TODO Make it configurable
        interval = 1
        if anime['datetime']['g']:
            interval = 2
        event.add('rrule',
                  {'FREQ': 'WEEKLY',
                   'INTERVAL': interval,
                   'COUNT': 12})
        return event

    def cal_c(self, animes):
        """create ical of animes
        :returns: cal of iCal
        """
        cal = icalendar.Calendar()
        cal['prodid'] = '-//AniCal//ZH'
        cal['version'] = '2.0'
        for anime in animes:
            print(anime['intro'])
            if input(anime['title'] + 'y/[n]:  ') not in 'nN':
                cal.add_component(self.event_c(anime))
        return cal

    def write(self, filename, parser):
        """write to filename.ics
        :filename: filename
        """
        cal = ani.cal_c(parser.animes)
        with open(filename, 'wb') as f:
            f.write(cal.to_ical())

if __name__ == '__main__':
    # proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    parser = MoeParser()
    ani = AniCal()
    ani.write('test.ics', parser)
