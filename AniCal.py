#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AniCal : Generate anime iCal format file for calendar app(eg. Google Calendar)
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2016-11-08
Last Modified : 2017-01-20
'''

import datetime
import icalendar
from Parser import MoeParser


def event_c(anime):
    """create event of anime
    :anime: detail of anime in self._animes
    :returns: event of iCal
    """
    end = anime['datetime']['start'] + datetime.timedelta(seconds=30 * 60)
    event = icalendar.Event()
    event['summary'] = anime['title']
    event.add('dtstart', anime['datetime']['start'])
    event.add('dtend', end)
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

def cal_c(animes):
    """create ical of animes
    :returns: cal of iCal
    """
    cal = icalendar.Calendar()
    cal['prodid'] = '-//AniCal//ZH'
    cal['version'] = '2.0'
    for anime in animes:
        print(anime['intro'])
        if input(anime['title'] + 'y/[n]:  ') not in 'nN':
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
    write('test.ics', MoeParser())
