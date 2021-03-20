"""
    AboutMe popup window 
"""
import tkinter as tk
from tkinter.ttk import Separator
import pathlib
from utils import TestWindow

class AboutMe(tk.Toplevel):
    """About Me popup widow to display general application description"""

    def __init__(self, master):
        super().__init__(master)
        self.transient(master)
        self.title('About')
        self.resizable(False, False)
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.focus_set()

    def close(self):
        """Close window"""
        #self.master.focus_set()
        self.destroy()


if __name__ == '__main__':
    w = TestWindow()
    AboutMe(w)
    w.mainloop()        