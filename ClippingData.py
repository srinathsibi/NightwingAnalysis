#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: To process the raw eye tracker files, quad video and the iMotions data
#Note:
#1. After the data was reorged by participants number, we are processing each participant one at a time.
#2. We are clipping 3 minutes before marker 1(Participant enters highway) and until marker 10 (study end)
#3. We might have to create global variables for each of the time start variables and time end varibales since markers are constant,
#4. Running this file on the nightwing participants data will create nearly double the amount of data.
#but time stamp formats are all different
#Data folder only contains the participant folder with sorted data in them. NOTHING ELSE!
#STEPS: #1. Process the iMotions Data. It has some of the sim data, the physio data and the marker information. It is also quite large, beware!
#2. The time for the iMotions file is not UTC, it is coded from standadrd military clock. It is imoprtant to note that event though the file says UTC
#timestamp, it is not!
#3. Video Cutting: The timings for the videos were coded by hand. The file is located in the top level 'Data' folder and contains the time for Marekr 1 for
# Quad and Eye tracker videos given that they exist.
#Note: The first column in every iMotionsClipped.csv file is a Time in secs. This is the shimmer file time converted to time in seconds. 0 is when marker 1 is placed.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
from moviepy.editor import *

#Function to process iMotions data
def ProcessiMoData():
    iMotionsMarker1TimeAbs=0.00#Abs Marker 1 time for iMotionsData
    iMotionsMarker1Time=0.00#Marker 1 time for iMotionsData
    fileinfo =[]#Top level file information. To be written
    time_abs = []#Calculating absolute time for iMotions Data
    iMotionsfile = open(glob.glob('P0??.txt')[0])#There is no other discrening feature to the name of the iMotions file
    iMotionsReader = csv.reader(iMotionsfile)
    #Opening a new file for writing. I am labelling the file as "Clipped"
    outfile = open('iMotionsClipped.csv','wb')
    outwriter = csv.writer(outfile)# We need to read and store the first 4 line of the iMotions file in the clipped data folder, discard line 5, since it is empty and keep line 6, since it is the header line
    i = 1
    while i<=5:
        fileinfo.append(next(iMotionsReader))
        i=i+1
    headerrow = next(iMotionsReader)
    #Searching for the time at which simulator marker is 1
    for i,row in enumerate(iMotionsReader):
        iMotionsMarker1TimeAbs = iMotionsTimeConverter(float(row[0].split('\t')[9].split('_')[1]))
        iMotionsMarker1Time = float(row[0].split('\t')[9].split('_')[1])
        try:
            if float(row[0].split('\t')[15]) == 1:
                break
        except ValueError:
            pass
    print "\n\nMarker 1 Time Stamp : " , iMotionsMarker1Time ,"\n\n"
    iMotionsfile.seek(0)#Get back to top of the file again
    skiplines(iMotionsReader,6)
    #Writing the rows with markers from 1 onwards
    for row in iMotionsReader:
        try:
            if float(row[0].split('\t')[9].split('_')[1]) > (iMotionsMarker1Time-300000):#We are starting the clipped file 4 min 30 seconds mins before the 1 Marker.
            #To do this because of the structure of the iMotions Time data, we are going to be subtracting 430,000 from the time or 4 min and 30 seconds
            #if float(row[0].split('\t')[15]) >= 1:
                #print "Marker: ", float(row[0].split('\t')[15])
                deltat = iMotionsTimeConverter(float(row[0].split('\t')[9].split('_')[1])) - iMotionsMarker1TimeAbs
                newrow = [item for item in row[0].split('\t')]
                newrow.insert(0,deltat)
                outwriter.writerow(newrow)
        except ValueError:
            pass
    #Writing the info file
    iMotionsinfofile = open('iMotionsInfo.csv','wb')
    iMotionsinfowriter = csv.writer(iMotionsinfofile)
    for info in fileinfo:
        iMotionsinfowriter.writerow(info)
    newheader = headerrow[0].split('\t')
    newheader.insert(0,'Time(in seconds)')
    iMotionsinfowriter.writerow(newheader)
    iMotionsinfofile.close()
    iMotionsfile.close()
    outfile.close()
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Function to convert the time read into number of seconds from the start
def iMotionsTimeConverter(inputcode):
    decimal = float(inputcode%1000)/1000
    inputcode = (inputcode - 1000*decimal)/1000
    secs = float(inputcode%100)
    inputcode = (inputcode -secs)/100
    mins = float(inputcode%100)
    inputcode = (inputcode-mins)/100
    hours = float(inputcode)
    time_abs = hours*3600 + mins*60 + secs + decimal
    return time_abs
def ETTimeConverter(inputtime):
    #print "Input time here is : ", inputtime
    pieces = inputtime.split(':')
    pieces_ = [float(i) for i in pieces]
    time = pieces_[0] * 3600 + pieces_[1]*60 + pieces_[2] + pieces_[3]/1000
    return time
