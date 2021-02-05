#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a trader that can use robinhood or webull"""

__authors__ = ["Justin Furuness"]
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from datetime import datetime
import time
import re

import email
import imaplib
import traceback

from lib_config import Config
from lib_utils import utils
from webull import paper_webull, webull

from .actions import Actions


class Trader:
    def __init__(self, real_money=False):
        self.wb = webull() if real_money else paper_webull()
        self.webull_login()

    def webull_login(self):
        utils.write_to_stdout("Logging in to webull")
        self.wb_start_time = datetime.now()
        _email, trade_token, password = Config().webull_creds()
        self.wb.get_mfa(_email)
        print("sleeping 15 secs")
        time.sleep(15)
        mfa = self.get_webull_verification_code()
        print("got mfa", mfa)
        time.sleep(1)
        self.trade_token = trade_token
        result = self.wb.login(_email, password, "JMF", mfa)
        print("got result")
        time.sleep(1)
        for err in ["Incorrect", "Wrong format"]:
            assert err not in str(result)
        utils.write_to_stdout(result)
        utils.write_to_stdout("Logged in to webull")

    def get_webull_verification_code(self):
        # https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/
        _email, password = Config().webull_email_creds()
        SMTP_SERVER = "imap.gmail.com"

        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(str(_email), str(password))
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id, first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)')
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        if "webull" in email_from.lower():
                            return re.findall("Verification Code: .*?(\d{6})",
                                              str(msg))[0]
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')

        except Exception as e:
            traceback.print_exc()
            print(str(e))

    def trade(self, alert):
        # Alert object from lib_quant_2/lib_quant_2/alert.py
        utils.write_to_stdout(alert.text)
        utils.write_to_stdout(f"About to {alert.action.name}")
        self.wb.get_trade_token(self.trade_token)
        self.trade_actions_dict[alert.action](alert)
        utils.write_to_stdout(f"Done {alert.action.name}")

    @property
    def trade_actions_dict(self):
        return {Actions.BUY: self.buy,
                Actions.SELL: self.sell,
                Actions.SHORT: self.short,
                Actions.COVER: self.cover,
                Actions.ADD: self.add}

    def buy(self, alert):
        print(self.wb.place_order(stock=alert.ticker,
                                  action="BUY",
                                  orderType="MKT",
                                  quant=alert.shares,
                                  enforce="DAY"))
    def sell(self, alert):
        print(alert.shares)
        print(alert.ticker)
        print(self.wb.place_order(stock=alert.ticker,
                                  action="SELL",
                                  orderType="MKT",
                                  quant=alert.shares,
                                  enforce="DAY"))
    def short(self, alert):
        utils.write_to_stdout("Placeholder for short")
    def cover(self, alert):
        utils.write_to_stdout("Placeholder for cover")
    def add(self, alert):
        if "long" in alert.text:
            self.buy(alert)
        elif "short" in alert.text:
            self.short(alert)
        else:
            raise Exception(f"Unknown alert with add: {alert.text}")
