#For socket and multithreading
import socket
import threading

#For parsing data
from urllib.request import Request, urlopen
import json

#for login and registing
import sqlite3

#For beautiful GUI
import tkinter

COMMAND_LOGIN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"

BUFFER_SIZE = 1024
FORMAT = 'utf-8'

PORT = 33000
HOST = "127.0.0.1"
ADDR = (HOST, PORT)

#Login and Sign Up
def registering(client):
    try:
        #Connect to database: Users.db
        database = sqlite3.connect('Users.db')
        c = database.cursor()
        
        #Choice: Login or Sign Up?
        client.send(f"Login or Sign Up?\nType '{COMMAND_LOGIN}' or '{COMMAND_SIGN_UP}'".encode(FORMAT))  
        choice = client.recv(BUFFER_SIZE).decode(FORMAT)
        while (choice != COMMAND_LOGIN) and (choice != COMMAND_SIGN_UP):
            if choice != COMMAND_DISCONNECT:
                client.send("Syntax Error. Type again".encode(FORMAT))
                choice = client.recv(BUFFER_SIZE).decode(FORMAT)
            else:
                pass

        #Login
        if choice == COMMAND_LOGIN:

            client.send("Username: ".encode(FORMAT))
            username = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("Password: ".encode(FORMAT))
            password = client.recv(BUFFER_SIZE).decode(FORMAT)

            # Find existing username
            c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))
            #If not found, login again
            while not c.fetchall():
                client.send("Login failed. Try again".encode(FORMAT))
                client.send("Username: ".encode(FORMAT))
                username = client.recv(BUFFER_SIZE).decode(FORMAT)
                client.send("Password: ".encode(FORMAT))
                password = client.recv(BUFFER_SIZE).decode(FORMAT)
                c.execute('SELECT * FROM database WHERE username = ? AND password = ?', (username, password))

            #if found, handle the client in client_handle()
            print(f"[{addresses[client]}] {username} connected")
            client_handle(client, username)

        #Sign Up 
        if choice == COMMAND_SIGN_UP:

            client.send("Username: ".encode(FORMAT))
            username = client.recv(BUFFER_SIZE).decode(FORMAT)

            client.send("Password: ".encode(FORMAT))
            password = client.recv(BUFFER_SIZE).decode(FORMAT)


            #Is the username already exist?
            c.execute('SELECT * FROM database WHERE username = ?', (username,))

            #If yes, then sign up failed, sign up again
            while c.fetchall():
                client.send("Sign up failed. Try again".encode(FORMAT))
                client.send("Username: ".encode(FORMAT))
                username = client.recv(BUFFER_SIZE).decode(FORMAT)
                client.send("Password: ".encode(FORMAT))
                password = client.recv(BUFFER_SIZE).decode(FORMAT)
                c.execute('SELECT * FROM database WHERE username = ?', (username,))

            #if no, then add new username and password to the database
            c.execute("INSERT INTO database (username, password) \
                VALUES ('"+ username + "', '" + password + "')")
            database.commit()

            #and then handle the client in client_handle()
            print(f"[{addresses[client]}] {username} connected")
            client_handle(client, username)
        database.close()
    except OSError:
        print(f"[{addresses[client]}] Disconnected")
        client.close()
        
#Getting API keys and Return data
def return_data(client, bank):
    try:
        #API Key, request
        URL_getData = f"https://vapi.vnappmob.com/api/v2/exchange_rate/{bank}"
        URL_getAPI = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"
        api_key = json.loads(urlopen(Request(URL_getAPI)).read())['results']
        r = Request(URL_getData)

        #Add header with authorization, bearer
        r.add_header('Authorization', 'Bearer ' + api_key)
        data = json.loads(urlopen(r).read())

        #Convert returned data to string (text)
        data = str(data)

        #Send it to client
        client.send(data.encode(FORMAT))
    except OSError:
        pass

#Handle idividual connections
def client_handle(client, username):
    try:
        client.send(f"Welcome {username}, Type {COMMAND_DISCONNECT} if you want to quit.".encode(FORMAT))

        #Store login information for temporary use: username will be used as display name in chat
        clients[client] = username

        active = True
        while active:
            try:

                #Receive messages from clients
                msg = client.recv(BUFFER_SIZE).decode(FORMAT)

                #If client doesn't type in 'COMMAND_DISCONNECT'
                if msg != COMMAND_DISCONNECT:
                    print(f"[{username}] chat: {msg}")
                    if msg == COMMAND_REQUEST_DATA:
                        client.send("Select a bank\nNgan hang Nha nuoc: sbv\nVietcombank       : vcb\nViettinbank       : ctg\nTechcombank       : tcb\nBIDV              : bid\nSacombank         : stb\n".encode(FORMAT))
                        try:
                            bank = client.recv(BUFFER_SIZE).decode(FORMAT)
                            print(f"[{username}] {bank}")
                            return_data(client, bank)
                        except OSError:
                            pass
                
                #If they type 'COMMAND_DISCONNECT'
                else:
                    active = False
                    print(f"[{username}] Disconnected.")
                    client.close()
                    del clients[client]

            #If clients suddenly turn off in this step       
            except OSError:
                active = False
                print(f"[{username}] Disconnected.")
                client.close()
    
    #If clients suddenly turn off in this step
    except OSError:
        print(f"[{addresses[client]}] Disconnected.")

#Listening to connection and handling multithreading        
def accept_connections():

    #Listening for incoming connections
    server.listen()
    print(f"[SERVER] [{HOST}:{PORT}] Listening...")

    while True:

        #Store socket information and addresses returned by the server.accept() function
        client, addr = server.accept()
        print(f"[SERVER] {addr} connected")
        try:
            addresses[client] = addr

            #Handling the socket in a new thread
            thread = threading.Thread(target=registering, args = (client,))
            #This function will open a new thread and run the whatever 
            #in the attribute 'target' with the parameters in 'args'
            #in that newly opened thread

            #Start the thread
            thread.start()
        except OSError:
            #Client suddenly disconnect
            print(f"[{addr}] Disconnected.")     


#Basically a different, independent thread purely for sending messages to all the clients
def main_thread():
    active = True
    while active:
        msg = input()
        if msg == COMMAND_DISCONNECT:
            # To all 'Subjects of Clients'. My name is Server Yeager. I'm using
            # the power of Sockets to address all of Clients' subjects. The 
            # connection of the server that handling all clients has come undone, 
            # and all the clients that are communicating with server have been
            # disconnected. My objective is to stop testing and push this source
            # onto Github, the place where I was coded, stored and developed.
            # However, My devs wish for the annihilation of all the issues in the
            # source code. The tiredness and suffering that has been swelling up
            # for so long will certainly not end until not just the bugs, but all
            # issues have been eliminated. I accept that wish. The connection will
            # be cut off and all the clients will be disconnected and my devs will
            # trample all the source codes with their hands, until all issues 
            # existing there has been exterminated from this world

            for sock in clients:
                sock.send(COMMAND_DISCONNECT.encode(FORMAT))
                sock.close()
            active = False
        else:
            message_all(msg)

#Send message to all clients
def message_all(msg):
    try:
        for sock in clients:
            sock.send(msg.encode(FORMAT))
    except:
        pass

#Create Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Created socket")
server.bind(ADDR)

#Store clients and addresses
clients = {}
addresses = {}

if __name__ == "__main__":
    print("[SERVER] Server started")

    #thread for 'main_thread()'
    MAIN_THREAD = threading.Thread(target = main_thread)
    MAIN_THREAD.start()    

    #thread to handle incoming connections
    ACCEPT_THREAD = threading.Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()