
import tkinter as tk
from about import AboutMe
from utils import TestWindow
import utils
import os
import threading
import subprocess


class InCall(tk.Toplevel):

    def __init__(self, master, number, name=None):
        super().__init__(master)
        self.transient(master)
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('Calling')
        self.config(bg=utils.BACK)
        self.master = master

        tk.Label(self, text=utils.CONTACTS_TEXT, anchor='center', bg=utils.BACK, fg=utils.FRONT,  
                                font=('Franklin Gothic Book', 68,)).grid(row=0)
        
        size = 28
        if not name == None:
            self.lbl = tk.Label(self, text=name, anchor='center', bg=utils.BACK, fg=utils.FRONT, 
                                font=('Franklin Gothic Book', 28,))
            self.lbl.grid(row=1, sticky='ew', padx=4, pady=2, )
            size = 16
        
        self.lbl = tk.Label(self, text=number, anchor='center', bg=utils.BACK, fg=utils.FRONT,
                                font=('Franklin Gothic Book', size,))
        self.lbl.grid(row=2, sticky='ew', padx=4, pady=2, )

        self.end_call_btn = self.std_btn(utils.CALL_TEXT, utils.RED, 10, 0)

    def about_me(self):
        """Application and license info"""
        AboutMe(self)

    def close(self):
        """Close window"""
        self.master.wait = None
        #todo find better way to end call
        subprocess.check_output(utils.cmd_endCall())
        self.destroy()

    def std_btn(self, text, bg, row, col, width=7, height=2, font=('Franklin Gothic Book', 24), fg='white'):
        btn = tk.Label(self, text=text, anchor='center', bg=bg, fg=fg, font= font, width=width, height= height)
        btn.bind("<Button-1>", func=lambda event: self.event_click(text))
        btn.grid(row=row, column=col, padx=4, pady=4)
        return btn

    def event_click(self, event):
        if event == utils.CALL_TEXT:
            self.end_call()


    # click events
    def end_call(self):
        #todo    
        self.close()

if __name__ == '__main__':
    s = TestWindow()
    InCall(s, '555', 'asd')
    s.mainloop()