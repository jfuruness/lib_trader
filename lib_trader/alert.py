#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This contains alert format"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from datetime import datetime
import re

from .actions import Actions

class Alert:

    __slots__ = ["el", "year", "valid", "text", "time_str", "action_str",
                 "other_text", "datetime", "action", "ticker", "shares",
                 "price"]

    fake_tickers = set(["IRA", "BTC", "ETH", "SPAC", "BOOO",
                        "OOOO", "OOOM", "BOOOM", "BOOM"])

    default_shares = 1

    def __init__(self, element, year=datetime.now().year):
        self.el = element
        self.year = year
        self.valid = True
        # Gets text
        self._get_text()
        # Gets time string, action, other text
        self._parse_text()
        # Gets ticker, type of action, and price
        self._parse_action()
        # Gets time
        self.datetime = self._parse_time(year)

    def _get_text(self):
        self.text = ""
        self.valid = False

    def _parse_text(self):
        self.time_str = str(datetime.now())
        self.action_str = ""
        self.other_text = ""
        self.valid = False

    def _parse_action(self):
        self.action = ""
        self.ticker = ""
        self.shares = 0
        self.price = 0
        self.valid = False

    @property
    def action_word(self):
        return self.action_str

    def _get_action(self):
        self.action = None
        self._check_for_action(Actions.BUY, ["buying", "bought"])
        self._check_for_action(Actions.SELL, ["selling", "sold"])
        self._check_for_action(Actions.SHORT, ["shorting", "shorted"])
        self._check_for_action(Actions.COVER, ["covering", "covered"])
        self._check_for_action(Actions.ADD, ["added", "adding"])
        if self.action is None:
            self.valid = False
        return self.action

    def _check_for_action(self, action_type, action_words):
        for word in action_words:
            if word.lower() in self.action_word.lower():
                if self.action is not None:
                    self.valid = False
                self.action = action_type

    def _parse_time(self, year):
        return datetime.now()

    def __eq__(self, other):
        if isinstance(other, Alert):
            return self.text == other.text
        else:
            return False

    @property
    def position_size(self):
        return self.price * self.shares

    def __str__(self):
        string = "VALID\n" if self.valid else "INVALID\n"
        return string + (f"Time:   {self.datetime}\n"
                         f"Action: {self.action}\n"
                         f"Shares: {self.shares}\n"
                         f"Ticker: {self.ticker}\n"
                         f"Price:  {self.price}\n"
                         f"Text:   {self.text[:50]}\n")

    def hash(self):
        return str([x for x in self.__str__().split("\n") if "Time" not in x])

    def ticker_search(self, text):
        return [x for x in re.findall("[A-Z]{3,4}", text)
                if x not in self.fake_tickers]
