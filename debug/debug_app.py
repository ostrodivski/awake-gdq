#!/usr/bin/python3

import time
import tkinter as tk
import os

from awake_gdq.application import *
from debug.change import *

class DebugApplication(Application) :
    def __init__(self, master) :
        self.active = False
        self.stopped = True

        self.origin_effective_date = 0
        self.origin_real_date = 0
        self.last_real_date = 0
        self.last_effective_date = 0

        self.time_multiplier = 1

        self.now_guid = None
        initialize()

        Application.__init__(self, master)

        self.debug_panel = DebugPanel(self.master)
        self.debug_panel.time_rule.config(command = self.set_time_multiplier)

        self.debug_panel.play_button.config(command = self.play)
        self.debug_panel.stop_button.config(command = self.stop)
        self.debug_panel.pause_button.config(command = self.pause)
        self.debug_panel.command_button.config(command = self.parse)

        self.refresh_period = 180

        self.set_origin_date()
        self.display_now_guid()

        self.cmd_guid = []
        self.cmd_line = []
        self.cmd_date = []
        self.cmd_index = 0




    # guids

    def display_now_guid(self) :
        if self.now_guid :
            self.now_guid.destroy()
        day = int((self.last_effective_date - self.origin_effective_date) / (3600 * 24))
        hours = ((self.last_effective_date - self.origin_effective_date) - day * 3600 * 24) / 3600
        self.now_guid = Guid(self.time_table.sc_frame[day], background = 'red')
        self.now_guid.place(x = 0, y = hours * HOUR_LENGTH)

    def display_cmd_guids(self) :
        for day, hour in self.cmd_guid :
            guid = Guid(self.time_table.sc_frame[day], background = 'blue')
            guid.place(x = 0, y = hour * HOUR_LENGTH)

    # control

    def play(self) :
        if not self.stopped and not self.active :
            self.last_real_date = time.time()
        elif self.stopped and not self.active :
            self.set_origin_date()
        self.stopped = False
        self.active = True

    def stop(self) :
        self.stopped = True
        self.active = False
        self.cmd_index = 0
        initialize()
        self.initialize()

    def pause(self) :
        self.active = False
        self.cmd_index = 0


    # time data settings

    def set_time_multiplier(self, value) :
        self.time_multiplier = int(value)

    def set_origin_date(self) : # save the date at which you launched the simulation (real + effective)
        self.origin_real_date = time.time()
        self.last_real_date = self.origin_real_date
        date = self.sc.time_origin
        self.origin_effective_date = floor(date / (3600 * 24)) * 3600 * 24
        self.last_effective_date = date
        self.last_refresh = self.origin_effective_date

    def set_last_date(self) :
        self.last_effective_date = self._date(time.time())
        self.last_real_date = time.time()

    def parse(self) : 
        self.cmd_guid = []
        self.cmd_line = []
        self.cmd_date = []
        self.cmd_index = 0
        file = open(os.path.join(DEBUG_PATH, 'command.txt'), 'r')
        for line in file.readlines() :
            print(line)
            cmd = line.split(' - ')
            self.cmd_line.append(cmd[1])
            date_str = cmd[0].split()
            day = int(date_str[0])
            hour = int(date_str[1][0:2]) + int(date_str[1][3:5]) / 60
            self.cmd_guid.append((day, hour))
            self.cmd_date.append(self.origin_effective_date + day * 24 * 3600 + hour * 3600)
            self.display_cmd_guids()
        file.close()


    # debug

    def _update(self) :
        if self.active :
            self.set_last_date()
            self.display_now_guid()
            if self.cmd_index < len(self.cmd_guid) :
                if self.cmd_date[self.cmd_index] <= self.last_effective_date :
                    change(self.cmd_line[self.cmd_index])
                    self.cmd_index = self.cmd_index + 1

    def _refresh(self) :
        self.display_cmd_guids()

    def _map_schedule(self) :
        for entry in iter(self.sc) :
            identifier = tk.Label(entry.principal_chunk, text = entry.identifier)
            identifier.place(x = 0, y = 0)

    def _date(self, date) : # get real date, return effective date
        time_offset = self._duration(date - self.last_real_date)
        return self.last_effective_date + time_offset

    def _duration(self, duration) :
        return duration * self.time_multiplier

    def _active(self) :
        return self.active

    def _get_schedule_path(self) :
        return os.path.join(LOCAL_PATH, 'new_schedule.html')

class Guid(tk.Frame) :
    def __init__(self, master, *args, **kwargs) :
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.config(height = 3, width = COL_WIDTH)


class DebugPanel(tk.Toplevel) :
    def __init__(self, master, *args, **kwargs) :
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        self.title('Debug Panel')

        self.multiplier = tk.IntVar()
        self.multiplier.set(1)
        self.time_rule = tk.Scale(self, orient = 'horizontal', length = 400, showvalue = 0, \
                variable = self.multiplier, from_ = 1, to = 2000)
        self.time_rule.grid(row = 0, column = 0)

        self.play_button = tk.Button(self, text = 'Play')
        self.play_button.grid(row = 1, column = 0)
        self.pause_button = tk.Button(self, text = 'Pause')
        self.pause_button.grid(row = 2, column = 0)
        self.stop_button = tk.Button(self, text = 'Stop')
        self.stop_button.grid(row = 3, column = 0)

        self.command_button = tk.Button(self, text = 'Set Commands')
        self.command_button.grid(row = 0, column = 1)
