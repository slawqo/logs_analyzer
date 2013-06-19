# -*- coding: utf-8 -*-

'''
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

from PyQt4 import QtCore, QtGui

from mainWindow import Ui_MainWindow
from loginWindowClass import loginWindow
from downloaderClass import downloader
from analyzerClass import analyzer
from statsGeneratorClass import statsGenerator
from logsSettingsClass import logsSettings
from xml.dom import minidom
import os, sys
import time
import re

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
    logsLinesItems = [] #elementy logu (linie) wyświetlone w analizatorze
    lastSelectedLine = [] #ostatnio podświetlona linia w widoku logu
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        super(mainApp, self).__init__(parent)
        
        self.titleFont = QtGui.QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)
        self.titleFont.setWeight(75)

        #self.parser = parsePage()
        
        self.logsParseSettings = logsSettings()
        self.logsDownloader = downloader(self.logsParseSettings)
        self.logsAnalyzer = analyzer(self.logsParseSettings)
        self.statsGen = statsGenerator(self.logsParseSettings)
        
        
        self.logsProxy = QtGui.QSortFilterProxyModel(self)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #akcja wyłączona ponieważ na razie jest problem z wydajnością pojawiania się tego pola wyszukiwania 
        #przy dużej ilości logów w qlistwidget 
        self.searchAction = QtGui.QAction("search", self)
        self.searchAction.setShortcut("Ctrl+f")
        self.searchAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.addAction(self.searchAction)
        
        self.connectSignals()
        self.setWindowTitle(_fromUtf8("Logs analizer"))
        


    def connectSignals(self):
        self.ui.getLogsButton.clicked.connect(self.getLogs)
        self.ui.pageAddress.returnPressed.connect(self.getLogs)
        #sygnał nie przypisany ze względu na problem z wydajnością wyświetlania pola search:
        self.searchAction.triggered.connect(self.searchBox)
        self.ui.searchButton.clicked.connect(self.searchItem)
        self.ui.searchTextValue.returnPressed.connect(self.searchItem)
        self.ui.clearButton.clicked.connect(self.clearSearchResults)
        self.ui.searchColumns.currentIndexChanged.connect(self.searchItem)


    def getLogs(self):
        page = str(self.ui.pageAddress.text())
        if len(page) != 0:
            self.logsDownloader.logs = "" #zeruję logi zapisane w klasie parser aby ewentualnie przy kolejnym pobraniu klasa pobrała nowe logi a nie korzystała już z tego co ma zapisane z poprzeniej próby
            
            start = self.ui.startDateValue.date()
            end = self.ui.endDateValue.date()
            
            #jeżeli ktoś podał zły zakres dat:
            if start > end:
                end = start #wyrównaj datę końcową z początkową jeżeli koniec jest wcześniejszy niż poczętek
                self.ui.endDateValue.setDate(start)
           
            logsType = str(self.ui.logsTypeValue.currentText())
            self.logsParseSettings.test_page = page 
            self.logsParseSettings.prepareTimeValues(start.toPyDate().strftime("%d.%m.%Y"), end.toPyDate().strftime("%d.%m.%Y"))
            self.logsParseSettings.prepareLogsType(logsType) 
                        
            try:
                #ustawienie paska postępu pobierania logów:
                progressBar = QtGui.QProgressDialog("Downloading logs", "Cancel", 0, 100, self)
                #@TODO: dodać akcję dla przycisku "cancel"
                #Dopóki pobieranie wszystkiego nie będzie w osobnym wątku to nie da się anulować tego pobierania 
                #i dlatego przycisk "Cancel" jest ukryty
                progressBar.setCancelButton(None)
                progressBar.show()
            
                #pobranie logów:
                logsFile = self.logsDownloader.saveLogs(progressBar)
                logs = self.logsDownloader.getDownloadedLogs()
            
                #usunięcie informacji o generowaniu logów:
                progressBar.close()
                        
                #analiza i wyswietlenie pobranych wyników 
                if logs == "401":
                    logWin = loginWindow(self)
                    logWin.exec_()
                    if self.loginCanceled == False:
                        self.logsDownloader.login = self.login
                        self.logsDownloader.password = self.password
                        self.getLogs()
                    else:
                        return
                elif logs == "404":
                    QtGui.QMessageBox.about(self, "Error 404", "Error 404 - page not found")
                elif logs == "-1":
                    QtGui.QMessageBox.about(self, "Error", "Unknown error")
                else:
                    self.displayDataInColumns(logs, logsType)
            
                #i dodanie nowej informacji o generowaniu logów:
                if logsType == "access":
                    print ("Generate report...")
                    self.generateReport(logsFile)
                    self.generateStats(logsFile)
            
            except Exception as e:
                QtGui.QMessageBox.about(self, "Error", _fromUtf8(str(e)))
                progressBar.close()
        else:
            QtGui.QMessageBox.about(self, "Error", "Page name must be given to get logs")



    def generateReport(self, logsFile):
        progressBar = QtGui.QProgressDialog("Generating report...", "Cancel", 0, 100, self)
        #Dopóki pobieranie wszystkiego nie będzie w osobnym wątku to nie da się anulować tego pobierania 
        #i dlatego przycisk "Cancel" jest ukryty:
        progressBar.setCancelButton(None)
        progressBar.show()
        reportFile = self.logsAnalyzer.createReport(logFile = logsFile, progressBarWindow = progressBar)
        report = self.parseAndDisplayReport(reportFile)
        progressBar.close()
        
        
        
    def generateStats(self, logsFile):
        progressBar = QtGui.QProgressDialog("Generating statistics...", "Cancel", 0, 0, self)
        #Dopóki pobieranie wszystkiego nie będzie w osobnym wątku to nie da się anulować tego pobierania 
        #i dlatego przycisk "Cancel" jest ukryty:
        progressBar.setCancelButton(None)
        progressBar.show()
        awstatsFile = self.statsGen.createAwstats(logFile = logsFile, progressBarWindow = progressBar)
        #report = self.parseAndDisplayReport(reportFile)
        self.ui.showPage(awstatsFile)
        progressBar.close()
        
        
        
    def displayDataInColumns(self, logs, logsType):
        self.logsLinesItems = [] #wyzerowanie listy elementów wyświetlanych
        self.ui.logsItemsModel.clear()
        self.ui.setItemsHeaders(logsType)
        self.ui.prepareSearchFilters(logsType)
        
        logs_lines = logs.split("\n")
        longestTexts = self.ui.accessColumnsToView[:]
        
        row = 0
        for line in logs_lines:
            splittedLine = self.splitLogLine(line, logsType)
            col = 0
            if len(splittedLine) != 0:
                singleLineItems = []
                for columnValue in splittedLine:
                    item = QtGui.QStandardItem(columnValue)
                    self.ui.logsItemsModel.setItem(row, col, item)
                    singleLineItems.append(item)
                    if len(columnValue) > len(longestTexts[col]):
                        longestTexts[col] = columnValue
                    col += 1
                self.logsLinesItems.append(singleLineItems)
            row += 1
        
        self.logsProxy.setSourceModel(self.ui.logsItemsModel)
        self.ui.resultsView.setModel(self.logsProxy)
        row = 0
        col = 0
        
        for longestValue in longestTexts:
            itemWidth = int(QtGui.QFontMetrics(self.ui.resultsView.font()).width(longestValue))
            if itemWidth <= 200:
                self.ui.resultsView.setColumnWidth(col, itemWidth+25) #nie wiem dlaczego, ale bez tego zawsze trochę brakuje
            else:
                self.ui.resultsView.setColumnWidth(col, itemWidth*0.6)
            col += 1
   
   
   
    def parseAndDisplayReport(self, reportFile):
        self.reportLinesItems = []
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
                    if len(description) > len(longestText):
                        longestText = description
            
        #obliczenie szerokości najdłuższego wpisu:
        itemWidth = int(QtGui.QFontMetrics(self.ui.reportView.font()).width(longestText))
        self.ui.reportView.setColumnWidth(0, itemWidth*0.6)

        #dodanie sygnału do elementów listy:
        self.ui.reportView.itemActivated.connect(self.showLineInResultsView)
    
        
        
    def searchItem(self):
        columnToSearch = int(self.ui.searchColumns.currentIndex())-1
        self.logsProxy.setFilterKeyColumn(columnToSearch)
        searchExpression = QtCore.QRegExp(self.ui.searchTextValue.text(),
                                            QtCore.Qt.CaseInsensitive,
                                            QtCore.QRegExp.RegExp
                                        )
        self.logsProxy.setFilterRegExp(searchExpression)
        if self.ui.searchTextValue.text() == "":
            self.ui.clearButton.setEnabled(False)
        else:
            self.ui.clearButton.setEnabled(True)



    def clearSearchResults(self):
        self.logsProxy.setFilterKeyColumn(-1)
        #clear is only search with empty string:
        searchExpression = QtCore.QRegExp("",
                                        QtCore.Qt.CaseInsensitive,
                                        QtCore.QRegExp.RegExp
                                        )
        self.logsProxy.setFilterRegExp(searchExpression)
        self.ui.searchTextValue.setText = ""
        self.ui.clearButton.setEnabled(False)


    def searchBox(self):
        if self.ui.tabsContainer.currentIndex() == 0:
            if self.searchWidgetDisplayed == False:
                self.showSearchBox()
            else:
                self.hideSearchBox()

    
    
    def showSearchBox(self):    
        self.ui.searchWidget.show()
        self.ui.searchTextValue.setFocus()
        self.searchWidgetDisplayed = True
        
        
    
    def hideSearchBox(self):
        self.ui.searchWidget.hide()
        self.searchWidgetDisplayed = False
    
    
    
    def showLineInResultsView(self, item, column = 0):
        line_nr = int(item.text(1)) - 1 
        if len(self.lastSelectedLine) > 0 :
            self.deselectLine(self.lastSelectedLine)
        
        lineToSelect = self.logsLinesItems[line_nr]
        self.selectLine(lineToSelect)
        
        self.lastSelectedLine = lineToSelect
        
        
        
    def selectLine(self, line):
        selectionModel = self.ui.resultsView.selectionModel()
        for item in line:
            itemToSelect = self.ui.logsItemsModel.indexFromItem(item)
            selectionModel.select(itemToSelect, selectionModel.Select)
            
            
            
    def deselectLine(self, line):
        selectionModel = self.ui.resultsView.selectionModel()
        for item in line:
            itemToSelect = self.ui.logsItemsModel.indexFromItem(item)
            selectionModel.select(itemToSelect, selectionModel.Deselect)
    
    
    
    def splitLogLine(self, line, logType):
        result = []
        if logType == "access":
            return self.splitAccessLogLine(line)
        elif logType == "error":
            return self.splitErrorLogLine(line)
        elif logType == "ftp":
            return self.splitFtpLogLine(line)
        elif logType == "ssh":
            return self.splitSshLogLine(line)
        elif logType == "out":
            return self.splitOutLogLine(line)
        else:
            raise Exception("Wrong log type given")
    
    
    
    def splitAccessLogLine(self, line):
        result = []
        regex = '([(\d\.)]+) (.*?) (.*?) \[(.*?)\] "(.*?)" (\d+) (-|\d+) "(.*?)" "(.*?)"'
        if len(line) != 0:
            values = list(re.match(regex, line).groups())
            del(values[1]) #usunięcie kolumny której nie używam późniejszych
            #usunięcie białych znaków z każdego elementu
            for value in values:
                result.append(value.strip())
        return result
    
    
    
    def splitErrorLogLine(self, line):
        result = []
        regex = "\[(.*?)\] \[(.*?)\] \[(.*?)\] \[(.*?)\] (.*)"
        if len(line) != 0:
            values = list(re.match(regex, line).groups())
            #usunięcie białych znaków z każdego elementu
            for value in values:
                result.append(value.strip())
        return result
    
    
    
    def splitFtpLogLine(self, line):
        result = []
        regex = '\[(.*?)\] \((.*?)\) \[(.*?)\] (.*)'
        if len(line) != 0:
            values = list(re.match(regex, line).groups())
            #usunięcie białych znaków z każdego elementu
            for value in values:
                result.append(value.strip())
        return result
    
    
    
    def splitSshLogLine(self, line):
        result = []
        regex = '\[(.*?)\] (.*)'
        if len(line) != 0:
            values = list(re.match(regex, line).groups())
            #usunięcie białych znaków z każdego elementu
            for value in values:
                result.append(value.strip())
        return result
    
    
    def splitOutLogLine(self, line):
        result = []
        regex = '\[(.*?)\] (.*)'
        if len(line) != 0:
            values = list(re.match(regex, line).groups())
            #usunięcie białych znaków z każdego elementu
            for value in values:
                result.append(value.strip())
        return result