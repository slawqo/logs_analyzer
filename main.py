#-*- coding: utf-8 -*-
'''
Created on 20-06-2012

@author: slawek
'''
import sys
from PyQt4 import QtGui
from mainAppClass import mainApp

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = mainApp()
    
    myapp.show()
    sys.exit(app.exec_())
    
