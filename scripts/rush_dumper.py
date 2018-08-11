#!/bin/env python3

import csv
import subprocess
import datetime
import os

filename = "rush_events_2018.csv"

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
        return None

EDT = FixedOffset(-240, "EDT")

def make_file(line):
    time = datetime.datetime.strptime(line[1], "%Y-%m-%d %H:%M")
    time = time.replace(tzinfo=EDT)

    event_title = line[3][8:] # Strip out "(Co-ed) "
    event_desc = line[4]
    event_location = line[0]
    iso_date = time.isoformat()

    file_string = """\
+++
date = "{iso8601_date}"
draft = false
location = "{location}"
title="{title}"
+++

{desc}
""".format(iso8601_date=iso_date, title=event_title, desc=event_desc, location=event_location)

    file_name = "{title}.md".format(title="-".join(event_title.split()))
    directory = "../content/rush/" + time.strftime("%Y-%m-%d")
    if not os.path.exists(directory):
        os.makedirs(directory)
    output = open(directory +  "/" + file_name, 'w')
    output.write(file_string)

with open(filename, newline='') as schedule_csv:
    schedule_reader = csv.reader(schedule_csv)

    linect = 0 # for debugging
    for line in schedule_reader:
        linect += 1
        print("Line: "+str(linect)) # progress bar
        make_file(line)
