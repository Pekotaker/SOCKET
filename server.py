# For socket and multithreading
import socket
import threading

# For parsing data
import ssl
import json

# for login and registing
import sqlite3

# For beautiful GUI
import tkinter

COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"

BUFFER_SIZE = 8192
FORMAT = 'utf-8'

PORT = 12345
HOST = "127.0.0.1"
ADDR = (HOST, PORT)

# Log in and Sign Up
def registering(client, addr):
    # Choice: Log in or Sign Up?
    log[client] = 0
    choice = ""
    try:
        client.send(f"Log In or Sign Up?\nType '{COMMAND_LOG_IN}' or '{COMMAND_SIGN_UP}'".encode(FORMAT))  
        choice = client.recv(BUFFER_SIZE).decode(FORMAT)
        while (choice != COMMAND_LOG_IN) and (choice != COMMAND_SIGN_UP):
            if choice != COMMAND_DISCONNECT:
                client.send("Syntax Error. Type again".encode(FORMAT))
                choice = client.recv(BUFFER_SIZE).decode(FORMAT)
            else:
                break
    except OSError:
        pass
        
    if choice != "" and choice != COMMAND_DISCONNECT:
        log[client] = 1
    # Log In
        if choice == COMMAND_LOG_IN:
                
            database = sqlite3.connect('Users.db')
            c = database.cursor()
            #Ask for username and password
            try:
                client.send("Username: ".encode(FORMAT))
                username = client.recv(BUFFER_SIZE).decode(FORMAT)
                if username != COMMAND_DISCONNECT:
                    try:   
                        client.send("Password: ".encode(FORMAT))
                        password = client.recv(BUFFER_SIZE).decode(FORMAT)
                        if password != COMMAND_DISCONNECT:

                            # Find existing username and corresponding password
                            c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))
                            
                            # If not found, login again
                            while not c.fetchall():
                                log[client] = 0
                                client.send("Logged in failed. Try again".encode(FORMAT))
                                client.send("Username: ".encode(FORMAT))
                                try:
                                    username = client.recv(BUFFER_SIZE).decode(FORMAT)
                                    if username == COMMAND_DISCONNECT:
                                        break
                                    client.send("Password: ".encode(FORMAT))
                                    try:
                                        password = client.recv(BUFFER_SIZE).decode(FORMAT)
                                        if password == COMMAND_DISCONNECT:
                                            break
                                    except OSError:
                                        log[client] = 0
                                except OSError:
                                    log[client] = 0
                                c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))
                                print(username)
                                log[client] = 1
                            if log[client] == 1:
                                # if found, handle the client in client_handle()
                                print(f"[{username}] Logged in successfully")
                                log[client] = 1
                                database.close()
                                client_handle(client, username)
                            else:
                                database.close()  
                        else:
                            database.close()
                    except OSError:
                        log[client] = 0
                else:
                    database.close()
            except OSError:
                log[client] = 0

    # Sign Up 
        if choice == COMMAND_SIGN_UP:
            database = sqlite3.connect('Users.db')
            c = database.cursor()

            try:
                #Ask for username
                client.send("Username: ".encode(FORMAT))
                try:
                    username = client.recv(BUFFER_SIZE).decode(FORMAT)
                    if username != COMMAND_DISCONNECT:
                        # Is the username already exist?
                        c.execute('SELECT * FROM database WHERE username = ?', (username,))
                        # If yes, then sign up failed, sign up again
                        while c.fetchall():
                            log[client] = 0
                            client.send(f"{username} already existed. Try again".encode(FORMAT))
                            client.send("Username: ".encode(FORMAT))
                            try:
                                username = client.recv(BUFFER_SIZE).decode(FORMAT)
                                if username == COMMAND_DISCONNECT:
                                    break
                                c.execute('SELECT * FROM database WHERE username = ?', (username,))
                                log[client] = 1
                            except OSError:
                                log[client] = 0
                        
                        if log[client] == 1:
                            # if no, then ask for a password, add new username and password to the database
                            client.send("Password: ".encode(FORMAT))
                            try:
                                password = client.recv(BUFFER_SIZE).decode(FORMAT)
                                if password != COMMAND_DISCONNECT:
                                    c.execute("INSERT INTO database (username, password) \
                                        VALUES ('"+ username + "', '" + password + "')")
                                    database.commit()

                                    # and then handle the client in client_handle()
                                    print(f"[{username}] Signed up successfully")
                                    log[client] = 1
                                    database.close()
                                    client_handle(client, username)
                                else:
                                    database.close()
                            except OSError:
                                log[client] = 0
                        else:
                            database.close()
                    else:
                        database.close()
                except OSError:
                    log[client] = 0
            except OSError:
                log[client] = 0
    else:
        pass
    if log[client] == 1:
        print(f"[{clients[client]}] Disconnected")
    else:
        print(f"[{addr}] Disconnected")
    log[client] = 0
    client.close()
    
