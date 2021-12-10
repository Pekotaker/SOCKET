# File
socket project provip
    client.py           : client
    server.py           : server
    Users.db            : Store accounts' information
    initdatabase.py     : Initialize database.
      - Empty database by deleting everything in Users.db using notepad, then run this file to initialize a new database
    databasechecker.py  : Run this file to check what's in Users.db

# Commands:
COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"

# Instructions:
- Run server_OOP version.py and client_OOP version.py to start the program.
- In client.py's terminal console, you will be required to type in the HOST (IP address) and PORT, which is 127.0.0.1 and 33000 correspondingly by default.
- After that, type in [COMMAND_LOG_IN] if you already signed up, otherwise type [COMMAND_SIGN_UP] to create a new accounts.
- Type [COMMAND_REQUEST_DATA], server.py will return the information of the exchange rate of the chosen currency of the chosen bank.
- Type [COMMAND_DISCONECT] to end communication with the server.
