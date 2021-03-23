import tkinter as tk

# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(tk.Frame):
    def __init__(self, parent, bg='white'):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background=bg)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background=bg)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.


# ********************************
# Example usage of the above class
# ********************************

class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)


        self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
        
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        for row in range(100):
            a = row
            tk.Label(self.scrollFrame.viewPort, text="%s" % row, width=3, borderwidth="1", 
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Button(self.scrollFrame.viewPort, text=t, command=lambda x=a: self.printMsg("Hello " + str(x))).grid(row=row, column=1)

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
    

    def printMsg(self, msg):
        print(msg)

if __name__ == "__main__":
    root=tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()




from tkinter import *

class Planificador(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Plan")
        self.frameOne = Frame(self.master)
        self.frameOne.grid(row=0,column=0)

        self.frameTwo = Frame(self.master)
        self.frameTwo.grid(row=1, column=0)

        #Creating of a new frame, inside of "frameTwo" to the objects to be inserted
        #Creating a scrollbar

        #The reason for this, is to attach the scrollbar to "FrameTwo", and when the size of frame "ListFrame" exceed the size of frameTwo, the scrollbar acts
        self.canvas=Canvas(self.frameTwo)
        self.listFrame=Frame(self.canvas)
        self.scrollb=Scrollbar(self.master, orient="vertical",command=self.canvas.yview)
        self.scrollb.grid(row=1, column=1, sticky='nsew')  #grid scrollbar in master, but
        self.canvas['yscrollcommand'] = self.scrollb.set   #attach scrollbar to frameTwo

        self.canvas.create_window((0,0),window=self.listFrame,anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        self.scrollb.grid_forget()                         #Forget scrollbar because the number of pieces remains undefined by the user. But this not destroy it. It will be "remembered" later.

        self.canvas.pack(side="left")
        self.frameThree = Frame(self.master)
        self.frameThree.grid(row=2, column=0)

        # Borrar esto?
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.piezastext = Label(self.frameOne, text = " Amount of pieces ", justify="center")
        self.piezastext.grid(row=1, column=0)
        self.entrypiezas = Entry(self.frameOne,width=3)
        self.entrypiezas.grid(row=2, column=0, pady=(5,5))
        self.aceptarnumpiezas = Button(self.frameOne,text="Click me", command=self.aceptar_piezas,width=8)
        self.aceptarnumpiezas.grid(row=6, column=0, pady=(5,5))

    def AuxscrollFunction(self,event):
        #You need to set a max size for frameTwo. Otherwise, it will grow as needed, and scrollbar do not act
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=600,height=500)

    def aceptar_piezas(self):



        #IMPORTANT!!! All the objects are now created in "ListFrame" and not in "frameTwo"
        #I perform the alterations. Check it out
        try:
            val = int(self.entrypiezas.get())
            self.aceptar_piezas_ok()
            self.scrollb.grid(row=1, column=1, sticky='nsew')  #grid scrollbar in master, because user had defined the numer of pieces
        except ValueError:
            'showerror(Error, "Introduce un numero")'

    def aceptar_piezas_ok(self):
        self.num_piezas = self.entrypiezas.get()

        self.piezastext.grid_remove()
        self.entrypiezas.grid_remove()
        self.aceptarnumpiezas.grid_remove()

        self.optionmenus_piezas = list()
        self.numpiezas = []
        self.numerolotes = []
        self.optionmenus_prioridad = list()
        self.lotes = list()

        self.mispiezas = ['One', 'Two', 'Three', 'Four', 'Five']

        self.n = 1
        while self.n <= int(self.num_piezas):
            self.textopieza = Label(self.listFrame, text = "Pieza: ", justify="left")
            self.textopieza.grid(row=self.n, column=0)

            var = StringVar()
            menu = OptionMenu(self.listFrame, var, *self.mispiezas)
            menu.config(width=10)
            menu.grid(row=self.n, column=1)
            var.set("One")
            self.optionmenus_piezas.append((menu, var))

            self.numpiezastext = Label(self.listFrame, text = "Numero de piezas: ", justify="center")
            self.numpiezastext.grid(row=self.n, column=2, padx=(10,0))
            self.entrynumpiezas = Entry(self.listFrame,width=6)
            self.entrynumpiezas.grid(row=self.n, column=3, padx=(0,10))
            self.entrynumpiezas.insert(0, "0")

            self.textoprioridad = Label(self.listFrame, text = "Prioridad: ", justify="center")
            self.textoprioridad.grid(row=self.n, column=4)
            var2 = StringVar()
            menu2 = OptionMenu(self.listFrame, var2, "Normal", "Baja", "Primera pieza", "Esta semana")
            menu2.config(width=10)
            menu2.grid(row=self.n, column=5)
            var2.set("Normal")
            self.optionmenus_prioridad.append((menu2, var2))

            self.lotestext = Label(self.listFrame, text = "Por lotes?", justify="center")
            self.lotestext.grid(row=self.n, column=6, padx=(10,0))
            self.var1 = IntVar()
            self.entrynumlotes = Checkbutton(self.listFrame, variable=self.var1)
            self.entrynumlotes.grid(row=self.n, column=7, padx=(5,10))
            self.lotes.append(self.var1)
            self.numpiezas.append(self.entrynumpiezas)

            self.n += 1

        self.anadirpiezas = Button(self.frameThree, text="Add row", command=self.addpieza, width=10)
        self.anadirpiezas.grid(row=0, column=2, pady=(10,10))

        self.calculotext = Label(self.frameThree, text = "Other stuff ")
        self.calculotext.grid(row=1, column=2, padx=(10,0), pady=(10,10))

        self.graspbutton = Button(self.frameThree, text="OPT 1", width=10)
        self.graspbutton.grid(row=2, column=1)

        self.parettobutton = Button(self.frameThree, text="OPT 2",width=10)
        self.parettobutton.grid(row=2, column=2, pady=(10,10), padx=(10,0))

        self.parettoEvolbutton = Button(self.frameThree, text="OPT 2", width=10)
        self.parettoEvolbutton.grid(row=2, column=3, pady=(10,10), padx=(10,0))


    def addpieza(self):
            self.textopiezanuevo = Label(self.listFrame, text = "Pieza: ", justify="left")
            self.textopiezanuevo.grid(row=int(self.num_piezas)+1, column=0)

            var = StringVar()
            menu = OptionMenu(self.listFrame, var, *self.mispiezas)
            menu.grid(row=self.n, column=1)
            menu.config(width=10)
            menu.grid(row=int(self.num_piezas)+1, column=1)
            var.set("One")
            self.optionmenus_piezas.append((menu, var))

            self.numpiezastext = Label(self.listFrame, text = "Numero de piezas: ", justify="center")
            self.numpiezastext.grid(row=int(self.num_piezas)+1, column=2, padx=(10,0))
            self.entrynumpiezas = Entry(self.listFrame,width=6)
            self.entrynumpiezas.grid(row=int(self.num_piezas)+1, column=3, padx=(0,10))
            self.entrynumpiezas.insert(0, "0")

            self.textoprioridad = Label(self.listFrame, text = "Prioridad: ", justify="center")
            self.textoprioridad.grid(row=int(self.num_piezas)+1, column=4)
            var2 = StringVar()
            menu2 = OptionMenu(self.listFrame, var2, "Normal", "Baja", "Primera pieza", "Esta semana")
            menu2.config(width=10)
            menu2.grid(row=int(self.num_piezas)+1, column=5)
            var2.set("Normal")
            self.optionmenus_prioridad.append((menu2, var2))

            self.lotestext = Label(self.listFrame, text = "Por lotes?", justify="center")
            self.lotestext.grid(row=int(self.num_piezas)+1, column=6, padx=(10,0))
            self.var1 = IntVar()
            self.entrynumlotes = Checkbutton(self.listFrame, variable=self.var1)
            self.entrynumlotes.grid(row=int(self.num_piezas)+1, column=7, padx=(5,10))
            self.lotes.append(self.var1)

            self.numpiezas.append(self.entrynumpiezas)
            self.num_piezas = int(self.num_piezas)+1

if __name__ == "__main__":
    root = Tk()
    aplicacion = Planificador(root)
    root.mainloop()    