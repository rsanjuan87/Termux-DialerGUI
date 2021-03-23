
import tkinter as tk
from about import AboutMe
from utils import TestWindow
import utils
import os
import threading
import subprocess
from json import JSONDecoder, JSONDecodeError
from inCall import InCall


class ContactDetailsView(tk.Toplevel):

    wait = None

    def __init__(self, master, json={}):
        super().__init__(master)
        self.transient(master)
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('Contact details')
        self.config(bg=utils.BACK)
        self.master = master

        j = JSONDecoder().decode(json)
        name = j['name']
        number = j['number']        
        size = 28

        tk.Label(self, text=utils.CONTACTS_TEXT, anchor='center', bg=utils.BACK, fg=utils.FRONT,  
                                font=('Franklin Gothic Book', 68,)).grid(row=0)

        if not name == None:
            self.lbl = tk.Label(self, text=name, anchor='w', bg=utils.BACK, fg=utils.FRONT, 
                                font=('Franklin Gothic Book', 28))
            self.lbl.grid(row=1, sticky='w', padx=10, pady=2)
            size = 16

        frm = tk.Frame(self, bg=utils.BACK)
        frm.grid(row=2)

        self.lbl = tk.Label(frm, text=number, anchor='w', bg=utils.BACK, fg=utils.FRONT,
                                font=('Franklin Gothic Book', size))
        self.lbl.grid(row=0, sticky='w', padx=10, pady=2, column= 0)
        
        self.btnCall = tk.Label(frm, text=utils.CALL_TEXT, anchor='center', bg='green', fg=utils.FRONT, 
                                font=('Franklin Gothic Book', 24))
        self.btnCall.grid(row=0, sticky='e', padx=4, pady=2, column=1)
        self.btnCall.bind("<Button-1>", func=lambda text: self.call(json))
        
        self.btnSms = tk.Label(frm, text=utils.SMS_TEXT, anchor='center', bg='orange', fg=utils.FRONT, 
                                font=('Franklin Gothic Book', 24))
        self.btnSms.grid(row=0, sticky='e', padx=4, pady=2, column=2)
        self.btnSms.bind("<Button-1>", func=lambda text: self.sms(json))

    def close(self):
        """Close window"""
        self.master.wait = None
        self.destroy()

    def call(self, json):
        if not self.wait == None:
            return
        j = JSONDecoder().decode(json)
        self.wait = InCall(self, j['number'], j['name'])
        self.wait.wait_window()
        self.wait = None

    def sms(self, json):
        'todo'

if __name__ == '__main__':
    s = TestWindow()
    ContactDetailsView(s, '{"number":"555", "name":"asd"}')
    s.mainloop()