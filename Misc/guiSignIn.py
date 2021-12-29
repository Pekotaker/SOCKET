import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

errorIcon = path.join(path.dirname(__file__), "error.png")
acceptIcon = path.join(path.dirname(__file__), "accept.png")
background = path.join(path.dirname(__file__), "background.jpg")
background = background.replace('\\', '/')
stylesheet = '''
        background-image: url("''' + background + '''"); 
        background-repeat: no-repeat; 
        background-position: center;
'''

class UI_MainWindow(object):

    def errorBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("The username or password is incorrect")
        msg.setWindowIcon(QtGui.QIcon(errorIcon))
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def loginSuccess(self):
        msg = QMessageBox()
        msg.setWindowTitle("success")
        msg.setText("Logged in successfully")
        msg.setWindowIcon(QtGui.QIcon(acceptIcon))
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 429)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 280, 430))
        self.label.setStyleSheet(stylesheet)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 280, 430))
        self.label_2.setStyleSheet("background-color: rgba(0,0,0,80);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 0, 240, 430))
        self.label_3.setStyleSheet("background-color: rgba(255,255,255,255);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

################################################ Phía trên là khung với background ###############################################
######################################################## Button CreateAccount ####################################################

        self.createAccount = QtWidgets.QPushButton(self.centralwidget)
        self.createAccount.setGeometry(QtCore.QRect(260, 340, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.createAccount.setFont(font)
        self.createAccount.setStyleSheet("QPushButton#createAccount{"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);"
"    border-radius:5px;\n"
"}"
"QPushButton#createAccount:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}"
"QPushButton#createAccount:pressed{"
"    padding-left:5px;"
"    padding-top:5px;"
"    background-color:rgba(150,123,111,255);}")
        self.createAccount.setObjectName("createAccount")

####################################################### Button Login ################################################################

        self._login = QtWidgets.QPushButton(self.centralwidget)
        self._login.setGeometry(QtCore.QRect(260, 270, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self._login.setFont(font)
        self._login.setStyleSheet("QPushButton#_login{"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);"
"    border-radius: 5px;}"
"QPushButton#_login:hover{"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));}"
"QPushButton#_login:pressed{"
"    padding-left:5px;"
"    padding-top:5px;"
"    background-color:rgba(150,123,111,255);}")
        self._login.setObjectName("_login")

################################################### Chữ login trên giao diện ####################################################

        self.Login_text = QtWidgets.QLabel(self.centralwidget)
        self.Login_text.setGeometry(QtCore.QRect(290, 50, 110, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Login_text.setFont(font)
        self.Login_text.setStyleSheet("color:rgba(0,0,0,200);")
        self.Login_text.setObjectName("Login_text")

###################################################### Username input ###########################################################

        self.userName = QtWidgets.QLineEdit(self.centralwidget)
        self.userName.setGeometry(QtCore.QRect(260, 120, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.userName.setFont(font)
        self.userName.setStyleSheet("background-color: rgba(0,0,0,0);"
"border:none;"
"border-bottom:2px solid rgba(46,82,101,200);"
"color: rgba(0,0,0,240);"
"padding-bottom: 7px;")
        self.userName.setObjectName("userName")

######################################################## Password input #######################################################

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(260, 190, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: rgba(0,0,0,0);"
"border:none;"
"border-bottom:2px solid rgba(46,82,101,200);"
"color: rgba(0,0,0,240);"
"padding-bottom: 7px;")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")

################################################################################################################################

########################################### Vài chữ linh tinh trên màn hình ################################################

        self.text = QtWidgets.QLabel(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(20, 50, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.text.setFont(font)
        self.text.setStyleSheet("color:rgba(255,255,255,110);")
        self.text.setObjectName("text")
        self.text1 = QtWidgets.QLabel(self.centralwidget)
        self.text1.setGeometry(QtCore.QRect(50, 120, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.text1.setFont(font)
        self.text1.setStyleSheet("color: rgba(255,255,255,180);")
        self.text1.setObjectName("text1")
##################################################################################################################################

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

######################################### Thêm text vào các đối tượng ###################################################

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Log In"))
        MainWindow.setWindowIcon(QtGui.QIcon('login.jpg'))
        self.createAccount.setText(_translate("MainWindow", "Create Account"))
        self._login.setText(_translate("MainWindow", "L o g  I n"))
        self.Login_text.setText(_translate("MainWindow", "Log In"))
        self.userName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.text.setText(_translate("MainWindow", "WELCOME TO"))
        self.text1.setText(_translate("MainWindow", "CLIENT"))

########################################################################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
