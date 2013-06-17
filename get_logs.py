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


import sys
import os
import base64
import datetime
import calendar
import gzip
import StringIO
import scalp
import subprocess as sub


#TODO: zaimportować tu ewentualnie nowe klasy generujące raporty i pobierające logi przerobienie tego tak, aby działało to z linii poleceń

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


