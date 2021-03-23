
import tkinter as tk
from about import AboutMe
from utils import TestWindow
import subprocess
import os
import utils as utils
from utils import MessageDialog
from json import JSONDecoder, JSONDecodeError
from utils import ScrollFrame
from inCall import InCall
import json
from ContactDetails import ContactDetailsView

def Contact(self, jso={}, fg='black', bg='white', font=('Franklin Gothic Book', 14), onClick=lambda text: print(text)):
    lbl = tk.Label(self, text=jso['name'], anchor='w', fg=fg, bg=bg, font=font)
    lbl.bind("<Button-1>", func=lambda text: onClick(json.dumps(jso)))
    return lbl
    
def ContactListView(self, json=[], fg='black', bg='white', onClick=lambda text: print(text) ):
    j = JSONDecoder().decode(json)
    for i in range(0, len(j)):
        cont = Contact(self.scrollFrame.viewPort, jso=j[i], fg=fg, bg=bg, onClick = lambda text: onClick(text) )
        cont.grid(row=i, column=0, sticky='w')
    
def createIndex(self, row = 0, col = 0, rowSpan = 1, colSpan = 1):
    frm = tk.Frame(self,)
    for i in range(0, 30):
        lbl = tk.Label(frm, text=str(i))
        lbl.grid(row=i)
    frm.grid(row = row, column= col, rowspan = rowSpan, columnspan = colSpan)
    return frm

class ContactsPage(tk.Tk):

    wait = None
    offset=0

    def __init__(self):
        super().__init__()
        self.transient()
        #self.resizable(true, False)
        #self.master = master
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('Contacts')
        self.config(bg=utils.BACK)

        self.scrollFrame = ScrollFrame(self, bg=utils.BACK) # add a new scrollable frame.
        
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        self.fillContacts()
        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        
        #self.index = createIndex(self, col=12, rowSpan=9)
      

    def close(self):
        """Close window"""
        #self.master.wait = None
        self.destroy()

    def event_click(self, event):
        print()

    def favClic(self, text):
        print(text)

    def fillContacts(self):
        a = str(subprocess.check_output(utils.cmd_contact()))
        if a.__contains__('error'):
            self.wait = EOFError(a)
            utils.Utils.showError(self, a)
        else:
            a=utils.clean(a)
            ContactListView(self, a, bg=utils.BACK, fg=utils.FRONT, onClick=lambda text: self.openContact(text))

    def openContact(self, json):
        if not self.wait == None:
            return
        self.wait = ContactDetailsView(self, json)
        self.wait.wait_window()
        self.wait = None
            


if __name__ == '__main__':
    s = ContactsPage()
    s.mainloop()           
    
