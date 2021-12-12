# File
socket project provip
    client_OOP version.py           : client
    server_OOP version.py           : server
    Users.db                        : Store accounts' information
    initdatabase.py                 : Initialize database.
      - Empty database by deleting everything in Users.db and ExchangeData.db using notepad, then run this file to initialize a new database
    databasechecker.py              : Run this file to check what's in Users.db and ExchangeData.db

# Commands:
COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"

# Instructions:
- Run server_OOP version.py and client_OOP version.py to start the program.
- In client_OOP version.py's terminal console, you will be required to type in the HOST (IP address) and PORT, which is 127.0.0.1 and 55000 correspondingly by default.
- After that, type in [COMMAND_LOG_IN] if you already signed up, otherwise type [COMMAND_SIGN_UP] to create a new accounts.
- Type in date, bank and currency to get data
- Type [COMMAND_DISCONECT] to end communication with the server.

# Notes:
- Client.py and Server.py are prototype version, don't bother checking them.
