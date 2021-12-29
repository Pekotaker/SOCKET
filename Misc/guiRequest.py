import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class UI_MainWindow(object):
    
    def errorBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("An unknown error")
        msg.setWindowIcon(QtGui.QIcon('error.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(660, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 661, 781))
        self.label.setStyleSheet("background-color:rgba(255,255,255,255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 661, 781))
        self.label_2.setStyleSheet("background-color:rgba(186, 191, 148, 180);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

################################################## Phía trên là khung và màu nền ####################################################

########################################################### Date Input ##############################################################

        self.dateEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(70, 60, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateEdit.setFont(font)
        self.dateEdit.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.dateEdit.setText("")
        self.dateEdit.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.dateEdit.setObjectName("dateEdit")

####################################################### Text (Không cần quan tâm) ###############################################

        

##################################################### Message Input ###########################################################

        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(70, 130, 220, 40))
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

######################################################### Bank Input #########################################################

        self.bank = QtWidgets.QLineEdit(self.centralwidget)
        self.bank.setGeometry(QtCore.QRect(370, 60, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bank.setFont(font)
        self.bank.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.bank.setText("")
        self.bank.setObjectName("bank")

######################################################### Button Send ########################################################

        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(220, 230, 190, 40))
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

####################################################### Button Disconnect ###################################################

        self.disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect.setGeometry(QtCore.QRect(220, 350, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.disconnect.setFont(font)
        self.disconnect.setStyleSheet("QPushButton#disconnect{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius: 5px;\n"
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
"}\n"
"\n"
"\n"
"")
        self.disconnect.setObjectName("disconnect")


####################################################### Phần OutPut cho Client ##############################################

        self.listView = QtWidgets.QTextEdit(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 430, 640, 330))
        self.listView.setObjectName("listView")

######################################################## Currency Input #######################################################

        self.currency = QtWidgets.QLineEdit(self.centralwidget)
        self.currency.setGeometry(QtCore.QRect(370, 130, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.currency.setFont(font)
        self.currency.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.currency.setText("")
        self.currency.setObjectName("currency")

#################################################################################################################################

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        MainWindow.setWindowIcon(QtGui.QIcon('client.png'))
        self.message.setPlaceholderText(_translate("MainWindow", "Messenger"))
        self.dateEdit.setPlaceholderText(_translate("MainWindow", "Date"))
        self.bank.setPlaceholderText(_translate("MainWindow", "Bank"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.currency.setPlaceholderText(_translate("MainWindow", "Currency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
