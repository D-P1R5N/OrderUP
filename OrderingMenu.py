from tkinter import *
from tkinter import ttk

class OrderMenu(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Order UP!")
        self.resizable(False,False)
        self.display = self.geometry("+500+300")
        self['bg'] = 'black'
        self.person = 0

        self.order = self.ActiveOrder(self)
        self.order.grid(row=0,column=2,rowspan=10, sticky="N,S")

        self.item = self.Item(self)
        self.item.grid(row=0, column=1, sticky="N,S")

        self.serv_opt = self.ServerOptions(self)
        self.serv_opt.grid(row=1,column=1, sticky="N,E,W")

        self.menu = self.MenuBook(self)
        self.menu.grid(row=0, column=0, rowspan=10, sticky= "N,W")


    class ActiveOrder(Text):
        def __init__(self,root):
            Text.__init__(self,root)
            self.root = root
            self['width'] = 50
            self['height'] = 35
            self['state'] = "disabled"
            self['wrap'] = 'word'
            self['bg'] = 'honeydew'
            self['highlightthickness'] = 3
            self['highlightbackground'] = "DarkGreen"
            self['highlightcolor'] = "DarkGreen"
            self['relief'] = 'sunken'

    class Item(LabelFrame):
        def __init__(self,root):
            LabelFrame.__init__(self,root)
            self['text']="Item"
            self['background'] = 'orangered'
            self['width'] = 100
            self['height'] = 100

            self.root = root

            self.item = Text(self, width='25', height='8')
            self.item['bg'] = 'PapayaWhip'
            self.item['wrap'] = 'word'
            self.item.focus_set()
            self.item.grid(row=0,column=0,columnspan=10,pady=3)

            self.food_opt = Frame(self)
            self.food_opt.grid(row=1,column=0,columnspan=3)

            self.mod = Button(
                self.food_opt,text="++/--", width = 8, command=None,
                bg='coral', activebackground='coral2')
            self.mod.grid(row=1,column=0,ipady=3)

            self.request = Button(
                self.food_opt,text="Request",width = 9, command = None,
                bg = 'light blue', activebackground = 'blue1')
            self.request.grid(row=1,column=1,ipady=3)

            self.alert = Button(
                self.food_opt,text="!!",width=8,command= None,
                bg = 'red', activebackground = 'DarkRed')
            self.alert.grid(row=1,column=2,ipady=3)

            self.finish = Frame(self)
            self.finish.grid(row=2,column=0,columnspan=3)

            def add_order(self, root):
                #print(self.item.get(1.0, 'end'))
                next = int(root.order.index('end-1c').split('.')[0])
                if self.item.get(1.0, 'end') == '\n':
                    pass
                else:
                    root.order.configure(state="normal")
                    root.order.insert(next+1.0, self.item.get(1.0, 'end'))
                    root.order.configure(state="disabled")

                    self.item.delete(1.0, 'end')
                self.item.focus_set()

            cmd1 = lambda root=self.root:  add_order(self, root)
            self.confirm = Button(
                self.finish,text="Confirm", width='20',command=cmd1,
                bg='honeydew', activebackground='DarkGreen')
            self.confirm.grid(row=2,column=0,ipady=3)

            def clear():
                self.item.delete(1.0,'end')

            self.cancel = Button(
                self.finish, text="X", width='7', command=clear,
                bg='pink1', activebackground='red')
            self.cancel.grid(row=2,column=1,ipady=3)

    class ServerOptions(Frame):
        def __init__(self,root):
            Frame.__init__(self,root)
            #self.grid()
            self.root = root

            def add_client(self, root):
                root.person +=1
                next = int(root.order.index('end-1c').split('.')[0])
                next_line=["\n","-"*20, "Seat #", str(root.person), "-"*20, "\n"]

                root.order.configure(state="normal")
                root.order.insert(next+1.0, ''.join(next_line), 'tag-center')
                root.order.configure(state="disabled")

                root.item.item.focus_set()


                self.add_guest['text']=''.join(["Seat #", str(root.person+1)])

                #print(''.join(next_line))

            cmd = lambda x = self.root : add_client(self, x)
            self.add_guest = Button(
                self, text="Add Guest", width = 29, command=cmd,
                bg='PapayaWhip', activebackground='orangered')
            self.add_guest.grid(column=0, row=0, ipady=10,sticky="N,E,W")

            self.edit_guest = Button(
                self, text="Edit Guest", width=29, command=None,
                bg='lavender', activebackground='purple1')
            self.edit_guest.grid(column=0,row=1,ipady=10,sticky="N,E,W")


            def remove_client(self, root):
                """This area is for removing a client from the menu widget,
                it would be best to store all the info inside that widget as a
                dictionary then all items added to it are stored under keyval = seat#"""
                text = root.order.get(1.0,'end')
                text = [i for i in text.split("\n") if i != '']
                #minus_guest = list(filter(lambda x: x))
                print(text)
                root.order.configure(state="normal")
                root.order.delete('end-2l','end')
                root.order.configure(state="disabled")
                if root.person == 1: pass
                else: root.person -= 1
                self.add_guest['text'] = ''.join(["Seat #", str(root.person)])

            cmd2 = lambda x = self.root: remove_client(self, x)
            self.remove_guest = Button(
                self, text="Remove Guest", width=29, command=cmd2,
                bg='pink1', activebackground='red')
            self.remove_guest.grid(column=0,row=2, ipady=10,sticky="N,E,W")

            self.confirm = Button(
                self, text="Submit Order", width=29, command=None,
                bg='pale green', activebackground='green1')
            self.confirm.grid(column=0,row=3,ipady=10,sticky="N,E,W")

    class MenuBook(ttk.Notebook):
        def __init__(self,root):
            ttk.Notebook.__init__(self,root)
            self.root = root

            self.style = ttk.Style()
            self.style.theme_create( "MyStyle", parent="alt", settings={
                "TNotebook": {"configure":{
                    "background": 'black',
                    "tabmargins": [2,5,2,0] } },
                "TNotebook.Tab": {"configure": {
                    "background": 'light blue',
                    "padding":[50,10] },
                "map": {
                    "highlightthickness":[("selected", 0)],
                    "background": [("selected", "blue1")],
                    "expand":[("selected",[2,2,2,0])]
                }}})
            self.style.theme_use("MyStyle")
            self.style.configure('lefttab.TNotebook', tabposition='wn')

            self.f1 = Frame(self,width=250,height=self.root.order.winfo_reqheight(),bg='light blue')
            self.f2 = Frame(self,width=250,height=self.root.order.winfo_reqheight(),bg='light blue')

            self.f1['highlightthickness'],self.f2['highlightthickness'] = 3,3
            self.f1['highlightbackground'],self.f2['highlightbackground'] = 'blue1', 'blue1'
            self.f1['relief'],self.f2['relief'] = "raised","raised"

            self.add(self.f1, text='Food')
            self.add(self.f2, text='Drink')

            #print(self.root.order.winfo_reqheight())

if __name__ == "__main__":
    menu = OrderMenu()
    menu.mainloop()
