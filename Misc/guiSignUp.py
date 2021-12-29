import sys
from os import path
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

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
        msg.setText("The username is incorrect or already exists")
        msg.setWindowIcon(QtGui.QIcon(errorIcon))
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def createAccountSuccess(self):
        msg = QMessageBox()
        msg.setWindowTitle("success")
        msg.setText("Registered successfully")
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
        self.label_2.setStyleSheet("background-color: rgba(0,0,0,80);\n"
"\n"
"")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 0, 240, 430))
        self.label_3.setStyleSheet("background-color: rgba(255,255,255,255);\n"
"")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

############################################ Phía trên là background với khung ############################################
################################################## Button Create Account ##################################################

        self.createAccount = QtWidgets.QPushButton(self.centralwidget)
        self.createAccount.setGeometry(QtCore.QRect(260, 300, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.createAccount.setFont(font)
        self.createAccount.setStyleSheet("QPushButton#createAccount{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#createAccount:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"\n"
"QPushButton#createAccount:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150,123,111,255);\n"
"}")
        self.createAccount.setObjectName("createAccount")

############################################### text (cái này không cần quan tâm) ############################################

        self.text_2 = QtWidgets.QLabel(self.centralwidget)
        self.text_2.setGeometry(QtCore.QRect(250, 20, 211, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.text_2.setFont(font)
        self.text_2.setStyleSheet("color:rgba(0,0,0,200);")
        self.text_2.setObjectName("text_2")

#################################################### User Name Input ######################################################

        self.userName = QtWidgets.QLineEdit(self.centralwidget)
        self.userName.setGeometry(QtCore.QRect(260, 80, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.userName.setFont(font)
        self.userName.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.userName.setObjectName("userName")

#################################################### Password Input #######################################################

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(260, 150, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.password.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.password.setObjectName("password")

##################################################### text (Không cần quan tâm phần text)  ############################################################

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

################################################### Confirm Password input ######################################################

        self.password_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.password_2.setGeometry(QtCore.QRect(260, 220, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password_2.setFont(font)
        self.password_2.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.password_2.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit) ############ Ẩn pass khi nhập ở ô khác ##############
        self.password_2.setObjectName("password_2")

######################################################## Button Back ############################################################

        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(260, 370, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.back.setFont(font)
        self.back.setStyleSheet("QPushButton#back{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#back:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"\n"
"QPushButton#back:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150,123,111,255);\n"
"}")
        self.back.setObjectName("back")

#########################################################################################################################################

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sign Up"))
        MainWindow.setWindowIcon(QtGui.QIcon('signup.png'))
        self.createAccount.setText(_translate("MainWindow", "Create Account"))
        self.text_2.setText(_translate("MainWindow", "Create Account"))
        self.userName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.text.setText(_translate("MainWindow", "WELCOME TO"))
        self.text1.setText(_translate("MainWindow", "CLIENT"))
        self.password_2.setPlaceholderText(_translate("MainWindow", "Confirm Password"))
        self.back.setText(_translate("MainWindow", "Back"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

