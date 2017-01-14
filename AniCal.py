#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AniCal : Generate anime iCal format file for calendar app(for example:Google Calendar)
Copyright (C) 2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2016-11-08
Last Modified : 2017-01-11
'''

from Parser import MoeParser
import icalendar

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
        cal = self.cal_c(parser.animes)
        with open(filename, 'wb') as f:
            f.write(cal.to_ical())

if __name__ == '__main__':
    # proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    parser = MoeParser()
    ani = AniCal()
    ani.write('test.ics', parser)
