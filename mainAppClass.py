# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from mainWindow import Ui_MainWindow
from get_logs import parsePage 
from loginWindowClass import loginWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class mainApp(QtGui.QMainWindow):

    login = ""
    password = ""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        super(mainApp, self).__init__(parent)
                              
        self.titleFont = QtGui.QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)
        self.titleFont.setWeight(75)

        self.parser = parsePage()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectSignals()
        self.setWindowTitle(_fromUtf8("Logs analizer"))
        


    def connectSignals(self):
        self.ui.getLogsButton.clicked.connect(self.getLogs)



    def getLogs(self):
        page = str(self.ui.pageAddress.text())
        if len(page) != 0:
            start = self.ui.startDateValue.date()
            end = self.ui.endDateValue.date()
            self.parser.test_page = page 
            self.parser.prepareTimeValues(start.toPyDate().strftime("%d.%m.%Y"), end.toPyDate().strftime("%d.%m.%Y"))
            self.parser.logs_type = "/" #@TODO: dodać możliwość wybierania typu logów
            self.parser.report_format = "xml" #@TODO: dodać drugą kartę z raportem
            print type(start)
            if start > end:
                print "Error"
            logs = self.parser.loadLogs()
            if logs == "-1":
                logWin = loginWindow(self)
                logWin.exec_()
                self.parser.login = self.login
                self.parser.password = self.password
                self.getLogs()
            else:
                self.displayDataInColumns(logs)



    def displayDataInColumns(self, logs):
        logs_lines = logs.split("\n")
        for line in logs_lines:
            self.ui.resultsView.addItem(str(line))
