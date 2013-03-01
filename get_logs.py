#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 14-06-2012

@author: slawek
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
    main_address = "http://logs.ovh.net"
    logs = ""
    login = ""
    password = ""



    def __init__(self, address="", date_start="", date_end="", logs_type="", report_format=""):
        self.today = datetime.date.today()
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
            self.logs_type = logs_type+"/"   
        else:
            raise Exception("Logs type should be given as String and should have one of values: access, error, ftp, cgi, out, ssh")

        if type(report_format) is str and (report_format == "" or report_format == "xml" or report_format == "html" or report_format == "txt"):
            self.report_format = report_format
        else:
            raise Exception("Report format should be given as string and have one of values: xml, html, txt")



    def prepareTimeValues(self, date_start, date_end):
        self.date_start = self.prepareTime(date_start)
        self.date_end = self.prepareTime(date_end)
        self.days_range = self.generateDays(self.date_start, self.date_end)



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
        if day != self.today: 
            self.logs_address = self.main_address+"/"+self.test_page+"/logs-"+day.strftime("%m")+"-"+day.strftime("%Y")+"/"+self.logs_type+self.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log.gz"
        else:
            self.logs_address = self.main_address+"/"+self.test_page+"/osl/"+self.logs_type+self.test_page+"-"+day.strftime("%d")+"-"+day.strftime("%m")+"-"+day.strftime("%Y")+".log"



    def prepareLoginData(self):
        return {'Authorization': "Basic "+base64.b64encode("%s:%s" % (self.login, self.password))}




    def loadPage(self):
        try:
            if len(self.login) != 0:
                params = urllib.urlencode("")
                request = urllib2.Request(self.logs_address, params, self.prepareLoginData())
                opened_url = urllib2.urlopen(request)
                print opened_url
            else:
                opened_url = urllib2.urlopen(self.logs_address)

            self.page_handle = StringIO.StringIO(opened_url.read())
            return True
        except urllib2.HTTPError as error:
            print error
            return False



    def loadLogsFromDay(self, day):
        self.prepareAddress(day)
        getPageResult = self.loadPage()
        if getPageResult == True:
            if day == self.today:
                result = self.page_handle.read()
            else:
                result = self.decompresFile()    
        else:
            result = "-1"

        return result
    

    
    def loadLogs(self):
        if len(self.logs) == 0 or self.logs == "-1":
            if (self.date_start == self.date_end):
                result =  self.loadLogsFromDay(self.date_start)
            else:
                result = ""
                percent_per_day = 100/len(self.days_range)
                counter = 0
                for day in self.days_range:
                    result = result+self.loadLogsFromDay(day)
                    counter = counter + percent_per_day
                    self.progressBar(counter)
            
                sys.stdout.write("\n")
            self.logs = result
        
        return self.logs
        


    def saveLogs(self):
        fileDir = os.path.abspath(os.curdir)+"/logs"
        if os.path.isdir(fileDir) == False:
            os.makedirs(fileDir)

        if (self.date_start == self.date_end):
            fileName = fileDir+"/"+self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")+".log"
        else:
            fileName = fileDir+"/"+self.test_page+"_"+self.date_start.strftime("%Y.%m.%d")+"-"+self.date_end.strftime("%Y.%m.%d")+".log"
        
        if os.path.isfile(fileName) == False or self.today in self.days_range:
            self.loadLogs()
            out = open(fileName, "w")
            out.write(self.logs)
            out.close()

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



    def createReport(self):
        reportsDir = os.path.abspath(os.curdir)+"/reports"
        filtersDir = os.path.abspath(os.curdir)+"/filters"

        if os.path.isdir(reportsDir) == False:
            os.makedirs(reportsDir)

        filters = filtersDir+"/default_filter.xml"
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
		    'odir'       : reportsDir,
		    'sample'     : float(100)
	    }

        logFile = self.saveLogs()
        report = scalp.scalper(logFile, filters, preferences)


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


#    try:
    checker = parsePage(page, day_start, day_end, logs_type, report_format)
    logs = checker.saveLogs();
    
    report = checker.createReport()
    #if len(report) != 0:
    print report
    #else:
    #print "There was no "+logs_type+" logs from "+day_start+" to "+day_end+" for domain "+page+" \n"
#    except Exception as e:
#        print e
#    except BaseException as be:
#        print be


