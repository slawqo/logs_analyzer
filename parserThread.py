# -*- coding: utf-8 -*-
'''
Created on 25-06-2012

@author: slawek
'''

#import threading
import time
from PyQt4 import QtCore
#from mainAppClass import mainApp


class instanceChecker(QtCore.QThread):


    def __init__(self, parent, cloudInstance, container, iId, refreshrate):
        super(instanceChecker, self).__init__(parent)
        self.cloud = cloudInstance
        self.container = container
        self.instanceId = iId
        self.parent = parent
        self.refreshRate = float(refreshrate)
    
    
    def run(self):
        status = "pending"
        while (status == "pending"):
            print "Getting new data of instance id "+str(self.instanceId)
            time.sleep(self.refreshRate)
            instanceData = self.cloud.getInstance(self.instanceId)
            if (type(instanceData) != 'instance'):
                print "Instance Data is null. Exiting..."
                break
            else:
                status = instanceData.status
            
        print "Instance id "+str(self.instanceId)+" updated."
        self.parent.instanceData = instanceData
