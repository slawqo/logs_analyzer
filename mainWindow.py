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

# Form implementation generated from reading ui file 'main_window_project.ui'
#
# Created: Tue Feb 26 16:52:43 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    
    logsTypes = [ "access", "error", "ftp", "cgi", "out", "ssh" ]
    columnsToView = ['IP Address', 'User', 'Time', 'Request', 'Answear Status', 'Answear size', 'Referer', 'User Agent']
    
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
            
        self.mainWidgetLayout.addWidget(self.topWidget)
        self.mainWidgetLayout.addWidget(self.centralWidget)


    def prepareTopWidget(self):
        self.topWidget = QtGui.QWidget()
        self.topWidget.setObjectName(_fromUtf8("topWidget"))
        
        self.firstLineTopWidget = QtGui.QWidget()
        self.firstLineTopWidget.setObjectName(_fromUtf8("firstLineTopWidget"))
        self.secondLineTopWidget = QtGui.QWidget()
        self.secondLineTopWidget.setObjectName(_fromUtf8("secondLineTopWidget"))  

        self.topWidgetLayout = QtGui.QVBoxLayout()
        self.firstLineTopWidgetLayout = QtGui.QHBoxLayout()
        self.secondLineTopWidgetLayout = QtGui.QHBoxLayout()

        #deklaracja elementów w pierwszej linii górnego widgetu:
        self.pageAddressLabel = QtGui.QLabel(_fromUtf8("Page name: "))
        self.pageAddressLabel.setObjectName(_fromUtf8("pageAddressLabel"))
        self.firstLineTopWidgetLayout.addWidget(self.pageAddressLabel)    
    
        self.pageAddress = QtGui.QLineEdit()
        self.pageAddress.setObjectName(_fromUtf8("pageAddress"))
        self.firstLineTopWidgetLayout.addWidget(self.pageAddress)
    
        self.logsTypeLabel = QtGui.QLabel(_fromUtf8("Logs type: "))
        self.logsTypeLabel.setObjectName(_fromUtf8("logsTypeLabel"))
        self.firstLineTopWidgetLayout.addWidget(self.logsTypeLabel)

        self.logsTypeValue = QtGui.QComboBox()
        self.logsTypeValue.setObjectName(_fromUtf8("logsTypeValue"))
        self.logsTypeValue.addItems(self.logsTypes)
        self.firstLineTopWidgetLayout.addWidget(self.logsTypeValue)

        self.startDateLabel = QtGui.QLabel(_fromUtf8("Start date: "))
        self.startDateLabel.setObjectName(_fromUtf8("startDateLabel"))
        self.firstLineTopWidgetLayout.addWidget(self.startDateLabel)

        self.startDateValue = QtGui.QDateEdit()
        self.startDateValue.setObjectName(_fromUtf8("startDateValue"))
        self.startDateValue.setDate(QtCore.QDate().currentDate())
        self.firstLineTopWidgetLayout.addWidget(self.startDateValue)

        self.endDateLabel = QtGui.QLabel(_fromUtf8("End date: "))
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.firstLineTopWidgetLayout.addWidget(self.endDateLabel)
        
        self.endDateValue = QtGui.QDateEdit()
        self.endDateValue.setObjectName(_fromUtf8("endDateValue"))
        self.endDateValue.setDate(QtCore.QDate().currentDate())
        self.firstLineTopWidgetLayout.addWidget(self.endDateValue)
        
        self.firstLineTopWidget.setLayout(self.firstLineTopWidgetLayout)
        # koniec konfiguracji pierwszej linii górnego widgetu

        #druga linia górnego widgetu:
        self.getLogsButton = QtGui.QPushButton(_fromUtf8("Get Logs"))
        self.getLogsButton.setObjectName(_fromUtf8("getLogsButton"))
        self.getLogsButton.setFixedSize(100, 25)
        self.secondLineTopWidgetLayout.addWidget(self.getLogsButton, 0, QtCore.Qt.AlignLeft)

        #self.secondLineTopWidgetLayout.addStretch(0)
        self.secondLineTopWidget.setLayout(self.secondLineTopWidgetLayout)
        #koniec konfiguracji drugiej linii górnego widgetu    

        #poskładanie do kupy tych widgetów:
        self.topWidgetLayout.addWidget(self.firstLineTopWidget)
        self.topWidgetLayout.addWidget(self.secondLineTopWidget)
        self.topWidget.setLayout(self.topWidgetLayout)



    def prepareCentralWidget(self):
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.centralWidgetLayout = QtGui.QVBoxLayout()
        
        self.tabsContainer = QtGui.QTabWidget()
        self.tabsContainer.setEnabled(True)
    
        self.resultsView = QtGui.QTreeWidget()
        self.resultsView.setObjectName(_fromUtf8("resultsTable"))
        self.resultsView.setIndentation(0)
        self.setTableHeaders()
        self.reportView = QtGui.QTreeWidget()
        self.reportView.setGeometry(QtCore.QRect(30, 20, 256, 192))
        self.reportView.headerItem().setText(0, _fromUtf8("Possible attacks"))

        self.reportView.setObjectName(_fromUtf8("reportView"))

        self.addTab(self.tabsContainer, self.resultsView, "Log")
        self.addTab(self.tabsContainer, self.reportView, "Report")

        self.centralWidgetLayout.addWidget(self.tabsContainer)
        self.centralWidget.setLayout(self.centralWidgetLayout)



    def prepareSearchWidget(self):
        self.searchWidget = QtGui.QWidget()
        self.searchWidgetLayout = QtGui.QHBoxLayout()
        
        self.searchLabel = QtGui.QLabel(_fromUtf8("Search text: "))
        self.searchTextValue = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton(_fromUtf8("Search"))
        self.nextResultButton = QtGui.QPushButton(_fromUtf8("Next"))
        self.nextResultButton.setEnabled(False)
        self.previousResultButton = QtGui.QPushButton(_fromUtf8("Previous"))
        self.previousResultButton.setEnabled(False)
        
        self.searchWidgetLayout.addWidget(self.searchLabel)
        self.searchWidgetLayout.addWidget(self.searchTextValue)
        self.searchWidgetLayout.addWidget(self.searchButton)
        self.searchWidgetLayout.addWidget(self.nextResultButton)
        self.searchWidgetLayout.addWidget(self.previousResultButton)
    
        self.searchWidget.setLayout(self.searchWidgetLayout)



    def addTab(self, container, widget, title):
        layout = QtGui.QVBoxLayout()
        centralWidget = QtGui.QWidget()
        layout.addWidget(widget)
        if title == "Log":
            self.prepareSearchWidget()
            layout.addWidget(self.searchWidget)
        centralWidget.setLayout(layout)
        container.addTab(centralWidget, _fromUtf8(""))
        container.setTabText(container.indexOf(centralWidget), _fromUtf8(title))
        
     
    def setTableHeaders(self):
        i = 0
        for label in self.columnsToView:
            self.resultsView.headerItem().setText(i, _fromUtf8(label))
            i += 1

