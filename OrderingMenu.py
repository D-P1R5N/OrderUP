import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from copy import deepcopy
from datetime import datetime
import sqlite3
import json

settings = {
"TNotebook":{
    "configure":{
        "background": "black",
        "tabmargins": [2, 5, 2, 0]}},
"TNotebook.Tab":{
    "configure":{
        "background":"light blue",
        "padding": [50, 10],
        "font": "Bahnschrift"},
    "map": {
        "highlightthickness": [["selected", 3]],
        "highlightcolor": [["selected", "blue1"]],
        "background": [["selected", "blue1"]],
        "expand": [["selected", [2, 2, 2, 0]]]}},
"mainsect.TNotebook":{
    "configure":{
        "bordercolor": "CornSilk2",
        "borderwidth": 0}},
"lefttab.TNotebook": {
    "configure": {
        "tabposition": "wn"}},
"lefttab.TNotebook.Tab": {
    "configure":{
        "background": "lavender",
        "padding": [10, 10, 0, 10],
        "width": 5,
        "height": 5,
        "font": "Bahnschrift"},
    "map": {
            "highlightthickness": [["selected", 3]],
            "highlightcolor": [["selected", "dark violet"]],
            "background": [["selected", "dark violet"]],
            "expand": [["selected", [2, 0, 2, 0]]]}},
"mystyle.Treeview":{
    "configure":{
        "highlightthickness":0,
        "bd":0,
        "font":('Calibri', 11)
    }
},
"mystyle.Treeview.Heading":{
    "configure":{
        "font":('Calibri', 13,'bold')
    }
}}


class MyStyle(ttk.Style):
    global settings
    def __init__(self):
        ttk.Style.__init__(self)
        style_configure = None
        with open('OrderUPstyle.txt', 'r') as j_load:
            style_configure = json.load(j_load)
        self.theme_create( "MyStyle", parent="clam", settings=settings)

class OrderMenu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Order UP!")
        self.resizable(False,False)
        self.geometry("+500+300")
        self['bg'] = 'black'
        self.person = 0
        self.ticket = dict()

        self.style = MyStyle()
        self.style.theme_use("MyStyle")

        #self.order = ActiveOrder(self)
        self.order = GuestNote(self)
        #self.order.grid(row=0,column=2,rowspan=10, sticky="N,S,E,W")
        self.order.pack(side="right",expand=True,fill='both', anchor='e')

        self.serv_opt = ServerOptions(self)
        #self.serv_opt.grid(row=1,column=1, sticky="N,E,W,S")
        self.serv_opt.pack(fill='both', expand=True, anchor='c')

        self.menu = MainNote(self)
        #self.menu.grid(row=0, column=0, rowspan=10, sticky= "N,W")
        self.menu.pack(side='left',fill='both',expand=True,anchor='w')
    def _update(self, words):
        self.item.item.insert('end',(words['name'],"\t\t",words['price'],"\n"))

