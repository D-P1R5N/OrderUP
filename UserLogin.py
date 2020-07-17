import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import sqlite3

class Keywin(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Login")
        self.resizable(False,False)
        self.overrideredirect(True)
        self.geometry("+300+300")
        self.pin = str()

        self.entry = ttk.Entry(width=15)
        self.entry.grid(column=0,row=0, pady=2)

        self.numpad = self.Numpad()
        self.numpad.grid(column=0,row=1,padx=5,pady=2)

        self.destruct = ttk.Button(command=self.close,text="Close",width=15)
        self.destruct.grid(column=0, row=4, ipady=5, pady=(2,5))

    def close(self):
        self._root().destroy()

    class Numpad(ttk.Frame):
        def __init__(self):
            ttk.Frame.__init__(self)
            self.root = self._root()
            self.numpad_create([*range(1,10), *['Del','0','Enter']])

        def numpad_create(self,nums):
            r,c = 1,0

            for b in nums:
                cmd = lambda x=b: self.code(x)
                self.b = ttk.Button(self, text=b,width=15,command=cmd)
                self.b.grid(row=r,column=c,ipady=20, sticky='N,E,S,W')
                c += 1
                if c>= 3:
                    c=0
                    r+=1

        def code(self, value):
            entry = self.root.entry
            if value == 'Del':
                self.root.pin = self.root.pin[:-1]
                entry.delete('0', 'end')
                entry.insert('end', self.root.pin)

            elif value == 'Enter' :
                pin = entry.get()
                try:
                    with sqlite3.connect('OrderUp.db') as conn:
                    #There should only be one EMPLOYEE per PIN
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM employee WHERE password = ?', (pin,))
                        employee = cur.fetchone()

                        if not employee:
                            print("The PIN was incorrect")
                            entry.delete('0', 'end')
                            self.root.pin = str()
                            entry.insert('end', self.root.pin)

                        else:
                            print("Welcome", employee[1])
                            entry.delete('0', 'end')
                            self.root.pin = str()
                            entry.insert('end', self.root.pin)

                except sqlite3.OperationalError as e:
                    _err = messagebox.showerror("Operational Error", e)
            else:
                if len(self.root.pin) < 4:
                    self.root.pin += str(value)
                    entry.insert('end', value)
                else: pass

if __name__ == "__main__":

    keypad = Keywin()
    keypad.mainloop()
