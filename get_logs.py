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

import urllib
import urllib2
import sys
import os
import base64
import datetime
import calendar
import gzip
import StringIO
import scalp

#Exception class:
class Exception(BaseException):
    def __init__(self, m):
        self.message = m
    
    
    def __str__(self):
        return self.message

#*********************************


# parsing Page class***************
class parsePage:
    '''
    classdocs
    '''
    homeDir = os.path.expanduser("~")
    dataDir = ".logs_analyzer"
    
    main_address = "http://logs.ovh.net"
    logs = ""
    login = ""
    password = ""



    def __init__(self, address="", date_start="", date_end="", logs_type="", report_format=""):
        self.today = datetime.date.today()
        
        #definiowanie i tworzenie katalogów z danymi:
        self.createAndLoadDirs()

        if (type(address) is str):
            self.test_page = address
        else:
            raise Exception("Web page address should be given as String")

        if (type(date_start) is str and type(date_end) is str):
            if len(date_start) != 0 and len(date_end) != 0:
                self.prepareTimeValues(date_start, date_end)
        else:
            raise Exception("Date should be given as String")
        
        if type(logs_type) is str and (logs_type == "" or logs_type == "access" or logs_type == "error" or logs_type == "ftp" or logs_type == "cgi" or logs_type == "out" or logs_type == "ssh"):
            self.prepareLogsType(logs_type)   
        else:
            raise Exception("Logs type should be given as String")

        if type(report_format) is str and (report_format == "" or report_format == "xml" or report_format == "html" or report_format == "txt"):
            self.report_format = report_format
        else:
            raise Exception("Report format should be given as string and have one of values: xml, html, txt")



    def createAndLoadDirs(self):
        self.reportsDir = self.homeDir+"/"+self.dataDir+"/"+"reports"
        self.logsDir = self.homeDir+"/"+self.dataDir+"/"+"logs"
        self.filtersDir = self.homeDir+"/"+self.dataDir+"/"+"filters"
        #self.filtersDir = os.path.abspath(os.curdir)+"/filters"

        if os.path.isdir(self.homeDir) == False:
            os.makedirs(self.homeDir)
        if os.path.isdir(self.logsDir) == False:
            os.makedirs(self.logsDir)
        if os.path.isdir(self.reportsDir) == False:
            os.makedirs(self.reportsDir)
        if os.path.isdir(self.filtersDir) == False:
            os.makedirs(self.filtersDir)
        
        if os.path.isfile(self.filtersDir+"/filters.xml"):
            self.filters = self.filtersDir+"/filters.xml"
        else:
            self.filters = os.path.abspath(os.path.dirname(__file__))+"/filters/default_filter.xml"



    def prepareTimeValues(self, date_start, date_end):
        self.date_start = self.prepareTime(date_start)
        self.date_end = self.prepareTime(date_end)
        self.days_range = self.generateDays(self.date_start, self.date_end)



    def prepareLogsType(self, logs_type):
        if (logs_type == "" or logs_type == "error" or logs_type == "ftp" or logs_type == "cgi" or logs_type == "out" or logs_type == "ssh"):
            self.logs_type = logs_type   
        elif logs_type == "access":
            self.logs_type = ""
        else:
            raise Exception("Logs type should have one of values: access, error, ftp, cgi, out, ssh")



    def prepareTime(self, day):
        '''Prepare date into datetime format from input string
           arguments: String day (in format dd.mm.YYYY)
        '''
        tmp_date = day.split(".")
        if len(tmp_date) == 3:
            return datetime.date(int(tmp_date[2]), int(tmp_date[1]), int(tmp_date[0]))
        else:
            #jeżeli data rozdzielona znakiem "-" to znaczy że jest przekazana z GUI i wtedy jest w formacie YYYY-MM-DD:
            tmp_date = day.split("-")
            if len(tmp_date) == 3:
                return datetime.date(int(tmp[0]), int(tmp_date[1]), int(tmp_date[2]))
            else:
                raise Exception("Wrong date format. It should be in format DD.MM.YYYY")


    def prepareAddress(self, day):
        '''prepare logs file web address with correct date and server page name
           arguments: datetime day
        '''
        if self.logs_type == "":
            logs_type = "/"
        else:
            logs_type = "/"+self.logs_type+"/"
        
        if day != self.today: 
            self.logs_address = self.main_address+"/"+self.test_page+"/logs-"+day.strftime("%m")+"-"+day.strftime("%Y")+logs_type+self.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log.gz"
        else:
            self.logs_address = self.main_address+"/"+self.test_page+"/osl"+logs_type+self.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log"
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
            if (self.date_start == self.date_end):
                result =  self.loadLogsFromDay(self.date_start)
            else:
                result = ""
                percent_per_day = 100/len(self.days_range)
                counter = 0
                for day in self.days_range:
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
        if self.logs_type == "":
            file_logs_type = "access"
        else:
            file_logs_type = self.logs_type

        if (self.date_start == self.date_end):
            fileName = self.logsDir+"/"+self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")+"-"+file_logs_type+".log"
        else:
            fileName = self.logsDir+"/"+self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")+"-"+self.date_end.strftime("%Y.%m.%d")+"-"+file_logs_type+".log"
        
        if os.path.isfile(fileName) == False or self.today in self.days_range:
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
    
   

    def generateDays(self, start, end):
        dif = end - start
        days = dif.days+1
        dates = []
        for i in range(0,days):
            dates.append(start + datetime.timedelta(days = i))
        return dates


    def progressBar(self, progress):
        sys.stdout.write('\r[{0}{1}] {2}%'.format('#'*(progress/1),'-'*((100-progress)/1), progress))
        sys.stdout.flush()



    def graphicalProgressBar(self, bar, progress):
        bar.setValue(progress)
        #bar.show()


    def createReport(self, logFile = "", progressBarWindow = None):
      
        if (self.date_start == self.date_end):
            reportsFileName = self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")
        else:
            reportsFileName = self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")+"-"+self.date_end.strftime("%Y.%m.%d")

        
        preferences = {
		    'attack_type' : [],
		    'period' : {
			    'start' : [01, 00, 0000, 00, 00, 00],# day, month, year, hour, minute, second
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
            logFile = self.saveLogs(progressBarWindow)
            print "Pobieramy logi"
        outputFile = self.reportsDir+"/"+reportsFileName+"."+self.report_format
        #sprawdzanie czy plik już przypadkiem nie istnieje, jeżeli tak to raport nie jest tworzony na nowo:
        if os.path.isfile(outputFile) == False or self.today in self.days_range:
            report = scalp.scalper(logFile, self.filters, preferences, fileName=reportsFileName, progressBar = progressBarWindow)
        
        return outputFile
        


#### Koniec klasy parsera ###



def parseDates(day_1, day_2):
    today = datetime.date.today()
    tmp = day_1.split(".")
    tmp_2 = day_2.split(".")
    #podany tylko miesiąc:
    if len(tmp) == 2:
        date_1 = "01."+day_1
        #czy to jest aktualny miesiąc czy nie:
        if int(tmp[0]) == today.month:
            date_2 = today.strftime("%d.%m.%Y")
        # jeżeli nie jest to aktualny miesiąc to robimy cały miesiąc
        else:
            last_month_day = calendar.monthrange(int(tmp[1]), int(tmp[0]))[1]
            date_2 = str(last_month_day)+"."+str(day_2)
    #jeżeli podane były dwa różne dni to:
    else:
        date_1 = day_1
        date_2 = day_2
    
    return [date_1, date_2]



###### Main program #################

if __name__ == '__main__':
   
    today = datetime.date.today()
    day_start = today.strftime("%d.%m.%Y")
    day_end = today.strftime("%d.%m.%Y")
    page = "";
    logs_type = ""  #default is Access log when is empty
    report_format = "xml"

    for arg in sys.argv:
        splitted = arg.split("=")
        if len(splitted) == 2:
            if splitted[0] == "page":
                page = splitted[1]
            elif splitted[0] == "day":
                splitted_day = splitted[1].split("-")
                if len(splitted_day) == 2:
                    [day_start, day_end] = parseDates(splitted_day[0], splitted_day[1])
                else:
                    [day_start, day_end] = parseDates(splitted[1], splitted[1])
            elif splitted[0] == "type":
                if splitted[1] != "access":
                    logs_type = splitted[1]
            elif splitted[0] == "report":
                report_format = splitted[1]


    try:
        checker = parsePage(page, day_start, day_end, logs_type, report_format)
        logs = checker.saveLogs();
    
        report = checker.createReport()
        if len(report) != 0:
            print report
        else:
            print "There was no "+logs_type+" logs from "+day_start+" to "+day_end+" for domain "+page+" \n"
    except Exception as e:
        print e
    except BaseException as be:
        print be


