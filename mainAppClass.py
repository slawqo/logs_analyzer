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

            #jeżeli ktoś podał zły zakres dat:
            if start > end:
                end = start #wyrównaj datę końcową z początkową jeżeli koniec jest wcześniejszy niż poczętek
                self.ui.endDateValue.setDate(start)
            
            self.parser.test_page = page 
            self.parser.prepareTimeValues(start.toPyDate().strftime("%d.%m.%Y"), end.toPyDate().strftime("%d.%m.%Y"))
            self.parser.prepareLogsType(str(self.ui.logsTypeValue.currentText())) 
            self.parser.report_format = "xml" #@TODO: dodać drugą kartę z raportem
           
            #ustawienie paska postępu pobierania logów:
            progressBar = QtGui.QProgressBar()
            progressBar.setMinimum(0)
            progressBar.setMaximum(100)
            self.ui.secondLineTopWidgetLayout.addWidget(progressBar)
        
            #pobranie logów:
            logs = self.parser.loadLogs(progressBar)
            self.parser.logs = "" #zeruję logi zapisane w klasie parser aby ewentualnie przy kolejnym pobraniu klasa pobrała nowe logi a nie korzystała już z tego co ma zapisane z poprzeniej próby
            
            #usunięcie paska postępu:
            progressBar.deleteLater()
           
            #analiza i wyswietlenie pobranych wyników 
            if logs == "401":
                logWin = loginWindow(self)
                logWin.exec_()
                self.parser.login = self.login
                self.parser.password = self.password
                self.getLogs()
            elif logs == "404":
                QtGui.QMessageBox.about(self, "Error 404", "Error 404 - page not found")
            elif logs == "-1":
                QtGui.QMessageBox.about(self, "Error", "Unknown error")
            else:
                self.displayDataInColumns(logs)
        else:
            QtGui.QMessageBox.about(self, "Error", "Page name must be given to get logs")



    def displayDataInColumns(self, logs):
        self.ui.resultsView.clear()
        logs_lines = logs.split("\n")
        for line in logs_lines:
            self.ui.resultsView.addItem(str(line))
