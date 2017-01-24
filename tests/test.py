#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test thu_utils

usage:
    python -m unittest test.py
"""

import unittest
import os
import inspect

from context import Parser


class TestParser(unittest.TestCase):
    """Unittest for thu_utils"""

    def test_parser(self):
        """test Wiki"""
        for name, obj in inspect.getmembers(Parser):
            if inspect.isclass(obj):
                parser = obj()
                print(len(parser.animes))

if __name__ == "__main__":
    unittest.main()
