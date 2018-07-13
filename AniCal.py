#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AniCal : Generate anime iCal format file for calendar app(eg. Google Calendar)
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2016-11-08
Last Modified : 2017-01-23
"""

import datetime
import icalendar
from Parser import BangumiParser


def event_c(anime):
    """create event of anime
    :anime: detail of anime in self._animes
    :returns: event of iCal
    """
    start = anime['datetime']['start']
    end = start + datetime.timedelta(seconds=30 * 60)
    event = icalendar.Event()
    event['summary'] = anime['title']
    event.add('dtstart', start)
    event.add('dtend', end)
    event['description'] = anime['intro']
    event['location'] = anime['site']
    interval = anime['datetime']['interval']
    event.add('rrule',
              {'FREQ': 'WEEKLY',
               'INTERVAL': interval,
               'COUNT': 12})
    return event


def cal_c(animes):
    """create ical of animes
    :returns: cal of iCal
    """
    cal = icalendar.Calendar()
    cal['prodid'] = '-//AniCal//ZH'
    cal['version'] = '2.0'
    for anime in animes:
        print(anime['intro'])
        if input(anime['title'] + ' Y/[n]:  ') in 'yY':
            cal.add_component(event_c(anime))
    return cal


def write(filename, parser):
    """write to filename.ics
    :filename: filename
    """
    cal = cal_c(parser.animes)
    with open(filename, 'wb') as output:
        output.write(cal.to_ical())


if __name__ == '__main__':
    # proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    write('test.ics', BangumiParser())
