# For socket and multithreading
import socket
import threading

# For parsing data
import ssl
import json
import sched, time
from datetime import date

# for login and registing
import sqlite3

# For beautiful GUI
import tkinter

"""-------COMMANDS LIST-------"""
COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"


"""---DEFAULT CONFIGURATION---"""
BUFFER_SIZE = 8192
FORMAT = 'utf-8'
DEFAULT_PORT = 55000
DEFAULT_HOST = "127.0.0.1"
EXCHANGE_RATE_DATABASE = "ExchangeData.db"
USER_LOGIN_DATABASE = "Users.db"
GETTING_DATA_INTERVAL = 1800 # seconds


"""---------MAIN BODY---------"""
class SERVER():

    '''-------MAIN FUNCTIONS-------'''
    #---------------------------------------------------------------------------------------------------------#
    def __init__(self):
        self.bufsize = BUFFER_SIZE
        self.format = FORMAT
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.addr = (self.host, self.port)
        self.exchange_data = EXCHANGE_RATE_DATABASE
        self.users_data = USER_LOGIN_DATABASE
        self.interval = GETTING_DATA_INTERVAL

        self.datelist = []
        self.banklist = {"vcb", "ctg", "tcb", "bid", "stb", "sbv"}
        self.log = {}
        self.clients = {}
        self.addresses = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
 
    # For sending commands to all clients
    def command_thread(self):
        while True:
            msg = input()
            self.message_all(msg)

    # Listening for connections
    def accept_connections(self):
        # Listening for incoming connections
        self.server.listen()
        print(f"[{self.host}:{self.port}] Listening...")

        while True:

            # Store socket information and addresses returned by the server.accept() function
            client, addr = self.server.accept()
            print(f"[{addr}] connected")
            
            self.addresses[client] = addr
            self.clients[client] = client
            try:
                # Handling the socket in a new thread
                thread = threading.Thread(target=self.registering, args = (client,))
                # This function will open a new thread and run the whatever 
                # in the attribute 'target' with the parameters in 'args'
                # in that newly opened thread
    
                # #Start the thread
                thread.start()
            except OSError:
                pass
    
    # Log In and Sign Up
    def registering(self, client):
        # Choice: Log in or Sign Up?
        self.log[client] = 0
        choice = ""
        try:
            client.send(f"Log In or Sign Up?\nType '{COMMAND_LOG_IN}' or '{COMMAND_SIGN_UP}'".encode(self.format))  
            choice = client.recv(self.bufsize).decode(self.format)
            while (choice != COMMAND_LOG_IN) and (choice != COMMAND_SIGN_UP):
                if choice != COMMAND_DISCONNECT:
                    client.send("Syntax Error. Type again".encode(self.format))
                    choice = client.recv(self.bufsize).decode(self.format)
                else:
                    client.send(COMMAND_DISCONNECT.encode(self.format))
                    break
        except OSError:
            pass
            
        if choice != "" and choice != COMMAND_DISCONNECT:
            # Log In
            self.log[client] = 1
            if choice == COMMAND_LOG_IN:
                database = sqlite3.connect(self.users_data)
                c = database.cursor()
                
                try:
                    #Ask for username and password
                    client.send("Username: ".encode(self.format))
                    username = client.recv(self.bufsize).decode(self.format)
                    if username != COMMAND_DISCONNECT:
                        try:   
                            client.send("Password: ".encode(self.format))
                            password = client.recv(self.bufsize).decode(self.format)
                            if password != COMMAND_DISCONNECT:

                                # Find existing username and corresponding password
                                c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))
                                
                                # If not found, login again
                                while not c.fetchall():
                                    self.log[client] = 0
                                    try:
                                        client.send("Logged in failed. Try again".encode(self.format))
                                        client.send("Username: ".encode(self.format))
                                        
                                        try:
                                            username = client.recv(self.bufsize).decode(self.format)
                                            if username == COMMAND_DISCONNECT:
                                                client.send(COMMAND_DISCONNECT.encode(self.format))
                                                self.log[client] = 0
                                                break
                                        except OSError:
                                            self.log[client] = 0
                                        client.send("Password: ".encode(self.format))
                                        try:
                                            password = client.recv(self.bufsize).decode(self.format)
                                            if password == COMMAND_DISCONNECT:
                                                self.log[client] = 0
                                                client.send(COMMAND_DISCONNECT.encode(self.format))
                                                break
                                        except OSError:
                                                self.log[client] = 0
                                        
                                        self.log[client] = 1
                                        c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))
                                    except OSError:
                                        self.log[client] = 0
                                
                                if self.log[client] == 1:
                                    # if found, handle the client in client_handle()
                                    print(f"[{username}] Logged in successfully")
                                    database.close()
                                    self.client_handle(client, username)
                                else:
                                    database.close()  
                            else:
                                self.log[client] = 0
                                client.send(COMMAND_DISCONNECT.encode(self.format))
                                database.close()
                        except OSError:
                            self.log[client] = 0
                    else:
                        self.log[client] = 0
                        client.send(COMMAND_DISCONNECT.encode(self.format))
                        database.close()
                except OSError:
                    self.log[client] = 0

            # Sign Up 
            if choice == COMMAND_SIGN_UP:
                database = sqlite3.connect(self.users_data)
                c = database.cursor()

                try:
                    #Ask for username
                    client.send("Username: ".encode(self.format))
                    try:
                        username = client.recv(self.bufsize).decode(self.format)
                        if username != COMMAND_DISCONNECT:
                            # Is the username already exist?
                            c.execute('SELECT * FROM database WHERE username = ?', (username,))
                            # If yes, then sign up failed, sign up again
                            while c.fetchall():
                                self.log[client] = 0
                                client.send(f"{username} already existed. Try again".encode(self.format))
                                client.send("Username: ".encode(self.format))
                                try:
                                    username = client.recv(self.bufsize).decode(self.format)
                                    if username == COMMAND_DISCONNECT:
                                        self.log[client] = 0
                                        client.send(COMMAND_DISCONNECT.encode(self.format))
                                        break
                                    c.execute('SELECT * FROM database WHERE username = ?', (username,))
                                    self.log[client] = 1
                                except OSError:
                                    self.log[client] = 0
                            
                            if self.log[client] == 1:
                                # if no, then ask for a password, add new username and password to the database
                                client.send("Password: ".encode(self.format))
                                try:
                                    password = client.recv(self.bufsize).decode(self.format)
                                    if password != COMMAND_DISCONNECT:
                                        c.execute("INSERT INTO database (username, password) \
                                            VALUES ('"+ username + "', '" + password + "')")
                                        database.commit()

                                        # and then handle the client in client_handle()
                                        print(f"[{username}] Signed up successfully")
                                        database.close()
                                        self.client_handle(client, username)
                                    else:
                                        self.log[client] = 0
                                        client.send(COMMAND_DISCONNECT.encode(self.format))
                                        database.close()
                                except OSError:
                                    self.log[client] = 0
                            else:
                                database.close()
                        else:
                            self.log[client] = 0
                            client.send(COMMAND_DISCONNECT.encode(self.format))
                            database.close()
                    except OSError:
                        self.log[client] = 0
                except OSError:
                    self.log[client] = 0
        if self.log[client] == 1:
                print(f"[{self.clients[client]}] Disconnected.") 
                del self.clients[client]
                del self.addresses[client]
                self.log[client] = 0
                client.close()
        else:
            print(f"[{self.addresses[client]}] Disconnected")
            del self.addresses[client]
            client.close()  

    # Handle individual clients after registering
    def client_handle(self,client, username):
        try:
            # Store login information for temporary use: username will be used as display name in chat  
            self.clients[client] = username
            self.log[client] = 1
            client.send(f"Welcome {username}!\nType '{COMMAND_DISCONNECT}' to quit.\nType '{COMMAND_REQUEST_DATA}' to request data.".encode(self.format))

            active = True
            while (active):
                try:
                    msg = client.recv(self.bufsize).decode(self.format)
                    if msg != COMMAND_DISCONNECT:
                        if msg == COMMAND_REQUEST_DATA:
                            
                            date = ""
                            bank = ""

                            # Select a date
                            client.send("Select a date: ".encode(self.format))
                            # Send a list of available dates
                            for items in self.datelist:
                                client.send(f"\r\n{items}".encode(self.format))
                            try:
                                msg = client.recv(self.bufsize).decode(self.format)
                                if msg == COMMAND_DISCONNECT:
                                    active = False
                                    break
                                else:
                                    date = str(msg)
                            except OSError:
                                active = False
                                break
                            
                            # Select a bank
                            client.send("Select a bank: ".encode(self.format))
                            # Send a list of available banks
                            for items in self.banklist:
                                client.send(f"\r\n{items}".encode(self.format))
                            try:
                                msg = client.recv(self.bufsize).decode(self.format)
                                
                                if msg == COMMAND_DISCONNECT:
                                    active = False
                                    break
                                else: 
                                    bank = str(msg)
                            except OSError:
                                active = False
                                break

                            
                            if (date != "") and (bank != ""):
                                self.return_data(client, date, bank)

                except OSError:
                    active = False
            
        except OSError:
            pass
    
    # Periodically getting data by scheduling tasks using recursion
    def get_data(self):
        
        # Get available dates
        ExchangeRate = sqlite3.connect(self.exchange_data)
        c = ExchangeRate.execute("SELECT date, bank, data from database")
        for row in c:
            if (row[0] not in self.datelist):
                self.datelist.append(row[0])
        ExchangeRate.close()

        # scheduling tasks
        scheduler = sched.scheduler(time.time, time.sleep)
        def periodic(scheduler, interval):
            scheduler.enter(interval, 1, periodic, (scheduler, interval))
            self.update_data()       
            scheduler.run()
        periodic(scheduler, self.interval)
         
    # Get the data from database and return it to users     
    def return_data(self, client, date, bank):
        # Open Exchange Rate database
        data = ""
        ExchangeData = sqlite3.connect(self.exchange_data)
        cursor = ExchangeData.execute('SELECT * FROM database WHERE date = ? AND bank = ?', (date, bank))

        if cursor:
            for row in cursor:
                data = json.loads(row[2])
            try: 


                client.send("Select a currency: ".encode(self.format))
                for items in data["results"]:
                    client.send(f"\r\n{items['currency']}".encode(self.format))

                try:
                    msg = client.recv(self.bufsize).decode(self.format)      
                    if msg != COMMAND_DISCONNECT:
                        currency = str(msg)
                except OSError:
                    pass

                if msg != COMMAND_DISCONNECT:        
                    found = False
                    for items in data["results"]:
                        if items['currency'] == currency:
                            found = True
                            for element in items:
                                if element != "currency" and element != "Currency":
                                    client.send(f"\r\n{element}: {items[element]}".encode(self.format))
                            break
                    if found == False:
                        client.send("Currency not found".encode(self.format))
                else:
                    pass
            except OSError:
                pass        
        else:
            client.send("Data not found. ".encode(self.format))
    #---------------------------------------------------------------------------------------------------------#


    '''-------MISC FUNCTIONS-------'''
    #---------------------------------------------------------------------------------------------------------#
    # Sending message to all clients
    def message_all(self, msg):
        try:
            for sock in self.addresses:
                sock.send(msg.encode(self.format))
        except OSError:
            pass

    # Insert data into Exchange Rate database
    def insert_data(self, date, bank, data):
        # Open Exchange Rate database
        ExchangeData = sqlite3.connect(self.exchange_data)
        c = ExchangeData.cursor()
        c.execute("INSERT INTO database (date, bank, data) \
            VALUES ('" + date + "', '" + bank + "', '" + data + "')")
        ExchangeData.commit()
        ExchangeData.close()
    
    # Sending requests and call 'insert_data()'
    def update_data(self):

        # Get current date
        today = str(date.today())

        # HOST and port address
        host = "vapi.vnappmob.com"
        address = (host, 443)

        # Wrapper with default settings
        context = ssl.create_default_context()

        # Create and connect to SSL socket
        ssl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(ssl_socket, server_hostname=host)
        conn.connect(address)

        # API request syntax
        get_API_request = f"GET /api/request_api_key?scope=exchange_rate HTTP/1.1\r\nHost: {host} \r\n\r\n"


        # Request API key
        conn.sendall(get_API_request.encode(self.format))
        API_key = conn.recv(self.bufsize).decode(self.format)

        # Remove API header
        index = API_key.find("{")
        temp1 = API_key[index:]
        temp2 = json.loads(temp1)
        API_key = temp2["results"]

        # Delete today's data
        ExchangeData = sqlite3.connect(self.exchange_data)
        ExchangeData.execute("DELETE FROM database WHERE date = ?", (today,))
        ExchangeData.commit()
        ExchangeData.close()

        # Send request of all the bank:
        for bank in self.banklist:
                
            # Data request syntax
            get_data_request = f"GET /api/v2/exchange_rate/{bank} HTTP/1.1\r\nHost: {host}\r\nAccept: application/json\r\nAuthorization: Bearer {API_key}\r\n\r\n"
                
            # Request data
            conn.sendall(get_data_request.encode(self.format))
            
            # This will receive the header, we don't need that
            temp1 = conn.recv(self.bufsize).decode(self.format)
            # This will receive the data, which is what we want
            data = conn.recv(self.bufsize).decode(self.format)
            
            # Insert new data into Exchange Rate database
            self.insert_data(today, bank, data)
    #---------------------------------------------------------------------------------------------------------#
    
server = SERVER()

# thread for 'command_thread()'
MAIN_THREAD = threading.Thread(target = server.command_thread)
MAIN_THREAD.start()

# thread for periodically getting data
GET_DATA_THREAD = threading.Thread(target = server.get_data)   
GET_DATA_THREAD.start()

# thread to handle incoming connections
ACCEPT_THREAD = threading.Thread(target=server.accept_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()

