from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import json
import sqlite3


class MyStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        style_configure = None
        with open('OrderUPstyle.txt', 'r') as j_load:
            style_configure = json.load(j_load)
        self.theme_create( "MyStyle", parent="alt", settings=style_configure)

class MenuMaker(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Menu Creation")
        self.resizable(False,False)
        self.geometry("+100+100")
        self.style = MyStyle()
        self.style.theme_use("MyStyle")
        self.style.configure('lefttab.TNotebook', tabposition='wn')

        self.f1 = CreationFrame(self)
        self.f1.pack(expand=True,fill="both",side="left")

        self.f2 = LabelFrame(self, text="Your Creation")
        self.f2.pack(expand=True,fill="both",side="left")

        self.c = Canvas(self.f2)
        self.c.configure(width=540, height=750)
        self.c.pack(expand=True,fill="both",side="left")
        self._frame(self.c)


    def _frame(self, destination):
        self.sf = ttk.Frame(self.c)
        self.n1 = MainNote(self.c)
        self.c.create_window((0,0),window=self.n1,anchor="nw", height=755)


class CreationFrame(LabelFrame):
    def __init__(self,root):
        LabelFrame.__init__(
            self,root,text="Enter your item name:")
        self.f = Frame(self, bg="Dark Green")
        self.f.grid(row=0,column=0)
        self.root = root

        self.defaults = {
            "id" : "Please Enter Item Name",
            'price' : '{:.2f}'.format(0.00),
            'descr' : "# Enter a description"
            }

        self.category = CatFrame(self.f)
        self.category.grid(row=2,column=0,rowspan=2,padx=5, sticky="E")

        self.price = Entry(
            self.f, width=10, font=("Cambria", 14),
            relief='sunken',justify = RIGHT, bg = "light blue",
            borderwidth = 2)
        self.price.insert("end", self.defaults['price'])
        self.price.grid(row=0, column=1, sticky= "E,W", pady=1, ipadx=2, padx=1)

        self.item_id = Entry(
            self.f, bg='Peach Puff',borderwidth=2)
        self.item_id.configure(font = ("Cambria", 14), relief='sunken')
        self.item_id.insert("end", self.defaults['id'])
        self.item_id.grid(row=0,column=0, sticky="E,W", pady=1, ipadx=2, padx=1)

        self.description = Text(
            self.f, width=50, height=5,relief='sunken',
            font=("Candara",12), wrap= "word", bg='honeydew',
            borderwidth=2)
        self.description.insert("end", self.defaults['descr'])
        self.description.grid(
            row=1,column=0, columnspan=2, pady=1,padx=1, sticky = "E, W")

        self.submit = Button(
            self.f, width = 25, text= 'Submit', command=self.j_create,
            bg = 'pale green', activebackground='green1')
        self.submit.grid(row=2,column=1, sticky="SE", ipady=2, pady=(2,1), padx=2)

        self.clear = Button(
            self.f, width = 25, text = 'Clear', command=self.clean,
            bg = 'pink1', activebackground = 'red'
        )
        self.clear.grid(row=3,column=1,sticky="SE", ipady=2, pady=(1,2),padx=2)

    def clean(self):
        self.item_id.delete('0', 'end')
        self.item_id.insert('end', self.defaults['id'])

        self.price.delete('0','end')
        self.price.insert('end', self.defaults['price'])

        self.description.delete('1.0','end')
        self.description.insert('end', self.defaults['descr'])

    def j_create(self):
        catg = self.category.sub.get()
        id = self.item_id.get()
        price = '{:.2f}'.format(float(self.price.get()))
        desc = self.description.get('1.0','end-1c').strip()
        if id != self.defaults['id'] and desc != self.defaults['descr']:
            with sqlite3.connect('OrderUP.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO item (item_name, item_price, sub_cat_id, description)
                    VALUES  (?, ?, ?, ?)''', (id,price,int(catg),desc))
                conn.commit()

        self.item_id.delete('0','end')
        self.item_id.insert("end", self.defaults['id'])

        self.price.delete("0","end")
        self.price.insert("end", self.defaults['price'])

        self.description.delete("1.0", "end")
        self.description.insert("end", self.defaults['descr'])

        self.root.c.delete()
        self.root._frame(self.root.c)

class CatFrame(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root
        self.main = IntVar()
        self.sub = StringVar()
        try:
            self.button_mode(root)
            self.create_radios('0')
        except sqlite3.Error as e:
            _err = messagebox.showerror("Database Error", "{}\nThere is no categories in database. Fix Note: ".format(e))

    def _update(self):
        self.f.destroy()
        main = str(self.main.get())
        self.create_radios(main)

    def button_mode(self,root):
        c = 0
        with sqlite3.connect('OrderUP.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM main_cat')
            for item in cursor:
                self.cat = Radiobutton(
                    self, padx= 10,text=item[1], width=15,
                    command=self._update,value=item[0],variable = self.main,
                    bg='light blue',activebackground='light blue',
                    indicatoron=0, selectcolor='blue1')
                self.cat.grid(row=0,column=c,sticky="E,W")

                self.cat.value = item[0]
                self.cat.font = Font(family = 'Cambria', size = 12, weight = 'bold')
                self.cat.configure(font =self.cat.font)
                c += 1

    def create_radios(self,index):
        self.f = Frame(self)
        self.f.grid(row=1,column=0,columnspan=2,sticky="E,W")
        c1 = 0
        with sqlite3.connect('OrderUp.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sub_cat WHERE main_cat_id=?',(index,))
            for item in cursor:
                self.subcat = Radiobutton(
                    self.f, variable=self.sub, text=item[1],value=item[0],indicatoron=0,
                    bg='lavender', activebackground='lavender', selectcolor='dark violet')
                self.subcat.pack(side="left", expand=True, fill="both")
                c1+=1

class MainNote(ttk.Notebook):
    def __init__(self,root):
        ttk.Notebook.__init__(self,root)
        self.root = root
        self.main_notes(root)

    def main_notes(self,root):
        conn = sqlite3.connect('OrderUp.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM main_cat')
        for item in cur:
            self.section = ttk.Notebook(root, style="lefttab.TNotebook")
            self.section.grid(row=0,column=0)
            self.add(self.section,text=item[1])
            self.sub_notes(item[0])

    def sub_notes(self,index):
        conn = sqlite3.connect('OrderUp.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM sub_cat WHERE main_cat_id=?', (index,))
        for item in cur:
            self.subsection = FoodPad(self.section,catg=item[0])
            self.section.add(self.subsection, text='\n'.join(list(item[1])))

class FoodPad(Frame):
    def __init__(self,root, catg=None):
        Frame.__init__(self,root)
        self.root = root
        self.catg = catg
        self.canvas = Canvas(self,bg='honeydew')
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=scroll.set, width=460, height=460)
        scroll.pack(side="right",fill="y")
        self.create_frame(self.canvas)

    def create_frame(self, destination):
        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.create_buttons(self.scroll_frame, self.catg)
        self.canvas.create_window((0,0),window=self.scroll_frame,anchor="nw")

    def create_buttons(self, destination,index):
        conn = sqlite3.connect('OrderUP.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM item WHERE sub_cat_id=?', (self.catg,))
        r = 0
        for item in cur:

            self.item = ItemPane(destination, item)
            self.item.grid(row=r,column=0,sticky="E,W")
            r+=1

class ItemPane(Frame):

    def __init__(self,root,data):
        Frame.__init__(self,root)
        self.font = Font(family='Georgia', size=12)
        self.data = data
        cmd = lambda x = root : self.printItemData(x)
        self.bind_class("ret_info", "<Double-1>", cmd)

        self.grid(sticky="E,W")
        self.configure(
            bg = 'honeydew',
            highlightthickness = 3,
            highlightbackground = "DarkGreen",
            highlightcolor = 'DarkGreen'
        )

        self.l1 = Label(self, text=data[0])
        self.l1.configure(
            font=self.font,
            bg = 'Peach Puff',
            borderwidth = 2,
            relief = 'groove'
        )
        self.l1.grid(row=0,column=0,sticky="NW,E",ipady=2)
        self.l1.bindtags("ret_info")

        self.l2 = Label(self, text='${}'.format(data[1]))
        self.l2.configure(
            font=self.font,
            bg = 'light blue',
            borderwidth = 2,
            relief = 'groove'
        )
        self.l2.grid(row=0,column=1,sticky="NE,W",ipady=2)
        self.l2.bindtags("ret_info")

    #This is the ['desc'] section
        self.t = Text(self,width=45,height=3)
        self.t.font = Font(family='Georgia', size=8)
        self.t.grid(row=1,column=0,columnspan=2,sticky="N,E,W,S")
        self.t.configure(
            font = self.font,
            wrap = 'word',
            bg = 'honeydew',
            bd = 2,
            relief = 'groove'
        )
        self.t.insert("end", data[3])
        self.t['state']="disabled"
        self.t.bindtags("ret_info")
        #print(data)
        #self.bind_all("<Double-1>", cmd)

    def printItemData(self, root):
        '''This finds which item called the event, then gets the data
        associated with it'''
        try:
            parent = root.widget.winfo_parent()
            item_info = self.nametowidget(parent).data #< Host frame
            display = messagebox.showinfo(item_info[0], item_info[:2])
        except AttributeError as e:
            print(e)
if __name__ == '__main__':

    root = MenuMaker()
    root.mainloop()

