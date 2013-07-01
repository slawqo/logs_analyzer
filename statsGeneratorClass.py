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
import os, sys, datetime

class statsGenerator(QtCore.QThread):
    
    homeDir = os.path.expanduser("~")
    dataDir = ".logs_analyzer"
    programDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    settings = None
    logFile = ""
    
    stats_created = QtCore.pyqtSignal(object)
    stats_aborted = QtCore.pyqtSignal()
    
    def __init__(self, settings):
        QtCore.QThread.__init__(self)
        self.today = datetime.date.today()
        self.settings = settings
        self.createAndLoadDirs()
    
    
    
    def run(self):
        output_file = ""
        if self.logFile != "":
            output_file = self.createAwstats(self.logFile)
        self.stats_created.emit(output_file)



    def stop(self):
        if self.isRunning():
            self.terminate()
            self.stats_aborted.emit()

    
    
    def createAndLoadDirs(self):
        self.awstatsDir = self.homeDir+"/"+self.dataDir+"/"+"awstats"

        if os.path.isdir(self.homeDir) == False:
            os.makedirs(self.homeDir)
        if os.path.isdir(self.awstatsDir) == False:
            os.makedirs(self.awstatsDir)
    
    
    
    def createAwstats(self, logFile = ""):
        if self.settings.logs_type == "":
            file_logs_type = "access"
        else:
            file_logs_type = self.settings.logs_type
        
        if logFile == "" :
            raise Exception("No logs file given. No awstats will be generated")
        
        if self.settings.isLocalFile == True:
            awstatsResultFileName = self.awstatsDir+"/stats/"+self.settings.test_page+"_local.html"
        elif (self.settings.date_start == self.settings.date_end):
            awstatsResultFileName = self.awstatsDir+"/stats/"+self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")+"-"+file_logs_type+".html"
        else:
            awstatsResultFileName = self.awstatsDir+"/stats/"+self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")+"-"+self.settings.date_end.strftime("%Y.%m.%d")+"-"+file_logs_type+".html"
        
        if os.path.isfile(awstatsResultFileName) == False or self.today in self.settings.days_range or self.settings.isLocalFile == True:
            configFile = self.createTmpConfig()
            systemCommand = self.programDir+"/libs/awstats/wwwroot/cgi-bin/awstats.pl Logfile="+logFile+" -config="+configFile+" -update -output > "+awstatsResultFileName
            #systemProcess = sub.Popen(systemCommand, stdout=sub.PIPE, stderr=sub.PIPE)
            os.system(systemCommand)
            self.cleanAwstatsFiles()

        return awstatsResultFileName



    def createTmpConfig(self):
        awstatsBaseConfig = self.programDir+"/libs/awstats/base_access_config.conf"
        tmpConfig = self.awstatsDir+"/awstats_tmp_config.conf"
        base_file = open(awstatsBaseConfig, "r")
        tmp_file = open(tmpConfig, "w")
        config = base_file.read()
        config = config + '\nDirData="'+self.awstatsDir+'/archive"\nHostAliases="localhost 127.0.0.1 www.'+self.settings.test_page+'"\nSiteDomain="'+self.settings.test_page+'"'
        tmp_file.write(config)
        return tmpConfig



    def cleanAwstatsFiles(self):
        tmpConfig = self.awstatsDir+"/awstats_tmp_config.conf"
        os.system("rm "+tmpConfig)
        os.system("rm "+self.awstatsDir+"/archive/* -rf")