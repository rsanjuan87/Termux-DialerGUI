
import tkinter as tk
from about import AboutMe
from inCall import InCall


WHITE = "#F8F8F8" # black/white
TAN = "#F1EABC" # black/tan
GREEN = "#00AA00" # green
BACK='#272533'
CALL_TEXT="✆"
RECENT_TEXT='⏱'
ABOUT_TEXT='❓'


class PhoneDialer(tk.Tk):

    incall = None

    def __init__(self):
        super().__init__()
        self.transient()
        self.resizable(False, False)
        #self.wm_attributes('-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title('PhoneDialer')
        self.config(bg=BACK)

        self.lbl = tk.Label(self, text='Recent 4', anchor='e', bg=BACK, fg='white', font=('Franklin Gothic Book', 14, 'bold'))
        self.lbl.grid(row=0, columnspan=4, sticky='ew', padx=4, pady=2, )

        self.fav1 = self.createFav('', 1)
        self.fav2 = self.createFav('', 2)
        self.fav3 = self.createFav('', 3)
        self.fav3 = self.createFav('', 4)

        self.number = tk.Text(self, width=7, height=2, font=('Franklin Gothic Book', 24), bg='black', fg='gray')
        self.number.grid(row=5, columnspan=2, sticky='ew', padx=4, pady=2)
        
        self.std_btn("<", BACK, 5, 2)
    
        self.std_btn("1", WHITE, 6, 0), self.std_btn("2", WHITE, 6, 1), self.std_btn("3", WHITE, 6, 2), 
        self.std_btn("4", WHITE, 7, 0), self.std_btn("5", WHITE, 7, 1), self.std_btn("6", WHITE, 7, 2), 
        self.std_btn("7", WHITE, 8, 0), self.std_btn("8", WHITE, 8, 1), self.std_btn("9", WHITE, 8, 2), 
        self.std_btn("*", TAN, 9, 0), self.std_btn("0", WHITE, 9, 1), self.std_btn("#", TAN, 9, 2)
        self.std_btn(ABOUT_TEXT, TAN, 10, 0), 
        self.std_btn(CALL_TEXT, GREEN, 10, 1), 
        self.std_btn(RECENT_TEXT, TAN, 10, 2)
 
        self.number.focus_set() 

        #tests
        self.number.insert(1.0, '123456789')

    def about_me(self):
        """Application and license info"""
        AboutMe(self)

    def close(self):
        """Close window"""
        self.destroy()

    def std_btn(self, text, bg, row, col, width=7, height=2, font=('Franklin Gothic Book', 24)):
        btn = tk.Button(self, text=text, bg=bg, width=width, height=height, font=font, command=lambda: self.event_click(text))
        return btn.grid(row=row, column=col, padx=4, pady=4)

    def createFav(self, text, r):
        lbl = tk.Label(self, text=text, anchor='e', bg=BACK, fg='white', font=('Franklin Gothic Book', 14, 'bold'))
        return lbl.grid(row=r, columnspan=4, sticky='ew', padx=4, pady=2, )

    def event_click(self, event):
        if self.incall == None:
            if event in ['<']:
                self.back_space()
            if event in ['0','1','2','3','4','5','6','7','8','9','*','#']:
                self.number_click(event)
            if event == CALL_TEXT and len(self.number.get(1.0, tk.END))>1:
                self.call_number()
            if event == RECENT_TEXT:
                self.recent()
            if event == ABOUT_TEXT:
                self.about_me()


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
        self.incall = InCall(self, self.number.get(1.0, tk.END))
        self.incall.mainloop()

    def recent(self):
        print('recent')    
   

if __name__ == '__main__':
    w = PhoneDialer()
    w.mainloop()        