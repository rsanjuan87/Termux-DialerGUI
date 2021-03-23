
import tkinter as tk
from tkinter.ttk import Separator
import pathlib
from config import *



class Utils():
    def showError(self, error):
        "mostrara el error en cuestion"
        err = str(error)
        if(err.__contains__("android.permission.CALL_PHONE")):
            print(error)
            MessageDialog(self, 'Enable call permission to Termux:API', 'Error')


class MessageDialog(tk.Toplevel):

    def __init__(self, master, text, title):
        super().__init__(master)
        self.transient(master)
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title(title)
        self.master = master
        tk.Label(self, text=text).grid(row=0, columnspan=2, padx=4, pady=2, )
        tk.Button(self, text='Ok', command=lambda: self.close()).grid(row=1, column=1, padx=4, pady=2)

    def close(self):
        """Close window"""
        self.master.wait = None
        self.destroy()

class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""
    def __init__(self):
        super().__init__()

def clean(text):
    return text.replace('b\'', '').replace('\\n\'','').replace('\\r','').replace('\\','\\\\').replace('\\\\n','\n').replace('\\\\"','\\"')


if __name__ == '__main__':
    w = TestWindow()
    MessageDialog(w, '', '')
    w.mainloop()            