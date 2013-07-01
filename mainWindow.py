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

DOAWSTATS = True

try:
    from PyQt4 import QtCore, QtGui, QtWebKit
except ImportError:
    DOAWSTATS = False


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    
    logsTypes = [ "access", "error", "ftp", "out", "ssh" ]
    accessColumnsToView = ['IP Address', 'User', 'Time', 'Request', 'Answear Status', 'Answear size', 'Referer', 'User Agent']
    errorColumnsToView = ['Data', 'Type', 'IP Address', 'Host', 'Message']
    ftpColumnsToView = ['Data', 'User@IP Address', 'Type', 'Command']
    sshColumnsToView = ['Data', 'Message']
    outColumnsToView = ['Data', 'Message']
    
    logTabIndex = 1
    reportTabIndex = 2
    statsTabIndex = 3
    
    searchWidget = None
    
    def setupUi(self, MainWindow):
        self.main_window = MainWindow

        self.prepareMainWidget()
        
        self.main_window.setObjectName(_fromUtf8("MainWindow"))
        self.main_window.resize(1024, 768)
        self.main_window.setCentralWidget(self.mainWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)



    def retranslateUi(self):
        self.main_window.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        
        

    def prepareMainWidget(self):
        #declare widgets (containers):
        self.mainWidget = QtGui.QWidget(self.main_window)
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
            
        #declare layouts for containers
        self.mainWidgetLayout = QtGui.QVBoxLayout()    

        self.mainWidget.setLayout(self.mainWidgetLayout)
        
        #utworzenie widgeta górnego i środkowego:
        self.prepareTopWidget()
        self.prepareCentralWidget()
        self.prepareProgressBars()
            
        self.mainWidgetLayout.addWidget(self.topWidget)
        self.mainWidgetLayout.addWidget(self.centralWidget)


    def prepareTopWidget(self):
        self.topWidget = QtGui.QWidget()
        self.topWidget.setObjectName(_fromUtf8("topWidget"))
        self.topWidgetLayout = QtGui.QVBoxLayout()
        
        #deklaracja elementów w pierwszej linii górnego widgetu:
        self.prepareFirstLineTopWidget()

        #druga linia górnego widgetu:
        self.prepareSecondLineTopWidget()
        
        #poskładanie do kupy tych widgetów:
        self.topWidgetLayout.addWidget(self.firstLineTopWidget)
        self.topWidgetLayout.addWidget(self.secondLineTopWidget)
        self.topWidget.setLayout(self.topWidgetLayout)
    
    
    
    def prepareFirstLineTopWidget(self):
        self.firstLineTopWidget = QtGui.QWidget()
        self.firstLineTopWidget.setObjectName(_fromUtf8("firstLineTopWidget"))
        
        self.firstLineTopWidgetLayout = QtGui.QHBoxLayout()
        
        self.prepareOpenFileGroupBox()
        self.prepareDownloadLogGroupBox()
        
        self.firstLineTopWidgetLayout.addWidget(self.openFileGroupBox)
        self.firstLineTopWidgetLayout.addWidget(self.downloadFileGroupBox)

        self.firstLineTopWidget.setLayout(self.firstLineTopWidgetLayout)
        
        
        
    def prepareOpenFileGroupBox(self):
        self.openFileGroupBox = QtGui.QGroupBox(_fromUtf8("Open local log file"))
        self.openFileGroupBoxLayout = QtGui.QVBoxLayout()
        
        self.openFileGroupBoxFirstLine = QtGui.QWidget()
        self.openFileGroupBoxFirstLine.setObjectName(_fromUtf8("openFileGroupBoxFirstLine"))
        self.openFileGroupBoxFirstLineLayout = QtGui.QHBoxLayout()
        self.openFileGroupBoxFirstLineLayout.setObjectName(_fromUtf8("openFileGroupBoxFirstLineLayout"))
        
        self.openFileGroupBoxSecondLine = QtGui.QWidget()
        self.openFileGroupBoxSecondLine.setObjectName(_fromUtf8("openFileGroupBoxSecondLine"))
        self.openFileGroupBoxSecondLineLayout = QtGui.QHBoxLayout()
        self.openFileGroupBoxSecondLineLayout.setObjectName(_fromUtf8("openFileGroupBoxSecondLineLayout"))
        
        self.openFileButton = QtGui.QPushButton(_fromUtf8("Open file"))
        self.openFileButton.setObjectName(_fromUtf8("openFileButton"))
        self.openFileButton.setFixedSize(100, 25)
        self.openFileGroupBoxFirstLineLayout.addWidget(self.openFileButton)
        
        self.openFileName = QtGui.QLabel(_fromUtf8("File to open: "))
        self.openFileName.setObjectName(_fromUtf8("openFileName"))
        self.openFileName.setVisible(False)
        self.openFileGroupBoxFirstLineLayout.addWidget(self.openFileName)

        self.openFileClearButton = QtGui.QPushButton(_fromUtf8("Clear"))
        self.openFileClearButton.setObjectName(_fromUtf8("openFileClearButton"))
        self.openFileClearButton.setVisible(False)
        self.openFileClearButton.setFixedSize(100, 25)
        self.openFileGroupBoxSecondLineLayout.addWidget(self.openFileClearButton)
        
        self.openFileGroupBoxFirstLineLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.openFileGroupBoxFirstLineLayout.setSpacing(20)
        self.openFileGroupBoxSecondLineLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.openFileGroupBoxSecondLineLayout.setSpacing(20)
        
        self.openFileGroupBoxFirstLine.setLayout(self.openFileGroupBoxFirstLineLayout)
        self.openFileGroupBoxSecondLine.setLayout(self.openFileGroupBoxSecondLineLayout)
        
        self.openFileGroupBoxLayout.addWidget(self.openFileGroupBoxFirstLine)
        self.openFileGroupBoxLayout.addWidget(self.openFileGroupBoxSecondLine)
        self.openFileGroupBox.setLayout(self.openFileGroupBoxLayout)
    


    def prepareDownloadLogGroupBox(self):
        self.downloadFileGroupBox = QtGui.QGroupBox(_fromUtf8("Download log file from logs.ovh.net"))
        self.downloadFileGroupBoxLayout = QtGui.QHBoxLayout()
        
        self.pageAddressLabel = QtGui.QLabel(_fromUtf8("Page name: "))
        self.pageAddressLabel.setObjectName(_fromUtf8("pageAddressLabel"))
        self.downloadFileGroupBoxLayout.addWidget(self.pageAddressLabel)    
    
        self.pageAddress = QtGui.QLineEdit()
        self.pageAddress.setObjectName(_fromUtf8("pageAddress"))
        self.downloadFileGroupBoxLayout.addWidget(self.pageAddress)
    
        self.logsTypeLabel = QtGui.QLabel(_fromUtf8("Logs type: "))
        self.logsTypeLabel.setObjectName(_fromUtf8("logsTypeLabel"))
        self.downloadFileGroupBoxLayout.addWidget(self.logsTypeLabel)

        self.logsTypeValue = QtGui.QComboBox()
        self.logsTypeValue.setObjectName(_fromUtf8("logsTypeValue"))
        self.logsTypeValue.addItems(self.logsTypes)
        self.downloadFileGroupBoxLayout.addWidget(self.logsTypeValue)

        self.startDateLabel = QtGui.QLabel(_fromUtf8("Start date: "))
        self.startDateLabel.setObjectName(_fromUtf8("startDateLabel"))
        self.downloadFileGroupBoxLayout.addWidget(self.startDateLabel)

        self.startDateValue = QtGui.QDateEdit()
        self.startDateValue.setObjectName(_fromUtf8("startDateValue"))
        self.startDateValue.setDate(QtCore.QDate().currentDate())
        self.downloadFileGroupBoxLayout.addWidget(self.startDateValue)

        self.endDateLabel = QtGui.QLabel(_fromUtf8("End date: "))
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.downloadFileGroupBoxLayout.addWidget(self.endDateLabel)
        
        self.endDateValue = QtGui.QDateEdit()
        self.endDateValue.setObjectName(_fromUtf8("endDateValue"))
        self.endDateValue.setDate(QtCore.QDate().currentDate())
        self.downloadFileGroupBoxLayout.addWidget(self.endDateValue)
        
        self.downloadFileGroupBox.setLayout(self.downloadFileGroupBoxLayout)



    def prepareSecondLineTopWidget(self):
        self.secondLineTopWidgetLayout = QtGui.QHBoxLayout()
        
        self.secondLineTopWidget = QtGui.QWidget()
        self.secondLineTopWidget.setObjectName(_fromUtf8("secondLineTopWidget"))  
        
        self.getLogsButton = QtGui.QPushButton(_fromUtf8("Get Logs"))
        self.getLogsButton.setObjectName(_fromUtf8("getLogsButton"))
        self.getLogsButton.setFixedSize(100, 25)
        self.secondLineTopWidgetLayout.addWidget(self.getLogsButton, 0, QtCore.Qt.AlignLeft)

        self.generateReportCheckBox = QtGui.QCheckBox(_fromUtf8("Generate report"))
        self.generateReportCheckBox.setChecked(True)
        self.secondLineTopWidgetLayout.addWidget(self.generateReportCheckBox)

        self.generateStatsCheckBox = QtGui.QCheckBox(_fromUtf8("Generate statistics"))
        self.generateStatsCheckBox.setChecked(True)
        self.secondLineTopWidgetLayout.addWidget(self.generateStatsCheckBox)
        
        self.secondLineTopWidgetLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.secondLineTopWidgetLayout.setSpacing(20)
        self.secondLineTopWidget.setLayout(self.secondLineTopWidgetLayout)
        
        
        
    def prepareCentralWidget(self):
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.centralWidgetLayout = QtGui.QVBoxLayout()
        
        self.tabsContainer = QtGui.QTabWidget()
        self.tabsContainer.setEnabled(True)
    
        self.resultsView = QtGui.QTreeView()
        self.resultsView.setObjectName(_fromUtf8("resultsTable"))
        self.resultsView.setIndentation(0)
        self.resultsView.setSortingEnabled(True)
        self.resultsView.header().setClickable(True)
        
        self.logsItemsModel = QtGui.QStandardItemModel()
        self.setItemsHeaders()
        self.resultsView.setModel(self.logsItemsModel)
        
        self.reportView = QtGui.QTreeWidget()
        self.reportView.setGeometry(QtCore.QRect(30, 20, 256, 192))
        self.reportView.headerItem().setText(0, _fromUtf8("Possible attacks"))

        self.reportView.setObjectName(_fromUtf8("reportView"))
        
        self.logTabIndex = self.addTab(self.tabsContainer, self.resultsView, "Log")
        self.reportTabIndex = self.addTab(self.tabsContainer, self.reportView, "Report")
        
        if DOAWSTATS:
            self.statsView = QtWebKit.QWebView()
            self.showPage()
            self.statsView.setObjectName(_fromUtf8("statsView"))
            self.statsTabIndex = self.addTab(self.tabsContainer, self.statsView, "Statistics")

        self.centralWidgetLayout.addWidget(self.tabsContainer)
        self.centralWidget.setLayout(self.centralWidgetLayout)



    def prepareSearchWidget(self, logsType = "access"):
        self.searchWidget = QtGui.QWidget()
        self.searchWidgetLayout = QtGui.QHBoxLayout()
        
        self.searchLabel = QtGui.QLabel(_fromUtf8("Search text: "))
        self.searchTextValue = QtGui.QLineEdit()
        self.searchColumns = QtGui.QComboBox()
        self.searchButton = QtGui.QPushButton(_fromUtf8("Search"))
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.clearButton = QtGui.QPushButton(_fromUtf8("Clear results"))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.clearButton.setEnabled(False)
        
        self.prepareSearchFilters(logsType)
        
        self.searchWidgetLayout.addWidget(self.searchLabel)
        self.searchWidgetLayout.addWidget(self.searchTextValue)
        self.searchWidgetLayout.addWidget(self.searchColumns)
        self.searchWidgetLayout.addWidget(self.searchButton)
        self.searchWidgetLayout.addWidget(self.clearButton)
        
        self.searchWidget.hide()
        self.searchWidget.setLayout(self.searchWidgetLayout)



    def prepareProgressBars(self):
        #download Progress Bar:
        self.downloadLogsProgressWidget = QtGui.QWidget()
        #self.downloadLogsProgressLayout = QtGui.QHBoxLayout()
        self.downloadLogsProgressLabel = QtGui.QLabel(_fromUtf8("Downloading logs"), self.downloadLogsProgressWidget)
        self.downloadLogsProgressBar = QtGui.QProgressBar(self.downloadLogsProgressWidget)
        self.downloadLogsProgressCancelButton = QtGui.QPushButton("Cancel", self.downloadLogsProgressWidget)
        
        self.downloadLogsProgressLabel.move(10, 10)
        self.downloadLogsProgressBar.move(10, 30)
        self.downloadLogsProgressBar.setGeometry(10, 30, 310, 30)
        self.downloadLogsProgressCancelButton.move(10, 60)
        
        #report Progress Bar:
        self.reportProgressWidget = QtGui.QWidget()
        #self.downloadLogsProgressLayout = QtGui.QHBoxLayout()
        self.reportProgressLabel = QtGui.QLabel(_fromUtf8("Generating report..."), self.reportProgressWidget)
        self.reportProgressBar = QtGui.QProgressBar(self.reportProgressWidget)
        self.reportProgressBar.setMinimum(0)
        self.reportProgressBar.setMaximum(0)
        self.reportProgressCancelButton = QtGui.QPushButton("Cancel", self.reportProgressWidget)
        
        self.reportProgressLabel.move(10, 10)
        self.reportProgressBar.move(10, 30)
        self.reportProgressBar.setGeometry(10, 30, 310, 30)
        self.reportProgressCancelButton.move(10, 60)
        
        #stats Progress Bar:
        self.statsProgressWidget = QtGui.QWidget()
        #self.downloadLogsProgressLayout = QtGui.QHBoxLayout()
        self.statsProgressLabel = QtGui.QLabel(_fromUtf8("Generating statistics..."), self.statsProgressWidget)
        self.statsProgressBar = QtGui.QProgressBar(self.statsProgressWidget)
        self.statsProgressBar.setMinimum(0)
        self.statsProgressBar.setMaximum(0)
        self.statsProgressCancelButton = QtGui.QPushButton("Cancel", self.statsProgressWidget)
        
        self.statsProgressLabel.move(10, 10)
        self.statsProgressBar.move(10, 30)
        self.statsProgressBar.setGeometry(10, 30, 310, 30)
        self.statsProgressCancelButton.move(10, 60)



    def prepareSearchFilters(self, logsType):
        columns = ["All",]
        columns.extend(self.getColumnsToView(logsType))
        self.searchColumns.clear()
        self.searchColumns.addItems(columns)



    def addTab(self, container, widget, title, index = -1):
        layout = QtGui.QVBoxLayout()
        centralWidget = QtGui.QWidget()
        layout.addWidget(widget)
        if title == "Log":
            if self.searchWidget == None:
                self.prepareSearchWidget()
            layout.addWidget(self.searchWidget)
        centralWidget.setLayout(layout)
        #if tab exists with this widger it will be removed:
        if index != -1:
            container.removeTab(index)
            container.insertTab(index, centralWidget, _fromUtf8(""))
        else:
            container.addTab(centralWidget, _fromUtf8(""))
        
        container.setTabText(container.indexOf(centralWidget), _fromUtf8(title))
        container.setCurrentIndex(self.logTabIndex)
        return container.indexOf(centralWidget)



    def setItemsHeaders(self, logsType = "access"):
        columnsToView = self.getColumnsToView(logsType)
        self.logsItemsModel.setColumnCount(len(columnsToView))
        self.logsItemsModel.setRowCount(0)
        i = 0
        for label in columnsToView:
            self.logsItemsModel.setHeaderData(i, QtCore.Qt.Horizontal, label)
            i += 1



    def showPage(self, page = ""):
        self.statsView.load(QtCore.QUrl(page))
        self.statsView.show()


    def getColumnsToView(self, logType):
        if logType == "access":
            return self.accessColumnsToView
        elif logType == "error":
            return self.errorColumnsToView
        elif logType == "ftp":
            return self.ftpColumnsToView
        elif logType == "ssh":
            return self.sshColumnsToView
        elif logType == "out":
            return self.outColumnsToView
        else:
            raise Exception("Wrong log type given")
    
    
    
    def getProgressTabWidget(self, tabTitle):
        if tabTitle == "Log":
            return self.downloadLogsProgressWidget
        elif tabTitle == "Report":
            return self.reportProgressWidget
        elif tabTitle == "Statistics":
            return self.statsProgressWidget
    
    
    
    def getResultTabWidget(self, tabTitle):
        if tabTitle == "Log":
            return self.resultsView
        elif tabTitle == "Report":
            return self.reportView
        elif tabTitle == "Statistics":
            return self.statsView
        
    
    
    def getTabIndex(self, tabTitle):
        if tabTitle == "Log":
            return self.logTabIndex
        elif tabTitle == "Report":
            return self.reportTabIndex
        elif tabTitle == "Statistics":
            return self.statsTabIndex


    
    def openProgressStatus(self, tabTitle):
        widget = self.getProgressTabWidget(tabTitle)
        index = self.getTabIndex(tabTitle)
        self.addTab(self.tabsContainer, widget, tabTitle, index)
    
    
    
    def closeProgressStatus(self, tabTitle):
        widget = self.getResultTabWidget(tabTitle)
        index = self.getTabIndex(tabTitle)
        self.addTab(self.tabsContainer, widget, tabTitle, index)



    def setOpenFileGroupState(self, newState):
        self.downloadFileGroupBox.setVisible(newState)
        self.pageAddress.setEnabled(newState)
        self.logsTypeValue.setEnabled(newState)
        self.startDateValue.setEnabled(newState)
        self.endDateValue.setEnabled(newState)
