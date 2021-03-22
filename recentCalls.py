
import tkinter as tk
from about import AboutMe
from inCall import InCall
import subprocess
import os
import utils as utils
from utils import MessageDialog
from json import JSONDecoder, JSONDecodeError



class PhoneDialer(tk.Tk):

    wait = None

    def __init__(self):
        super().__init__()
        self.transient()
        self.resizable(False, False)
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('PhoneDialer')
        self.config(bg=utils.BACK)

        self.lbl = tk.Label(self, text='Recent 4', anchor='e', bg=utils.BACK, fg='white', font=('Franklin Gothic Book', 14))
        self.lbl.grid(row=0, columnspan=4, sticky='ew', padx=4, pady=2, )

        self.fav1t = tk.StringVar(self)
        self.fav2t = tk.StringVar(self)
        self.fav3t = tk.StringVar(self)
        self.fav4t = tk.StringVar(self)
        self.fav1t1 = tk.StringVar(self)
        self.fav2t1 = tk.StringVar(self)
        self.fav3t1 = tk.StringVar(self)
        self.fav4t1 = tk.StringVar(self)

        self.fav1 = self.createFav(1, self.fav1t, self.fav1t1)
        self.fav2 = self.createFav(2, self.fav2t, self.fav2t1)
        self.fav3 = self.createFav(3, self.fav3t, self.fav3t1)
        self.fav4 = self.createFav(4, self.fav4t, self.fav4t1)

        self.number = tk.Text(self, width=7, height=2, font=('Franklin Gothic Book', 12), bg=utils.BACK, fg='gray')
        self.number.grid(row=5, columnspan=2, sticky='ew', padx=4, pady=2)
        
        self.std_btn(utils.BACKSPACE_TEXT, utils.BACK, 5, 2, fg=utils.WHITE)
    
        self.std_btn("1", utils.WHITE, 6, 0), self.std_btn("2", utils.WHITE, 6, 1), self.std_btn("3", utils.WHITE, 6, 2), 
        self.std_btn("4", utils.WHITE, 7, 0), self.std_btn("5", utils.WHITE, 7, 1), self.std_btn("6", utils.WHITE, 7, 2), 
        self.std_btn("7", utils.WHITE, 8, 0), self.std_btn("8", utils.WHITE, 8, 1), self.std_btn("9", utils.WHITE, 8, 2), 
        self.std_btn("*", utils.TAN, 9, 0), self.std_btn("0", utils.WHITE, 9, 1), self.std_btn("#", utils.TAN, 9, 2)
        self.std_btn(utils.ABOUT_TEXT, utils.TAN, 10, 0), 
        self.std_btn(utils.CALL_TEXT, utils.GREEN, 10, 1), 
        self.std_btn(utils.RECENT_TEXT, utils.TAN, 10, 2)
 
        self.number.focus_set() 
        self.checkDependencies()

        self.fillRecent()

        #tests

    def about_me(self):
        """Application and license info"""
        AboutMe(self)

    def close(self):
        """Close window"""
        self.destroy()

    def std_btn(self, text, bg, row, col, width=7, height=2, font=('Franklin Gothic Book', 12), fg='black'):
        btn = tk.Button(self, text=text, bg=bg, fg=fg, width=width, height=height, font=font, command=lambda: self.event_click(text))
        return btn.grid(row=row, column=col, padx=4, pady=4)

    def createFav(self, r, textvar1, textvar2):
        frm = tk.Frame(self,bg=utils.BACK)
        lbl1 = tk.Label(frm, textvariable= textvar1, anchor='e', bg=utils.BACK, fg='white', font=('Franklin Gothic Book', 14),)
        lbl1.grid(row=0, sticky='e')
        lbl2 = tk.Label(frm,textvariable= textvar2, anchor='e', bg=utils.BACK, fg='white', font=('Franklin Gothic Book', 10))
        lbl2.grid(row=1, sticky='e')
        #command=lambda: self.favClic(str(textvar2).split(' ')[0])
        return frm.grid(row=r, columnspan=4, sticky='e', padx=4, pady=2, )

    def event_click(self, event):
        if self.checkDependencies() and self.wait == None:
            if event in [utils.BACKSPACE_TEXT]:
                self.back_space()
            if event in ['0','1','2','3','4','5','6','7','8','9','*','#']:
                self.number_click(event)
            if event == utils.CALL_TEXT and len(self.number.get(1.0, tk.END))>1:
                self.call_number()
            if event == utils.RECENT_TEXT:
                self.recent()
            if event == utils.ABOUT_TEXT:
                self.about_me()

    def favClic(self, text):
        print(text)

    # click events
    def number_click(self, event):
        ''' add digit to front or back list when clicked '''
        self.number.insert(tk.END, event)
        self.number.focus_set()

    def clear_click(self):
        self.number.replace(1.0, tk.END, '')
        self.number.focus_set()

    def back_space(self):
        s = self.number.get(1.0, tk.END)
        self.number.replace(1.0, tk.END, '')
        l = float(len(s))
        i = 0
        while i < l-2 :
            self.number.insert(float(i+1), s[i])
            i+=1
        self.number.focus_set()
        

    def call_number(self):
        num = self.number.get(1.0, tk.END).replace('\n', '')
        a = subprocess.check_output(["termux-telephony-call", num])
        if len(a)<=1 or a.__contains__('error'):
            self.wait = InCall(self,num )
        else :
            self.wait = EOFError(a)
            utils.Utils.showError(self, a)

    def recent(self):
        print('recent')    
   
    def checkDependencies(self):
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

    def fillRecent(self):
        if self.checkDependencies():
            a = str(subprocess.check_output(["termux-call-log", "-l", '4']))#['/bin/sh','/Volumes/Datos/_Projects/+python/PhoneDialer/termux-call-log']))#["termux-call-log", "-l", '4']))
            if a.__contains__('error'):
                self.wait = EOFError(a)
                utils.Utils.showError(self, a)
            else:
                a=a.replace('b\'', '').replace('\\n\'','').replace('\\n','')
                j = JSONDecoder().decode(a)
                lista = [self.fav4t, self.fav3t, self.fav2t, self.fav1t, ]
                lista1 = [self.fav4t1, self.fav3t1, self.fav2t1, self.fav1t1, ]
                for i in range(0,4):
                    s = '⬇️'
                    if str(j[i]['type']) == 'OUTGOING':
                        s = '⬆️'
                    lista[i].set(j[i]['name']+' '+j[i]['duration']+' '+s)
                    lista1[i].set(j[i]['phone_number']+' '+j[i]['date'])


if __name__ == '__main__':
    w = PhoneDialer()
    w.mainloop()        
    
