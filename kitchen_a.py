import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
#from multiprocessing import Pool
from datetime import datetime
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
        "qvs_button.TButton":{"configure":{
            "background":"honeydew",
            "anchor":"center",
            "font":("Bahnschrift",10)
        },
        "map":{
            "background":[("pressed","green")]
        }},
        "qvc_button.TButton":{"configure":{
            "background":"pink1",
            "anchor":"center",
            "font":("Bahnschrift",10)
        },
        "map":{
            "background":[("pressed","red")]
        }}
        })
        self.map('qvbutton.TButton',background=[('active', 'red'),('pressed', 'blue'),])
        self.theme_use("ProgStyle")


class MainKitchen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("+50+25")
        self.style = ProgStyle()
        self.ticket_list = self.TicketList(self)
        self.ticket_list.pack(side='left',expand=False, fill='x', anchor='nw')

        self.ticket_view = self.TicketView(self)
        self.ticket_view.pack(side='left',expand=True, fill='x', anchor='ne')

        self.bottom_panel = ttk.Frame(self.ticket_view)
        self.bottom_panel.pack(side='bottom',expand=True, fill='x', anchor='s')



        self.protocol("WM_DELETE_WINDOW", self.stop_timer)

    def stop_ticket(self,t):
        t.stop()

    def stop_timer(self):
        m = messagebox.askyesno(self)
        if m:
            x = map(self.stop_ticket, self.ticket_view.ticket_pool)
            for _ in x:
                pass
            self.ticket_view.execute_state = False
            self.ticket_view.executor.shutdown(wait=False)
            self.destroy()
        else:
            pass

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
            ticket = MainKitchen.QuickT(self.ref,self.data)
            self.ticket_label['background'] = 'blue1'


    class TicketList(ttk.Frame):
        def __init__(self,root):
            super().__init__(root)
            self.ref = root
            self.timer = self.TimerBox(self)
            self.timer.pack (expand=False,fill='x', anchor='nw')

            self._t = ttk.Frame(self)
            self._t.pack(expand=True,fill='y', anchor='w')

            self.ticketlist = tk.Canvas(self._t)
            self.ticketlist.pack(side='left',expand=True, fill='y', anchor='w')

            scroll = ttk.Scrollbar(self._t)
            scroll.pack(side='left',anchor='e',expand=True, fill='y')
            scroll.configure(command=self.ticketlist.yview)
            self.ticketlist.configure(yscrollcommand=scroll.set, width=180)

            self.allday = self.AllDay(self)
            self.allday.pack(side='bottom',expand=True,fill='both', anchor='s')

            self.create_frame(self.ticketlist)
            self.populate()

        class AllDay(ttk.Treeview):
            def __init__(self,root):
                super().__init__(root)

        class TimerBox(ttk.Frame):
            def __init__(self,root):
                super().__init__(root)
                self.val = tk.StringVar()

                self.display = ttk.Label(self, textvariable=self.val)
                self.display.pack(side="top", fill="x", expand=True)

                self.update_val()

            def update_val(self):

                def commit_time():
                    time = datetime.now().strftime("%I:%M %p")
                    self.val.set(time)

                def real_update():
                    while True:
                        commit_time()
                        time.sleep(60)

                self.t = threading.Thread(target = real_update, daemon=True)
                self.t.start()

        def create_frame(self, destination):
            self.scroll_frame = ttk.Frame(self.ticketlist, height=600)
            self.scroll_frame.bind(
                "<Configure>",
                lambda x: self.ticketlist.configure(
                    scrollregion = self.ticketlist.bbox("all")
                )
            )
            self.ticketlist.create_window((0,0),window=self.scroll_frame,anchor="nw")

        def populate(self):
            with sqlite3.connect('OrderUP.db') as conn:
                statement = '''SELECT * FROM active_orders'''
                cur = conn.cursor()
                cur.execute(statement)
                data = cur.fetchall()
            for d in data:
                ticket_tab = self.TicketTab(self.scroll_frame,d)
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
                #to make things more legible:
                _main = self.ref.master.master.master.ref
                if self.state:
                    #Add a ticket to Active Tickets
                    #Create a bottom widget for quick select
                    #Add Ticket to list of tickets in view
                    if hasattr(_main, 'ticket_view'):

                        self.ticket = _main.Ticket(_main.ticket_view, self.data, self)
                        self.ticket.pack(side='left',expand=True,fill='x',anchor='n')

                        self.bot_tab = _main.TicketQuickView(_main.bottom_panel, self.data, self)
                        self.bot_tab.pack(side="left", expand=False)

                        self.state = False
                        self.ticket_tab.configure(background='Blue1')

                        _main.ticket_view.ticket_pool.append(self.ticket)

                    else:
                        print("Does not have ticket_view.")
                        print(self.ref.master.ref)

                else: self.ticket_tab.unbind('<1>')
                self.changeView()

            def changeView(self):
                widget = self.ref.master.master.master.ref.ticket_view
                if len(widget.ticket_pool) >= 6:
                    t1 = widget.ticket_pool.pop(0)
                    t1.pack_forget()
                else:
                    pass

    class TicketView(ttk.LabelFrame):
        def __init__(self,root):
            super().__init__(root,text='Active Order')
            self.execute_state = True
            self.ticket_pool = []
            self.ticket_timer()

        def ticketControl(self, event):
            t = str(event.widget).split('.')
            t = t[:3]

            widg = self.nametowidget('.'.join(t))
            widg.stop()
            pass

        def ticket_timer(self):

            def cycleStyle(t):
                if t.prog_bar['value'] >= 99:
                    if not t.terminated:
                        t.terminate()
                    else:
                        return
                elif t.prog_bar['value'] >=65:
                    t.prog_bar['style'] = 'red.Horizontal.TProgressbar'
                elif t.prog_bar['value'] >=35:
                    t.prog_bar['style'] = 'yellow.Horizontal.TProgressbar'
                else:
                    t.prog_bar['style'] = "green.Horizontal.TProgressbar"

            def incrementOne(t):
                if not t.stopped():
                    t.prog_bar.step()

            def real_timer():
                while self.execute_state:
                    with ThreadPoolExecutor(max_workers=5) as self.executor:
                        if self.ticket_pool:
                            x = self.executor.map(incrementOne, self.ticket_pool)
                            y = self.executor.map(cycleStyle, self.ticket_pool)
                            for i in x and y:
                                pass
                    #900 seconds/15 minutes
                    #9 for each step
                        time.sleep(.1)
                        #time.sleep(9)

                    self.executor.shutdown(wait=False)

            self.bind_class('importCommand','<1>', self.ticketControl)
            self.thread = threading.Thread(target=real_timer, daemon=True)
            self.thread.start()

    class Ticket(ttk.Frame):
        def __init__(self,root,data,reference):
            super().__init__(root)
            self.data = data
            self.ref = reference
            self.display = self.winfo_geometry()
            self._stop = threading.Event()
            #self._stop.set()
            self.terminated = False
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

        def terminate(self):
            self.terminated = True
            self._stop.set()

        def stop(self):
            if not self.terminated:
                if not self.stopped():
                    self._stop.set()
                else:
                    self._stop.clear()
            else:
                pass

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
                            print("Ticket._maker")

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
                        #self.stop()
                        return
                    elif self.prog_bar['value'] >=65:
                        self.prog_bar['style'] = 'red.Horizontal.TProgressbar'
                    elif self.prog_bar['value'] >=35:
                        self.prog_bar['style'] = 'yellow.Horizontal.TProgressbar'

            self.thread = threading.Thread(target=real_timer, daemon=True)
            self.thread.start()

    class QuickT(tk.Toplevel):
        def __init__(self,reference, data):
            super().__init__()
            self.geometry("+300+300")
            self.ref = reference
            self.info = self.master.Ticket(self, data, None)
            self.info.prog_bar.pack_forget()
            self.info.pack(side='top', expand=True, fill='both')
            self.info.bind("<1>", self.close)

            self.submit = ttk.Button(self, text= 'Sell Ticket', command=self.sell, style='qvs_button.TButton')
            self.submit.pack(side='bottom', expand=True, fill='x', ipady=5)

            self.close = ttk.Button(self, text= 'Close', command=self.close, style='qvc_button.TButton')
            self.close.pack(side='bottom', expand=True, fill='x', ipady=5)

        def close(self):
            self.ref.bot_tab.ticket_label.configure(background = 'SkyBlue1')

            self.destroy()

        def _fin(self,t):
            t.destroy()

        def sell(self):
            #print(self.ref)
            pool = [self.ref.ticket, self.ref.ticket_tab, self.ref.bot_tab, self.ref.ticket, self.ref, self]
            if not self.ref.ticket.stopped():
                self.ref.ticket.stop()
            #self.ref.ticket_tab.destroy()
            #self.ref.bot_tab.destroy()
            #self.ref.ticket.destroy()
            #self.ref.destroy()
            try:
                self.master.ticket_view.ticket_pool.remove(self.ref.ticket)
            except Exception as e:
                print(e)
            #self.destroy()
            for p in pool:
                p.destroy()
if __name__ == '__main__':
    main = MainKitchen()
    main.mainloop()
