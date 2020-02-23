#!/usr/bin/python3

import tkinter as tk
import tkSnack

import time
import os

from awake_gdq.path import *
from awake_gdq.schedule import *
from awake_gdq.retriever import *
from awake_gdq.update import *
from awake_gdq.widgets import *
from awake_gdq.config import *

UPDATE_PERIOD = 500    # milliseconds

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



class Application() :
    def __init__(self, master) :
        self.master = master
        self.master.title('Schedule')


        # initialize widgets

        self.time_table = TimeTable(self.master)
        self.time_table.grid(row = 0, column = 0)

        self.panel = tk.Frame(self.master, height = 50, width = 200)
        self.panel.grid(row = 1, column = 0)

                # bottom panel

        self.refresh_button = tk.Button(self.panel, text = 'Refresh', command = self.refresh)
        self.refresh_button.grid(row = 0, column = 0)

        self.auto_refresh = tk.IntVar()
        self.auto_refresh_button = tk.Checkbutton(self.panel, text = 'Auto Refresh', \
                variable = self.auto_refresh, command = self.set_auto_refresh)
        self.auto_refresh_button.grid(row = 0, column = 1)

        self.option_button = tk.Button(self.panel, text = 'Options', command = self.pop_option_panel)
        self.option_button.grid(row = 0, column = 2)

        self.reinitialize_button = tk.Button(self.panel, text = 'Reinitialize', \
                command = self.initialize)
        self.reinitialize_button.grid(row = 0, column = 3)

                # LED path

        led_on = tk.PhotoImage(file = os.path.join(ABSOLUTE_PATH, 'led_on.png'))
        led_off = tk.PhotoImage(file = os.path.join(ABSOLUTE_PATH, 'led_off.png'))

        fake_led = LED(None)    # set the image path in the LED class
        fake_led.set_image(led_on, led_off)
        fake_led.destroy()

                # pop-up windows

        self.wake_up_window = None
        self.option_panel = None
        self.option_panel_open = False

        # initialize schedule

        self.schedule_path = self._get_schedule_path()
        self.sc = DisplayableSchedule(self.master)
        self.initialize()


        # initialize alarm

        self.music_path = os.path.join(ABSOLUTE_PATH, MUSIC_PATH)
        tkSnack.initializeSnack(self.master)
        tkSnack.audio.inputDevices()
        self.music = tkSnack.Sound()
        self.music.read(self.music_path)


        # intialize time data

        self.last_refresh = 0
        self.is_updating = True
        self.update_period = UPDATE_PERIOD
        self.refresh_period = REFRESH_PERIOD
        self.time_before_start = TIME_BEFORE_START

        self.update()


    def initialize(self) :
        self.sc.initialize()
        get_schedule(self.sc, self.schedule_path)
        self.map_schedule()

    def update(self) :
        if self._active() and self.is_updating :
            now = self._date(time.time())
            for entry in iter(self.sc) :
                if entry.alarm_on.get() :
                    start_date = entry.start_date
                    end_date = start_date + entry.duration
                    if now < end_date and now > start_date - self.time_before_start * 60 : 
                        self.play_alarm()
                        entry.switch_alarm()
    
            if self.auto_refresh.get() :
                if now - self.last_refresh > self.refresh_period * 60 :
                    self.refresh()
                    self.last_refresh = now

        self.master.after(self.update_period, self.update)
        self._update()

    # alarm

    def play_alarm(self) :
        self.is_updating = False # stop updating to be sure that the alarm keep playing
        self.wake_up_window = WakeUpWindow(self.master)
        self.wake_up_window.stop_button.config(command = self.stop_alarm)
        self.wake_up_window.protocol('WM_DELETE_WINDOW', self.stop_alarm)
        self.music.play(blocking = 0)

    def stop_alarm(self) :
        self.music.stop()
        self.wake_up_window.destroy()
        self.is_updating = True

    # options

    def pop_option_panel(self) :
        if not self.option_panel_open :
            self.option_panel = OptionPanel(self.master)
            self.option_panel.apply.config(command = self.apply_change)
            self.option_panel.exit.config(command = self.close_option_panel)
            self.option_panel.protocol('WM_DELETE_WINDOW', self.close_option_panel)
            self.option_panel.set_default_values(color1 = self.time_table.color_1, \
                    color2 = self.time_table.color_2, \
                    background = self.time_table.background, before = self.time_before_start, \
                    refresh = self.refresh_period,
                    music = self.music_path)
            self.option_panel_open = True

    def close_option_panel(self) :
        self.option_panel_open = False
        self.option_panel.destroy()

    def apply_change(self) :
        color_1, color_2, background = self.option_panel.get_colors()
        self.time_table.change_color(color_1, color_2, background)
        switch_color = False
        for entry in self.sc :
            entry.change_color(color_1 if switch_color else color_2)
            switch_color = not switch_color
        self.music_path = self.option_panel.music_path
        self.music.read(self.music_path)
        self.refresh_period = self.option_panel.get_refresh_period()
        self.time_before_start = self.option_panel.get_time_before_start()

    # refresh

    def set_auto_refresh(self) :
        if self.auto_refresh.get() :
            self.refresh_button.config(state = 'disabled')
            self.refresh()
            self.last_refresh = self._date(time.time())
        else :
            self.refresh_button.config(state = 'normal')

    def refresh(self) :
        new_sc = DisplayableSchedule(self.master, False)    # False means that we don't want to numerote
                                                            # entries
        e = get_schedule(new_sc, self.schedule_path)
        if e == 0 : # we check if the schedule has been successfully retrieved
            update(self.sc, new_sc)
            del self.sc
            self.sc = new_sc
            self.map_schedule()
            self._refresh()

    def map_schedule(self) :
        self.time_table.clear()
        for entry in iter(self.sc) :
            entry.display(self.time_table)
        self._map_schedule()

    # debug

    def _get_schedule_path(self) :
        return ''

    def _update(self) :
        pass

    def _refresh(self) :
        pass

    def _map_schedule(self) :
        pass

    def _duration(self, duration) : # duration = seconds ; return seconds
        return duration

    def _date(self, date) : # date = seconds (timestamp) ; return seconds
        return date - time.timezone     # that works ; don't ask

    def _active(self) :
        return True


