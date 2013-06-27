#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 14-06-2012

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

from PyQt4 import QtCore
from exceptionClass import Exception
import scalp
import os, sys, datetime

class analyzer(QtCore.QThread):
    
    homeDir = os.path.expanduser("~")
    dataDir = ".logs_analyzer"
    programDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    report_format = "xml";
    settings = None
    logFile = ""
    
    report_created = QtCore.pyqtSignal(object)
    report_aborted = QtCore.pyqtSignal()
    
    def __init__(self, settings):
        QtCore.QThread.__init__(self)
        self.today = datetime.date.today()
        self.settings = settings
        self.createAndLoadDirs()
        
        
    
    def run(self):
        output_file = ""
        if self.logFile != "":
            output_file = self.createReport(self.logFile)
        self.report_created.emit(output_file)



    def stop(self):
        if self.isRunning():
            self.terminate()
            self.download_aborted.emit()

    
    
    def createAndLoadDirs(self):
        self.reportsDir = self.homeDir+"/"+self.dataDir+"/"+"reports"
        self.filtersDir = self.homeDir+"/"+self.dataDir+"/"+"filters"

        if os.path.isdir(self.homeDir) == False:
            os.makedirs(self.homeDir)
        if os.path.isdir(self.reportsDir) == False:
            os.makedirs(self.reportsDir)
        if os.path.isdir(self.filtersDir) == False:
            os.makedirs(self.filtersDir)
            
        if os.path.isfile(self.filtersDir+"/filters.xml"):
            self.filters = self.filtersDir+"/filters.xml"
        else:
            self.filters = os.path.abspath(os.path.dirname(__file__))+"/filters/default_filter.xml"
    
    
    def createReport(self, logFile = ""):
      
        if (self.settings.date_start == self.settings.date_end):
            reportsFileName = self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")
        else:
            reportsFileName = self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")+"-"+self.settings.date_end.strftime("%Y.%m.%d")

        
        preferences = {
            'attack_type' : [],
            'period' : {
                'start' : [1, 0, 0, 0, 0, 0],# day, month, year, hour, minute, second
                'end'   : [31, 11, 9999, 24, 59, 59]
            },
            'except'     : False,
            'exhaustive' : False,
            'encodings'  : False,
            'output'     : self.report_format,
            'odir'       : self.reportsDir,
            'sample'     : float(100)
        }
        
        if logFile == "" :
            raise Exception("No logs file given. Analyze will not start")
            
        outputFile = self.reportsDir+"/"+reportsFileName+"."+self.report_format
        #sprawdzanie czy plik już przypadkiem nie istnieje, jeżeli tak to raport nie jest tworzony na nowo:
        if os.path.isfile(outputFile) == False or self.today in self.settings.days_range:
            report = scalp.scalper(logFile, self.filters, preferences, fileName=reportsFileName)
        
        return outputFile