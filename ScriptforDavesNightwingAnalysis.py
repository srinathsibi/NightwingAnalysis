#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: This script is to extract the data from Sim, iMotions and Eye tracking data from
# 3 minutes before marker 3 (start of marker value 5) and 1 minute after the marker 4 (start of
# marker 10)
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
def ExtractData(foldername):
    print "\n\nIn Clipped data folder for:",foldername
    FirstLineArray =[]#First Line Array contains the three first lines from the iMotions, eye tracking and Sim file
    IOErrorFlag = []#Flag for whether the files are present or not.
    try:
        iMotionsFile = open('StrippediMotionsData.csv','r')
        iMotionsfilereader = csv.reader(iMotionsFile)
        FirstLineArray.append(next(iMotionsfilereader))
        iMotionsdata = list(iMotionsfilereader)
        IOErrorFlag.append(1)
    except IOError:
        print "No iMotions file here"
        IOErrorFlag.append(0)
    try:
        EyetrackingFile = open('StrippedEyeTrackingFile.csv','r')
        Eyetrackingreader = csv.reader(EyetrackingFile)
        FirstLineArray.append(next(Eyetrackingreader))
        Eyetrackingdata = list(Eyetrackingreader)
        IOErrorFlag.append(1)
    except IOError:
        print "No EyeTracker file here"
        IOErrorFlag.append(0)
    try:
        Simfile = open('StrippedSimData.csv','r')
        Simreader = csv.reader(Simfile)
        FirstLineArray.append(next(Simreader))
        SimData = list(Simreader)
        IOErrorFlag.append(1)
    except IOError:
        print "No Sim Data here"
        IOErrorFlag.append(0)
    if os.path.exists("EndSectionData"):
        print "\n"
        #print " End Section data folder already exists."
    else:
        print "Creating new directory for End Section data"
        os.makedirs("EndSectionData")
    try:
        if IOErrorFlag[0]:
            for i in range(len(iMotionsdata)):
                if float(iMotionsdata[i][2])==5:
                    Marker3Index = i
                    Marker3time = float(iMotionsdata[i][0])
                    break
            print "\n Marker from iMotions ", Marker3time
        elif IOErrorFlag[2]:
            for i in range(len(SimData)):
                if float(SimData[i][21])==5:
                    Marker3Index = i
                    Marker3time = float(SimData[i][0])
                    break
            print "\n Marker 3 time is : ", Marker3time
    except UnboundLocalError:
        print " Unable to locate Marker 3, We need to ignore this participant data ", foldername
        return None
    #We have to create the Outputfilelist and the data list on the basis of whether eye tracking data
    #exists for this participant.
    if IOErrorFlag[1] == 0:
        Outputfilelist = [ 'iMotionsFile.csv','SimFile.csv' ]
        Datalist = [iMotionsdata, SimData]
    elif IOErrorFlag[1]==1:
        Outputfilelist = [ 'iMotionsFile.csv','EyetrackingFile.csv', 'SimFile.csv' ]
        Datalist = [iMotionsdata, Eyetrackingdata, SimData]
    #Writing a function to automate the process of extracting the relevant information and
    # move to EndSectionData folder
    for i,filename in enumerate(Outputfilelist):
        os.chdir('EndSectionData/')
        WriteOutputFile(filename,Marker3time,Datalist[i],FirstLineArray[i])
        os.chdir('../')
#Function to write the files from the arrays. This function uses the output file name and the
#the data from the csv readers.
def WriteOutputFile(filename,Marker3time,Data,FirstLine):
    print "Printing File : ", filename
    outfile = open(filename,'wb')
    outwriter = csv.writer(outfile)
    outwriter.writerow(FirstLine)
    """for i in range(len(Data)):
        if float(Data[i][0])>=Marker3time:
            outwriter.writerow(Data[i])"""
    outfile.close()
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Main Function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the folder containing the data
    listoffolders = os.listdir('.')#Getting the list of folders
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'
    for folder in listoffolders:
        os.chdir(folder + '/ClippedData/')
        #print "List of Contents in ClippedData Folder : \n", os.listdir('.')
        ExtractData(folder)
        os.chdir('../../')
    print "\n\n################# END OF SIGNAL PROCESSING! #################\n\n"
