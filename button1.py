from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import json
import copy


class FoodPad(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root
        canvas = Canvas(self)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.pack(side="left", fill="x", expand=True)
        canvas.create_window((0,0),window=self.scroll_frame,anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y")

        self.create_buttons(self.scroll_frame)
        #self.grid_propagate(0)

    def hello(self, root):
        #Pathway to Widget
        try:
            _ = self.widget.winfo_parent()
            print(_)
            print(root.nametowidget(_).data) #< Host frame

        except AttributeError:
            pass
        #print(self)
    def create_buttons(self, destination):
        r = 0
        with open('menu.json','r') as reader:
            data = [json.loads(line) for line in reader]
            #self.data = data[:]
        for _i,_d in enumerate(data):
            self.f = self.ItemPane(destination, _d)
            self.f.grid(row=r,column=0,sticky="E,W")
            r +=1
    class ItemPane(Frame):
        def __init__(self,root,data):
            Frame.__init__(self,root)
            #self['width'] = root.winfo_width()
            self.grid(sticky="E,W")
            self.data = data
            self['bg']= 'honeydew'
            self['highlightthickness'] = 3
            self['highlightbackground'] = 'DarkGreen'
            self.font = Font(family='Georgia', size=12)

            self.l1 = Label(self, text=data['name'])
            self.l1.configure(
                font=self.font,
                bg = 'Peach Puff',
                borderwidth = 2,
                relief = 'groove'
                )
            self.l1.grid(row=0,column=0,sticky="NW,E",ipady=2)
            self.l2 = Label(self, text=data['price'])
            self.l2.configure(
                font=self.font,
                bg = 'light blue',
                borderwidth = 2,
                relief = 'groove'
                )
            self.l2.grid(row=0,column=1,sticky="NE,W",ipady=2)

        #This is the ['desc'] section
            self.t = Text(self,width=45,height=3)
            self.t.font = Font(family='Georgia', size=8)
            self.t.grid(row=1,column=0,columnspan=2,sticky="N,E,W,S",padx=(0,0),pady=(0,0))
            self.t.configure(
                font = self.font,
                wrap = 'word',
                bg = 'honeydew',
                bd = 2,
                relief = 'groove'
                )
            self.t.insert("end", data['desc'])
            self.t['state']="disabled"

            #print(data)
            cmd = lambda self, x = root : FoodPad.hello(self, x)
            self.bind_all("<Double-1>", cmd)





root = Tk()


frame = FoodPad(root)
frame.pack(fill="x", expand=True)

root.mainloop()