#Function to move files to some path relative to the current directory. Moves all files in the filelist
def MoveFileToClippedData(filelist, target_relativepath):
    if not os.path.exists('ClippedData'):
        os.makedirs('ClippedData/')
        print "clippedData folder created inside participant folder!"
    for file in filelist:
        shutil.move(file, target_relativepath+file)
#Function to process Eye Tracker Files
# 1. There are 5 lines to skip from the start
# 2. Markers are labelled as 'user event' and the column next to it contains the counter for it as well
# 3. Note that when moving files some of the participants don't have participant eye tracking exports
# 4. Markers are in the 13th column in the file (index 12). Column 14 (index 13) contains the counter for the makrker
# 5. The first column of the Eye Tracking data called 'RecordingTime [ms]' is kinda useless. So we pop that data out in both the info and clipped file and then
# replace it with our own ETTimeConverter data.
def EyeTrackingDataProcessing(participantfolder):
    FILE_PRESENT_ = None
    MARKER_PRESENT = False
    try:
        eyetrackingfile = open(glob.glob('Raw Data*.txt')[0])
        eyetrackingreader = csv.reader(eyetrackingfile)
        FILE_PRESENT_ = True
    except IndexError:
        print "!!!!! There is no eye tracker file for this participant: " + participantfolder
        FILE_PRESENT_ = False
        pass
    if FILE_PRESENT_:
        #First Read and Save top level information
        i =1
        eyetrackinginfofile = open('EyeTrackingInfo.csv', 'wb')
        eyetrackinginfowriter = csv.writer(eyetrackinginfofile)
        while i <=5:
            row = next(eyetrackingreader)
            if i ==5:
                row.pop(0)# Removing the First Value RecordingTime and replacing with
                row.insert(0,'Time (sec)')
            eyetrackinginfowriter.writerow(row)
            i = i +1
        eyetrackinginfofile.close()
        for row in eyetrackingreader:
            if row[12] == 'User Event' and float(row[13]) == 1:
                #print "Eye tracker marker 1 time : " , row[1] , "\n Converted: " , ETTimeConverter(row[1])
                eyetracker1stmarkertime = row[1]
                MARKER_PRESENT = True
            elif row[12] == 'User Event':
                MARKER_PRESENT = True # This value is serving as a marker for now
        if not MARKER_PRESENT:
            print " !!!!!! THIS PARTICIPANT EYE TRACKER INFO HAS NO MARKER 1 : ", foldername
        # The clipped data writing can be done only for those with the MARKER_PRESENT = True, others have no eyetracker1stmarkertime to reference
        if MARKER_PRESENT:
            #Resetting to the top again
            eyetrackingfile.seek(0)
            #Now process the rest of the data. We need to clip at 3 min before the first marker
            #Keep in mind, we have to convert the data before comparison, Luckily ETTimeConverter returns float for string input
            skiplines(eyetrackingreader, 5)
            #Beginning clipping process
            etoutfile = open('EyetrackingClipped.csv' , 'wb')
            etoutwriter = csv.writer(etoutfile)
            for i,row in enumerate(eyetrackingreader):
                try:
                    if ETTimeConverter(row[1]) >= ETTimeConverter(eyetracker1stmarkertime) - ETTimeConverter('00:03:00:000'):
                        row.pop(0)#Removing the first value and replacing it with Time in seconds from ETTimeConverter
                        row.insert(0, str(ETTimeConverter(row[0])- ETTimeConverter(eyetracker1stmarkertime)) )
                        etoutwriter.writerow(row)
                except ValueError:
                    print "********This participant data has a weird row at the marker row, so we skip those rows.\n"
                    pass
            etoutfile.close()
#Function to Compare the end times of the iMotions and Eye Trackers and clip the longer one.
#The difference in time is recordings will be calculated and stored in a test file.
#NOTE : We will have to add to this file the video file and sim data end times as well
#So we hold off on this till we clip sim data and some videos as well.
#We also have to ensure that the extracts from iMotions are the same length as the data extracts from them. Then, we can by pass having to do some
#painful video coding.
def CompareAndRecordEndTimeDifferences():
    print "Doing nothing here for now!"
