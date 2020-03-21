from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import sqlite3

class Keywin(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Login")
        self.resizable(False,False)
        self.overrideredirect(True)
        self.geometry("+300+300")
        self.pin = str()
        self.entry = self.Pin(self)
        self.entry.grid(column=0,row=0, pady=2)
        self.numpad = self.Numpad(self).grid(column=0,row=1)
        self.destuct = self.destructButton(self).grid(column=0, row=4, ipady=5, pady=2)
    def close():
        window.destroy()

    def code(Keywin, value):
        entry = Keywin.entry
        if value == 'Del':
            Keywin.pin = Keywin.pin[:-1]
            entry.delete('0', 'end')
            entry.insert('end', Keywin.pin)
        elif value == 'Enter' :
            conn = sqlite3.connect('employee.db')
            cur = conn.cursor()
            user = entry.get()
            cur.execute('SELECT * FROM EMP WHERE Pass= ?', (entry.get(),))
            employee = cur.fetchone()
            if employee == None:
                print("The PIN was incorrect")
                entry.delete('0', 'end')
                Keywin.pin = str()
                entry.insert('end', Keywin.pin)
            else:
                print("Welcome", employee[0])
                conn.close()
                entry.delete('0', 'end')
                Keywin.pin = str()
                entry.insert('end', Keywin.pin)
        else:
            if len(Keywin.pin) < 4:
                Keywin.pin += str(value)
                entry.insert('end', value)
            else: pass
    class Numpad(ttk.Frame):
        def __init__(self, root):
            ttk.Frame.__init__(self,root)
            self.root = root
            self.grid()
            self.numpad_create()

        def numpad_create(self):
            r,c = 1,0
            nums = [*range(1,10), *['Del','0','Enter']]
            for b in nums:
                cmd = lambda button = b: Keywin.code(self.root, button)
                self.b = Button(self, text=b,width=15,command=cmd, background = 'honeydew', foreground= 'blue')
                self.b.font = Font(family = 'Arial Baltic', size = 12, weight= 'bold')
                self.b.configure(font=self.b.font,activebackground='DarkGreen')
                self.b.grid(row=r,column=c,ipady=20, sticky=(N,E,S,W))
                c += 1
                if c>= 3:
                    c=0
                    r+=1
    class Pin(ttk.Entry):
        def __init__(self,root):
            ttk.Entry.__init__(self, root)
            self.width = 15
            self.font = Font(family = "Franklin Gothic Medium", size = 18)
            self.configure(font=self.font, justify = CENTER)
            self.textvariable = StringVar()
    class destructButton(Button):
        def __init__(self,parent):
            Button.__init__(self,parent)
            self['text'] = "Close"
            self['command'] = parent.destroy
            self['width'] = 27
            self['bg'] = 'orangered'
            self['activebackground'] ='red2'
            self.font = Font(family = "Bahnschrift", size = 12, weight = "bold")
            self.configure(font=self.font)
if __name__ == "__main__":

    keypad = Keywin()
    keypad.mainloop()
