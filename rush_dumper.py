#!/bin/env python
import csv
import subprocess
import datetime

class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

EDT = FixedOffset(-240, "EDT")

def parse_date(line):
    date = datetime.datetime.strptime(line[0], "%m/%d")
    return datetime.datetime(2016, date.month, date.day)

def make_file(cur_date, line):
    time = datetime.datetime.strptime(line[0][0:7], "%I:%M%p")
    time = time.replace(tzinfo=EDT)
    event_datetime = datetime.datetime.combine(cur_date.date(), time.timetz())
    event_title = line[1]
    event_desc = line[4]
    iso_date = event_datetime.isoformat()
    if u'\u000A' in iso_date:
        print("ALERT ALERT" * 20)
        print(iso_date)
    file_string = """\
+++
date = "{iso8601_date}"
draft = true
location = ""
title="{title}"
+++

{desc}
""".format(iso8601_date=event_datetime.isoformat(),title=event_title,desc=event_desc)
    print(file_string)
    file_name = "{datetime}_{title}.md".format(datetime=event_datetime.isoformat(), title=event_title[0:4])
    print(file_name)
    output = open("content/rush/schedule_dump/"+file_name, 'w')
    output.write(file_string)

with open("Rush_Schedule.csv", newline='') as schedule_csv:
    schedule_reader = csv.reader(schedule_csv)
    current_date = None
    linect = 0
    for line in schedule_reader:
        linect += 1
        print("Line: "+str(linect))
        if current_date == None:
            current_date = parse_date(line)
            continue
        if line[0] == '':
            current_date = None
            continue
        make_file(current_date, line)
