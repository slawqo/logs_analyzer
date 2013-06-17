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

import urllib2
import urllib
import os, sys, base64, datetime, calendar, gzip, StringIO
from exceptionClass import Exception


class downloader:
    homeDir = os.path.expanduser("~")
    dataDir = ".logs_analyzer"
    programDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    settings = ""
    
    main_address = "http://logs.ovh.net"
    logs = ""
    login = ""
    password = ""
    
    def __init__(self, settings):
        self.today = datetime.date.today()
        
        self.settings = settings
        
        #definiowanie i tworzenie katalogów z danymi:
        self.createAndLoadDirs()
        
    
    
    def createAndLoadDirs(self):
        self.logsDir = self.homeDir+"/"+self.dataDir+"/"+"logs"

        if os.path.isdir(self.homeDir) == False:
            os.makedirs(self.homeDir)
        if os.path.isdir(self.logsDir) == False:
            os.makedirs(self.logsDir)
    
    
    
    



    



    


    def prepareAddress(self, day):
        '''prepare logs file web address with correct date and server page name
           arguments: datetime day
        '''
        if self.settings.logs_type == "":
            logs_type = "/"
        else:
            logs_type = "/"+self.settings.logs_type+"/"
        
        if day != self.today: 
            self.logs_address = self.main_address+"/"+self.settings.test_page+"/logs-"+day.strftime("%m")+"-"+day.strftime("%Y")+logs_type+self.settings.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log.gz"
        else:
            self.logs_address = self.main_address+"/"+self.settings.test_page+"/osl"+logs_type+self.settings.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log"
        print "page address: "+self.logs_address



    def prepareLoginData(self):
        return {'Authorization': "Basic "+base64.b64encode("%s:%s" % (self.login, self.password))}



    def loadPage(self):
        print self.logs_address
        try:
            if len(self.login) != 0:
                params = urllib.urlencode("")
                request = urllib2.Request(self.logs_address, params, self.prepareLoginData())
                opened_url = urllib2.urlopen(request)
                #print opened_url
            else:
                opened_url = urllib2.urlopen(self.logs_address)

            self.page_handle = StringIO.StringIO(opened_url.read())
            return 1
        except urllib2.HTTPError as error:
            errMsg = str(error)
            if "401" in errMsg:
                return 401
            elif "404" in errMsg:
                return 404
            else:
                return -1



    def loadLogsFromDay(self, day):
        self.prepareAddress(day)
        getPageResult = self.loadPage()
        if getPageResult == 1:
            if day == self.today:
                result = self.page_handle.read()
            else:
                result = self.decompresFile()    
        else:
            result = str(getPageResult)

        return result
    

    
    def loadLogs(self, progressBarWindow = None):
        if len(self.logs) == 0:
            if (self.settings.date_start == self.settings.date_end):
                result =  self.loadLogsFromDay(self.settings.date_start)
            else:
                result = ""
                percent_per_day = 100/len(self.settings.days_range)
                counter = 0
                for day in self.settings.days_range:
                    day_result = ""
                    day_result = self.loadLogsFromDay(day)
                    if day_result != "401" and day_result != "404" and day_result != "-1":
                        result = result+self.loadLogsFromDay(day)
                    elif day_result == "401":
                        self.logs = day_result
                        return self.logs
                    
                    counter = counter + percent_per_day
                    print "Download counter: "+str(counter)
                    if progressBarWindow == None:
                        self.progressBar(counter)
                    else:
                        self.graphicalProgressBar(progressBarWindow, counter)

                sys.stdout.write("\n")
            self.logs = result
        
        return self.logs
        


    def getDownloadedLogs(self):
        return self.logs



    def saveLogs(self, progressBarWindow = None):
        if self.settings.logs_type == "":
            file_logs_type = "access"
        else:
            file_logs_type = self.settings.logs_type

        if (self.settings.date_start == self.settings.date_end):
            fileName = self.logsDir+"/"+self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")+"-"+file_logs_type+".log"
        else:
            fileName = self.logsDir+"/"+self.settings.test_page+"_"+self.settings.date_start.strftime("%Y.%m.%d")+"-"+self.settings.date_end.strftime("%Y.%m.%d")+"-"+file_logs_type+".log"
        
        if os.path.isfile(fileName) == False or self.today in self.settings.days_range:
            self.loadLogs(progressBarWindow)
            if len(self.logs) > 3 :
                out = open(fileName, "w")
                out.write(self.logs)
                out.close()
        else:
            self.logs = open(fileName, "r").read()

        return fileName
    
    
    
    def decompresFile(self):
        params = urllib.urlencode("")
        if len(self.login) != 0:
            request = urllib2.Request(self.logs_address, params, self.prepareLoginData())
        else:
            request = urllib2.Request(self.logs_address)

        handle = urllib2.urlopen(request)
        f = gzip.GzipFile(fileobj=self.page_handle)
        return f.read()
    
   

    



    def progressBar(self, progress):
        sys.stdout.write('\r[{0}{1}] {2}%'.format('#'*(progress/1),'-'*((100-progress)/1), progress))
        sys.stdout.flush()



    def graphicalProgressBar(self, bar, progress):
        bar.setValue(progress)