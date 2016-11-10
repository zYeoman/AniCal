#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider import Spider
import datetime
import icalendar

_SEASON = ['冬','冬','冬','春','春','春','夏','夏','夏','秋','秋','秋']

def parse_moe_time(string):
    """parse moegirl time format yyyy年mm月dd日起 每周wHH:MM
    Notice that HH may be bigger than 24

    :string: TODO
    :returns: TODO

    """
    fmt = '%Y年%m月%d日起%z'
    dur = 10 if '泡面番' in string else 30
    (date_str, delta_str) = string.split(' ')[:2]
    delta_str = delta_str[3:]
    (hours, mins) = delta_str.split(':')[:2]
    start = datetime.datetime.strptime(date_str+'+0900', fmt)
    seconds = 60*(60*int(hours)+int(mins[:2]))
    delta = datetime.timedelta(seconds=seconds)
    start += delta
    end = start+datetime.timedelta(seconds=dur*60)
    return {'start':start, 'end':end}

class AniCal(Spider):

    """AniCal: Dump anime info from wiki and serve iCal"""

    def __init__(self, proxy=None):
        """TODO: to be defined1. """
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        self._dict_wiki = ['date','title_zh','title','company','extra']
        # /zh-cn/日本动画列表(2016年)
        self.root_moe  = 'https://zh.moegirl.org'
        self.url_moe   = '/zh/日本{}年{}季动画'.format(year,
                                                       _SEASON[month])
        Spider.__init__(self, self.root_moe, proxy)
        self._moe_page = self.geturl(self.url_moe)

    def parse_moe(self):
        """parse moegirl page
        :returns: TODO

        """
        # 前两个是目录和导航, 后两个是参见和导航菜单
        animes = self._moe_page('h2')[2:-2]
        self._animes = []
        for anime in animes:
            content_list = anime.find_next('dl')('dd')
            content_intro = anime.find_next('h3')
            timetype = content_list[1].text
            if content_intro.text == '简介':
                intro = content_intro.next_sibling.next_sibling.text.strip('\n')
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
            content_dict = {'title': anime.text,
                            'datetime': parse_moe_time(timetype),
                            'jpTV': jpTV,
                            'zhTV': zhTV,
                            'intro': intro
                           }
            self._animes.append(content_dict)
    def event_c(self, anime):
        """create event of anime

        :anime: TODO
        :returns: TODO

        """
        event = icalendar.Event()
        event['summary'] = anime['title']
        event.add('dtstart', anime['datetime']['start'])
        event.add('dtend', anime['datetime']['end'])
        event['description'] = anime['intro']
        event['location'] = anime['zhTV']
        # TODO Make it configurable
        event.add('rrule', {'FREQ':'WEEKLY', 'INTERVAL':1, 'COUNT':12})
        return event

    def cal_c(self, animes):
        """create ical of animes

        :animes: TODO
        :returns: TODO

        """
        cal = icalendar.Calendar()
        cal['prodid'] = '-//AniCal//ZH'
        cal['version'] = '2.0'
        for anime in animes:
            print(anime['intro'])
            if input(anime['title']+'y/[n]:  ') not in 'nN':
                cal.add_component(self.event_c(anime))
        return cal

    def parse_wiki(self):
        """parse wiki page, get anime list.
        :returns: TODO

        """
        tables = self._wiki_page.find_all('table', class_='wikitable')
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
                content_dict = dict(zip(self._dict_wiki, content))
                content_dict['url'] = line.find_all('td')[1].a['href']
                contents.append(content_dict)
        return contents

if __name__ == '__main__':
    # proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    ani = AniCal()
    ani.parse_moe()
    cal = ani.cal_c(ani._animes)
    with open('test.ics', 'wb') as f:
        f.write(cal.to_ical())
