#/usr/bin/python3

import tkinter as tk

from awake_gdq.application import Application

def main() :
    root = tk.Tk()
    a = Application(root)
    root.mainloop()

if __name__ == '__main__' :
    main()
