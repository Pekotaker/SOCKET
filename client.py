import socket
import threading
import tkinter

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
COMMAND_DISCONNECT = "!disconnect"

def receive():
    while True:
        try:
            msg = client.recv(BUFFER_SIZE).decode(FORMAT)
            if msg:
                if msg != COMMAND_DISCONNECT:
                    print(f"[SERVER] {msg}")
                else:
                    active = False
                    print(f"[SERVER] {HOST} Disconnected")
                    client.close()
                    break
        except OSError:
            active = False
            print(f"[SERVER] {HOST} Disconnected")
            client.close()
            break
           

def send(msg):
    try:
        client.send(msg.encode(FORMAT))
    except OSError:
        pass

def process(event = None):
    try:
        #Registering
        active = True
        while active:
            msg = input()
            send(msg)
            if msg == COMMAND_DISCONNECT:
                active = False
                client.close()
    except OSError:
        print(f"[SERVER] {HOST} Disconnected")
        client.close()
                            

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
    print(f"Connected to {HOST} successfully.")
    RECEIVE_THREAD = threading.Thread(target = receive)
    RECEIVE_THREAD.start()
    SEND_THREAD = threading.Thread(target = process)
    SEND_THREAD.start()
except:
    print(f"Cannot connect to {HOST}:{PORT}")









    