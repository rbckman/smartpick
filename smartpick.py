#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Smartpi Consumption Kalkulator | smartpick.py
by rbckman
'''
import os
import time
import requests
import code
import re
from datetime import datetime
from datetime import timedelta
import argparse
from calendar import monthrange

parser = argparse.ArgumentParser(description='Get power consumption of today or a specific date using smartpi API.')
parser.add_argument('url', metavar='url', type=str,
                            help='ip address or hostname to smartpi server')
parser.add_argument('-y', '--year', metavar='y', type=int,
                            help='the year in which the month you wish to calculate ex. 2018')
parser.add_argument('-m', '--month', metavar='m', type=int,
                            help='month')
parser.add_argument('-d', '--day', metavar='d', type=int,
                            help='day')
args = parser.parse_args()

if args.year == None and args.month == None and args.day == None:
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
elif args.month == None and args.day == None:
    year = args.year
    month = datetime.now().month
    day = 0
elif args.day == None:
    year = args.year
    month = args.month
    day = 0
else:
    print('no input, getting todays consumption')
    year = args.year
    month = args.month
    day = args.day

totkwh = 0
i = 0
days = 1

if day == 0:
    days = monthrange(args.year, args.month)[1]
    day = 1

print("days to calculate: " + str(days))

while i < days:
    gettime = (datetime.strptime(str(year) + "-" + str(month).zfill(2) + '-' + str(day).zfill(2), "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
    print("calculating day: " +  gettime)
    readsmartpi = requests.get(url=args.url + ":1080/api/chart/123/energy_pos/from/" + gettime + "T00:00:00.000Z/to/" + gettime + "T23:59:00.000Z").json()
    #print(readsmartpi)
    #code.interact(local=locals())
    try:
        for p in readsmartpi:
            for a in p['values']:
                totkwh += int(a['value'])
    except:
        pass
    i += 1

print("Total kwh: " + str(totkwh/1000))
