# -*- coding: utf-8 -*-
import httplib
import urllib
import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL="traffic.smstitan.ru"
PATH="/API:0.9/"
APIKey="c95537060ed22142bbd810635309e6547eb12fd5"
Command="SendOne"
company="RENET"
sms_autocopmplit = ['fio']


def agregator(sms, phone):
    accept='text/plain'
    data = {'Number': phone,
            'Sender': 'RENET',
            'Command': Command,
            'Content': sms,
            'Concatenated': 1,
            'APIKey': APIKey
            }
    http_conn = httplib.HTTPSConnection(URL)
    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": accept}
    http_conn.request('POST', PATH, urllib.urlencode(data), headers)
    resp = http_conn.getresponse().read()
    http_conn.close()
    return str(resp)

if __name__ == '__main__':
    text = 'test'
    phone = '9030457526'
    ret = agregator(text, phone)
    print ret