# Getting API keys and Return data
def return_data(client, bank):
    try:
        # HOST and port address
        host = "vapi.vnappmob.com"
        ADDR = (host, 443) 

        # Wrapper with default settings
        context = ssl.create_default_context()
            
        # Create and connect to SSL socket
        ssl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(ssl_socket, server_hostname=host)
        conn.connect(ADDR)

        # API request syntax
        get_API_request = f"GET /api/request_api_key?scope=exchange_rate HTTP/1.1\r\nHost: {host} \r\n\r\n"

        # Request API key
        conn.sendall(get_API_request.encode(FORMAT))
        API_key = conn.recv(BUFFER_SIZE)

        # Remove API header
        index = API_key.find(bytes("{",FORMAT))
        temp1 = API_key[index:]
        temp2 = json.loads(temp1)
        API_key = temp2["results"]

        # Data request syntax
        get_data_request = f"GET /api/v2/exchange_rate/{bank} HTTP/1.1\r\nHost: {host}\r\nAccept: application/json\r\nAuthorization: Bearer {API_key}\r\n\r\n"

        # Request data
        conn.sendall(get_data_request.encode(FORMAT))
        
        # This will receive the header, we dont need that
        temp1 = conn.recv(BUFFER_SIZE)
        # This will receive the data, which is what we want
        temp1 = conn.recv(BUFFER_SIZE)
        temp2 = json.loads(temp1)

        # Client will choose a currency:
        #   Send the list of available currency in the chosen bank
        try:
            client.send("Choose a currency".encode(FORMAT))
            for items in temp2["results"]:
                client.send(f"\r\n{items['currency']}".encode(FORMAT))

            try:
                currency = client.recv(BUFFER_SIZE).decode(FORMAT)
                print(f"[{clients[client]}] chat: {currency}")
            except OSError:
                pass
        except OSError:
            pass

        #   Find the currency and send the data to the client
        try:
            found = False
            for items in temp2["results"]:
                if items['currency'] == currency:
                    found = True
                    client.send(f"Currency: {currency}".encode(FORMAT))
                    for element in items:
                        if element != "currency" and element != "Currency":
                            client.send(f"\r\n{element}: {items[element]}".encode(FORMAT))
                    break
            if found == False:
                client.send("Currency not found".encode(FORMAT))
        except OSError:
            pass      
    except OSError:
        pass

# Handle idividual connections
def client_handle(client, username):
    try:

        # Store login information for temporary use: username will be used as display name in chat  
        clients[client] = username
        log[client] = 1
        client.send(f"Welcome {username}!\nType '{COMMAND_DISCONNECT}' to quit.\nType '{COMMAND_REQUEST_DATA}' to request data.".encode(FORMAT))

        active = True
        while active:
            try:

                # Receive messages from clients
                msg = client.recv(BUFFER_SIZE).decode(FORMAT)

                # If client doesn't type in 'COMMAND_DISCONNECT'
                if msg != COMMAND_DISCONNECT:
                    print(f"[{username}] chat: {msg}")
                    if msg == COMMAND_REQUEST_DATA:
                        client.send("Select a bank\nNgan hang Nha nuoc: sbv\nVietcombank       : vcb\nViettinbank       : ctg\nTechcombank       : tcb\nBIDV              : bid\nSacombank         : stb\n".encode(FORMAT))
                        try:
                            bank = client.recv(BUFFER_SIZE).decode(FORMAT)
                            while bank not in banklist:
                                try:
                                    if bank != COMMAND_DISCONNECT:
                                        client.send("Bank not found. Try again".encode(FORMAT))
                                        bank = client.recv(BUFFER_SIZE).decode(FORMAT)
                                    else:
                                        active = False
                                        break
                                except OSError:
                                    pass
                            if bank != COMMAND_DISCONNECT:
                                print(f"[{username}] chat: {bank}")
                                return_data(client, bank)
                            print("shit0")
                        except OSError:
                            pass
                        print("shit1")
                
                # If they type 'COMMAND_DISCONNECT'
                else:
                    active = False
                print("shit2")

            # If clients suddenly turn off in this step       
            except OSError:
                active = False
            print("shit3")
    
    # If clients suddenly turn off in this step
    except OSError:  
        pass
    print("shit4")

# Listening to connection and handling multithreading        
def accept_connections():

    # Listening for incoming connections
    server.listen()
    print(f"[{HOST}:{PORT}] Listening...")

    while True:

        # Store socket information and addresses returned by the server.accept() function
        client, addr = server.accept()
        print(f"[{addr}] connected")
        
        addresses[client] = addr
        clients[client] = client
        try:
            # Handling the socket in a new thread
            thread = threading.Thread(target=registering, args = (client, addr))
            # This function will open a new thread and run the whatever 
            # in the attribute 'target' with the parameters in 'args'
            # in that newly opened thread
 
            # #Start the thread
            thread.start()
        except OSError:
            if log[client] == 1:
                print(f"[{client}] Disconnected.") 
            else:
                print(f"[{addresses[client]}] Disconnected")
                log[client] = 0
                client.close()                    
            pass
# Basically a different, independent thread purely for sending messages to all the clients
def main_thread():
    while True:
        msg = input()
        message_all(msg)

# Send message to all clients
def message_all(msg):
    try:
        for sock in addresses:
            sock.send(msg.encode(FORMAT))
    except OSError:
        pass

# Create Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Created socket")
server.bind(ADDR)

# Store clients and addresses

banklist = {"vcb", "ctg", "tcb", "bid", "stb", "sbv"}
log = {}
clients = {}
addresses = {}

if __name__ == "__main__":
    print("Server started")

    # thread for 'main_thread()'
    MAIN_THREAD = threading.Thread(target = main_thread)
    MAIN_THREAD.start()    

    # thread to handle incoming connections
    ACCEPT_THREAD = threading.Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()