# -*- coding: utf-8 -*-

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
        #self.label.setText(QtGui.QApplication.translate("MainWindow", "Domena", None, QtGui.QApplication.UnicodeUTF8))
        #self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Typ", None, QtGui.QApplication.UnicodeUTF8))
        #self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Pobierz log", None, QtGui.QApplication.UnicodeUTF8))



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
        
        self.centralWidgetLayout = QtGui.QHBoxLayout()
        
        self.tabsContainer = QtGui.QTabWidget()
        self.tabsContainer.setEnabled(True)
    
        self.resultsView = QtGui.QListWidget()
        self.resultsView.setObjectName(_fromUtf8("resultsTable"))
        self.resultsView.setResizeMode(self.resultsView.Adjust)
        self.reportView = QtGui.QTreeWidget()
        self.reportView.setGeometry(QtCore.QRect(30, 20, 256, 192))
        self.reportView.headerItem().setText(0, _fromUtf8("Possible attacks"))

        self.reportView.setObjectName(_fromUtf8("reportView"))

        self.addTab(self.tabsContainer, self.resultsView, "Log")
        self.addTab(self.tabsContainer, self.reportView, "Report")

        self.centralWidgetLayout.addWidget(self.tabsContainer)
        self.centralWidget.setLayout(self.centralWidgetLayout)



    def addTab(self, container, widget, title):
        layout = QtGui.QHBoxLayout()
        centralWidget = QtGui.QWidget()
        layout.addWidget(widget)
        centralWidget.setLayout(layout)
        container.addTab(centralWidget, _fromUtf8(""))
        container.setTabText(container.indexOf(centralWidget), _fromUtf8(title))