#We now process Sim data. In LibreOffice Calc, we have column 'AX' for the markers. This has been visually confirmed. Python index is 49
#NOTE: As in all other clipped files, we are adding a column at the start of each row which shows the realtive time to marker 1 placed in the data.
#As a result column of the marker is now moved to index 50 in the output cliiped file from 49.
#The headers are not available here. We have to decipher them from simCreator.
def ProcessSimData():
    #print "Clipping Sim Data now."
    os.chdir('SimData/')# All sim data exists inside this folder
    try:
        simfile = open (glob.glob('*Drive_[0-9][0-9].plt')[0],'r')
        simfilereader = csv.reader(simfile)
        #print "\n\nSim File opened!\n\n"
    except IndexError:
        try:
            simfile = open (glob.glob('*Drive_[0-9].plt')[0],'r')
            simfilereader = csv.reader(simfile)
            #print "\n\nSim File opened!\n\n"
        except IndexError:
            try:
                simfile = open (glob.glob('*Drive_[0-9][0-9][0-9].plt')[0],'r')
                simfilereader = csv.reader(simfile)
                #print "\n\nSim File opened!\n\n"
            except IndexError:
                print "***************All three syntaxes for sim file recognition failed! Error!********************"
                pass
    for i, row in enumerate(simfilereader):
        if row[0].split(' ')[49] == '1':
            print "Time at marker 1 for participant " , foldername , " is :" , row[0].split(' ')[0]
            simtimeatmarker1 = float(row[0].split(' ')[0])
            break
    simfile.seek(0)#Resetting to the top of the file again
    #To create the file in the ClippedData file, we will use the path in the open command instead. os.chdir() might be unnecessary
    simclipfile = open('../ClippedData/ClippedSimData.csv' , 'wb')
    simclipwriter = csv.writer(simclipfile)#This should automatically create the file in the ClippedData folder and write it there
    for i,row in enumerate(simfilereader):
        if float(row[0].split(' ')[0]) >= (simtimeatmarker1 - 180):#We are subtracting 180 seconds or 3 minutes
            simclipwriter.writerow([str(float(row[0].split(' ')[0]) - simtimeatmarker1) + ' '] + row)
    simclipfile.close()
    simfile.close()
    os.chdir('../')
def ProcessiMoVideos():
    print "\n\nNow clipping the movies to same length as the other clipped files.\n\n"
    iMotionsinfofile = open('ClippedData/iMotionsInfo.csv','r')
    infofilereader = csv.reader(iMotionsinfofile)
    iMotionsClippedFile = open('ClippedData/iMotionsClipped.csv', 'r')
    iMotionsfilereader = csv.reader(iMotionsClippedFile)
    skiplines(infofilereader,3)
    studystarttime_ = next(infofilereader)[0].split(' ')[3].split(':')
    studystarttime = [float(x) for x in studystarttime_]
    studystarttime_sec = studystarttime[0]*3600 + studystarttime[1]*60 + studystarttime[2]
    #print "Study Start Time : " , studystarttime_sec , "\n"
    clipfilestarttime = iMotionsTimeConverter(float(next(iMotionsfilereader)[10].split('_')[1]))
    #print "Clip Start Time: " , clipfilestarttime , "\n"
    timediff = clipfilestarttime - studystarttime_sec# Time difference to be taken off the front of the videos for syncing
    print " Time Difference to be taken off at the start of the videos for syncing is : " , timediff
    #Get the eye tracker and the quad files with the same glob command. The same process is used for both to clip
    videofilelist = glob.glob('*.wmv')
    print " The video files to be clipped are : ", videofilelist , "\n"
    #Normally I would use a try/except statement here. This time around, I don't want to do that. If there is a video file missing
    #I want the module to exit and throw an error.
    for i,file in enumerate(videofilelist):
        try:
            clip_ = VideoFileClip(file)
            clip = clip_.subclip(timediff, clip_.duration)
            clip.write_videofile('ClippedData/File' + str(i) + '.mp4', fps = clip_.fps , audio_bitrate="1000k")
        except IndexError:
            print "***************************************************************\n\n\
 Participant : ", foldername, " has problematic video files in iMotions. Please verify or clip them by hand! \n\
***************************************************************"
            pass
    iMotionsinfofile.close()
    iMotionsClippedFile.close()
    print " The video files for " , foldername , " have been clipped!"
#in the main function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the data folder6
    #Now to query all the files that exist in the data folder
    listoffolders = ['P006']#os.listdir('.')
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    #The os.listdir() returns a list of strings. each folder name is convenienetly a string
for foldername in listoffolders:
    os.chdir(foldername+'/')#Navigating into each folder
    print "\n\n\nInside the participant data folder : ",foldername,'\n'
    ProcessiMoData()#Function to process the iMotions Data
    EyeTrackingDataProcessing(foldername)
    ProcessSimData()
    ProcessiMoVideos()
    try:
        MoveFileToClippedData(['iMotionsClipped.csv','iMotionsInfo.csv'],'ClippedData/')#The two files created from the iMotions Processing File
    except IOError:
        print "There were no iMotions files here to move to Clipped Data Folder"
        pass
    try:
        MoveFileToClippedData(['EyetrackingClipped.csv','EyeTrackingInfo.csv'],'ClippedData/')#The two files created from the iMotions Processing File
    except IOError:
        print "There were no Eyetracking files here to move to Clipped Data Folder"
        pass
    #CompareAndRecordEndTimeDifferences()
    os.chdir('../')#Navigating back into the Data folder
