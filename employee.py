import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class EmployeeMainTk(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Employee HUB")
        self.resizable(False,False)
        self.geometry("+300+300")

        self.e_frame = ttk.Frame(self)
        self.e_frame.pack(expand=True, fill="both", side="left")

        self.first_label_frame = ttk.LabelFrame(self.e_frame, text="Employee First Name:")
        self.first_label_frame.grid(row=0,column=0, ipadx=2,ipady=2,padx=2,pady=2)

        self.firstname = StringVar()
        self.first_entry = ttk.Entry(self.first_label_frame, width = 25, textvariable = self.firstname)
        self.first_entry.pack(side="top", fill="both", expand = True, ipadx=2,ipady=2,padx=2,pady=2)

        self.last_label_frame = ttk.LabelFrame(self.e_frame, text="Employee Last Name:")
        self.last_label_frame.grid(row=1,column=0, ipadx=2,ipady=2,padx=2,pady=2)

        self.lastname = StringVar()
        self.last_entry = ttk.Entry(self.last_label_frame, width = 25, textvariable = self.lastname)
        self.last_entry.pack(side="top", fill="both", expand = True, ipadx=2,ipady=2,padx=2,pady=2)

        self.pin_label_frame = ttk.LabelFrame(self.e_frame, text = "Employee Desired PIN:")
        self.pin_label_frame.grid(row=2,column=0, ipadx=2,ipady=2,padx=2,pady=2)

        self.pin = StringVar()
        self.pin_entry = Entry(self.pin_label_frame, width = 17, textvariable = self.pin)
        self.pin_entry.pack(side="left", fill="both", expand = True, ipadx=2,padx=(2,0),pady=2)

        self.pin_avail = None
        self.pin_check = ttk.Button(self.pin_label_frame, width = 6, text="@", command = self.check)
        self.pin_check.pack(side="right", fill="both", expand= True, ipadx=2,padx=(0,2),pady=2)

        self.submit_frame = ttk.Frame(self.e_frame)
        self.submit_frame.grid(row=3,column=0, ipadx=2,ipady=2,padx=2,pady=2)

        self.submitButton = Button(self.submit_frame, width=10, text= "Confirm", command = self.submit)
        self.submitButton['bg'] = 'Pale Green'
        self.submitButton['activebackground'] = 'green1'
        self.submitButton.pack(side="left", fill="both", expand= True,ipadx=2,ipady=2,padx=2,pady=2)

        self.cancelButton = Button(self.submit_frame, width=10, text= "Cancel", command = self.destroy)
        self.cancelButton['bg'] = 'pink1'
        self.cancelButton['activebackground'] = 'red'
        self.cancelButton.pack(side="right", fill="both", expand= True, ipadx=2,ipady=2,padx=2,pady=2)

    def check(self):
        _pin = self.pin_entry.get()
        if len(_pin) < 4:
            self.pin_entry['bg'] = "pink1"
            self.pin_avail = False
            messagebox.showerror(
                "Pin Error",
                "A PIN must be 4 digits or longer."
            )
            return

        sql_check = """SELECT * FROM employee WHERE password = ?"""
        with sqlite3.connect('OrderUP.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_check, (_pin,))
            pin_status = cursor.fetchone()

            if pin_status:
                self.pin_entry['bg'] = "pink1"
                self.pin_avail = False
                messagebox.showerror(
                    "Pin Error",
                    "The PIN is unavailable."
                )
            else:
                self.pin_entry['bg'] = 'honeydew'
                self.pin_avail = True

    def submit(self):
        if not self.pin_avail:
            messagebox.showerror(
                "Pin Error",
                "This message is to confirm the PIN is not available. Please reconfirm with '@' "
            )
            return
        _pin = self.pin_entry.get()
        f_name = self.first_entry.get()
        l_name = self.last_entry.get()
        if f_name and l_name:

            name_val = ','.join([l_name,f_name])
            last_check = messagebox.askyesno(
                "Confirm Employee Entry",
                '\n'.join([name_val, _pin, "Confirm the following employee info?"]))

            if last_check:
                sql_statement = """INSERT INTO employee (password, name)
                    VALUES (?,?)"""
                with sqlite3.connect('OrderUP.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql_statement, (_pin, name_val))

                self.first_entry.delete('0', 'end')
                self.last_entry.delete('0', 'end')
                self.pin_entry.delete('0', 'end')
            else:
                return
        else:
            messagebox.showerror(
                "Name Error",
                "Please enter a name to associate with the PIN."
            )

if __name__ == '__main__':
    main = EmployeeMainTk()
    main.mainloop()
