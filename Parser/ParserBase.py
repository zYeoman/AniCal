#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Parser : Parser for AniCal. Return anime list.
Copyright (C) 2016-2017 Yongwen Zhuang

Author        : Yongwen Zhuang
Created       : 2017-01-11
Last Modified : 2017-01-20
'''

import requests
from bs4 import BeautifulSoup


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

    def parse(self):
        '''virtual method parse
        '''
        raise NotImplementedError

    @property
    def animes(self):
        """property anime list
        :return: anime list.
        """
        if self._animes is None:
            self.parse()
        return self._animes
