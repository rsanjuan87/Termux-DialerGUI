
import tkinter as tk
from about import AboutMe
from utils import TestWindow
import subprocess
import os
import utils as utils
from utils import MessageDialog
from json import JSONDecoder, JSONDecodeError

def Contact(self, json={}, row=0):
    lbl = tk.Label(self, text=json['name'])
    lbl.grid(row=row)
    return lbl
    
def ContactListView(self, json, row=0):
    frm = tk.Frame(self)
    print(json)
    j = JSONDecoder().decode(json)
    for i in range(0, len(j)):
       cont = Contact(frm, j[i])
       cont.grid(row = i)
    frm.grid(row= row)
    return frm

    
    
def createIndex(self, row = 0, col = 0, rowSpan = 1, colSpan = 1):
    frm = tk.Frame(self,)
    for i in range(0, 30):
        lbl = tk.Label(frm, text=str(i))
        lbl.grid(row=i)
    frm.grid(row = row, column= col, rowspan = rowSpan, columnspan = colSpan)
    return frm
    




class RecentCallsPage(tk.Toplevel):

    wait = None
    offset=0

    def __init__(self, master):
        super().__init__()
        self.transient()
        self.resizable(False, False)
        self.master = master
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('Contacts')
        self.config(bg=utils.BACK)

        self.lbl = tk.Label(self, text='Contacs', anchor='e', bg=utils.BACK, fg=utils.FRONT, font=('Franklin Gothic Book', 14))
        self.lbl.grid(row=0, columnspan=4, sticky='ew', padx=4, pady=2, )
        
        self.fillContacts()
        
        #self.index = createIndex(self, col=12, rowSpan=9)
      

    def close(self):
        """Close window"""
        self.master.wait = None
        self.destroy()

    def event_click(self, event):
        print()

    def favClic(self, text):
        print(text)

    def fillContacts(self):
        a = str(subprocess.check_output(["/bin/sh","termux-contact-list"]))
        if a.__contains__('error'):
            self.wait = EOFError(a)
            utils.Utils.showError(self, a)
        else:
            a=utils.clean(a)
            self.lista = ContactListView(self, a, row=1)
            


if __name__ == '__main__':
    s = TestWindow()
    RecentCallsPage(s)
    s.mainloop()           
    
