#Author : Srinath Sibi ssibi@stanford.edu
#Purpose : House the primary functions for signal processing for all the SECTION data (HR, GSR AND PUPDIA). This script is meant to be imported into the CalculateValuesforStatistics.py script
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
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
