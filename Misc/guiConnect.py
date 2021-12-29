import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

background = path.join(path.dirname(__file__), "background.jpg")
background = background.replace('\\', '/')
stylesheet = '''
        background-image: url("''' + background + '''"); 
        background-repeat: no-repeat; 
        background-position: center;
'''
errorIcon = path.join(path.dirname(__file__), "error.png")

class UI_MainWindow(object):

    def errorBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Can't connect to server")
        msg.setWindowIcon(QtGui.QIcon(errorIcon))
        msg.setStandardButtons(QMessageBox.Ok)
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
        self.text_2 = QtWidgets.QLabel(self.centralwidget)
        self.text_2.setGeometry(QtCore.QRect(260, 20, 181, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.text_2.setFont(font)
        self.text_2.setStyleSheet("color:rgba(0,0,0,200);")
        self.text_2.setObjectName("text_2")
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

#################################### Phía trên là khung, text và background (Không cần quan tâm) ###############################
######################################################## IP Input ##############################################################

        self.ip = QtWidgets.QLineEdit(self.centralwidget)
        self.ip.setGeometry(QtCore.QRect(260, 90, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ip.setFont(font)
        self.ip.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.ip.setText("")
        self.ip.setObjectName("ip")

##################################################### Button Connect ###########################################################

        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(260, 260, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.connect.setFont(font)
        self.connect.setStyleSheet("QPushButton#connect{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#connect:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"\n"
"QPushButton#connect:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150,123,111,255);\n"
"}")
        self.connect.setObjectName("connect")

####################################################### Port Input ###########################################################

        self.port = QtWidgets.QLineEdit(self.centralwidget)
        self.port.setGeometry(QtCore.QRect(260, 160, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.port.setFont(font)
        self.port.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color: rgba(0,0,0,240);\n"
"padding-bottom: 7px;")
        self.port.setText("")
        self.port.setObjectName("port")

###############################################################################################################################

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Enter IP"))
        MainWindow.setWindowIcon(QtGui.QIcon('ip.png'))
        self.text_2.setText(_translate("MainWindow", "Enter Server IP"))
        self.text.setText(_translate("MainWindow", "WELCOME TO"))
        self.text1.setText(_translate("MainWindow", "CLIENT"))
        self.ip.setPlaceholderText(_translate("MainWindow", "IP"))
        self.connect.setText(_translate("MainWindow", "Connect"))
        self.port.setPlaceholderText(_translate("MainWindow", "Port"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
