# For socket and multithreading
import socket
import threading

# For parsing data
import ssl
import json
import sched, time
import datetime

# For P A T H S
import sys
from os import path

# For login and registing
import sqlite3

"""-------COMMANDS LIST-------"""
COMMAND_LOG_IN = "!login"
COMMAND_SIGN_UP = "!signup"
COMMAND_DISCONNECT = "!disconnect"
COMMAND_REQUEST_DATA = "!request data"


"""---DEFAULT CONFIGURATION---"""
# -----SECTION 1-----#
BUFFER_SIZE = 8192
FORMAT = 'utf-8'
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 55000
EXCHANGE_RATE_DATABASE = "ExchangeData.db"
USER_LOGIN_DATABASE = "Users.db"
MISC_FOLDER_NAME = "Misc"

# For beautiful GUI
sys.path.append(path.join(path.dirname(__file__),MISC_FOLDER_NAME))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
import error



# -----SECTION 2-----#
GETTING_DATA_INTERVAL = 1800 # seconds
GETTING_DATA_HOST = "vapi.vnappmob.com"
GETTING_DATA_PORT = 443
GETTING_API_KEY_REQUEST = f"GET /api/request_api_key?scope=exchange_rate HTTP/1.1\r\nHost: {GETTING_DATA_HOST} \r\n\r\n"
BANKLIST = {"vcb", "ctg", "tcb", "bid", "stb", "sbv"}

