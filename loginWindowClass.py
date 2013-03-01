#-*- coding: utf-8 -*-
'''
Created on 26-06-2012

@author: slawek
'''
import sys
from PyQt4 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class loginWindow(QtGui.QDialog):

    def __init__(self, parent="None") :
        QtGui.QDialog.__init__(self)
        self.parent = parent

        self.loginLabel = QtGui.QLabel(_fromUtf8("Login: "))
        self.login = QtGui.QLineEdit(self)
        self.passwordLabel = QtGui.QLabel(_fromUtf8("Password: "))
        self.password = QtGui.QLineEdit()
        self.buttonLogin = QtGui.QPushButton(_fromUtf8("Login"))
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.loginLabel, 1, 1)
        layout.addWidget(self.login, 1, 2)
        layout.addWidget(self.passwordLabel, 2, 1)
        layout.addWidget(self.password, 2, 2)
        layout.addWidget(self.buttonLogin, 3, 2)
        self.setLayout(layout)
        self.setWindowTitle(_fromUtf8("Login required"))
        print self   
        self.show()


    def handleLogin(self):
        self.parent.login = str(self.login.text())
        self.parent.password = str(self.password.text())
        self.deleteLater()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test = loginWindow()
    
    sys.exit(app.exec_())

