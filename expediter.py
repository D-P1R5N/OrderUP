import tkinter as tk
from tkinter import ttk
from tkinter import font
from copy import deepcopy
import time
import threading
import sqlite3
import json

values = [(5, '{"1": [{"ID": "Jalapeno Poppers", "$$": "8.00", "++": ["Bacon", "Lettuce", "Tomato", "Pickle"], "--": ["Bacon", "Lettuce", "Tomato", "Pickle"], "!!": ["Soy", "Seeds", "Nuts", "Dairy", "Eggs", "Other..."], "..": "This is a special request...\\n"}, {"ID": "Soft Drink", "$$": "2.00"}], "2": [{"ID": "Sirloin Steak", "$$": "18.00", "++": ["Lettuce", "Tomato"], "--": ["Lettuce", "Pickle"], "!!": ["Dairy"]}, {"ID": "Moscato ", "$$": "8.00"}], "3": [{"ID": "Spaghetti", "$$": "2.00", "--": ["Lettuce", "Tomato"], "!!": ["Seeds"]}, {"ID": "Soft Drink", "$$": "2.00"}], "4": [{"ID": "Sirloin Steak", "$$": "18.00", "--": ["Pickle"]}, {"ID": "Basic App", "$$": "1.00", "++": ["Bacon"]}, {"ID": "Soft Drink", "$$": "2.00"}]}', '19:19:49', '2020-07-23'),
(3, '{"1": [{"ID": "Spaghetti", "$$": "2.00"}]}', '17:16:20', '2020-07-23'),
(9, '{"1": [{"ID": "Basic App", "$$": "1.00", "++": ["Lettuce", "Pickle"], "!!": ["Nuts"]}], "2": [{"ID": "Soft Drink", "$$": "2.00"}, {"ID": "Jalapeno Poppers", "$$": "8.00", "++": ["Pickle"]}]}', '12:33:18', '2020-08-05')]


class ProgStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.theme_create("ProgStyle", parent="clam", settings={
        "green.Horizontal.TProgressbar":{"configure":{
            "troughcolor":"orangered",
            "background":"DarkGreen",
            "bordercolor":"black",
            "lightcolor":"red",
            "darkcolor":"blue"}},
        "yellow.Horizontal.TProgressbar":{"configure":{
            "troughcolor":"orangered",
            "background":"Yellow",
            "bordercolor":"black",
            "lightcolor":"red",
            "darkcolor":"blue"}},
        "red.Horizontal.TProgressbar":{"configure":{
            "troughcolor":"orangered",
            "background":"red",
            "bordercolor":"black",
            "lightcolor":"red",
            "darkcolor":"blue"}},
        "border.TFrame":{"configure":{
            "background":"black",
            "padding":(0,0,0,0)},
            "borderwidth": 0},
        "tickettab.TLabel":{"configure":{
            "background": "honeydew",
            "font":("Bahnschrift",11),
            "anchor":"center",
            "relief":'raised',
            'borderwidth':[15,5,15,5],
            "bordercolor":'Dark Green',
            'padding':[0,10,0,10]
        },
        "map":{
            "background":[('active', 'blue1')]
        }},
        "qvticket.TLabel":{"configure":{
            "background":"SkyBlue1",
            'font':('Condi',12)

        }},
        "qvbutton.TButton":{"configure":{
            "background":"honeydew",
            "anchor":"center",
            "font":("Bahnschrift",10)
        }}
        })
        self.map('qvbutton.TButton',background=[('active', 'red'),('pressed', 'blue'),])
        self.theme_use("ProgStyle")


