#Checking database

import sqlite3

Users = sqlite3.connect('Users.db')
print("Opened database successfully")

c = Users.execute("SELECT username, password from database")
for row in c:
   print("Username:" ,row[0])
   print("Password:" ,row[1])

print("Operation done successfully")
Users.close()

ExchangeRate = sqlite3.connect('ExchangeData.db')
print("Opened database successfully")

c = ExchangeRate.execute("SELECT date, bank, data from database")
for row in c:
   print("date    :", row[0])
   print("bank    :", row[1])
   print("data:   :", row[2])

print("Operation done successfully")
ExchangeRate.close()
