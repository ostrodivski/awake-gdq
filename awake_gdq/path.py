import os

ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
DEBUG_PATH = os.path.join(ABSOLUTE_PATH, '../debug/')
HOME = os.path.abspath(os.path.expanduser('~'))
LOCAL_PATH = os.path.join(HOME, '.awake-gdq/')
