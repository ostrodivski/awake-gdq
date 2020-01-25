#!\usr\bin\python3

import urllib3
from bs4 import BeautifulSoup
import re
import time
import os

from debug.mutable_schedule import *
from awake_gdq.path import *
from awake_gdq.retriever import *


def make_html_entry(entry) :
    date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(entry.start_date))
    item = '<tr>\n<td class="start-time text-right">' + date + '</td>\n<td>' + entry.title + '</td>\n<td>lorem</td>\n<td>ipsum</td>\n<td rowspan="2" class="visible-lg text-center"> <i class="fa fa-clock-o text-gdq-red" aria-hidden="true"></i> 0:19:00 </td>\n</tr>\n<tr class="second-row">\n<td class="text-right "> <i class="fa fa-clock-o" aria-hidden="true"></i> 0:19:00 </td>\n<td>amet</td>\n<td><i class="fa fa-microphone"></i> consectetur</td>\n</tr>'
    return item


def make_html_schedule(schedule) :
    content = ''
    for entry in iter(schedule) :
        content += make_html_entry(entry)
        table = '<table id="runTable" class="table table-condensed">\n<thead>\n<tr class="day-split">\n<td>Time &amp; Length</td>\n<td>Run</td>\n<td>Runners &amp; <i class="fa fa-microphone"></i> Host</td>\n<td class="visible-lg">Setup&nbsp;Length</td>\n</tr>\n</thead><tbody>\n' + content + '\n</tbody>\n</table>'
    return table


def parse(cmd_line) :
    cmd = cmd_line.split(' ')
    arg = []
    f = None

    if cmd[0] == 'remove' :
        arg = (int(cmd[1]),)
        f = remove
        return(f, arg)
    elif cmd[0] == 'add' :
        arg = (int(cmd[2]), cmd[1], 60 * int(cmd[3]))
        f = add
        return(f, arg)
    elif cmd[0] == 'shift' :
        arg = (int(cmd[1]), int(cmd[2]))
        f = shift
        return(f, arg)
    elif cmd[0] == 'swap' :
        arg = (int(cmd[1]), int(cmd[2]))
        f = swap
        return(f, arg)
    elif cmd[0] == 'change_title' :
        arg = (cmd[1], int(cmd[2]))
        f = change_title
        return(f, arg)


# the reason we declare this variable global is that we use here singleton pattern : indeed,
# we only need one instance of this, and nobody outside here is going to try to access it, so...
# ...
# okay, the real reason is, I was just too lazy to create a whole new class :/

mutable_schedule = MutableSchedule()

def initialize() :
    global mutable_schedule
    mutable_schedule.initialize()
    get_schedule(mutable_schedule, os.path.join(DEBUG_PATH, 'base_schedule.html'))
    file = os.open(os.path.join(LOCAL_PATH, 'new_schedule.html'), os.O_WRONLY|os.O_CREAT)
    os.write(file, bytes(make_html_schedule(mutable_schedule), 'utf-8'))
    os.close(file)

def change(cmd_line) :
    f = None
    arg = []

    f, arg = parse(cmd_line)
    f(mutable_schedule, *arg)

    file = os.open(os.path.join(LOCAL_PATH, 'new_schedule.html'), os.O_WRONLY|os.O_CREAT)
    os.write(file, bytes(make_html_schedule(mutable_schedule), 'utf-8'))
    os.close(file)
