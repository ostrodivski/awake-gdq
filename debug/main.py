#!/usr/bin/python3

import tkinter as tk
from debug.debug_app import DebugApplication

def main() :
    root = tk.Tk()
    a = DebugApplication(root)
    root.mainloop()

if __name__ == '__main__' :
    main()

