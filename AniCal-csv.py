#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
AniCal-Csv : Generate anime list in csv format
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2018-10-12
Last Modified : 2018-10-12
"""

import datetime
from Parser import MoeParser


def write(filename, parser):
    """Writre to filename.csv """
    with open(filename, 'w') as f:
        for anime in parser.animes:
            f.write('{}, {}, {}\n'.format(
                anime['title'], anime['site'].replace('\n', ''), anime['datetime']['start'].isoformat()))


if __name__ == '__main__':
    # proxy = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}
    write('test.csv', MoeParser())