class MainKitchen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("+350+150")
        self.style = ProgStyle()
        self.ticket_list = self.TicketList(self)
        self.ticket_list.pack(side='left', expand=True, fill='x', anchor='w')

        self.ticket_view = self.TicketView(self)
        self.ticket_view.pack(side='right', expand=True, fill='x', anchor='ne')

        self.bottom_panel = ttk.Frame(self.ticket_view)
        self.bottom_panel.pack(side='bottom',expand=True, fill='x', anchor='s')

        self.all_day = self.AllDay(self.ticket_view)
        self.all_day.pack(side="bottom", expand=True,fill='both', anchor='s')

    class AllDay(ttk.LabelFrame):
        def __init__(self,root):
            super().__init__(root)
            self.tree = ttk.Treeview(self)
            self.tree.pack(side = 'left', expand=0)

        class AllDayTree(ttk.Treeview):
            def __init__(self,root,data):
                super().__init__(root)


    class TicketQuickView(ttk.Frame):
        def __init__(self,root,data,reference):
            super().__init__(root)
            self.data = data
            self.ref = reference
            self.border_frame = ttk.Frame(self, padding=10,style='border.TFrame')
            self.border_frame.pack(side="left", expand=True, fill='both', anchor='center')

            self.ticket_label = ttk.Label(self.border_frame, text=data[0], anchor='center', style='qvticket.TLabel')
            self.ticket_label.pack(side='top', expand=True, fill='x', anchor='center', ipadx= 20)
            self.ticket_label.bind('<1>', self.buildTick)

        def buildTick(self,event):
            #ticket_Top = tk.Toplevel(self)
            ticket = MainKitchen.QuickT(self.ref,self.data)
            self.ticket_label['background'] = 'blue1'


    class TicketList(ttk.Frame):
        def __init__(self,root):
            super().__init__(root)
            self.ref = root
            self.ticketlist = ttk.Frame(self)
            self.ticketlist.pack(side='left', expand=True, fill='both')
            self.populate()
            self.scroll = ttk.Scrollbar(self)
            self.scroll.pack(side= 'right',anchor='e', expand=True, fill='y')

        def populate(self):
            with sqlite3.connect('OrderUP.db') as conn:
                statement = '''SELECT * FROM active_orders'''
                cur = conn.cursor()
                cur.execute(statement)
                data = cur.fetchall()
            for d in data:
                ticket_tab = self.TicketTab(self.ticketlist,d)
                ticket_tab.pack(expand=False, fill='x')

        class TicketTab(ttk.Frame):
            def __init__(self, root, data):
                super().__init__(root)
                self.ref = root
                self.data = data
                self.state = True
                self.ticket_tab = ttk.Label(self, text=self.data[0], width= 20, style='tickettab.TLabel')
                self.ticket_tab.pack(expand=False,fill="x",side="top", ipadx=10)
                self.ticket_tab.bind('<1>', self.returnData)

            def returnData(self,event):
                if self.state:

                    if hasattr(self.ref.master.ref, 'ticket_view'):
                        self.ticket = self.ref.master.ref.Ticket(self.ref.master.ref.ticket_view, self.data, self)
                        self.ticket.pack(side='left',expand=True,fill='x',anchor='n')
                        self.bot_tab = self.ref.master.ref.TicketQuickView(self.ref.master.ref.bottom_panel, self.data, self)
                        self.bot_tab.pack(side="left", expand=False)
                        self.state = False
                        self.ticket_tab.configure(background='Blue1')


                    else:
                        print("Does not have ticket_view.")
                        print(self.ref.master.ref)
                else: self.ticket_tab.unbind('<1>')

    class TicketView(ttk.LabelFrame):
        def __init__(self,root):
            super().__init__(root,text='Active Order')

    class Ticket(ttk.Frame):
        def __init__(self,root,data,reference, command=None):
            super().__init__(root)
            self.command = command
            self.data = data
            self.ref = reference
            self.display = self.winfo_geometry()
            self._stop = threading.Event()
            self._stop.set()
            self.table_num = 0
            self.row = 0
            self.column = 0

            self.started = False


            self.dtframe = ttk.Frame(self)
            self.dtframe.pack(side='top', fill = 'x', expand=True)
            self.dtframe.bindtags("importCommand")

            self.header = ttk.Label(self.dtframe, text=data[0],anchor='center')
            self.header.pack(side='left', fill='x', expand=True, anchor='nw')
            self.header.bindtags("importCommand")

            self.t = ttk.Label(self.dtframe, text=data[-2],anchor='e')
            self.t.pack(side='right',fill='x', expand=True,ipadx=50, anchor='ne')
            self.t.bindtags("importCommand")

            self._makeTicket()
            self.update_idletasks()
            #self._root().filled_display += self.winfo_reqwidth()
            self.bind_class("importCommand",'<1>', self.importCommand)


        def importCommand(self,event):
            if not self.command:

                if self.stopped():
                    if not self.started:
                        self.ticket_timer()
                        self.started = True
                    else:
                        pass
                    self._stop.clear()
                else:

                    self.stop()
                    print('stopped')

            else:
                return self.command()

        def stop(self):
            self._stop.set()

        def stopped(self):
            return self._stop.isSet()

        def read_ticket(self):
            t_dat = json.loads(self.data[1])
            for t,dat in t_dat.items():
                yield (t,dat)

        def _makeTicket(self):
            self.border = ttk.Frame(self,style='border.TFrame')
            self.border.pack(side="top", fill="both", expand=False, ipadx=3,ipady=2)
            self.frame = ttk.Frame(self.border, relief='groove',style='border.TFrame')
            self.frame.pack(side="top", expand=False)

            self.prog_bar = ttk.Progressbar(self.frame, orient=tk.VERTICAL, length=100, mode='determinate',style="green.Horizontal.TProgressbar")
            self.prog_bar.pack(side='left',expand=True,fill='y',anchor='w')

            for seat,order in self.read_ticket():
                self.seat_frame = ttk.Label(self.frame, style='border.TFrame')
                self.seat_frame.pack(side="top", fill='x', expand=False, anchor='n')

                self.seat_id = ttk.Label(self.seat_frame,width=25, text=("Seat" + seat),anchor="e",background='DarkGreen',font="TimesNewRoman")
                self.seat_id.pack(side="top", fill="x", expand=False,anchor='n')
                self.seat_id.bindtags("importCommand")

                for item in order:
                    it_keys = item.keys()
                    self.item_id = ttk.Label(self.seat_frame, width=25, text=item['ID'].upper(),anchor='n', background="PapayaWhip",font='TimesNewRoman')
                    self.item_id.pack(side="top", fill='x', expand=False, anchor='n')
                    self.item_id.bindtags("importCommand")
                    for _k in it_keys:
                        if _k == '++':
                            for x in item['++']:
                                self.add_id = ttk.Label(self.seat_frame, width=25, text=("++"+x),anchor="n", background='pale green', font='TimesNewRoman')
                                self.add_id.pack(side="top",fill='x', expand=False,anchor='n')
                                self.add_id.bindtags("importCommand")
                        elif _k == '--':
                            for x in item['--']:
                                self.rem_id = ttk.Label(self.seat_frame, width=25, text=('--'+x),anchor='n', background='light pink', font='TimesNewRoman')
                                self.rem_id.pack(side='top', fill='x',expand=False, anchor='n')
                                self.rem_id.bindtags("importCommand")

                        elif _k == '!!':
                            for x in item['!!']:
                                self.alrg_id = ttk.Label(self.seat_frame, width=25, text=('!!'+x),anchor='n', background='orangered', font='TimesNewRoman')
                                self.alrg_id.pack(side='top',fill='x',expand=False, anchor='n')
                                self.alrg_id.bindtags("importCommand")

                        elif _k == '..':
                            if isinstance(item['..'], list):
                                for de in item['..']:

                                    desc = '..' + de
                                    self.desc_id = ttk.Label(self.seat_frame, width = 25, text=desc,anchor='n',wraplength=150, background='SkyBlue1')
                                    self.desc_id.pack(side='top', fill='x', expand=False, anchor='n')


                            else:
                                desc = '..' + item['..']
                                self.desc_id = ttk.Label(self.seat_frame, width = 25, text= desc, anchor='n', wraplength=150, background='SkyBlue1')
                                self.desc_id.pack(side='top', fill='x', expand=False, anchor='n')
                            self.desc_id.bindtags("importCommand")

                        elif _k == '$$':
                            print(item['$$'])

        def ticket_timer(self):
            def real_timer():

                while True:
                    if not self.stopped():
                        self.prog_bar.step()
                    #900 seconds/15 minutes
                    #90 for each step
                    time.sleep(.1)
                    #time.sleep(9)
                    if self.prog_bar['value'] >= 99:
                        self.stop()
                        return
                    elif self.prog_bar['value'] >=65:
                        self.prog_bar['style'] = 'red.Horizontal.TProgressbar'
                    elif self.prog_bar['value'] >=35:
                        self.prog_bar['style'] = 'yellow.Horizontal.TProgressbar'

            self.thread = threading.Thread(name=self,target=real_timer, daemon=True)
            self.thread.start()



    class QuickT(tk.Toplevel):
        def __init__(self,reference, data):
            super().__init__()
            self.geometry("+200+50")
            self.ref = reference
            self.info = self.master.Ticket(self, data, None, command=self.close)
            self.info.prog_bar.pack_forget()
            self.info.pack(side='top', expand=True, fill='both')
            self.info.bind("<1>", self.close)
            self.submit = ttk.Button(self, text= 'Sell Ticket', command=self.sell, style='qvbutton.TButton')
            self.submit.pack(side='bottom', expand=True, fill='x')

        def close(self):
            self.ref.bot_tab.ticket_label.configure(background = 'SkyBlue1')

            self.destroy()

        def sell(self):
            print(self.ref)
            if not self.ref.ticket.stopped():
                self.ref.ticket.stop()
            self.ref.ticket_tab.destroy()
            self.ref.bot_tab.destroy()
            self.ref.ticket.destroy()
            self.ref.destroy()
            self.destroy()

if __name__ == '__main__':
    main = MainKitchen()
    main.mainloop()
