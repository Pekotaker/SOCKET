import socket
import threading
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from os import path

# ./GUI (GUI folder in current project folder
# ../GUI (GUI folder a tier above the current project folder

# --------SECTION A (SECT A)--------
FORMAT = 'utf-8'
BUFFER_SIZE = 8192
COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 55000
MISC_FOLDER_NAME = "Misc"
sys.path.append(path.join(path.dirname(__file__),MISC_FOLDER_NAME))
import guiRequest, guiSignUp, guiSignIn, guiConnect

# --------SECTION B (SECT B)--------
def isDisconnectMessage(str):
    if str == COMMAND_DISCONNECT:
        return True
    else:
        return False

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
username = ""


def showSignIn():
    client.send2(COMMAND_LOG_IN)
    global ui
    ui = guiSignIn.UI_MainWindow()
    ui.setupUi(MainWindow)

    # Trigger a function on button press
    ui.createAccount.clicked.connect(showSignUp)
    ui._login.clicked.connect(processSignIn)

    MainWindow.show()

def showSignUp():
    if client.send2(COMMAND_SIGN_UP):
        global ui
        ui = guiSignUp.UI_MainWindow()
        ui.setupUi(MainWindow)

        # Trigger a function on button press
        ui.back.clicked.connect(showSignIn)
        #ui.createAccount.clicked.connect(showConnect)
        ui.createAccount.clicked.connect(processSignUp)

        MainWindow.show()
    else:
        guiRequest.UI_MainWindow().errorBox()
        showConnect()
        return

def showConnect():
    global ui
    ui = guiConnect.UI_MainWindow()
    ui.setupUi(MainWindow)

    # Trigger a function on button press
    ui.connect.clicked.connect(processConnect)
    # ui.connect.clicked.connect(showRequest)
    # ui.logOut.clicked.connect(showSignIn)


    MainWindow.show()

def showRequest():
    global ui
    ui = guiRequest.UI_MainWindow()
    ui.setupUi(MainWindow)
    RECEIVE_THREAD = threading.Thread(target = client.receive_thread)
    RECEIVE_THREAD.start()
    # ui.goBack.clicked.connect(showConnect)
    # ui.logOut.clicked.connect(showSignIn)
    ui.send.clicked.connect(processRequest)
    ui.disconnect.clicked.connect(processDisconnect)
    MainWindow.show()

def processDisconnect():
    if client.is_active:
        client.send2(COMMAND_DISCONNECT)
    client.reset()
    showConnect()

def isIPValid(str):
    if str.__len__() > 0:
        return True
    else:
        return False

def isPortValid(str):
    return str.isnumeric()

def processConnect():
    """
    # IP:
        # String length: 8 to 15
        # 3 dots
        #
    # Port: number && 0 -> 65535
        #
        #
    """
    myIP = ui.ip.text()
    myPort = ui.port.text()

    # For debugging
    '''
    print("Debug (connect): ", myIP)
    print("Debug (connect): ", myPort)
    '''

    if isIPValid(myIP) and isPortValid(myPort):
        client.server_host = myIP
        client.server_port = int(myPort)
        is_success = client.connect2()

        if (not is_success):
            ui.errorBox()
        else:
            showSignIn()
    else:
        ui.errorBox()

def processSignUp():
    """
    # Get text
    # If either is empty, error
    # If password mismatches confirm password, error
    ### If username already exist, later
    """
    myUsername = ui.userName.text()
    myPassword = ui.password.text()
    myPassword2 = ui.password_2.text()
    global username
    username = myUsername

    if len(myUsername) == 0:
        ui.errorBox()
    elif myPassword != myPassword2:
        ui.errorBox_password()
    else:
        temp = client.receive2() # Server should send request for username
        time.sleep(0.5)

        if client.send2(myUsername):
            temp = client.receive2() # Server should send request for password
            time.sleep(0.5)
        else:
            guiRequest.UI_MainWindow().errorBox()
            showConnect()
            return

        if client.send2(myPassword):
            temp = client.receive2()
        else:
            guiRequest.UI_MainWindow().errorBox()
            showConnect()
            return
        if "Username:" in temp:
            ui.errorBox()
        elif "successfully" in temp:
            showRequest()  

def processSignIn():
    """
    # Get text
    # Send to server
    # If username not exist OR wrong password, error
    # Else, guiRequest
    :return:
    """
    myUsername = ui.userName.text()
    myPassword = ui.password.text()
    global username
    username = myUsername

    temp = client.receive2() # Server should send request for username
    time.sleep(0.5)

    if client.send2(myUsername):
        temp = client.receive2() # Server should send request for password
    else:
        guiRequest.UI_MainWindow().errorBox()
        showConnect()
        return
    time.sleep(0.5)
    
    if client.send2(myPassword):
        temp = client.receive2()
    else:
        guiRequest.UI_MainWindow().errorBox()
        showConnect()
        return

    if "failed" in temp:
        ui.errorBox()
    elif "successfully" in temp:
        showRequest()

