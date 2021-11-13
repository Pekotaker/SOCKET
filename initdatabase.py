#For initialize database.
import sqlite3

database = sqlite3.connect('Users.db')
print("Opened database successfully")

database.execute('''CREATE TABLE database
         (username      TEXT,
         password       TEXT);''')
print("Table created successfully")
database.close()