class DisplayableSchedule(Schedule) :
    def __init__(self, master, identified = True) :
        Schedule.__init__(self, identified)

        self.master = master

        self.chunk = []
        self.principal_chunk = None

        self.info_frame = None
        self.info_displayed = False

        self.alarm_led = None
        self.alarm_on = tk.IntVar()
        self.alarm_on.set(0)

    def copy(self, target) :
        Schedule.copy(self, target)
        target.info_displayed = self.info_displayed
        target.info_frame = self.info_frame
        target.alarm_on = self.alarm_on

    def new_sc(self) :
        new = DisplayableSchedule(self.master, self.identified)
        return new


    # display

    def display(self, time_table) :
        if self.is_first :
            time_table.origin_date = self.time_origin

        self.chunk = time_table.map_entry(self.title, self.start_date, self.duration)
        for ch in self.chunk :
            ch.bind('<Button-1>', lambda e: self.pop_info_frame())
            if self.info_displayed :    # /!\ if the info panel is open, don't forget to remap
                                        # the alarm button
                self.info_frame.alarm.config(variable = self.alarm_on, command = self.switch_alarm)
                self.info_frame.protocol('WM_DELETE_WINDOW', self.delete_info_frame)
        self.principal_chunk = self.chunk[0]
        self.alarm_led = LED(self.principal_chunk, background = self.principal_chunk.cget('background'))
        self.alarm_led.place(x = COL_WIDTH - 2*COL_BORDER_WIDTH - SIZE_LED, \
                y = self.principal_chunk.cget('height') - SIZE_LED)
        if self.alarm_on.get() :
            self.alarm_led.set_on()

    def change_color(self, color) :
        for ch in self.chunk :
            ch.config(background = color)
            for child in ch.winfo_children() :
                child.config(background = color)

    # infos

    def pop_info_frame(self) :
        if not self.info_displayed :
            self.info_frame = InfoFrame(self.master)
            self.info_frame.bind_info(identifier = self.identifier, alarm = self.alarm_on.get(), \
                    entry_title = self.title, category = self.category, start_date = self.start_date, \
                    duration = self.duration, runners = self.runners, estimate = self.estimate,)
            self.info_displayed = True
            self.info_frame.protocol('WM_DELETE_WINDOW', self.delete_info_frame)
            self.info_frame.alarm.config(command = self.switch_alarm)

    def delete_info_frame(self) :
        try :   # the info panel may have remained open while the corresponding entry
                # does not exist animore
            self.info_displayed = False
        except tk.TclError :
            pass
        self.info_frame.destroy()

    def rm_info_frame(self) :
        if self.info_displayed :
            self.info_frame.destroy()
            self.info_displayed = False

    def switch_alarm(self) :
        try :
            if self.alarm_on.get() :
                self.alarm_led.set_off()
                self.alarm_on.set(0)   
                self.info_frame.alarm.deselect()    # if the function is not called from pop_info_frame
            else :
                self.alarm_led.set_on()
                self.alarm_on.set(1)
                self.info_frame.alarm.select()
        except tk.TclError :
            pass
