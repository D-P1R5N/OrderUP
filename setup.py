import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("OrderUP Setup Window")
        self.resizable(False,False)
        self.geometry("+800+0")

        self.db_iFrame = ttk.LabelFrame(self, text="Input DB Info Here")
        self.db_iFrame.grid(row=0,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,E,S,W')

        self.text_frame = ttk.LabelFrame(self.db_iFrame, text="Read Me")
        self.text_frame.grid(row=0,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,E,S,W',columnspan=2)

        self.readme_text = tk.Text(self.text_frame)
        self.readme_text.grid(row=0,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,E,S,W')
        self.readmeAppend()


        self.build_button = ttk.Button(self.db_iFrame, text = 'Run', command = self.setup_db)
        self.build_button.grid(row=1,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky="W")

        self.close_button = ttk.Button(self.db_iFrame, text='Close', command = self.destroy)
        self.close_button.grid(row=1,column=1,ipadx=2,ipady=2,padx=2,pady=2, sticky="E")


    def readmeAppend(self):
        with open('readme.txt', 'r', 8192) as reader:
            _r = reader.read(4096)
            self.readme_text.insert('end', _r)
        self.readme_text['state'] = 'disabled'



    def setup_db(self):
        conn = None;
        try:
            with sqlite3.connect('OrderUP.db') as conn:
                #print(sqlite3.version)
                self.create_table_statements(conn)
                self.create_table_defaults(conn)
                messagebox.showinfo("Database Created",
                'The OrderUP database has been created.')
                self.build_button['state'] = 'disabled'

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    def create_table_statements(self, conn):
        sql_table_employee = """CREATE TABLE IF NOT EXISTS employee (
        password text PRIMARY KEY,
        name text NOT NULL
        );"""

        sql_table_items = """CREATE TABLE IF NOT EXISTS item (
        item_name text PRIMARY KEY,
        item_price text NOT NULL,
        sub_cat_id integer NOT NULL,
        description text NOT NULL,
        FOREIGN KEY (sub_cat_id) REFERENCES sub_cat (id)

        );"""

        sql_main_cat = """CREATE TABLE IF NOT EXISTS main_cat (
        id integer PRIMARY KEY,
        title text NOT NULL
        );"""

        sql_sub_cat = """CREATE TABLE IF NOT EXISTS sub_cat (
        id integer PRIMARY KEY,
        title text NOT NULL,
        main_cat_id integer NOT NULL,
        FOREIGN KEY (main_cat_id) REFERENCES main_cat (id)
        );"""

        sql_kitchen_active_orders = """CREATE TABLE IF NOT EXISTS active_orders (
        table_num integer PRIMARY KEY,
        ticket_info blob NOT NULL,
        time integer NOT NULL,
        date text NOT NULL
        );"""

        sql_customer_sales = """CREATE TABLE IF NOT EXISTS customer_sales (
        id integer PRIMARY KEY,
        date text NOT NULL,
        time integer NOT NULL,
        payment_total real NOT NULL,
        payment_type text NOT NULL
        );"""



        statements = [
            sql_table_employee,
            sql_table_items,
            sql_main_cat,
            sql_sub_cat,
            sql_kitchen_active_orders,
            sql_customer_sales]

        cur = conn.cursor()
        for state in statements:

            cur.execute(state)

    def create_table_defaults(self, conn):
        cur = conn.cursor()

        sql_emps = """INSERT INTO employee (password, name)
            VALUES ('0000', 'DEFAULT')"""

        cur.execute(sql_emps)

        main_values = [
        (1, 'Food'),
        (2,'Drink')]

        for _m in main_values :
            m_id, m_title = _m
            sql_mains = """INSERT INTO main_cat (id, title)
                VALUES (?,?)"""
            cur.execute(sql_mains, (m_id, m_title))

        sub_values = [
        (1, 'Appetizer', 1),
        (2, 'Entree', 1),
        (3, 'Dessert', 1),
        (4, 'Soft', 2),
        (5, 'Beer & Wine', 2),
        (6, 'Spirits & Mixed', 2)]

        for _s in sub_values:
            s_id, s_title, s_m_id = _s
            sql_subs = """INSERT INTO sub_cat (id, title, main_cat_id)
                VALUES (?,?,?)"""
            cur.execute(sql_subs, (s_id, s_title, s_m_id))



if __name__ == '__main__':
    main_tk = Main()
    main_tk.mainloop()
