#For initialize database.
import sqlite3
"""
Users = sqlite3.connect('Users.db')
print("Opened Users database successfully")

Users.execute('''CREATE TABLE database
         (username      TEXT,
         password       TEXT);''')
print("Table created successfully")
Users.close()
"""
ExchangeData = sqlite3.connect('ExchangeData.db')
print("Opened Exchange Database successfully")

ExchangeData.execute('''CREATE TABLE database
         (date          TEXT,
         bank           TEXT,
         data           TEXT);''')
print("Table created successfully")
ExchangeData.close()
