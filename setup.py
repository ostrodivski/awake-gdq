#!/usr/bin/python3

import os
from setuptools import setup, find_packages

setup(
        name = 'awake-gdq',
        version = '1.0.1',
        author = 'Ostrodivski',
        description = 'An interactive schedule for GDQ\'s',
        url = 'https://github.com/ostrodivski/awake-gdq',
        packages = find_packages(),
        package_data = {
            'awake_gdq': ['*.png', '*.wav'],
            'debug': ['base_schedule.html', 'command.txt']
            },
        requires = ['bs4', 'urllib3'],
        entry_points = {
            'gui_scripts' : ['awake-gdq = awake_gdq.main:main']
            }
)
           
