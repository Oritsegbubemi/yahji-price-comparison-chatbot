# -*- coding: utf-8 -*-
###############################################################################
import sqlite3

conn = sqlite3.connect("Nicole.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS items(chat_id TEXT, message TEXT)")

def data_entry(arg):
    c.execute("INSERT INTO items VALUES(?,?)",
              (arg[0], arg[1]))
    conn.commit()

def read_data(arg):
    c.execute("SELECT * FROM items WHERE chat_id='{}'".format(arg))
    data = c.fetchall()
    return data
###############################################################################

if __name__ == "__main__":
    create_table()
    arg = [str(233232), "stuff message"]
    data_entry(arg)
    

    #d = read_data(arg1)
    #c.close()

