# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from mainWindow import Ui_MainWindow
from get_logs import parsePage 
from loginWindowClass import loginWindow
from xml.dom import minidom
import os
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class mainApp(QtGui.QMainWindow):

    login = ""
    password = ""
    loginCanceled = False
    searchWidgetDisplayed = False #flaga informująca czy wyświetlony jest panel wyszukiwania w logach
    displayedSearchedItemIndex = 0 #index aktualnie podświetlonego elemetnu jaki został znaleziony
    items = [] #elementy wyszukane przez użytkownika

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
                
        self.searchAction = QtGui.QAction("search", self)
        self.searchAction.setShortcut("Ctrl+f")
        self.searchAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.addAction(self.searchAction)
        
        self.connectSignals()
        self.setWindowTitle(_fromUtf8("Logs analizer"))
        


    def connectSignals(self):
        self.ui.getLogsButton.clicked.connect(self.getLogs)
        self.ui.pageAddress.returnPressed.connect(self.getLogs)
        self.searchAction.triggered.connect(self.searchBox)
        self.ui.searchButton.clicked.connect(self.searchItem)
        self.ui.searchTextValue.returnPressed.connect(self.searchItem)
        self.ui.nextResultButton.clicked.connect(self.showNextItem)
        self.ui.previousResultButton.clicked.connect(self.showPreviousItem)

    def getLogs(self):
        page = str(self.ui.pageAddress.text())
        if len(page) != 0:
            self.parser.logs = "" #zeruję logi zapisane w klasie parser aby ewentualnie przy kolejnym pobraniu klasa pobrała nowe logi a nie korzystała już z tego co ma zapisane z poprzeniej próby
            
            start = self.ui.startDateValue.date()
            end = self.ui.endDateValue.date()
            
            #jeżeli ktoś podał zły zakres dat:
            if start > end:
                end = start #wyrównaj datę końcową z początkową jeżeli koniec jest wcześniejszy niż poczętek
                self.ui.endDateValue.setDate(start)
           
            logsType = str(self.ui.logsTypeValue.currentText())
            self.parser.test_page = page 
            self.parser.prepareTimeValues(start.toPyDate().strftime("%d.%m.%Y"), end.toPyDate().strftime("%d.%m.%Y"))
            self.parser.prepareLogsType(logsType) 
            self.parser.report_format = "xml"
           
            #ustawienie paska postępu pobierania logów:
            progressBar = QtGui.QProgressDialog("Download logs file", "Cance", 0, 100, self)
            #@TODO: dodać akcję dla przycisku "cancel"
            #Dopóki pobieranie wszystkiego nie będzie w osobnym wątku to nie da się anulować tego pobierania 
            #i dlatego przycisk "Cancel" jest ukryty
            progressBar.setCancelButton(None)

            #pobranie logów:
            logsFile = self.parser.saveLogs(progressBar)
            logs = self.parser.getDownloadedLogs()
            
            #usunięcie informacji o generowaniu logów:
            progressBar.close()
                        
            #analiza i wyswietlenie pobranych wyników 
            if logs == "401":
                logWin = loginWindow(self)
                logWin.exec_()
                if self.loginCanceled == False:
                    self.parser.login = self.login
                    self.parser.password = self.password
                    self.getLogs()
                else:
                    return
            elif logs == "404":
                QtGui.QMessageBox.about(self, "Error 404", "Error 404 - page not found")
            elif logs == "-1":
                QtGui.QMessageBox.about(self, "Error", "Unknown error")
            else:
                self.displayDataInColumns(logs)
                
            #i dodanie nowej informacji o generowaniu logów:
            if logsType == "access":
                print "Generate report..."
                progressBar = QtGui.QProgressDialog("Generating report...", "Cancel", 0, 100, self)
                #Dopóki pobieranie wszystkiego nie będzie w osobnym wątku to nie da się anulować tego pobierania 
                #i dlatego przycisk "Cancel" jest ukryty:
                progressBar.setCancelButton(None)
                reportFile = self.parser.createReport(logFile = logsFile, progressBarWindow = progressBar)
                report = self.parseAndDisplayReport(reportFile)
                progressBar.close()

        else:
            QtGui.QMessageBox.about(self, "Error", "Page name must be given to get logs")



    def displayDataInColumns(self, logs):
        self.ui.resultsView.clear()
        logs_lines = logs.split("\n")
        for line in logs_lines:
            self.ui.resultsView.addItem(str(line))

        

    def parseAndDisplayReport(self, reportFile):
        self.ui.reportView.clear()
        self.ui.reportView.setHeaderHidden(True)
        maxLenght = 0
        longestText = ""
        
        if os.path.isfile(reportFile) == False:
            topLevelItem = QtGui.QTreeWidgetItem(self.ui.reportView)
            topLevelItem.setText(0, "No xml report file given")
            topLevelItem.setTextColor(0, QtGui.QColor(180, 180, 180))
            topLevelItem.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            return False
      
        reportDOMTree = minidom.parse(reportFile)
        mainNodes = reportDOMTree.childNodes
        attackValues = [];
        for attackNode in mainNodes[0].getElementsByTagName('attack'):
            #pobranie nazwy rodzaju potencjalnego ataku:
            attackName = attackNode.getAttribute('name')
            #jeżeli nazwa jest pusta to próba pobrania atrybutu type:
            if attackName == None or attackName == "":
                attackName = attackNode.getAttribute('type')
            
            #jeżeli rodzaj ataku nie był jeszcze na liście  to tworzymy nowy wpis topLevel:  
            if attackName not in attackValues:
                attackValues.append(attackName)
                topLevelItem = QtGui.QTreeWidgetItem(self.ui.reportView)
                topLevelItem.setText(0, _fromUtf8(attackName))
                
            #tworzenie listy wpisów podejrzanych dla danego typu ataku:
            impacts = attackNode.getElementsByTagName('impact')
            for impact in impacts:
                items = impact.getElementsByTagName('item')
                for item in items:
                    secondLevelItem = QtGui.QTreeWidgetItem(topLevelItem)
                    description = item.getElementsByTagName('reason')[0].childNodes[0].nodeValue + " \n " + item.getElementsByTagName('line')[0].childNodes[0].nodeValue
                    secondLevelItem.setText(0, _fromUtf8(description))
                    line_number = item.getElementsByTagName('line_number')[0].childNodes[0].nodeValue
                    #w kolumnie 1 która i tak jest niewidoczna zapisywany jest nr linii ktrórej dotyczy wpis:
                    secondLevelItem.setText(1, _fromUtf8(line_number))
                    if len(description) > maxLenght:
                        maxLenght = len(description)
                        longestText = description
            
        #obliczenie szerokości najdłuższego wpisu:
        itemWidth = int(QtGui.QFontMetrics(self.ui.reportView.font()).width(longestText))
        self.ui.reportView.setColumnWidth(0, itemWidth)

        #dodanie sygnału do elementów listy:
        self.ui.reportView.itemActivated.connect(self.showLine)
    
        
        
    def searchItem(self):
        searchExpression = self.ui.searchTextValue.text()
        self.items = self.ui.resultsView.findItems(searchExpression, QtCore.Qt.MatchContains)
        #wyzerowanie indeksu tak aby wyświetlić pierwszy znaleziony element
        self.displayedSearchedItemIndex = 0
        if len(self.items) > 0:
            self.items[self.displayedSearchedItemIndex].setSelected(True)
        
        #jeżeli jest więcej niż jeden element to aktywować trzeba przycisk "next":
        if len(self.items) > 1:
            self.ui.nextResultButton.setEnabled(True)
    
    
    #@TODO: trzeba zrobić aby przesuwało do aktywnego znalezionego rekordo
    def showNextItem(self):
        self.displayedSearchedItemIndex+=1
        self.items[self.displayedSearchedItemIndex].setSelected(True)
        #trzeba ustawić przycisk "previous" na aktywny:
        self.ui.previousResultButton.setEnabled(True)
        
        #jeżeli jest to ostatni element to trzeba zablokować przycisk next:
        if len(self.items) == (self.displayedSearchedItemIndex+1):
            self.ui.nextResultButton.setEnabled(False)
    
    
    
    def showPreviousItem(self):
        self.displayedSearchedItemIndex-=1
        self.items[self.displayedSearchedItemIndex].setSelected(True)
        #trzeba ustawić przycisk "previous" na aktywny:
        self.ui.nextResultButton.setEnabled(True)
        
        #jeżeli jest to pierwszy element to trzeba zablokować przycisk previous:
        if self.displayedSearchedItemIndex == 0:
            self.ui.previousResultButton.setEnabled(False)



    def searchBox(self):
        if self.ui.tabsContainer.currentIndex() == 0:
            if self.searchWidgetDisplayed == False:
                self.showSearchBox()
            else:
                self.hideSearchBox()

    
    
    def showSearchBox(self):    
        self.ui.bottomWidget.show()
        self.searchWidgetDisplayed = True
        
        
    
    def hideSearchBox(self):
        self.ui.bottomWidget.hide()
        self.searchWidgetDisplayed = False
    
    
    
    def showLine(self, item, column = 0):
        line_nr = int(item.text(1)) - 1 
        self.ui.resultsView.item(line_nr).setSelected(True)