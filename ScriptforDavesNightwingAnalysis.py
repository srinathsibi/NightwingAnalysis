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
from moviepy.editor import *
from StripData import PERCLOS
VIDEO_PROCESSING = 0#this value needs to be set to 1 if the videos needs to be cut along with the other streams of data
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
    if os.path.exists("EndSectionData"):
        print " "
        #print " End Section data folder already exists."
    else:
        print "Creating new directory for End Section data"
        os.makedirs("EndSectionData")
    #Note : All participants in the automation and control case have marker 5 to denote the start of the end event
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
            print "\n Marker from Sim data : ", Marker3time
    except UnboundLocalError:
        print " Unable to locate Marker 3, We need to ignore this participant data ", foldername
        return None
        pass
    #We have to create the Outputfilelist and the data list on the basis of whether eye tracking data
    #exists for this participant. Titrate here if needed.
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
        WriteOutputFile(filename,(Marker3time-240.0),(Marker3time+80.0),Datalist[i],FirstLineArray[i])
        #An interval of 80 seconds around marker 3 was chosen to clip the interval when the trucks
        #appear to after the accident
        os.chdir('../')
    #Processing End Section Videos here.
    if VIDEO_PROCESSING == 1:
        for i,video in enumerate(glob.glob('*.mp4')):
            print "Processing :" , video , "\n"
            clip = VideoFileClip(video).subclip((Marker3time-240+180), (Marker3time+80+180))
            clip.write_videofile('EndSectionData/File' + str(i) +'.mp4' , fps = clip.fps , audio_bitrate="1000k")
    #Opening the eye tracking file that was just saved
    try:
        file = open('EndSectionData/EyetrackingFile.csv','r')
        reader = csv.reader(file)
        skiplines(reader,1)
        ETData = list(reader)
        file.close()
        time = [float(ETData[i][0]) for i in range(len(ETData))]
        catbin =  [ETData[i][3] for i in range(len(ETData))]
        perclos_array = PERCLOS(time, catbin)
        print ' PERCLOS example : ', perclos_array[0]
        if perclos_array[0][0] != 0:
            perclos_file = open('EndSectionData/EndSectionPERCLOS.csv', 'wb')
            percloswriter = csv.writer(perclos_file)
            percloswriter.writerow(['Time','PERCLOS'])
            percloswriter.writerows([ perclos_array[i][1], perclos_array[i][0] ] for i in range(len(perclos_array)))
            perclos_file.close()
        #print " Eye Tracker Data example: \n\n" , ETData[1]
    except:
        print 'No Eye tracker file here.\n'
        pass
    Movedatatoendsection(foldername)
# This function is to move all requisite data to the end section folder for Dave's analysis of nightwing
def Movedatatoendsection(foldername):
    print "Moving other files."
    try:
        shutil.copy('EyeTrackingInfo.csv','EndSectionData/EyeTrackingInfo.csv')
    except:
        pass
    try:
        shutil.copy('iMotionsInfo.csv','EndSectionData/iMotionsInfo.csv')
    except:
        pass
    path = '../../../IgnoreThisFolder/ProcessedData/'+foldername+'/'
    try:
        shutil.copytree('EndSectionData',path+'EndSectionData')
    except OSError:
        try:
            shutil.rmtree(path+'EndSectionData/')
            shutil.copytree('EndSectionData',path+'EndSectionData')
            print 'End Section Data Removed and Copied for :', foldername
        except Exception as e:
            print "Error copying :", foldername
        pass
#Function to write the files from the arrays. This function uses the output file name and the
#the data from the csv readers.
def WriteOutputFile(filename,StartTime,StopTime,Data,FirstLine):
    print "Printing File : ", filename ," From : ", StartTime, " To : ", StopTime
    outfile = open(filename,'wb')
    outwriter = csv.writer(outfile)
    outwriter.writerow(FirstLine)
    for i in range(len(Data)):
        if float(Data[i][0]) >= StartTime:
            if float(Data[i][0]) <= StopTime:
                #print Data[i] , "\n"
                outwriter.writerow(Data[i])
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
    listoffolders =['P062','P063','P064','P065','P066','P067','P068','P069','P070','P071','P072','P073','P074','P075','P076','P077','P078','P079','P080','P081','P082','P083','P084','P085']# os.listdir('.')#Getting the list of folders
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'
    for folder in listoffolders:
        os.chdir(folder + '/ClippedData/')
        #print "List of Contents in ClippedData Folder : \n", os.listdir('.')
        ExtractData(folder)
        os.chdir('../../')
    print "\n\n################# END OF END-SECTION DATA PROCESSING! #################\n\n"
