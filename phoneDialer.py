
import tkinter as tk
from about import AboutMe
from inCall import InCall
import utils as utils
from utils import *
from utils import MessageDialog
from json import JSONDecoder, JSONDecodeError
from recentCalls import RecentListView
from recentCalls import RecentCallsPage
from Contacts import ContactsPage


class PhoneDialerPage(tk.Tk):

    wait = None

    def __init__(self):
        super().__init__()
        self.transient()
        self.resizable(False, False)
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('PhoneDialer')
        self.config(bg=utils.BACK)

        self.lbl = tk.Label(self, text='Recent 4', anchor='e', 
                            bg=utils.BACK, fg='white', 
                            font=('Franklin Gothic Book', 14),
                            borderwidth=0)
        self.lbl.grid(row=0, columnspan=4, sticky='ew', padx=4, pady=2, )

        self.number = tk.Text(self, width=7, height=2, font=('Franklin Gothic Book', 12), bg=utils.BACK, fg=utils.FRONT)
        self.number.grid(row=2, columnspan=2, sticky='ew', padx=4, pady=2)
        
        self.std_btn(utils.BACKSPACE_TEXT, utils.BACK, 2, 2, fg=utils.FRONT)
    
        self.std_btn("1", utils.BACK, 3, 0), self.std_btn("2", utils.BACK, 3, 1), self.std_btn("3", utils.BACK, 3, 2), 
        self.std_btn("4", utils.BACK, 4, 0), self.std_btn("5", utils.BACK, 4, 1), self.std_btn("6", utils.BACK, 4, 2), 
        self.std_btn("7", utils.BACK, 5, 0), self.std_btn("8", utils.BACK, 5, 1), self.std_btn("9", utils.BACK, 5, 2), 
        self.std_btn("*", utils.BACK, 6, 0), self.std_btn("0", utils.BACK, 6, 1), self.std_btn("#", utils.BACK, 6, 2)
        self.std_btn(utils.CONTACTS_TEXT, utils.BACK, 7, 0, font=('Franklin Gothic Book', 28), width=3, height=1), 
        self.std_btn(utils.CALL_TEXT, utils.GREEN, 7, 1, font=('Franklin Gothic Book', 28), width=3, height=1), 
        self.std_btn(utils.RECENT_TEXT, utils.BACK, 7, 2, font=('Franklin Gothic Book', 28), width=3, height=1)

 
        self.number.focus_set() 
        utils.checkDependencies(self)

        self.fillRecent()#row1

        #tests

    def contacts(self):
        """Application and license info"""
        self.wait = ContactsPage()
        self.wait.wait_window()
        self.wait=None

    def about_me(self):
        """Application and license info"""
        self.wait = AboutMe(self)

    def close(self):
        """Close window"""
        self.destroy()

    def std_btn(self, text, bg, row, col, width=5, height=2, font=('Franklin Gothic Book', 24), fg='white'):
        btn = tk.Label(self, text=text, anchor='center', bg=bg, fg=fg, font= font, width=width, height= height)
        btn.bind("<Button-1>", func=lambda event: self.event_click(text))
        btn.grid(row=row, column=col, padx=4, pady=4)
        return btn

    def event_click(self, event):
        if utils.checkDependencies(self) and self.wait == None:
            if event in [utils.BACKSPACE_TEXT]:
                self.back_space()
            if event in ['0','1','2','3','4','5','6','7','8','9','*','#']:
                self.number_click(event)
            if event == utils.CALL_TEXT and len(self.number.get(1.0, tk.END))>1:
                self.call_number()
            if event == utils.RECENT_TEXT:
                self.recent()
            if event == utils.CONTACTS_TEXT:
                self.contacts()

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
        a = subprocess.check_output(utils.cmd_call(num))
        if len(a)<=1 or a.__contains__('error'):
            self.wait = InCall(self,num )
            self.fillRecent()
        else :
            self.wait = EOFError(a)
            utils.Utils.showError(self, a)

    def recent(self):
        self.wait = RecentCallsPage(self) 
        self.fillRecent()

    def fillRecent(self):
        if utils.checkDependencies(self):
            a = str(subprocess.check_output(utils.recent4()))
            if a.__contains__('error'):
                self.wait = EOFError(a)
                utils.Utils.showError(self, a)
            else:
                a=utils.clean(a)
                RecentListView(self, a, row=1, bg=utils.BACK, fg=utils.FRONT, onClick = lambda text: self.number.replace(1.0, tk.END, text))


if __name__ == '__main__':
    w = PhoneDialerPage()
    w.mainloop()        
    
