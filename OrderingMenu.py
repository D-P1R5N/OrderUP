from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from copy import deepcopy
from datetime import datetime
import sqlite3
import json


class MyStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        style_configure = None
        with open('OrderUPstyle.txt', 'r') as j_load:
            style_configure = json.load(j_load)
        self.theme_create( "MyStyle", parent="alt", settings=style_configure)

class OrderMenu(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Order UP!")
        self.resizable(False,False)
        self.geometry("+500+300")
        self['bg'] = 'black'
        self.person = 0
        self.ticket = dict()

        self.style = MyStyle()
        self.style.theme_use("MyStyle")

        self.order = ActiveOrder(self)
        self.order.grid(row=0,column=2,rowspan=10, sticky="N,S")

        self.item = Item(self)
        self.item.grid(row=0, column=1, sticky="N,S")

        self.serv_opt = ServerOptions(self)
        self.serv_opt.grid(row=1,column=1, sticky="N,E,W,S")

        self.menu = MainNote(self)
        self.menu.grid(row=0, column=0, rowspan=10, sticky= "N,W")

    def _update(self, words):
        self.item.item.insert('end',(words['name'],"\t\t",words['price'],"\n"))

class ActiveOrder(Text):
    def __init__(self,root):
        Text.__init__(self,root)
        self.root = root
        self.configure(
            width= 50, height= 35, wrap="word", state='disabled',
            bg='honeydew', highlightthickness=3, highlightbackground= "DarkGreen",
            relief= 'sunken'
        )
        self.table = dict()

class Item(LabelFrame):
    def __init__(self,root):
        LabelFrame.__init__(
            self,root, text="Item", bg='orangered', width=100,height=100)
        self.root = root
        self.seat_item = dict()

        self.text = Text(
            self, width='25', height='8', bg='PapayaWhip', wrap='word')
        self.text.focus_set()
        self.text.grid(row=0,column=0,columnspan=10,pady=3)

        self.food_opt = Frame(self)
        self.food_opt.grid(row=1,column=0,columnspan=3, sticky="E,W")

        self.mod = Button(
            self.food_opt,text="++/--", command=self.modify_item,
            bg='coral', activebackground='coral2')
        self.mod.pack(side="left",expand=True,fill="both")

        self.request = Button(
            self.food_opt,text="Request",command = self.add_request,
            bg = 'light blue', activebackground = 'blue1')
        self.request.pack(side="left",expand=True,fill="both")

        self.alert = Button(
            self.food_opt,text="!!",command= self.add_alert,
            bg = 'red', activebackground = 'DarkRed')
        self.alert.pack(side="left",expand=True,fill="both")

        self.finish = Frame(self)
        self.finish.grid(row=2,column=0,columnspan=3)

        cmd1 = lambda root=self.root:  self.add_order(root)
        self.confirm = Button(
            self.finish,text="Confirm", width='20',command=cmd1,
            bg='honeydew', activebackground='DarkGreen')
        self.confirm.grid(row=2,column=0,ipady=3)

        self.cancel = Button(
            self.finish, text="X", width='10', command=self.clear,
            bg='pink1', activebackground='red')
        self.cancel.grid(row=2,column=1,ipady=3)
    def add_request(self):
        #Here is the request method. Uses ".."
        self._request = Special()
        pass

    def add_order(self, root):
        next = int(root.order.index('end-1c').split('.')[0])

        if self.text.get(1.0, 'end') != '\n':
            _data = deepcopy(self.seat_item)
            text = json.dumps(_data, indent=4)
            delimits = ['[',']','{','}',',']
            for _ in delimits:
                text = text.replace(_, '')

            root.order.configure(state="normal")
            root.order.insert(next+1.0, text)
            root.order.configure(state="disabled")

            try:
                root.order.table[root.person].append(_data)
            except:
                root.order.table[root.person] = [_data]

            self.seat_item.clear()
            self.text.delete(1.0, 'end')
            self.text.focus_set()

        else: pass


    def add_alert(self):
        #Here is the alert method for allergies. Uses "!!"
        self.allergies = Allergens()



    def clear(self):
        self.text.delete(1.0,'end')

    def modify_item(self):
        #++/--
        self.mods = AddOns()


class ServerOptions(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root

        self.add_guest = Button(
            self, text="Add Guest", width = 29, command=self.add_client,
            bg='PapayaWhip', activebackground='orangered')
        self.add_guest.pack(side="top",fill="both",expand=True)
        ##EDIT STILL NEEDS WORK
        self.edit_guest = Button(
            self, text="Edit Guest", width=29, command=None,
            bg='lavender', activebackground='purple1')
        self.edit_guest.pack(side="top",fill="both",expand=True)


        self.remove_guest = Button(
            self, text="Remove Guest", width=29, command=self.remove_client,
            bg='pink1', activebackground='red')
        self.remove_guest.pack(side="top", fill="both", expand=True)

        self.confirm = Button(
            self, text="Submit Order", width=29, command=self.send_ticket,
            bg='pale green', activebackground='green1')
        self.confirm.pack(side="top",fill="both",expand=True)

    def send_ticket(self):
        j_data = json.dumps(self._root().order.table)
        chron_time = datetime.now()
        _date = str(chron_time.date())
        _time = str(chron_time.time()).split('.')

        sql_statement = """INSERT INTO active_orders ( ticket_info, time, date)
            VALUES (?,?,?)"""
        with sqlite3.connect('OrderUP.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statement, (j_data,_time[0],_date))
        print(self._root().order.table)

        root = self._root()
        root.order.configure(state='normal')
        root.order.delete(1.0, 'end')
        root.order.configure(state = 'disabled')

    def add_client(self):
        root = self.root
        root.person += 1
        #This method adds a seat to the displayed ticket
        next = int(root.order.index('end-1c').split('.')[0])
        next_line=["\n","-"*20, "Seat #", str(root.person), "-"*20, "\n"]

        root.order.configure(state="normal")
        root.order.insert(next+1.0, ''.join(next_line), 'tag-center')
        root.order.configure(state="disabled")

        root.item.text.focus_set()

        self.add_guest['text']=''.join(["Seat #", str(root.person)])
        #print(''.join(next_line))

    def edit_client(self,root):
        #This is the section to select a seat and modify it further.
        pass


    def remove_client(self):
        root = self.root
        text = root.order.get(1.0,'end')
        text = [i for i in text.split("\n") if i != '']

        root.order.configure(state="normal")
        root.order.delete('end-1l','end')
        root.order.configure(state="disabled")
        if root.person == 1: pass
        else: root.person -= 1
        self.add_guest['text'] = ''.join(["Seat #", str(root.person)])

class MainNote(ttk.Notebook):
    def __init__(self,root):
        ttk.Notebook.__init__(self,root)
        self.root = root
        try:
            self.main_notes(root)
        except sqlite3.Error as e:
            _err = messagebox.showerror("Menu Error", "{}\nMenu does not exist.\nFix Note: ".format(e))

    def main_notes(self,root):
        with sqlite3.connect('OrderUp.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM main_cat')
            for item in cur:
                self.section = ttk.Notebook(root, style="lefttab.TNotebook")
                self.section.grid(row=0,column=0)
                self.add(self.section,text=item[1])
                self.sub_notes(item[0])

    def sub_notes(self,index):
        with sqlite3.connect('OrderUp.db') as conn:
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
            lambda x: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        try:
            self.create_buttons(self.scroll_frame, self.catg)
        except sqlite3.Error as e:
            _err = messagebox.showerror(
            "Menu Error",
            "{}\nMenu Error.\nFix Note:Run setup.py Database rebuild.".format(e))
        self.canvas.create_window((0,0),window=self.scroll_frame,anchor="nw")

    def create_buttons(self, destination,index):
        with sqlite3.connect('OrderUp.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM item WHERE sub_cat_id=?', (self.catg,))
            r = 0
            for item in cur:
                self.item = OrderItemPane(destination, item)
                self.item.grid(row=r,column=0,sticky="E,W")
                r+=1

class OrderItemPane(Frame):

    def __init__(self,root,data):
        Frame.__init__(self,root)
        self.font = Font(family='Georgia', size=12)
        self.data = data
        cmd = lambda x = root : self.add_item(x)
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

    def add_item(self, root):
        _r = self._root()
        try:
            parent = root.widget.winfo_parent()
            item_info = self.nametowidget(parent).data #< Host fram
            #item_info order is (item_name,price,sub_cat,desc)
            _r.item.text.insert('end', (item_info[0] + '\n'))
            _r.item.seat_item['ID'] = item_info[0]
            _r.item.seat_item['$$'] = item_info[1]


        except AttributeError as e:
            messagebox.showerror('Item Data Error', '/n'.join([e, "Delete item from database and recreate."]))
            #print(e)


class AddOns(Toplevel):
    def __init__ (self):
        Toplevel.__init__(self)
        self.extra = StringVar()
        self.extra.set('Bacon Lettuce Tomato Pickle')
        self.font = Font(family="Bahnschrift SemiLight SemiConde", size=14, weight="bold")

        self.lf = LabelFrame(self,text="Modifications", bg='orangered')
        self.lf.grid(row=0,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

        self.list = Listbox(
            self.lf, listvariable=self.extra,selectmode=MULTIPLE,
            bg='Peach Puff', selectbackground='honeydew', selectforeground='black')
        self.list.pack(expand=True,fill="x",side="top")
        self.list.configure(font=self.font)

        self.lf1 = LabelFrame(self, text="Review Your Choices:",bg='orangered')
        self.lf1.grid(row=1,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

        self.add = Button(
            self.lf1, command=self.add_mods, text="++", bg='pale green')
        self.add.pack(expand=True, fill="both",ipady=5)

        self.remove = Button(
            self.lf1, command=self.rem_mods, text="--", bg='pink1')
        self.remove.pack(expand=True, fill="both",ipady=5)

    def add_mods(self):
        _r = self._root()
        selection = self.list.curselection()
        mods = [str(self.list.get(idx)) for idx in selection]

        _r.item.seat_item['++'] = mods
        for mod in mods:
            _r.item.text.insert('end',''.join(["++", mod, "\n"]))
        self.destroy()

    def rem_mods(self):
        selection = self.list.curselection()
        mods = [str(self.list.get(idx)) for idx in selection]

        self._root().item.seat_item['--'] = mods
        for mod in mods:
            self.nametowidget(".").item.text.insert('end',''.join(["--", mod, "\n"]))
        self.destroy()

class Allergens(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.font = Font(family="Bahnschrift SemiLight SemiConde", size=14, weight="bold")

        self.lf = LabelFrame(self,text="Guest is allergic to:", bg='orangered')
        self.lf.grid(row=0,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

        self.allergen = StringVar()
        self.allergen.set('Soy Seeds Nuts Dairy Eggs Other')

        self.a_list=Listbox(
            self.lf, listvariable=self.allergen,selectmode=MULTIPLE,
            bg='light blue', selectbackground='pink1', selectforeground='black')
        self.a_list.configure(font=self.font, exportselection=False, activestyle='dotbox')
        self.a_list.pack(side="top", expand=True,fill="both")
        self.a_list.bind('<<ListboxSelect>>', self.toggle)

        self.other = StringVar()
        self.other.set("Other...")

        self.specify = Entry(self.lf, textvariable=self.other)
        self.specify.pack(side="top", expand=True, fill="both", pady=5, padx=5)
        self.specify['state'] = "disabled"

        self.submit = Button(self.lf, text="Submit", bg="pale green",command=self.r_allergen)
        self.submit.pack(side="top", expand=True,fill="both",padx=4, pady=(0,5))
        self.submit.bind('<1>', self.a_list.unbind('<1>'))

    def r_allergen(self):
        root = self._root()
        #gather and sterilize selection
        sel = self.a_list.curselection()
        alrg = [str(self.a_list.get(idx)) if self.a_list.get(idx) != "Other" else self.other.get() for idx in sel]

        root.item.seat_item['!!'] = alrg

        for a in alrg:
            self._root().item.text.insert('end', ('!!' + a +'\n'))

        self.destroy()


    def toggle(self, root):
    #this toggles the "Other..." Entry field
        bool = self.a_list.curselection()
        if 5 in bool:
            self.specify['state'] = "normal"
        else: self.specify['state'] = 'disabled'

class Special(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.lf = LabelFrame(self, text="Guest has a special request:", bg="orangered")
        self.lf.grid(row=0,column=0,sticky="N,E,W,S",ipady=10,ipadx=5)

        self.t = Text(self.lf,width=51,height=5,wrap="word")
        self.t.insert('end', "This is a special request...")
        self.t.pack(side="top", expand=True,fill="both")

        self._frame = Frame(self, bg="orangered")
        self._frame.grid(row=1,column=0, sticky="N,E,S,W", ipadx=5)

        self._submit = Button(
            self._frame, width=25, text = "Submit", command=self.submit_text,
            bg = 'pale green', activebackground='green1')
        self._submit.grid(row=0,column=0, sticky="N,S,W", ipady=2, padx=2)

        self._cancel = Button(
            self._frame, width=15, text = 'X', command=self.destroy,
            bg = 'pink1', activebackground = 'red')
        self._cancel.grid(row=0,column=1, sticky="N,E,S", ipady=2, padx=2)

    def submit_text(self):
        text = self.t.get(1.0, 'end')
        self._root().item.seat_item['..'] = text
        self._root().item.text.insert('end', text)

        self.destroy()


if __name__ == "__main__":

    menu = OrderMenu()
    menu.mainloop()
