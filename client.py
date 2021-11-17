import socket
import threading
import tkinter

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
COMMAND_DISCONNECT = "!disconnect"

# receive and printing messages function
def receive():
    while True:
        try:
            msg = client.recv(BUFFER_SIZE).decode(FORMAT)
            if msg:
                if msg != COMMAND_DISCONNECT:
                    print(f"[SERVER] {msg}")
                else:
                    send(COMMAND_DISCONNECT)
                    print(f"[SERVER] {HOST} Disconnected")
                    client.close()
                    break
        except OSError:
            print(f"[SERVER] {HOST} Disconnected")
            break
           
# send messages function
def send(msg):
    try:
        client.send(msg.encode(FORMAT))
    except OSError:
        pass

# main process for handling sending message
def process(event = None):
    try:
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

# If input PORT invalid, it will automatically be 33000
if not PORT:
    PORT = 12345
else:
    PORT = int(PORT)
ADDR = (HOST, PORT)

# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to the host's IP address with the Port number 
    # Stored inside the ADDR = (HOST, POST)    
    client.connect(ADDR)
    print(f"Connected to {HOST} successfully.")

    # thread for receive messages
    RECEIVE_THREAD = threading.Thread(target = receive)
    RECEIVE_THREAD.start()

    # thread for sending messages
    SEND_THREAD = threading.Thread(target = process)
    SEND_THREAD.start()
except:
    print(f"Cannot connect to {HOST}:{PORT}")









    