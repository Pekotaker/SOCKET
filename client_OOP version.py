import socket
import threading

# --------SECTION A--------
FORMAT = 'utf-8'
BUFFER_SIZE = 8192
COMMAND_DISCONNECT = "!disconnect"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 12345

# --------SECTION B--------
def isDisconnectMessage(str):
    if str == COMMAND_DISCONNECT:
        return True
    else:
        return False

# --------SECTION C--------
class MyClient():
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server_host = host
        self.server_port = port
        self.socket = None
        self.is_active = False
        self.thread = []

    def getAddress(self):
        # Prompts to enter
        self.server_host = input("Enter host IP: ")
        self.server_port = input("Enter PORT: ")

        # If port is not blank AND is only number
        if self.server_port.__len__() > 0 and self.server_port.isnumeric() == True:
            self.server_port = int(self.server_port)
        else:
            # Future code here
            self.server_port = DEFAULT_PORT

    def connect(self):
        adr = (self.server_host, self.server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connects to the host's IP address with the Port number
            self.socket.connect(adr)

            self.is_active = True

            print(f"Connected to {self.server_host} successfully.")

            receive_thread = threading.Thread(target=self.receive, name="Receive")
            send_thread = threading.Thread(target=self.process, name="Send")

            # self.thread.append(receive_thread)
            # self.thread.append(send_thread)

            # Starts threads
            receive_thread.start()
            send_thread.start()

            # Program will exit once all threads are done
            #send_thread.join()
            #receive_thread.join()
        except:
            print(f"Cannot connect to {self.server_host}:{self.server_port}")


        # Trinh Le Nguyen Vu: Moved below commands to the end of 
        # the receive thread and in the exception section of the
        # process thread

        # client.disconnect()
        # client.reset()

    def disconnect(self):
        if not self.is_active:
            self.send(COMMAND_DISCONNECT)

        self.socket.close()
        print(f"[SERVER] {self.server_host} Disconnected")

    def reset(self):
        self.socket.close()
        self.is_active = False
        self.socket = None
        self.thread.clear()

    def receive(self):
        """
        1. Receive message from server
        2. If message is !disconnect
            Disconnect
        3. Print message
        """
        while True:
            try:
                msg = self.socket.recv(BUFFER_SIZE).decode(FORMAT)

                should_print = False
                if msg.__len__() > 0:
                    should_print = True

                # If server wants to terminate
                if isDisconnectMessage(msg):
                    self.is_active = False

                    break

                if should_print:
                    print(f"[SERVER] {msg}")
            except OSError:
                print("Error! Most likely losing connection to server (receive)")

                break

        # Tring Le Nguyen Vu: added this from the connect thread
        # ------------------------
        client.disconnect()
        client.reset()
        print("All finished")
        # ------------------------

    def send(self, msg):
        try:
            self.socket.sendall(msg.encode(FORMAT))
        except OSError:
            print("Can't send message to server (send)")
            self.is_active = False

            return False

        return True

    def process(self):
        """
        1. Always wait for input
        2. Send message
            If can't send, exit
        """
        try:
            while self.is_active:
                # Future code here (needs to have a timeout for this)
                msg = input()

                # Sending to server. And check whether sending successfully
                if not self.send(msg):
                    self.is_active = False

                    break
        except OSError:
            print("Something terrible happened (process)")
            # Tring Le Nguyen Vu: added this from the connect thread
            # ------------------------
            client.disconnect()
            client.reset()
            print("All finished")
            # ------------------------
           
        

# --------SECTION D--------
client = MyClient()

# client.getAddress()
MAIN_THREAD = threading.Thread(target = client.connect)
MAIN_THREAD.start()
MAIN_THREAD.join()

# 
