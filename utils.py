
import tkinter as tk
from tkinter.ttk import Separator
import pathlib
from config import *
import os
import subprocess

testing = False

def recent4():
    if testing:
        return ['/bin/sh','termux-call-log']
    else:
        return ["termux-call-log", "-l", '4']

def recent10(offset):
    if testing:
        return ['/bin/sh','termux-call-log']
    else:
        return ["termux-call-log", "-l", '10', '-o', str(offset)]

def cmd_contact():
    if testing:
        return ["/bin/sh","termux-contact-list"]
    else:
        return ["termux-contact-list"]

def cmd_call(num):
    if testing:
        return ["/bin/sh", "termux-telephony-call", num]
    else:
        return ["termux-telephony-call", num]

def cmd_endCall():
    if testing:
        return ["/bin/sh", "termux-telephony-call", '1']
    else:
        return ["termux-telephony-call", '1']    

def checkDependencies(self):
    if testing:
        return True
    "chek if needed dependecies are instaled and return if are satisfacied"
    deps = ['termux-telephony-call', 'termux-call-log']
    complete = True
    pref = ''
    if not os.getenv('PREFIX') == None :
        pref = os.getenv('PREFIX') 
    for d in deps:
        if not os.path.isfile(pref+'/bin/'+d):
            complete = False
            break
    if not complete and self.wait == None:
        self.wait = MessageDialog(self, 'Please Use Termux For This Caller\nMake Sure You Installed Termux:API\n\tpkg install termux-api',  'Error', )
    return complete


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

class ScrollFrame(tk.Frame):
    def __init__(self, parent, bg='white', height=500, width=200):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background=bg)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background=bg)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)           
        self.canvas.config( height=height, width=width)                                      #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.




if __name__ == '__main__':
    w = TestWindow()
    MessageDialog(w, '', '')
    w.mainloop()            