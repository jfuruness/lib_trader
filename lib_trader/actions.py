#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This contains alert format"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


from enum import Enum


class Actions(Enum):
    BUY = "buy"
    SELL = "sell"
    SHORT = "short"
    COVER = "cover"
    ADD = "add"
