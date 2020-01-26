#/usr/bin/python3

import tkinter as tk
from tkinter import filedialog
import time
from math import floor

from awake_gdq.schedule import *
from awake_gdq.config import *

COL_WIDTH = 210
COL_HEIGHT = 850
COL_BORDER_WIDTH = 4
TIMELINE_WIDTH = 50
DAY_LABEL_HEIGHT = 50
HOUR_LENGTH = (COL_HEIGHT - 2*COL_BORDER_WIDTH) / 24
SIZE_LED = 15


days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



## This class implements the base schedule layout ##

class TimeTable(tk.Frame) :
    def __init__(self, master, *args, **kwargs) :
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.grid(row = 0, column = 0)

        self.dummy_frame = tk.Frame(self, height = DAY_LABEL_HEIGHT, width = TIMELINE_WIDTH)
        self.dummy_frame.grid_propagate(False)
        self.dummy_frame.grid(row = 0, column = 0)

        self.timeline_frame = tk.Frame(self, height = COL_HEIGHT, \
                width = TIMELINE_WIDTH)
        self.timeline_frame.grid_propagate(False)
        self.timeline_frame.grid(row = 1, column = 0)

        for i in range(24) :
            self.time = tk.Label(self.timeline_frame, text = str(i) + ':00')
            self.time.place(x = TIMELINE_WIDTH/2, y = (i + 0.5) * HOUR_LENGTH, anchor='center')

        self.sc_frame = [None, None, None, None, None, None, None, None]
        for i in range(8) :
            self.day_frame = tk.Frame(self, height = DAY_LABEL_HEIGHT, width = COL_WIDTH)
            self.day_frame.grid_propagate(False)
            self.day_frame.grid(row = 0, column = i+1)

            self.day_label = tk.Label(self.day_frame, text = days[i])
            self.day_label.place(y = DAY_LABEL_HEIGHT/2, x = COL_WIDTH/2, anchor = 'center')

            self.sc_frame[i] = tk.Frame(self, height = COL_HEIGHT, \
                    width = COL_WIDTH, background = BACKGROUND_COLOR,
                    relief = tk.SUNKEN, borderwidth = COL_BORDER_WIDTH)
            self.sc_frame[i].grid_propagate(False)
            self.sc_frame[i].grid(row = 1, column = i+1)

        self.origin_date = 0 
        self.color_switch = False

        self.color_1 = ENTRY_COLOR_1
        self.color_2 = ENTRY_COLOR_2
        self.background = BACKGROUND_COLOR

    def change_color(self, color_1, color_2, background) :
        self.color_1 = color_1
        self.color_2 = color_2
        self.background = background
        for frame in self.sc_frame :
            frame.config(background = self.background)

    def map_entry(self, title = '', start_date = 0, duration = 1800) :
        entry_height = (duration / 3600) * HOUR_LENGTH
        origin = floor(self.origin_date / (3600 * 24)) * (3600 * 24)
        offset_from_origin = start_date - origin
        day_num = floor(offset_from_origin / (3600 * 24))
        start_position = ((offset_from_origin - day_num * 3600 * 24) / 3600) * HOUR_LENGTH
        color = (self.color_1 if self.color_switch else self.color_2)
        self.color_switch = not self.color_switch

        chunk = [None]

        while start_position + entry_height > COL_HEIGHT - 2*COL_BORDER_WIDTH :
            chunk_height = COL_HEIGHT - 2*COL_BORDER_WIDTH - start_position
            ch = Chunk(self.sc_frame[day_num], title, height = chunk_height, \
                    width = COL_WIDTH - 2*COL_BORDER_WIDTH, background = color)
            ch.place(x = 0, y = start_position)

            entry_height = entry_height - chunk_height
            start_position = 0
            day_num = day_num + 1
            chunk.append(ch)

        ch = Chunk(self.sc_frame[day_num], title, height = entry_height + 1, \
                width = COL_WIDTH - 2*COL_BORDER_WIDTH, \
                background = color)
        ch.place(x = 0, y = start_position)

        chunk[0] = ch

        return chunk

    def clear(self) :
        for col in self.sc_frame :
            if col != None :
                for widget in col.winfo_children() :
                    widget.destroy()



class Chunk(tk.Frame) :
    def __init__(self, master, title, *args, **kwargs) :
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.entry_label = tk.Label(self, text = title)
        self.entry_label.place(x = kwargs.get('width', 0)/2, y = kwargs.get('height', 0)/2, anchor = 'center')
        self.entry_label.config(background = kwargs.get('background', None))

    def bind(self, sequence = None, evtGest = None, add = None) :
        tk.Frame.bind(self, sequence, evtGest, add)
        self.entry_label.bind(sequence, evtGest, add)




