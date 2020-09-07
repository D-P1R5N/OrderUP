import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
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
        self.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        self.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        self.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

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

        self.order = ActiveOrder(self)
        self.order.grid(row=0,column=2,rowspan=10, sticky="N,S")

        self.serv_opt = ServerOptions(self)
        self.serv_opt.grid(row=1,column=1, sticky="N,E,W,S")

        self.menu = MainNote(self)
        self.menu.grid(row=0, column=0, rowspan=10, sticky= "N,W")

    def _update(self, words):
        self.item.item.insert('end',(words['name'],"\t\t",words['price'],"\n"))

class ActiveOrder(tk.Canvas):
    def __init__(self,root):
        tk.Canvas.__init__(self,root)
        self.root = root
        self.configure(
            width= 500, height= 35, state='disabled',
            bg='honeydew', highlightthickness=3, highlightbackground= "DarkGreen",
            relief= 'sunken'
        )
        self.table = dict()

class ServerOptions(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.root = root

        self.add_guest = tk.Button(
            self, text="Add Guest", width = 29, command=self.add_client,
            bg='PapayaWhip', activebackground='orangered')
        self.add_guest.pack(side="top",fill="both",expand=True)
        ##EDIT STILL NEEDS WORK
        self.edit_guest = tk.Button(
            self, text="Edit Guest", width=29, command=None,
            bg='lavender', activebackground='purple1')
        self.edit_guest.pack(side="top",fill="both",expand=True)


        self.remove_guest = tk.Button(
            self, text="Remove Guest", width=29, command=self.remove_client,
            bg='pink1', activebackground='red')
        self.remove_guest.pack(side="top", fill="both", expand=True)

        self.confirm = tk.Button(
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

class OrderItemPane(tk.Frame):

    def __init__(self,root,data):
        tk.Frame.__init__(self,root)
        self.font = font.Font(family='Georgia', size=12)
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

        self.l1 = tk.Label(self, text=data[0])
        self.l1.configure(
            font=self.font,
            bg = 'Peach Puff',
            borderwidth = 2,
            relief = 'groove'
        )
        self.l1.grid(row=0,column=0,sticky="NW,E",ipady=2)
        self.l1.bindtags("ret_info")

        self.l2 = tk.Label(self, text='${}'.format(data[1]))
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
        self.t.insert("end", data[3])
        self.t['state']="disabled"
        self.t.bindtags("ret_info")

    def add_item(self, root):
        #this is the TOPLEVEL maker!!
        parent = root.widget.winfo_parent()
        item_info = self.nametowidget(parent).data

        self._item = ItemBuild(self, text=item_info[0], value=item_info[1])



class ItemBuild(tk.Toplevel):
    def __init__(self,root, text='This is a Test Item',value=None):
        super().__init__(root, takefocus=True)
        self.geometry('400x200+300+300')
        self.transient(root)
        self.item_data = dict()
        self.item_data['ID'] = text
        self.item_data['$$'] = value
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
        text = json.dumps(_data, indent=4)
        delimits = ['[',']','{','}',',']
        for _ in delimits:
            text=text.replace(_,'')
        self._root().order.configure(state="normal")
        self._root().order.insert('end', text)
        self._root().order.configure(state='disabled')

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
            self.lf.grid(row=0,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

            self.list = tk.Listbox(
                self.lf, listvariable=self.extra,selectmode=tk.MULTIPLE,
                bg='Peach Puff', selectbackground='honeydew', selectforeground='black')
            self.list.pack(expand=True,fill="x",side="top")
            self.list.configure(font=self.font)

            self.lf1 = tk.LabelFrame(self, text="Review Your Choices:",bg='orangered')
            self.lf1.grid(row=1,column=0,sticky="N,E,S,W",ipady=10,ipadx=5)

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

            print(item)

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


            print(item)

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
                    self.master.info_tree.insert('alrg', 'end', text=_a)

            except KeyError:
                item['!!'] = alrg
                self.master.info_tree.insert('','end','alrg',text='!!')
                self.master.info_tree.item('alrg', open=True)


                for _a in alrg:
                    self.master.info_tree.insert('alrg', 'end', text=_a)

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

            item = self.master.item_data
            try:
                item['..'].append(text)

                self.master.info_tree.insert('misc', 'end', text=text)

            except KeyError:
                item['..'] = [text]
                self.master.info_tree.insert('', 'end', 'misc', text='..')
                self.master.info_tree.item('misc', open=True)

                self.master.info_tree.insert('misc', 'end', text=text)

            print(item)
            self.destroy()


if __name__ == "__main__":

    menu = OrderMenu()
    menu.mainloop()
