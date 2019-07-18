#Author : Srinath Sibi ssibi@stanford.edu
#Purpose : House the primary functions for signal processing for all the SECTION data (HR, GSR AND PUPDIA). This script is meant to be imported into the CalculateValuesforStatistics.py script
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import pandas as pd
from math import factorial
from scipy.signal import butter, lfilter, freqz
from statistics import mean
import scipy.signal as signal
LOGFILE = os.path.abspath('.') + '/OutputFileForSignalProcessing.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
#Function to filter GSR
def FilterGSR(data , participant , section , LOGFILE):
    try:
        print "Filtering GSR"
    except Exception as e:
        print "Exception discovered at the GSR filtering function ", e
        file = open( LOGFILE , 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception discovered at the GSR filtering function for ', participant , 'at section', section , ' Exception : ', e])
        file.close()
#Function to filter PPG
def FilterHR(data , participant , section , LOGFILE):
    try:
        print "Filtering HR"
    except Exception as e:
        print " Exception discovered at the GSR filtering function ", e
        file = open (LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception discovered at the HR filtering function for ', participant, 'at section', section , ' Exception: ', e])
        file.close()
#Function to filter PupDia
def FilterPupilDiameter(data, participant, section , LOGFILE):
    try:
        print "Filtering Pupil Diameter"
    except Exception as e:
        print " Exception discovered at the Pupil Diameter filtering function", e
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerrow(['Exception discovered at the Pupil Diamter filtering function for ', participant, 'at section', section, 'Exception:',e])
        file.close()
#Function to filter Catbin
#Not sure, we need it. The perclos function extracts the relevant data pretty well.
def FilterCategoryBinocular():
    print "Filtering Category Binocular"
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Main Function
if __name__ == '__main__':
    outputfile = open(LOGFILE,'wb')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(['Output file and exception recorder for Python Script to signal process and eliminate bad data.'])
    outputfile.close()
    DataFolder_path = MAINPATH+'/Data/'
    os.chdir(DataFolder_path)
    listoffolders = os.listdir(MAINPATH+'/Data/')
    print "List of folders in Data : \n" , listoffolders
    for folder in listoffolders:
        try:
            print " Signal Processing for participant :" , folder
            ClippedData_path = MAINPATH+'/Data/'+folder+'/ClippedData/'
            #print " List of subfolders in the Clipped Data folder \n", os.listdir(ClippedData_path)
            listofsubfolders = os.listdir(ClippedData_path)
            result =[]
            for item in listofsubfolders:
                if 'SECTION' in item or 'Baseline' in item or 'EndSectionData' in item:
                    result.append(item)
            result.sort()#Doesn't sort the list the way we want, but it works for now and so we will keep it
            listofsubfolders = result
            print " Relevant subfolders in the Clipped Data folder\n " , listofsubfolders
        except Exception as e:
            print "Main Exception Catcher"
            file = open(LOGFILE,'a')
            writer = csv.writer(file)
            writer.writerow([' Main Function Exception Catcher ', folder , e])
            file.close()
