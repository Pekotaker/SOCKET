from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Login
import Create_Account
import EnterIP
import Client

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

def LoginUi():
    global ui
    ui = Login.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.createAccount.clicked.connect(CreateAccountUi)
    ui._login.clicked.connect(ui.errorBox)
    MainWindow.show()

def CreateAccountUi():
    global ui
    ui = Create_Account.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.back.clicked.connect(LoginUi)
    ui.createAccount.clicked.connect(ui.errorBox)
    MainWindow.show()

def EnterIPUi():
    global ui
    ui = EnterIP.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.connect.clicked.connect(ClientUi)
    ui.logOut.clicked.connect(LoginUi)
    MainWindow.show()

def ClientUi():
    global ui
    ui = Client.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.goBack.clicked.connect(EnterIPUi)
    ui.logOut.clicked.connect(LoginUi)
    model = QtGui.QStandardItemModel(ui.listView)
    foods = [
    'Cookie dough', # Must be store-bought
    'Hummus', # Must be homemade
    'Spaghetti', # Must be saucy
    'Dal makhani', # Must be spicy
    'Chocolate whipped cream' # Must be plentiful
]
    for food in foods:
    # Create an item with a caption
        item = QtGui.QStandardItem(food)
 
    # Add a checkbox to it
        item.setCheckable(True)
 
    # Add the item to the model
        model.appendRow(item)
    ui.listView.setModel(model)
    ui.listView.show()
    model.removeRows( 0, model.rowCount() )
    MainWindow.show()


LoginUi()

sys.exit(app.exec_())
