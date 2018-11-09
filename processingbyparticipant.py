#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: To process the raw eye tracker files, quad video and the iMotions data
#Note:
#1. After the data was reorged by participants number, we are processing each participant one at a time.
#2. We are clipping about 3 minutes before marker 1(Participant enters highway) and until marker 4 (study end)
#3. We might have to create global variables for each of the time start variables and time end varibales since markers are constant,
#4. Running this file on the nightwing participants data will create nearly double the amount of data.
#but time stamp formats are all different
#Data folder only contains the participant folder with sorted data in them. NOTHING ELSE!
#STEPS: #1. Process the iMotions Data. It has some of the sim data, the physio data and the marker information. It is also quite large, beware!
#2. The time for the iMotions file is not UTC, it is coded from standadrd military clock. It is imoprtant to note that event though the file says UTC
#timestamp, it is not!
import glob, os, sys
import matplotlib as plt
import numpy as np
import csv
iMotionsMarker1TimeAbs =0.00#Abs Marker 1 time for iMotionsData
iMotionsMarker1Time =0.00#Marker 1 time for iMotionsData
#Function to process iMotions data
def ProcessiMoData():
    global iMotionsMarker1TimeAbs
    global iMotionsMarker1Time
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
    print "\n\n\nTOP LEVEL INFO:\n\n",fileinfo,'\n\n',headerrow
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
    #Skipping the first 6 lines
    i = 1
    while i<=6:
        next(iMotionsReader)
        i=i+1
    #Writing the rows with markers from 1 onwards. Need to clip the end at some time.
    for row in iMotionsReader:
        try:
            if float(row[0].split('\t')[15]) >= 1:
                #print "Marker: ", float(row[0].split('\t')[15])
                outwriter.writerow(row)
        except ValueError:
            pass
    #Writing the info file
    iMotionsinfofile = open('iMotionsInfo.csv','wb')
    iMotionsinfowriter = csv.writer(iMotionsinfofile)
    for info in fileinfo:
        iMotionsinfowriter.writerow(info)
    iMotionsinfowriter.writerow(headerrow)
    iMotionsinfofile.close()
    iMotionsfile.close()
    outfile.close()
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
#in the main function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the data folder
    #Now to query all the files that exist in the data folder
    listoffolders = os.listdir('.')
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    #The os.listdir() returns a list of strings. each folder name is convenienetly a string
for foldername in listoffolders:
    os.chdir(foldername+'/')#Navigating into each folder
    print "\n\n\nInside the participant data folder : ",foldername,'\n'
    ProcessiMoData()#Function to process the iMotions Data
    os.chdir('../')#Navigating back into the Data folder
