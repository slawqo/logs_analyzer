#-*- coding: utf-8 -*-
'''
Created on 26-06-2012

@author: Sławek Kapłoński
@contact: slawek@kaplonski.pl

This file is part of Logs Analyzer.

    Logs Analyzer is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Logs Analyzer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Logs Analyzer; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    Ten plik jest częścią Foobar.

    Logs Analyzer jest wolnym oprogramowaniem; możesz go rozprowadzać dalej
    i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU,
    wydanej przez Fundację Wolnego Oprogramowania - według wersji 2 tej
    Licencji lub (według twojego wyboru) którejś z późniejszych wersji.

    Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
    użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
    gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
    ZASTOSOWAŃ. W celu uzyskania bliższych informacji sięgnij do
    Powszechnej Licencji Publicznej GNU.

    Z pewnością wraz z niniejszym programem otrzymałeś też egzemplarz
    Powszechnej Licencji Publicznej GNU (GNU General Public License);
    jeśli nie - napisz do Free Software Foundation, Inc., 59 Temple
    Place, Fifth Floor, Boston, MA  02110-1301  USA
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
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton(_fromUtf8("Login"))
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonCancel = QtGui.QPushButton(_fromUtf8("Cancel"))
        self.buttonCancel.clicked.connect(self.cancelLogin)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.loginLabel, 1, 1)
        layout.addWidget(self.login, 1, 2)
        layout.addWidget(self.passwordLabel, 2, 1)
        layout.addWidget(self.password, 2, 2)
        layout.addWidget(self.buttonLogin, 3, 1)
        layout.addWidget(self.buttonCancel, 3, 2)
        self.setLayout(layout)
        self.setWindowTitle(_fromUtf8("Login required"))
        self.show()



    def handleLogin(self):
        self.parent.login = str(self.login.text())
        self.parent.password = str(self.password.text())
        self.parent.loginCanceled = False
        self.deleteLater()
        
        
    
    def cancelLogin(self):
        self.parent.loginCanceled = True
        self.deleteLater()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test = loginWindow()
    
    sys.exit(app.exec_())

