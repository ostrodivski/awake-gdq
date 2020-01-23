#!/usr/bin/python3

import tkinter as tk
import sys

from awake_gdq.path import *
from awake_gdq.application import Application
from debug.debug_app import DebugApplication

def main() :
    if not os.path.exists(LOCAL_PATH) :
        os.makedirs(LOCAL_PATH, 0o766)

    root = tk.Tk()
    app = None
    if len(sys.argv) > 1 :
        if sys.argv[1] == '--debug' or sys.argv[1] == '-d' :
            app = DebugApplication(root)
        else :
            app = Application(root)
    else :
        app = Application(root)
    root.mainloop()

if __name__ == '__main__' :
    main()
