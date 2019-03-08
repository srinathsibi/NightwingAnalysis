#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: To create windowed data like Dave's End Section Creation File, but instead of Multiple Windows, we create 1 baseline window from -180 to 0 and several
# WINDOWSIZE windows, each window's start time a fixed STEPSIZE ahead of the previous window's start time.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from moviepy.editor import *
from StripData import PERCLOS
#Function to load the data from the Stripped Data List
def LoadData(folder):
    print "\n\n\n\nIn Clipped data folder for:",folder
    FirstLineArray =[]#First Line Array contains the three first lines from the iMotions, eye tracking and Sim file
    IOErrorFlag = []#Flag for whether the files are present or not.
    try:
        iMotionsFile = open('StrippediMotionsData.csv','r')
        iMotionsfilereader = csv.reader(iMotionsFile)
        FirstLineArray.append(next(iMotionsfilereader))
        iMotionsdata = list(iMotionsfilereader)
        IOErrorFlag.append(1)
        iMotionsFile.close()
    except IOError:
        print "No iMotions file here"
        IOErrorFlag.append(0)
        pass
    try:
        EyetrackingFile = open('StrippedEyeTrackingFile.csv','r')
        Eyetrackingreader = csv.reader(EyetrackingFile)
        FirstLineArray.append(next(Eyetrackingreader))
        Eyetrackingdata = list(Eyetrackingreader)
        IOErrorFlag.append(1)
        EyetrackingFile.close()
    except IOError:
        print "No EyeTracker file here"
        IOErrorFlag.append(0)
        pass
    try:
        Simfile = open('StrippedSimData.csv','r')
        Simreader = csv.reader(Simfile)
        FirstLineArray.append(next(Simreader))
        SimData = list(Simreader)
        IOErrorFlag.append(1)
        Simfile.close()
    except IOError:
        print "No Sim Data here"
        IOErrorFlag.append(0)
        pass
    """if os.path.exists("EndSectionData"):
        print " "
        #print " End Section data folder already exists."
    else:
        print "Creating new directory for End Section data"
        os.makedirs("EndSectionData")"""
    #Note : All participants in the automation and control case have marker 5 to denote the start of the end event
    try:
        if IOErrorFlag[0]:
            for i in range(len(iMotionsdata)):
                if float(iMotionsdata[i][2])==5:
                    Marker5Index = i
                    Marker5time = float(iMotionsdata[i][0])
                    print " Marker 5 from iMotions ", Marker5time , ' ', type(Marker5time)
                    break
        elif IOErrorFlag[2]:
            for i in range(len(SimData)):
                if float(SimData[i][21])==5:
                    Marker5Index = i
                    Marker5time = float(SimData[i][0])
                    print " Marker 5 from Sim data : ", Marker5time, ' ', type(Marker5time)
                    break
    except UnboundLocalError:
        print " Unable to locate Marker 5, We need to ignore this participant data ", folder
        return None
        pass
    #Note : Now we locate marker 21 for the for the start of data for analysis for participants 61 and under
    if int(folder[1:4]) <= 62:
        try:
            if IOErrorFlag[0]:
                for i in range(len(iMotionsdata)):
                    if float(iMotionsdata[i][2]) == 21:
                        Marker21Index = i
                        Marker21time = float(iMotionsdata[i][0])
                        print " Marker 21 from iMotions " , Marker21time , ' ', type(Marker21time)
                        break
            elif IOErrorFlag[2]:
                for i in range(len(SimData)):
                    if float(SimData[i][21]) == 21:
                        Marker21Index = i
                        Marker21time = float(SimData[i][0])
                        print " Marker 21 from Sim Data :", Marker21time,  ' ', type(Marker21time)
                        break
        except UnboundLocalError:
                print " Unable to locate Marker 21. We need to exclude this participant data ", folder
#Main Function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the folder containing the data
    listoffolders = os.listdir('.')
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        LoadData(folder)# The windowing algorithms are called inside the Load Data to avoid the troubles with creating global variables
        os.chdir('../../')
