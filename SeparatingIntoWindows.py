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
from ScriptforDavesNightwingAnalysis import WriteOutputFile
#Function to load the data from the Stripped Data List
WINDOWSIZE = 10;#Width of the windows
WINDOWSTEP = 10;#Difference between the start points of the windows
VIDEO_PROCESSING = 0; # This value needs to be set to 1 if we need the videos sliced along with the other data streams.
def CreateSegments(folder):
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
    #Note : We locate marker 21 for the for the start of data for analysis for participants 61 and under
    if int(folder[1:4]) <= 61:
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
    #We have to create the Outputfilelist and the data list on the basis of whether eye tracking data
    #exists for this participant. Titrate here if needed.
    if IOErrorFlag[1] == 0:
        Outputfilelist = [ 'iMotionsFile.csv','SimFile.csv' ]
        Datalist = [iMotionsdata, SimData]
    elif IOErrorFlag[1]==1:
        Outputfilelist = [ 'iMotionsFile.csv','EyetrackingFile.csv', 'SimFile.csv' ]
        Datalist = [iMotionsdata, Eyetrackingdata, SimData]
    # Start with Windows Separation for Automation Condition
    #Start with Baseline.
    ######## NOTE: All the participants have the same time restrictions for baseline segment, so we don't need to get the
    try:
        if not os.path.exists('Baseline'):
            print " Creating the Baseline Folder data "
            os.makedirs('Baseline')
        #Using the same iterative mechanism from the Script fro Dave's Analysis
        for i,filename in enumerate(Outputfilelist):
            #WriteOutputFile('Baseline/'+filename,(-180.00),(0.00),Datalist[i],FirstLineArray[i])
            WriteOutputFile('Baseline/'+filename,(-180.00),(0.00),Datalist[i],FirstLineArray[i])
        #Processing Baseline Video here.
        if VIDEO_PROCESSING == 1:
            for i,video in enumerate(glob.glob('*.mp4')):
                print "Processing :" , video , "\n"
                #clip = VideoFileClip(video).subclip(0.00, 180.00)
                clip = VideoFileClip(video).subclip(80.00, 180.00)#100 seconds before the start of the first marker
                clip.write_videofile('Baseline/File' + str(i) +'.mp4' , fps = clip.fps , audio_bitrate="1000k")
        #Moving auxillary files
        try:
            shutil.copy('EyeTrackingInfo.csv','Baseline/EyeTrackingInfo.csv')
        except:
            pass
        try:
            shutil.copy('iMotionsInfo.csv','Baseline/iMotionsInfo.csv')
        except:
            pass
    except Exception as e:
        print "\n Exception at Baseline : ", e
    ######## NOTE: We can ignore processing the end section data and use the data from Dave's analysis since it already has the relevant data we need
    ######## NOTE: We need only clip the data in the middle.
    if int(folder[1:4]) <= 61:
        if Marker21time >=0:
            wstart = Marker21time#Time of when the window studys
        else:
            wstop = 0
    elif int(folder[1:4])>=62:
        wstart = 0
    windex = 0;#Index of the window
    wstop = wstart + WINDOWSIZE
    wstartarray = []
    while wstop <= (Marker5time - 100):#works for both conditions since they both have marker 5
        wstartarray.append(wstart)
        try:
            #First Creating the folder for the section
            if not os.path.exists('SECTION'+str(windex)):
                os.makedirs('SECTION'+str(windex))
            filepath = 'SECTION'+str(windex)+'/'
            print "\n\nIn Folder Section"+str(windex)
            for i,filename in enumerate(Outputfilelist):
                WriteOutputFile(filepath+filename,wstart,wstop,Datalist[i],FirstLineArray[i])
            #Processing Section Videos here.
            if VIDEO_PROCESSING == 1:
                for i,video in enumerate(glob.glob('*.mp4')):
                    print "Processing :" , video , "\n"
                    clip = VideoFileClip(video).subclip(wstart+180,wstop+180)
                    clip.write_videofile(filepath + 'File' + str(i) + '.mp4' , fps = clip.fps , audio_bitrate="1000k")
            #Calculating the PERCLOS file for each section.
            #Opening the eye tracking file that was just saved
            try:
                file = open(filepath+'EyetrackingFile.csv','r')
                reader = csv.reader(file)
                skiplines(reader,1)
                ETData = list(reader)
                file.close()
                time = [float(ETData[i][0]) for i in range(len(ETData))]
                catbin =  [ETData[i][3] for i in range(len(ETData))]
                perclos_array = PERCLOS(time, catbin)
                print ' PERCLOS example : ', perclos_array[0]
                if perclos_array[0][0] != 0:
                    perclos_file = open(filepath+'PERCLOS.csv', 'wb')
                    percloswriter = csv.writer(perclos_file)
                    percloswriter.writerow(['Time','PERCLOS'])
                    percloswriter.writerows([ perclos_array[i][1], perclos_array[i][0] ] for i in range(len(perclos_array)))
                    perclos_file.close()
                #print " Eye Tracker Data example: \n\n" , ETData[1]
            except Exception as e:
                #print 'Unable to write the PERCLOS file.\n'
                file = open('../../../WindowingProcessOutput.txt', 'a')
                writer = csv.writer(file)
                writer.writerow(['Participant ' + folder + ' Section : ' + windex + ' has no PERCLOS data\n'])
                file.close()
                pass
            #Moving auxillary files
            try:
                shutil.copy('EyeTrackingInfo.csv',filepath+'EyeTrackingInfo.csv')
            except:
                pass
            try:
                shutil.copy('iMotionsInfo.csv',filepath+'iMotionsInfo.csv')
            except:
                pass
        except Exception as e:
            print "Exception at Section Creation of : ", windex , " \n Exception : ", e
            pass
        #Updating all the variables in the loop
        windex = windex+1
        wstart = wstart + WINDOWSTEP
        wstop = wstart + WINDOWSIZE
    print "\n Window Start Times : \n", wstartarray, "\n"
    file1 = open('WindowInformation.txt', 'wb')
    writer1 = csv.writer(file1)
    writer1.writerow(['Participant ' + folder + ' has ' + str(len(wstartarray)) + ' windows'])
    writer1.writerow([' Window Start Times :\n' + str(wstartarray)])
    file1.close()
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Main Function
if __name__=='__main__':
    #Initializing the main output text file that contains the error messages in the ClippingData.py process
    GenOutput = open('WindowingProcessOutput.txt', 'wb')
    GenOutputWriter = csv.writer(GenOutput)
    GenOutputWriter.writerow(['This is the output file for the Windowing Process. File contains the errors and exceptions from the main function in last run of the SeparatingIntoWindows.py '])
    GenOutput.close()
    os.chdir('Data/')#Moving to the folder containing the data
    listoffolders = os.listdir('.')
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        try:
            CreateSegments(folder)# The windowing algorithms are called inside the Load Data to avoid the troubles with creating global variables
        except Exception as e:
            print " Main Function Exception in SeparatingIntoWindows.\nException: ", e
            file = open('../../../WindowingProcessOutput.txt', 'a')
            writer = csv.writer(file)
            writer.writerow(['Participant ' + folder + ' has an exception\n'])
            file.close()
            pass
        os.chdir('../../')