## This class implements the window displaying entry informations ##

class InfoFrame(tk.Toplevel) :
    def __init__(self, master, *args, **kwargs) :
        tk.Toplevel.__init__(self, master, *args, **kwargs)

    def bind_info(self, **kwargs) :
        self.identifier = kwargs.get('identifier', 0)

        self.title('Informations')
        self.entry_title = tk.Label(self, text = kwargs.get('entry_title', ''), font = ('TKDefaultFont', 11, 'bold'))
        self.entry_title.pack()
        self.category = tk.Label(self, text = kwargs.get('category', ''), font = ('TKDefaultFont', 10, 'bold'))
        self.category.pack()
        self.start = tk.Label(self, text = 'starts at : ' + \
                time.asctime(time.gmtime(kwargs.get('start_date', 0))))
        self.start.pack()
        self.end = tk.Label(self, text = 'ends at : ' + \
                time.asctime(time.gmtime(kwargs.get('start_date', 0) + kwargs.get('duration', 0))))
        self.end.pack()
        self.runners = tk.Label(self, text = 'runners : ' + kwargs.get('runners', ''))
        self.runners.pack()
        self.estimate = tk.Label(self, text = 'estimate : ' + kwargs.get('estimate', '0:00:00'))
        self.estimate.pack()

        self.alarm = tk.Checkbutton(self, text = 'set alarm')
        self.alarm.pack()
        if kwargs.get('alarm', 0) : self.alarm.select()



class OptionPanel(tk.Toplevel) :
    def __init__(self, master, *args, **kwargs) :
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        self.title('Control Panel')

        self.panel = tk.Frame(self)
        self.panel.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.finish = tk.Frame(self, pady = 10, padx = 5)
        self.finish.grid(row = 1, column = 0)

        self.browse_music = tk.Button(self.panel, text = 'Browse File', command = self.browse_music)
        self.loaded_music = tk.Label(self.panel)
        self.time_before_start_frame = tk.Frame(self.panel)
        self.refresh_period_frame = tk.Frame(self.panel)
        self.color_1 = ColorPanel(self.panel)
        self.color_2 = ColorPanel(self.panel)
        self.background = ColorPanel(self.panel)

        self.time_before_start_var = tk.StringVar()
        self.refresh_period_var = tk.StringVar()
        self.music_path = ''

        self.time_before_start = tk.Spinbox(self.time_before_start_frame, \
                textvariable = self.time_before_start_var, \
                from_ = 0, to = 60, increment = 5,  width = 2)
        self.refresh_period = tk.Spinbox(self.refresh_period_frame, \
                textvariable = self.refresh_period_var, \
                from_ = 5, to = 60, increment = 5, width = 2)
        self.time_before_start.grid(row = 0, column = 0)
        self.refresh_period.grid(row = 0, column = 0)
        self.minute_1 = tk.Label(self.time_before_start_frame, text = 'minutes before start')
        self.minute_2 = tk.Label(self.refresh_period_frame, text = 'minutes')
        self.minute_1.grid(row = 0, column = 1)
        self.minute_2.grid(row = 0, column = 1)

        self.browse_music_label = tk.Label(self.panel, text = 'browse alarm :')
        self.time_before_start_label = tk.Label(self.panel, text = 'wake me up :')
        self.refresh_period_label = tk.Label(self.panel, text = 'refresh every :')
        self.color_1_label = tk.Label(self.panel, text = 'entry color #1 :')
        self.color_2_label = tk.Label(self.panel, text = 'entry color #2 :')
        self.background_label = tk.Label(self.panel, text = 'background color :')

        self.browse_music_label.grid(row = 0, column = 0, sticky = 'e')
        self.time_before_start_label.grid(row = 2, column = 0, sticky = 'e')
        self.refresh_period_label.grid(row = 3, column = 0, sticky = 'e')
        self.color_1_label.grid(row = 4, column = 0, sticky = 'e')
        self.color_2_label.grid(row = 5, column = 0, sticky = 'e')
        self.background_label.grid(row = 6, column = 0, sticky = 'e')

        self.browse_music.grid(row = 0, column = 1, sticky = 'w', pady = 10)
        self.loaded_music.grid(row = 1, column = 1, sticky = 'w')
        self.time_before_start_frame.grid(row = 2, column = 1, sticky = 'w', pady = 10)
        self.refresh_period_frame.grid(row = 3, column = 1, sticky = 'w', pady = 10)
        self.color_1.grid(row = 4, column = 1, sticky = 'w', pady = 10)
        self.color_2.grid(row = 5, column = 1, sticky = 'w', pady = 10)
        self.background.grid(row = 6, column = 1, sticky = 'w', pady = 10)

        self.apply = tk.Button(self.finish, text = 'Apply')
        self.save = tk.Button(self.finish, text = 'Save')
        self.exit = tk.Button(self.finish, text = 'Exit')

        self.apply.grid(row = 0, column = 0)
        self.save.grid(row = 0, column = 1)
        self.exit.grid(row = 0, column = 2)

    def browse_music(self) :
        music_path = tk.filedialog.askopenfilename(title = 'Browse audio file', \
                filetypes = (('mp3 files', '*.mp3'), \
                ('wav files', '*.wav'), ('au files', '*.au'), ('snd files', '*.snd'), \
                ('aiff files', '*.aiff'), ('sd files', '*.sd'), ('all files', '*')))
        if music_path != '' :
            self.music_path = music_path
            self.loaded_music.config(text = self.music_path)

    def set_default_values(self, **kwargs) :
        self.color_1.set_default_values(kwargs.get('color1', '#000000'))
        self.color_2.set_default_values(kwargs.get('color2', '#000000'))
        self.background.set_default_values(kwargs.get('background', '#000000'))

        self.time_before_start_var.set(kwargs.get('before', 10))
        self.refresh_period_var.set(kwargs.get('refresh', 5))
        self.music_path = kwargs.get('music', '')

    def get_colors(self) :
        return (self.color_1.get_rgb(), self.color_2.get_rgb(), self.background.get_rgb())

    def get_refresh_period(self):
        return int(self.refresh_period_var.get())

    def get_time_before_start(self):
        return int(self.time_before_start_var.get())
    


