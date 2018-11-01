# Srinath Sibi (ssibi@stanford.edu)
#Purpose: To analyze Eyetracker Data
import glob, os, csv, sys
import matplotlib as plt
import numpy as np
#Line of intro block end is at 31 using enumerate function on rows
#There are empty lines in the eye tracker export file. Check README.md
#Order of events:
#1. Get participant number
#2. Make Sub-Folder for subject information
# 3. Write the information into a information file for each participant
# 4. Make a text file for all the relevant data by using
    #if row[0].split('\t')[0] == '##':
        #print "\nEnd of Intro Block at line: ", i, "\n"
        #row[0].split('\t') is the list of all elements in a row for the relevant Data
        #For the intro block , things are still messed up
PARTICIPANTNUMBER = 0;
#############Get participant number#########################
def GetParticipantNumber(filereader):
    #print row[0].split('\t')[0], " : ", type(row[0].split('\t')[0]), "\n"
    pnum = 0
    for i,row in enumerate(filereader):
        try:
            if (row[0].split('\t')[0]).split(' ')[1] == 'Subject:':
                pnum = float(row[0].split('\t')[1])
                break
        except:
            pass
    return pnum
###############Get and Write Intro Info into the subfolder########
def WriteIntroInfo(filereader):
    if os.path.exists('P' + str(int(PARTICIPANTNUMBER))):
        os.chdir('P' + str(int(PARTICIPANTNUMBER)))
        print "Inside the participant folder P" + str(int(PARTICIPANTNUMBER)) ,"\n"
        os.chdir('../')
###############Starting Main Function######################
if __name__ == '__main__':
    #Look for eye tracking file in Data folder
    global PARTICIPANTNUMBER
    os.chdir('Data/EyeTrackingData/')
    print "In current folder!"
    #Listing all files in folder
    files = os.listdir('.')
    #print "\nAll files in current folder:\n",files
    for f in files:
        file  = open(f, 'r')
        print "\nOperating on File:\n" , f
        csv_file = csv.reader(file)
        PARTICIPANTNUMBER = GetParticipantNumber(csv_file)#Get participant number
        print "Participant number is : " , PARTICIPANTNUMBER , "\n"
        #Make a new folder with the same name as the participant
        if not os.path.exists('P' + str(int(PARTICIPANTNUMBER))):
            os.makedirs('P'+str(int(PARTICIPANTNUMBER)))
            print "Participant folder created.\n"
        #MAKE A ELSE STATEMENT FOR IF THE FOLDER ALREADY EXISTS
        #write intro information into a txt file in subfolder for each participant
        WriteIntroInfo(csv_file)
        file.close()
