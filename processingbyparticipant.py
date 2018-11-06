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
import glob, os, csv, sys
import matplotlib as plt
import numpy as np
#Function to process iMotions data
def ProcessiMoData():
    fileinfo =[]#Top level file information. To be written
    iMotionsfile = open(glob.glob('*_*.txt')[0])#There is no other discrening feature to the name of the iMotions file
    iMotionsReader = csv.reader(iMotionsfile)
    # We need to read and store the first 4 line of the iMotions file in the clipped data folder, discard line 5, since it is empty and keep line 6, since it is the header line
    i = 1
    while i<=5:
        fileinfo.append(next(iMotionsReader))
        i=i+1
    headerrow = next(iMotionsReader)
    print "\n\n\nTOP LEVEL INFO:\n\n",fileinfo,'\n\n',headerrow
#in the main function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the data folder
    #Now to query all the files that exist in the data folder
    listoffolders = os.listdir('.')
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    #The os.listdir() returns a list of strings. each folder name is convenienetly a string
for foldername in listoffolders:
    os.chdir(foldername+'/')#Navigating into each folder
    print "Inside the participant data folder : ",foldername,'\n'
    ProcessiMoData()#Function to process the iMotions Data
    os.chdir('../')#Navigating back into the Data folder
