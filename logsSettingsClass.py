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

import os, sys, datetime

class logsSettings:
    
    test_page = ""
    date_start = ""
    date_end = ""
    days_range = ""
    logs_type = "access"
    isLocalFile = False
    
    
    def prepareLogsType(self, logs_type):
        if (logs_type == "" or logs_type == "error" or logs_type == "ftp" or logs_type == "cgi" or logs_type == "out" or logs_type == "ssh"):
            self.logs_type = logs_type   
        elif logs_type == "access":
            self.logs_type = ""
        else:
            raise Exception("Logs type should have one of values: access, error, ftp, cgi, out, ssh")
        
        
    
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
    
    
    
    def generateDays(self, start, end):
        dif = end - start
        days = dif.days+1
        dates = []
        for i in range(0,days):
            dates.append(start + datetime.timedelta(days = i))
        return dates