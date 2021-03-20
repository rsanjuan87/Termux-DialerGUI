"""
    AboutMe popup window 
"""
import tkinter as tk
from tkinter.ttk import Separator
import pathlib

class AboutMe(tk.Toplevel):
    """About Me popup widow to display general application description"""

    def __init__(self, master):
        super().__init__(master)
        self.transient(master)
        self.title('About')
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.focus_set()

    def close(self):
        """Close window"""
        self.master.focus_set()
        self.destroy()

class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""
    def __init__(self):
        super().__init__()
        self.title('Testing Window')
        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END, 'This is a test. This is only a test.')


if __name__ == '__main__':

    w = TestWindow()
    AboutMe(w)
    w.mainloop()        