class ColorPanel(tk.Frame) :
    def __init__(self, master, *args, **kwargs) :
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.r = tk.IntVar()
        self.g = tk.IntVar()
        self.b = tk.IntVar()

        self.slide_r = self.make_color_scale(self.r)
        self.slide_g = self.make_color_scale(self.g)
        self.slide_b = self.make_color_scale(self.b)

        self.visual = tk.Frame(self, height = 20, width = 20, \
                relief = 'sunken', borderwidth = 2)

        self.slide_r.grid(row = 0, column = 0)
        self.slide_g.grid(row = 1, column = 0)
        self.slide_b.grid(row = 2, column = 0)
        self.visual.grid(row = 1, column = 1, padx = 10)

    def set_default_values(self, color) :
        r, g, b = self.hex_to_rgb(color)
        self.r.set(r)
        self.g.set(g)
        self.b.set(b)
        self.set_color()

    def make_color_scale(self, var) :
        return tk.Scale(self, orient = 'horizontal', sliderlength = 15, width = 10, length = 60, \
                showvalue = 0, from_ = 0, to = 255, variable = var, command = lambda e: self.set_color())

    def set_color(self) :
        self.visual.config(background = self.get_rgb())

    def get_rgb(self) :
        return '#%02x%02x%02x' % (self.r.get(), self.g.get(), self.b.get())

    def hex_to_rgb(self, color) :
        return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))



class WakeUpWindow(tk.Toplevel) :
    def __init__(self, master, *args, **kwargs) :
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        self.title('Wake Up')

        self.wake_label = tk.Label(self, text = 'It\'s time to wake up.', font = ('TKDefaultFont', 11, 'bold'))
        self.wake_label.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.stop_button = tk.Button(self, text = 'Stop')
        self.stop_button.grid(row = 1, column = 0, padx = 5, pady = 5)


class LED(tk.Canvas) :
    led_on = None
    led_off = None

    def __init__(self, master, *args, **kwargs) :
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.config(width = SIZE_LED, height = SIZE_LED, borderwidth = 0, highlightthickness = 0)
        if LED.led_off :
            self.set_off()

    def set_image(self, led_on, led_off) :
        LED.led_on = led_on
        LED.led_off = led_off
        self.set_off()

    def set_on(self) :
        self.delete('all')
        self.create_image(SIZE_LED/2, SIZE_LED/2, image = LED.led_on)

    def set_off(self) :
        self.delete('all')
        self.create_image(SIZE_LED/2, SIZE_LED/2, image = LED.led_off)
    
