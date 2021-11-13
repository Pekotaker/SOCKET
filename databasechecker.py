#Checking database

import sqlite3

database = sqlite3.connect('Users.db')
print("Opened database successfully")

c = database.execute("SELECT username, password from database")
for row in c:
   print("Username:" ,row[0])
   print("Password:" ,row[1])

print("Operation done successfully")
database.close()