class ServerOptions(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.root = root
        self.edit_mode = False
        self.guest = 1

        self.add_guest = tk.Button(
            self, text="Add\nGuest", command=self.add_client,
            bg='PapayaWhip', activebackground='orangered')
        self.add_guest.pack(side="left",fill="both",expand=True,ipady=10)
        self.add_guest.bind('<ButtonRelease-1>', self.clientOrdertoBook)

        ##EDIT STILL NEEDS WORK
        self.edit_guest = tk.Button(
            self, text="Edit\nGuest", command=self.edit_client,
            bg='lavender', activebackground='purple1')
        self.edit_guest.pack(side="left",fill="both",expand=True,ipady=10)


        self.remove_guest = tk.Button(
            self, text="Remove\nGuest", command=self.remove_client,
            bg='pink1', activebackground='red')
        self.remove_guest.pack(side="left", fill="both", expand=True,ipady=10)

        self.confirm = tk.Button(
            self, text="Submit\nOrder", command=self.send_ticket,
            bg='pale green', activebackground='green1')
        self.confirm.pack(side="left",fill="both",expand=True,ipady=10)
        self.add_client()

    def send_ticket(self):

        chron_time = datetime.now()
        _date = str(chron_time.date())
        _time = str(chron_time.time()).split('.')
        #cycle through the guests and update the ticket info with any items added to them
        for i,v in enumerate(self._root().order.tabs()):
            self._root().ticket[i+1] = self._root().order.nametowidget(v).guest_order

        j_data = json.dumps(self._root().ticket)

        sql_statement = """INSERT INTO active_orders ( ticket_info, time, date)
            VALUES (?,?,?)"""

        with sqlite3.connect('OrderUP.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statement, (j_data,_time[0],_date))

        self._root().ticket.clear()
        print(self._root().ticket)

    def clientOrdertoBook(self,event):
        w_id = self.root.order.select()
        w_val = self.root.order.nametowidget(w_id)
        #self.root.ticket[self.guest] = w_val.guest_order
        #print(w_val.guest_order)

    def add_client(self):
        try:
            self.root.order.select(self.root.order.index('end')-1)
        except:
            pass
        #check if guest has item
        if self.root.order.select():
            if not self.root.order.nametowidget(self.root.order.select()).guest_order:
                return
            else: pass

        #add sections to GuestNote
        client = GuestOrder(self.root.order)
        self.root.order.add(client, text=str(self.guest))

        #automatically cycle to next created tab
        if self.guest > 1:
            self.root.order.select([self.root.order.index('end')-1])
        self.guest += 1

    def edit_client(self):
        w_id = self.root.order.select()
        w_val = self.root.order.nametowidget(w_id)

        if self.edit_mode:
            self.edit_guest.configure(relief='raised', bg='lavender')
            self.add_guest.configure(state='normal')
            self.remove_guest.configure(state='normal')
            self.confirm.configure(state='normal')
            self.edit_mode = False

            for child in w_val.winfo_children():
                for g_child in child.winfo_children():
                    g = self._root().nametowidget(g_child)
                    g.deleteButton.pack_forget()

        else:
            self.edit_guest.configure(relief='sunken', bg='purple1')
            self.add_guest.configure(state='disabled')
            self.remove_guest.configure(state='disabled')
            self.confirm.configure(state='disabled')
            self.edit_mode = True



            for child in w_val.winfo_children():
                for g_child in child.winfo_children():
                    g = self._root().nametowidget(g_child)
                    g.deleteButton.pack(ipadx=5)

    def remove_client(self):
        t_indx = self.root.order.index('current')
        #self.root.order.hide('current')
        self.root.order.forget(t_indx)
        self.guest = t_indx + 1

        for i in self.root.order.tabs()[t_indx:]:
            self.root.order.tab(i, text=self.guest)
            self.guest += 1

class MainNote(ttk.Notebook):
    def __init__(self,root):
        ttk.Notebook.__init__(self,root, style='mainsect.TNotebook')
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
                self.section.pack()
                self.add(self.section,text=item[1])
                self.sub_notes(item[0])

    def sub_notes(self,index):
        with sqlite3.connect('OrderUp.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM sub_cat WHERE main_cat_id=?', (index,))
            for item in cur:
                self.subsection = FoodPad(self.section,catg=item[0])
                self.section.add(self.subsection, text='\n'.join(list(item[1])))

class GuestNote(ttk.Notebook):
    def __init__(self,root):
        ttk.Notebook.__init__(self,root, style='lefttab.TNotebook')
        self.root = root

class GuestOrder(ttk.Notebook):
    def __init__(self,root,guest=1):
        ttk.Notebook.__init__(self,root)
        self.guest_order = []
        self.root = root
        self.guest = guest
        self.food = ttk.Notebook(self, style="lefttab.TNotebook")
        self.food.pack()
        self.add(self.food, text="Food")

        self.drink = ttk.Notebook(self,style="lefttab.TNotebook")
        self.drink.pack()
        self.add(self.drink, text="Drink")

class FoodPad(tk.Frame):
    def __init__(self,root, catg=None):
        tk.Frame.__init__(self,root)
        self.root = root
        self.catg = catg
        self.canvas = tk.Canvas(self,bg='honeydew')
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

class GuestPad(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.root = root
        self.canvas = tk.Canvas(self, bg='honeydew')
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.pack(side="left", fill="both", expand=False)
        self.canvas.configure(yscrollcommand=self.scroll.set, width=460, height=460)
        self.scroll.pack(side="right", fill="y")
        self.create_frame()

    def create_frame(self):
        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda x: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.scroll_frame.pack(side="top", fill="x",expand=False)

class GuestItemPane(tk.Frame):
    def __init__(self,root,data):
        tk.Frame.__init__(self,root)
        self.font = font.Font(family='Georgia', size=12)
        self.data = data
        self.tree_height = 1

        self.configure(
            bg = 'purple1',
            highlightthickness = 3,
            highlightbackground = "DarkGreen",
            highlightcolor = 'DarkGreen'
        )
        self.info_tree = ttk.Treeview(self,height=self.tree_height, style="mystyle.Treeview")
        self.info_tree.pack(side='left',fill='both',expand=True,anchor='w')
        self.info_tree.heading('#0', text = 'Item Modifications')
        self.info_tree.pack(side="bottom", fill="x", expand=True)
        self.info_tree.bind('<ButtonRelease-1>', self.readjust_treeview)

        self.deleteButton = tk.Button(self, text = 'X', command=self.removeItem)
        self.deleteButton.pack(anchor="n", ipadx=5)
        self.update_info()
        if not self._root().serv_opt.edit_mode:
            self.deleteButton.pack_forget()
        else: pass

    def readjust_treeview(self, event):
        self.tree_height = len(self.info_tree.get_children()) + 1
        for _i in self.info_tree.get_children():
            item = self.info_tree.item(_i)
            sub_items = self.info_tree.get_children(_i)

            if item['open']:
                self.tree_height += len(sub_items)

            else:
                pass

        self.info_tree.configure(height=self.tree_height)

    def removeItem(self):
        #The grandfather widget contains the order data
        parent = self.winfo_parent()
        w_g_parent = self._root().nametowidget(parent).winfo_parent()
        g_parent = self._root().nametowidget(w_g_parent)

        g_parent.guest_order.remove(self.data)
        self.destroy()

    def update_info(self):
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(side="bottom", fill="x", expand=True)


        for i,mods in self.data.items():
            if i == 'ID':
                #self.tree_height += 1
                self.title = ttk.Label(self.title_frame, text= mods, background='Peach Puff')
                self.title.pack(side="left", anchor="w", fill="x", expand=True,ipadx=10)
            elif i == '$$':
                self.value = tk.StringVar()
                self.value.set(mods)
                self.price = ttk.Label(self.title_frame, textvariable=self.value, background='light blue')
                self.price.pack(side="right", anchor="e", fill="x", expand=True)
            elif i == '++':
                self.tree_height+=len(mods) + 1
                try:
                    for mod in mods:
                        self.info_tree.insert('adds', 'end', text=mod, tags = 'add_on')

                except:
                    self.info_tree.insert('', 'end', 'adds', text='++', tags = 'header')
                    self.info_tree.item('adds', open=True)

                    for mod in mods:
                        self.info_tree.insert('adds','end', mod, text=mod)
                        self.info_tree.item(mod, tags='add_on')

                self.info_tree.tag_configure('add_on', background='pale green')

            elif i == '--':
                self.tree_height+=len(mods) + 1
                try:
                    for mod in mods:
                        self.info_tree.insert('rems', 'end', text=mod, tags='rem_op')


                except:
                    self.info_tree.insert('', 'end', 'rems', text='--', tags= 'header')
                    self.info_tree.item('rems', open=True)

                    for mod in mods:
                        self.info_tree.insert('rems', 'end', text=mod, tags='rem_op')
                self.info_tree.tag_configure('rem_op', background='pink')

            elif i == '!!':
                self.tree_height+=len(mods) + 1
                try:
                    for mod in mods:
                        self.info_tree.insert('alrg', 'end', text=mod, tags='allrgy')

                except:
                    self.info_tree.insert('','end','alrg',text='!!', tags='header')
                    self.info_tree.item('alrg', open=True)


                    for mod in mods:
                        self.info_tree.insert('alrg', 'end', text=mod, tags='allrgy')
                self.info_tree.tag_configure('allrgy', background='red')

            elif i == '..':
                self.tree_height+=len(mods) + 1
                try:
                    for mod in mods:
                        self.info_tree.insert('descr', 'end', text=mod, tags='descr')
                except:
                    self.info_tree.insert('','end','descr', text='..', tags='header')
                    self.info_tree.item('descr', open=True)

                    for mod in mods:
                        self.info_tree.insert('descr', 'end', text=mod, tags='descr')
                self.info_tree.tag_configure('descr', background='SkyBlue1')
            print(self.tree_height)
            self.info_tree.configure(height=self.tree_height)
            self.info_tree.tag_configure('header', background='PapayaWhip')

class OrderItemPane(tk.Frame):

    def __init__(self,root,data):
        tk.Frame.__init__(self,root)
        self.font = font.Font(family='Georgia', size=12)
        self.data = data
        cmd = lambda x = root : self.add_item(x)
        self.bind_class("ret_info", "<Double-1>", cmd)

        self.configure(
            bg = 'honeydew',
            highlightthickness = 3,
            highlightbackground = "DarkGreen",
            highlightcolor = 'DarkGreen'
        )
        try:
            self.l1 = tk.Label(self, text=data[0])
        except:
            self.l1 = tk.Label(self, text=data['ID'])
        self.l1.configure(
            font=self.font,
            bg = 'Peach Puff',
            borderwidth = 2,
            relief = 'groove'
        )
        self.l1.grid(row=0,column=0,sticky="NW,E",ipady=2)
        self.l1.bindtags("ret_info")
        try:
            self.l2 = tk.Label(self, text='${}'.format(data[1]))
        except:
            self.l2 = tk.Label(self, text='${}'.format(data['$$']))
        self.l2.configure(
            font=self.font,
            bg = 'light blue',
            borderwidth = 2,
            relief = 'groove'
        )
        self.l2.grid(row=0,column=1,sticky="NE,W",ipady=2)
        self.l2.bindtags("ret_info")

        #This is the ['desc'] section
        self.t = tk.Text(self,width=45,height=3)
        self.t.font = font.Font(family='Georgia', size=8)
        self.t.grid(row=1,column=0,columnspan=2,sticky="N,E,W,S")
        self.t.configure(
            font = self.font,
            wrap = 'word',
            bg = 'honeydew',
            bd = 2,
            relief = 'groove'
        )
        try:
            self.t.insert("end", data[3])
            self.t['state']="disabled"
            self.t.bindtags("ret_info")
        except: pass

    def add_item(self, root):
        #this is the TOPLEVEL maker!!
        parent = root.widget.winfo_parent()
        item_info = self.nametowidget(parent).data
        print(item_info)
        try:
            self._item = ItemBuild(self, text=item_info[0], value=item_info[1])
        except:
            self._item = ItemBuild(self, text=item_info['ID'], value=item_info['$$'])

class ItemBuild(tk.Toplevel):
    def __init__(self,root, text='This is a Test Item',value=None):
        super().__init__(root, takefocus=True)
        self.geometry('400x200+300+300')
        self.transient(root)
        self.item_data = dict()
        self.item_data['ID'] = text
        self.item_data['$$'] = value
        self.root = root

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])


        self.id = ttk.Label(self, text = text, anchor=tk.CENTER, font=('Calibri', 20, 'bold'))
        self.id.pack( fill='both', expand=True, anchor='nw')

        self.opt_frame = ttk.Frame(self)
        self.opt_frame.pack(side='left', fill='both', expand=True, anchor='w')

        self.info_tree = ttk.Treeview(self, style="mystyle.Treeview")
        self.info_tree.pack(side='left',fill='both',expand=True,anchor='w')
        self.info_tree.heading('#0', text = 'Item Modifications')

        self.modifications = tk.Button(
            self.opt_frame, text='++ / --', command=self.modify_item)
        self.modifications.pack(side='top', expand=True, fill='both',anchor='n')

        self.alerts = tk.Button(
            self.opt_frame, text = ' !! ', command=self.add_alert)
        self.alerts.pack(expand=True, fill='both')

        self.misc = tk.Button(
            self.opt_frame, text = ' .. ', command=self.misc_info)
        self.misc.pack(side="bottom", expand=True, fill="both", anchor='s')

        self.sub_frame = ttk.Frame(self)
        self.sub_frame.pack(side='right', fill='both', expand=True, anchor='e')
        self.confirm = tk.Button(
            self.sub_frame, text = 'OK', command=self.submit_item)
        self.confirm.pack(side="top", expand=True, fill='both', anchor='n', ipady=50)

        self.cancel = tk.Button(
            self.sub_frame, text = 'X', command=self.cancel_item)
        self.cancel.pack(side='bottom', expand=True, fill='both', anchor='s', ipady=10)

    def add_alert(self):
        self.allergies = self.Allergens(self)

    def modify_item(self):
        #++/--
        self.mods = self.AddOns(self)

    def misc_info(self):
        self._request = self.Special(self)

    def submit_item(self):
        _data = self.item_data
        #gather the tkName for the selected Guest tab
        tName = self._root().order.select()

        if tName:
            t_idx = self._root().order.index('current')
            #Get the current notebook frame [food/drink] for the selected guest [1/2/3...]
            sub_t_idx = self._root().order.nametowidget(tName).select()
            self._root().order.nametowidget(tName).guest_order.append(deepcopy(_data))
            item = GuestItemPane(self._root().order.nametowidget(sub_t_idx), _data)
            item.pack(side="top", fill="x", expand=False, anchor='n')
        print(_data)

        print(self._root().order.nametowidget(tName).guest_order)

        self._root().order.index('current')

        self.destroy()


    def cancel_item(self):
        self.destroy()

    class AddOns(tk.Toplevel):
        def __init__ (self, root):
            super().__init__(root)
            self.extra = tk.StringVar()
            self.extra.set('Bacon Lettuce Tomato Pickle')
            self.font = font.Font(family="Bahnschrift SemiLight SemiConde", size=14, weight="bold")

            self.lf = tk.LabelFrame(self,text="Modifications", bg='orangered')
            #self.lf.grid(row=0,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)
            self.lf.pack(expand=True,fill='both',anchor='nw', ipadx=5,ipady=10)
            self.list = tk.Listbox(
                self.lf, listvariable=self.extra,selectmode=tk.MULTIPLE,
                bg='Peach Puff', selectbackground='honeydew', selectforeground='black')
            self.list.pack(expand=True,fill="x",side="top")
            self.list.configure(font=self.font)

            self.lf1 = tk.LabelFrame(self, text="Review Your Choices:",bg='orangered')
            #self.lf1.grid(row=1,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)
            self.lf1.pack(anchor="w", expand=True, fill='both', ipady=10, ipadx=5)
            self.add = tk.Button(
                self.lf1, command=self.add_mods, text="++", bg='pale green')
            self.add.pack(expand=True, fill="both",ipady=5)

            self.remove = tk.Button(
                self.lf1, command=self.rem_mods, text="--", bg='pink1')
            self.remove.pack(expand=True, fill="both",ipady=5)

        def add_mods(self):
            selection = self.list.curselection()
            mods = [str(self.list.get(idx)) for idx in selection]

            item = self.master.item_data

            try:
                item['++'].extend(mods)

                for mod in mods:
                    self.master.info_tree.insert('adds', 'end', text=mod, tags = 'add_on')

            except KeyError:
                item['++'] = mods
                self.master.info_tree.insert('', 'end', 'adds', text='++')
                self.master.info_tree.item('adds', open=True)

                for mod in mods:
                    self.master.info_tree.insert('adds','end', mod, text=mod)
                    self.master.info_tree.item(mod, tags='add_on')

            self.master.info_tree.tag_configure('add_on', background='pale green')

            #print(item)

            self.destroy()

        def rem_mods(self):
            selection = self.list.curselection()
            mods = [str(self.list.get(idx)) for idx in selection]

            item = self.master.item_data
            try:
                item['--'].extend(mods)

                for mod in mods:
                    self.master.info_tree.insert('rems', 'end', text=mod, tags='rem_op')

            except KeyError:
                item['--'] = mods
                self.master.info_tree.insert('', 'end', 'rems', text='--')
                self.master.info_tree.item('rems', open=True)

                for mod in mods:
                    self.master.info_tree.insert('rems', 'end', text=mod, tags='rem_op')
            self.master.info_tree.tag_configure('rem_op', background='pink')

            #print(item)

            self.destroy()

    class Allergens(tk.Toplevel):
        def __init__(self,root):
            super().__init__(root)

            self.font = font.Font(family="Bahnschrift SemiLight SemiConde", size=14, weight="bold")

            self.lf = tk.LabelFrame(self,text="Guest is allergic to:", bg='orangered')
            self.lf.grid(row=0,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

            self.allergen = tk.StringVar()
            self.allergen.set('Soy Seeds Nuts Dairy Eggs Other')

            self.a_list= tk.Listbox(
                self.lf, listvariable=self.allergen,selectmode=tk.MULTIPLE,
                bg='light blue', selectbackground='pink1', selectforeground='black')
            self.a_list.configure(font=self.font, exportselection=False, activestyle='dotbox')
            self.a_list.pack(side="top", expand=True,fill="both")
            self.a_list.bind('<<ListboxSelect>>', self.toggle)

            self.other = tk.StringVar()
            self.other.set("Other...")

            self.specify = tk.Entry(self.lf, textvariable=self.other)
            self.specify.pack(side="top", expand=True, fill="both", pady=5, padx=5)
            self.specify['state'] = "disabled"

            self.submit = tk.Button(self.lf, text="Submit", bg="pale green",command=self.r_allergen)
            self.submit.pack(side="top", expand=True,fill="both",padx=4, pady=(0,5))
            self.submit.bind('<1>', self.a_list.unbind('<1>'))

        def r_allergen(self):
            #gather and sterilize selection
            sel = self.a_list.curselection()
            alrg = [str(self.a_list.get(idx)) if self.a_list.get(idx) != "Other" else self.other.get() for idx in sel]

            item = self.master.item_data
            try:
                item['!!'].extend(alrg)

                for _a in alrg:
                    self.master.info_tree.insert('alrg', 'end', text=_a, tags='allergen')

            except KeyError:
                item['!!'] = alrg
                self.master.info_tree.insert('','end','alrg',text='!!')
                self.master.info_tree.item('alrg', open=True)


                for _a in alrg:
                    self.master.info_tree.insert('alrg', 'end', text=_a, tags='allergen')
            self.master.info_tree.tag_configure('allergen', background='red')

            print(item)
            self.destroy()


        def toggle(self, root):
            #this toggles the "Other..." Entry field
            bool = self.a_list.curselection()
            if 5 in bool:
                self.specify['state'] = "normal"
            else: self.specify['state'] = 'disabled'

    class Special(tk.Toplevel):
        def __init__(self,root):
            super().__init__(root)

            self.lf = tk.LabelFrame(self, text="Guest has a special request:", bg="orangered")
            self.lf.grid(row=0,column=0,sticky="N,E,W,S",ipady=10,ipadx=5)

            self.t = tk.Text(self.lf,width=51,height=5,wrap="word")
            self.t.insert('end', "This is a special request...")
            self.t.pack(side="top", expand=True,fill="both")

            self._frame = tk.Frame(self, bg="orangered")
            self._frame.grid(row=1,column=0, sticky="N,E,S,W", ipadx=5)

            self._submit = tk.Button(
                self._frame, width=25, text = "Submit", command=self.submit_text,
                bg = 'pale green', activebackground='green1')
            self._submit.grid(row=0,column=0, sticky="N,S,W", ipady=2, padx=2)

            self._cancel = tk.Button(
                self._frame, width=15, text = 'X', command=self.destroy,
                bg = 'pink1', activebackground = 'red')
            self._cancel.grid(row=0,column=1, sticky="N,E,S", ipady=2, padx=2)

        def submit_text(self):
            text = self.t.get(1.0, 'end')
            text = text.strip('\n')

            item = self.master.item_data
            try:
                item['..'].append(text)

                self.master.info_tree.insert('misc', 'end', text=text, tags='descrip')

            except KeyError:
                item['..'] = [text]
                self.master.info_tree.insert('', 'end', 'misc', text='..')
                self.master.info_tree.item('misc', open=True)

                self.master.info_tree.insert('misc', 'end', text=text, tags='descrip')
            self.master.info_tree.tag_configure('descrip', background='SkyBlue1')

            print(item)
            self.destroy()

if __name__ == "__main__":

    menu = OrderMenu()
    menu.mainloop()