class SERVER(QMainWindow):
    '''-------MAIN FUNCTIONS-------'''
    #---------------------------------------------------------------------------------------------------------#
    def __init__(self, MainWindow):
        
        super().__init__()
        self.bufsize = BUFFER_SIZE
        self.format = FORMAT
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.addr = (self.host, self.port)
        self.exchange_data = path.join(path.dirname(__file__), MISC_FOLDER_NAME, EXCHANGE_RATE_DATABASE)
        self.users_data = path.join(path.dirname(__file__), MISC_FOLDER_NAME, USER_LOGIN_DATABASE)

        self.banklist = BANKLIST
        self.datelist = []
        self.log = {}
        self.clients = {}
        self.addresses = {}

        self.interval = GETTING_DATA_INTERVAL
        self.get_data_host = GETTING_DATA_HOST
        self.get_data_port = GETTING_DATA_PORT
        self.get_API_request = GETTING_API_KEY_REQUEST
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)

       
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(719, 726)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 720, 730))
        self.label.setStyleSheet("background-color: rgba(255,255,255,255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 720, 730))
        self.label_2.setStyleSheet("background-color:rgba(149, 149, 112, 110)")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        ################################################# Phía trên là Khung và màu nền ######################################################

        ########################################################## Message Input #############################################################
 
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(110, 70, 501, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.message.setFont(font)
        self.message.setStyleSheet("background-color: rgba(0,0,0,0);\n"
                    "border:none;\n"
                    "border-bottom:2px solid rgba(46,82,101,200);\n"
                    "color: rgba(0,0,0,240);\n"
                    "padding-bottom: 7px;")
        self.message.setText("")
        self.message.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.message.setObjectName("message")


        ################################################## Phần Output cho server #########################################################

        self.listView = QtWidgets.QTextEdit(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(70, 150, 580, 370))
        self.listView.setObjectName("listView")
        

        ################################################## Button Send Message #############################################################

        
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(260, 550, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.send.setFont(font)
        self.send.setStyleSheet("QPushButton#send{\n"
                    "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                    "    color:rgba(255,255,255,210);\n"
                    "    border-radius:5px;\n"
                    "}\n"
                    "\n"
                    "QPushButton#send:hover{\n"
                    "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
                    "}\n"
                    "\n"
                    "QPushButton#send:pressed{\n"
                    "    padding-left:5px;\n"
                    "    padding-top:5px;\n"
                    "    background-color:rgba(150,123,111,255);\n"
                    "}")
        self.send.setObjectName("send")
        self.send.clicked.connect(self.on_click_send)
        
        ########################################################## Button Disconnect #######################################################

         
        self.disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect.setGeometry(QtCore.QRect(260, 610, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.disconnect.setFont(font)
        self.disconnect.setStyleSheet("QPushButton#disconnect{\n"
                    "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                    "    color:rgba(255,255,255,210);\n"
                    "    border-radius:5px;\n"
                    "}\n"
                    "\n"
                    "QPushButton#disconnect:hover{\n"
                    "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
                    "}\n"
                    "\n"
                    "QPushButton#disconnect:pressed{\n"
                    "    padding-left:5px;\n"
                    "    padding-top:5px;\n"
                    "    background-color:rgba(150,123,111,255);\n"
                    "}")
        self.disconnect.setObjectName("disconnect")
        self.disconnect.clicked.connect(self.on_click_disconnect)
        

        ################################################################################################################################

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # thread for periodically getting data
        GET_DATA_THREAD = threading.Thread(target = self.get_data)   
        GET_DATA_THREAD.start()

        # thread to handle incoming connections
        ACCEPT_THREAD = threading.Thread(target=self.accept_connections)
        ACCEPT_THREAD.start()

    # Listening for connections
    def accept_connections(self):
        # Listening for incoming connections
        self.server.listen()
        self.listView.append(f"[{self.host}:{self.port}] Listening...")
        while True:

            # Store socket information and addresses returned by the server.accept() function
            client, addr = self.server.accept()
            self.listView.append(f"[{addr}] connected")
            
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
        self.log[client] = 0

        # Default: log In, sign up when requested
        username = ""
        password = ""
        msg = client.recv(self.bufsize).decode(self.format)
        if msg == COMMAND_LOG_IN:
            msg = self.login(client, username, password)
        if msg != "":
            username = msg
            self.log[client] = 1
            self.listView.append(f"[{username}] Logged in successfully.")
            self.client_handle(client, username)
        
        if self.log[client] == 1:
            self.listView.append(f"[{self.clients[client]}] Disconnected.") 
            del self.clients[client]
            del self.addresses[client]
            self.log[client] = 0
            client.close()
        else:
            self.listView.append(f"[{self.addresses[client]}] Disconnected")
            del self.addresses[client]
            client.close()  

    # Handle individual clients after registering
    def client_handle(self,client, username):
        client.send("Logged in successfully".encode(self.format))
        try:
            # Store login information for temporary use: username will be used as display name in chat  
            self.clients[client] = username
            self.log[client] = 1
            active = True
            msg = ""
            while (active):
                try:
                    msg = client.recv(self.bufsize).decode(self.format)
                except OSError:
                    pass
                if (msg == COMMAND_REQUEST_DATA):
                    try:
                        # Get available dates
                        ExchangeRate = sqlite3.connect(self.exchange_data)
                        c = ExchangeRate.execute("SELECT date, bank, data from database")
                        for row in c:
                            if (row[0] not in self.datelist):
                                self.datelist.append(row[0])
                        ExchangeRate.close()

                        date = ""
                        bank = ""

                        # Select a date
                        # client.send("Select a date: ".encode(self.format))
                        # Send a list of available dates
                        # for items in self.datelist:
                        #    client.send(f"\r\n{items}".encode(self.format))
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
                        # client.send("Select a bank: ".encode(self.format))
                        # Send a list of available banks
                        # for items in self.banklist:
                        #     client.send(f"\r\n{items}".encode(self.format))
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
                else:
                    try:
                        if msg != "" and msg != COMMAND_DISCONNECT:
                            self.listView.append(f"[{username}] {msg}")
                        else:
                            active = False
                            break
                    except OSError:
                        active = False
                        pass
        except OSError:
            pass
    
    # Periodically getting data by scheduling tasks using recursion
    def get_data(self):
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
                #client.send("Select a currency: ".encode(self.format))
                #for items in data["results"]:
                    #client.send(f"\r\n{items['currency']}".encode(self.format))

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
    
    # Function for logging in
    def login(self, client, username, password) -> str:
        while not self.check_account_login(username, password):
            try:
                msg = ""
                client.send("Username: ".encode(self.format))
                try:
                    msg = client.recv(self.bufsize).decode(self.format)
                except OSError:
                    pass
                if msg == COMMAND_SIGN_UP:
                    msg = self.signup(client, username, password)
                    return msg
                if msg == COMMAND_DISCONNECT:
                    return ""
                if msg != "":
                    username = msg
                else:
                    return ""
            except OSError:
                return ""
            
            try:
                client.send("Password: ".encode(self.format))
                msg = ""
                try:
                    msg = client.recv(self.bufsize).decode(self.format)
                except OSError:
                    pass
                if msg == COMMAND_SIGN_UP:
                    msg = self.signup(client, username, password)
                    return msg
                if msg == COMMAND_DISCONNECT:
                    return ""
                if msg != "":
                    password = msg
                else:
                    return ""
            except OSError:
                return ""

            if not self.check_account_login(username, password):
                client.send("Log In failed. Please try again.\n".encode(self.format))
        return username        

    # Function for signing up
    def signup(self, client, username, password) -> str:
        while not self.check_account_availability(username):
            try:
                client.send("Username: ".encode(self.format))
                msg = ""
                try: 
                    msg = client.recv(self.bufsize).decode(self.format)
                except OSError:
                    pass
                if msg == COMMAND_LOG_IN:
                    msg = self.login(client, username, password)
                    return msg
                if msg == COMMAND_DISCONNECT:
                    return ""
                if msg != "":
                    username = msg
                else:
                    return ""
            except OSError:
                return ""

            if not self.check_account_availability(username):
                client.send("Username already exist. Try a different one.".encode(self.format))
                continue
            else: 
                pass
            
        try:
            client.send("Password: ".encode(self.format))
            msg = ""
            try:
                msg = client.recv(self.bufsize).decode(self.format)
            except OSError:
                pass 
            if msg == COMMAND_LOG_IN:
                msg = self.login(client, username, password)
                return msg
            if msg == COMMAND_DISCONNECT:
                return ""
            if msg != "":            
                password = msg
            else:
                return ""
        except OSError:
            return ""
        
        UsersData = sqlite3.connect(self.users_data)
        c = UsersData.cursor()
        c.execute("INSERT INTO database (username, password) \
            VALUES ('" + username + "', '" + password + "')")
        UsersData.commit()
        UsersData.close()
        return username

    # Check account information validity for logging in
    def check_account_login(self, username, password) -> bool:
        UsersData = sqlite3.connect(self.users_data)
        c = UsersData.cursor()
        c.execute("SELECT * FROM database WHERE username = ? AND password = ?", (username, password))
        if not c.fetchall():
            UsersData.close()
            return False
        else:
            UsersData.close()
            return True
        
    # Check account information availability for signing up   
    def check_account_availability(self, username) -> bool:
        UsersData = sqlite3.connect(self.users_data)
        c = UsersData.cursor()
        c.execute("SELECT * FROM database WHERE username = ?", (username, ))
        if not c.fetchall():
            UsersData.close()
            return True
        else:
            UsersData.close()
            return False

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
        today = str(datetime.date.today())
        # Change format to dd/mm/yyyy
        today = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%d/%m/%Y')

        # HOST and port address
        address = (self.get_data_host, self.get_data_port)

        # Wrapper with default settings
        context = ssl.create_default_context()

        # Create and connect to SSL socket
        ssl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(ssl_socket, server_hostname=self.get_data_host)
        conn.connect(address)

        # Request API key
        conn.sendall(self.get_API_request.encode(self.format))
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
            get_data_request = f"GET /api/v2/exchange_rate/{bank} HTTP/1.1\r\nHost: {self.get_data_host}\r\nAccept: application/json\r\nAuthorization: Bearer {API_key}\r\n\r\n"
                
            # Request data
            conn.sendall(get_data_request.encode(self.format))
            
            # This will receive the header, we don't need that
            temp1 = conn.recv(self.bufsize).decode(self.format)
            # This will receive the data, which is what we want
            data = conn.recv(self.bufsize).decode(self.format)
            
            # Insert new data into Exchange Rate database
            self.insert_data(today, bank, data)
    #---------------------------------------------------------------------------------------------------------#
    def errorBox(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = error.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()    

    def UI_main(self, MainWindow):
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.message.setPlaceholderText(_translate("MainWindow", "Messenger"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
    
    def on_click_send(self):
        sendText = self.message.text()
        self.message_all(sendText)
        self.message.setText("")
        if sendText != "":
            self.listView.append(f"[SERVER] {sendText}")

    def on_click_disconnect(self):
        try:
            self.message_all(COMMAND_DISCONNECT)
        except:
            pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    server = SERVER(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
