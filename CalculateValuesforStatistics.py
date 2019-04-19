#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose:
#   1. In each interval we extract the HR, PupilDiameter, GSR, Steer, Brake, Accel and other relevant data into a individual csv files and single averaged values for each interval
#   2. Single out the participants that are relevant and usable. Might have to revisit the pick sheet to see which ones are usable. This might be differnet from Dave's Criteria
#   3. Employ Signal processing for HR and GSR.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'
MAINPATH = os.path.abspath('.')
#Main Function
if __name__ == '__main__':
    outputfile = open(LOGFILE,'wb')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(['Output file and exception recorder for Python Script to '])
    outputfile.close()
    os.chdir(MAINPATH+'/Data/')
    listoffolders = os.listdir(MAINPATH+'/Data')
    print "List of folders in Data : \n" , listoffolders
    for folder in listoffolders:
        try:
            print " Analyzing Clipped Data Folder for :", folder
            os.chdir()
        except Exception as e:
            print "Main Exception Catcher"
            file = open(LOGFILE,'a')
            writer = csv.writer(file)
            writer.writerow([' Main Function Exception Catcher '])
            file.close()
