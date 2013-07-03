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
from io import StringIO, BytesIO, TextIOBase
import scalp
import subprocess as sub
from downloaderClass import *
from analyzerClass import *
from statsGeneratorClass import *
from logsSettingsClass import *


#TODO: zaimportować tu ewentualnie nowe klasy generujące raporty i pobierające logi przerobienie tego tak, aby działało to z linii poleceń


def show_help():
    print ("Logs downloader and analyzer by Slawek Kaplonski - http://kaplonski.pl")
    print ("usage:  ./get_logs.py [--log|-l log_file] or [--page|-p page_name] [OPTIONS]")
    print ("   --log           |-l:  the apache log file")
    print ("   --page          |-p:  the page name for which should be downloaded log from logs.ovh.net page")
    print ("   --filters       |-f:  the filter file     './default_filter.xml' by default")
    print ("   --report_file   |-r:  the output report file which will be generated")
    print ("   --stats_file    |-a:  the output file for awstats file which will be generated")
    print ("   --logs_type     |-t:  the logs type, it can be 'access', 'error', 'ftp', 'ssh', 'out'; default value is 'access'")
    print ("   --day_start     |-s:  the start date for which logs should be downloaded from logs.ovh.net; default value is today")
    print ("   --day_end       |-e:  the end date for which logs should be downloaded from logs.ovh.net; default value is today")




###### Main program #################
if __name__ == '__main__':
   
    today = datetime.date.today()
    day_start = today.strftime("%d.%m.%Y")
    day_end = today.strftime("%d.%m.%Y")
    page = "";
    logs_type = ""  #default is Access log when is empty
    report_format = "html"
    awstats_output_file = ""
    report_output_file = ""
    filters_file = ""
    isLocalFile = False

    if len(sys.argv) < 2 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
        sys.exit(0)
    else:
        for i in range(len(sys.argv)):
            arg = sys.argv[i]
            if arg in ('--log', '-l'):
                log_file = sys.argv[i+1]
                isLocalFile = True
            elif arg in ('--page', '-p'):
                page = sys.argv[i+1]
            elif arg in ('--filters', '-f'):
                filters_file = sys.argv[i+1]
            elif arg in ('--report_file', '-r'):
                splitted_file_name = sys.argv[i+1].split(".")
                if len(splitted_file_name) > 1:
                    ext = splitted_file_name[len(splitted_file_name)-1]
                    if ext in ("html", "xml"):
                        print (ext)
                        report_format = ext
                        report_output_file = sys.argv[i+1][:-len(ext)-1]
                    else:
                        report_output_file = sys.argv[i+1]
            elif arg in ('--stats_file', '-a'):
                awstats_output_file = sys.argv[i+1]
            elif arg in ('--logs_type', '-t'):
                logs_type = sys.argv[i+1]
            elif arg in ('--day_start', '-s'):
                day_start = sys.argv[i+1]
            elif arg in ('--day_end', '-e'):
                day_end = sys.argv[i+1]


    try:
        settings = logsSettings()
        logsDownloader = downloader(settings)
        logsAnalyzer = analyzer(settings)
        statsGen = statsGenerator(settings)
        
        settings.test_page = page 
        settings.isLocalFile = isLocalFile
        
        if isLocalFile == False:
            settings.prepareTimeValues(day_start, day_end)
            settings.prepareLogsType(logs_type)
        else:
            logsDownloader.fileName = log_file
        
        
        logs = logsDownloader.downloadLogs()
        logs_file = logsDownloader.saveLogs()
        
        if report_output_file != "":
            logsAnalyzer.report_format = report_format
            logsAnalyzer.createReport(logs_file, report_output_file)
        
        if awstats_output_file != "":
            statsGen.createAwstats(logs_file, awstats_output_file)
        
        print (logs)
        
    except Exception as e:
        print (e)
    except BaseException as be:
        print (be)


