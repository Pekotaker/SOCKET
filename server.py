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

CHOICE_LOGIN = "!login"
CHOICE_SIGN_UP = "!signup"

BUFFER_SIZE = 1024
DISCONNECT_MESSAGE = "!disconnect"
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
        client.send(f"Login or Sign Up?\nType '{CHOICE_LOGIN}' or '{CHOICE_SIGN_UP}'".encode(FORMAT))  
        
        choice = client.recv(BUFFER_SIZE).decode(FORMAT)
        while (choice != CHOICE_LOGIN) and (choice != CHOICE_SIGN_UP):
            if choice != DISCONNECT_MESSAGE:
                client.send("shit".encode(FORMAT))
                choice = client.recv(BUFFER_SIZE).decode(FORMAT)
            else:
                pass

        #Login
        if choice == CHOICE_LOGIN:

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
        if choice == CHOICE_SIGN_UP:

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
        

def return_data(client, bank):
    try:
        URL_getData = f"https://vapi.vnappmob.com/api/v2/exchange_rate/{bank}"
        URL_getAPI = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"
        api_key = json.loads(urlopen(Request(URL_getAPI)).read())['results']
        r = Request(URL_getData)
        r.add_header('Authorization', 'Bearer ' + api_key)
        data = json.loads(urlopen(r).read())
        data = str(data)
        client.send(data.encode(FORMAT))
    except OSError:
        pass

def client_handle(client, username):
    try:
        client.send(f"Welcome {username}, Type {DISCONNECT_MESSAGE} if you want to quit.".encode(FORMAT))
        clients[client] = username
        active = True
        while active:
            try:
                msg = client.recv(BUFFER_SIZE).decode(FORMAT)
                if msg != DISCONNECT_MESSAGE:
                    print(f"[{username}] chat: {msg}")
                    if msg == "request data":
                        client.send("Select a bank\nNgan hang Nha nuoc: sbv\nVietcombank       : vcb\nViettinbank       : ctg\nTechcombank       : tcb\nBIDV              : bid\nSacombank         : stb\n".encode(FORMAT))
                        try:
                            bank = client.recv(BUFFER_SIZE).decode(FORMAT)
                            print(bank)
                            return_data(client, bank)
                        except OSError:
                            pass
                else:
                    active = False
                    print(f"[{username}] Disconnected.")
                    client.close()
                    del clients[client]
            except OSError:
                active = False
                print(f"[{username}] Disconnected.")
                client.close()
    except OSError:
        print(f"[{addresses[client]}] Disconnected.")
        
def accept_connections():
    server.listen()
    print(f"[SERVER] [{HOST}:{PORT}] Listening...")
    while True:
        client, addr = server.accept()
        print(f"[SERVER] {addr} connected")
        try:
            addresses[client] = addr
            thread = threading.Thread(target=registering, args = (client,))
            thread.start()
        except OSError:
            print(f"[{addr}] Disconnected.")     
        
def main_thread():
    active = True
    while active:
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            for sock in clients:
                sock.send(DISCONNECT_MESSAGE.encode(FORMAT))
                sock.close()
            active = False
        else:
            message_all(msg)

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
    MAIN_THREAD = threading.Thread(target = main_thread)
    MAIN_THREAD.start()    
    ACCEPT_THREAD = threading.Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()