def processRequest():
    """
    # There are 4 fields: Date, bank, currency and messenger
    # If the messenger field contains text, once the send button is pressed, it will send 
        the messages
    # If the other 3 fields simultanously contains text, it will first send the
        request data command, then send the other 3 texts in the field to server
    # The response will be shown in the chatbox
    """
    msg = ui.message.text()
    if msg.__len__() > 0:
        if client.send2(msg):
            ui.listView.append(f"[{username}] {msg}")
            ui.message.setText("")
        else:
            ui.errorBox()
            showConnect()
            return
        
    date = ui.dateEdit.text()
    bank = ui.bank.text()
    currency = ui.currency.text()

    if date.__len__() > 0 and bank.__len__() > 0 and currency.__len__() > 0:
        if not client.send2(COMMAND_REQUEST_DATA):
            ui.errorBox()
            showConnect()
            return
        time.sleep(0.5)
        if not client.send2(date):
            ui.errorBox()
            showConnect()
            return
        time.sleep(0.5)
        if not client.send2(bank):
            ui.errorBox()
            showConnect()
            return
        time.sleep(0.5)
        if not client.send2(currency):
            ui.errorBox()
            showConnect()
            return  
     
# --------SECTION C  (SECT C)--------
class MyClient():
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server_host = host
        self.server_port = port
        self.socket = None
        self.is_active = False
        self.thread = []

        # Trinh Le Nguyen Vu: added this to kill thread
        self._kill = threading.Event()

    def getAddressConsole(self):
        # Prompts to enter
        self.server_host = input("IP: ")
        self.server_port = input("PORT: ")

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
            # send_thread.join()
            # receive_thread.join()
        except OSError:
            print(f"Cannot connect to {self.server_host}:{self.server_port}")

        # Trinh Le Nguyen Vu: Moved below commands to the end of
        # the receive thread and in the exception section of the
        # process thread

        # client.disconnect()
        # client.reset()

    def connect2(self) -> bool:
        adr = (self.server_host, self.server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connects to the host's IP address with the Port number
            self.socket.connect(adr)

            self.is_active = True
            
            print(f"Connected to {self.server_host} successfully.")

            return True
        except OSError:
            print(f"Cannot connect to {self.server_host}:{self.server_port}")
            return False

    def disconnect(self):
        if not self.is_active:
            self.send2(COMMAND_DISCONNECT)

        self.socket.close()
        print(f"[SERVER] {self.server_host} Disconnected")
        self.kill()

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
        print("Press Enter to finish")
        # ------------------------

    def receive2(self) -> str:
        """
        1. Receive message from server
        2. If message is !disconnect
            Disconnect
        3. Print message
        """
        try:
            msg = self.socket.recv(BUFFER_SIZE).decode(FORMAT)
            should_print = False
            if msg.__len__() > 0:
                should_print = True

            if should_print:
                print(f"[SERVER] {msg}")

            # If server wants to terminate
            if isDisconnectMessage(msg):
                client.send2(COMMAND_DISCONNECT)
                self.is_active = False

            return msg

        except OSError:
            print("Error! Most likely lost connection to server (receive)")
            return ""

    def receive_thread(self):
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
                    ui.listView.append(f"[SERVER] Disconnected")
                    self.socket.close()
                    break

                if should_print:
                    ui.listView.append(f"[SERVER] {msg}")
            except OSError:
                if ui == guiRequest.UI_MainWindow():
                    ui.listView.append("Error! Most likely losing connection to server (receive)")

                break

    def send2(self, msg):
        try:
            self.socket.sendall(msg.encode(FORMAT))
        except OSError:
            print("Can't send message to server (send)")
            self.is_active = False
            return False
        except:
            self.is_active = False
            return False

        return True

    def send(self, msg):
        try:
            self.socket.sendall(msg.encode(FORMAT))
        except OSError:
            print("Can't send message to server (send)")
            self.is_active = False

            return False
        except:
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
                if not self.send2(msg):
                    self.is_active = False

                    break
        except OSError:
            print("Something terrible happened (process)")
            # Tring Le Nguyen Vu: added this from the connect thread
            # ------------------------
            client.disconnect()
            client.reset()
            print("Press Enter to Finish")
            # ------------------------

    # Trinh Le Nguyen Vu: Added this function to kill thread
    def kill(self):
        self._kill.set()


# --------SECTION D  (SECT D)--------
client = MyClient()

use_gui = True

if (use_gui):
    showConnect()
    sys.exit(app.exec_())
else:
    client.getAddressConsole()

    MAIN_THREAD = threading.Thread(target=client.connect)
    MAIN_THREAD.start()
    MAIN_THREAD.join()



