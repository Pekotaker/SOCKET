#For socket and multithreading
import socket
import threading

#For parsing data
from urllib.request import Request, urlopen
import json

#For beautiful GUI
import tkinter

BUFFER_SIZE = 1024
DISCONNECT_MESSAGE = "!disconnect"
FORMAT = 'utf-8'

PORT = 33000
HOST = "127.0.0.1"
ADDR = (HOST, PORT)

def request_data(client, bank):
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

def client_handle(client):
    try: 
        name = client.recv(BUFFER_SIZE).decode(FORMAT)
        print(f"[SERVER] {addresses[client]} has changed their name to {name}")
        client.send(f"Welcome {name}, Type {DISCONNECT_MESSAGE} if you want to quit.".encode(FORMAT))
        clients[client] = name
        active = True
        while active:
            try:
                msg = client.recv(BUFFER_SIZE).decode(FORMAT)
                if msg != DISCONNECT_MESSAGE:
                    print(f"[{name}] chat: {msg}")
                    if msg == "request data":
                        client.send("Select a bank\nNgan hang Nha nuoc: sbv\nVietcombank       : vcb\nViettinbank       : ctg\nTechcombank       : tcb\nBIDV              : bid\nSacombank         : stb\n".encode(FORMAT))
                        try:
                            bank = client.recv(BUFFER_SIZE).decode(FORMAT)
                            print(bank)
                            request_data(client, bank)
                        except OSError:
                            pass
                else:
                    active = False
                    print(f"[{name}] Disconnected.")
                    client.close()
                    del clients[client]
            except OSError:
                active = False
                print(f"[{name}] Disconnected.")
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
            client.send("Type your name to enter: ".encode(FORMAT))
            addresses[client] = addr
            thread = threading.Thread(target=client_handle, args = (client,))
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
            for sock in clients:
                sock.send(msg.encode(FORMAT))



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Successfully created socket")
server.bind(ADDR)
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