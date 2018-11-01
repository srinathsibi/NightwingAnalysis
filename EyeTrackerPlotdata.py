# Srinath Sibi (ssibi@stanford.edu)
#Purpose: To analyze Eyetracker Data
import glob, os, csv, sys
import matplotlib as plt
import numpy as np

def FileCleaner(filereader):
    global PARTICIPANTNUMBER
    for i,row in enumerate(filereader):
        #this part was written to identify the end of the intro block.
        #Line of intro block end is at 31 using enumerate function on rows
        #There are empty lines in the eye tracker export file. Check README.md
        #try:
            #if row[0].split('\t')[0] == '##':
                #print "\nEnd of Intro Block at line: ", i, "\n"
                #row[0].split('\t') is the list of all elements in a row for the relevant Data
                #For the intro block , things are still messed up
                #print row[0].split('\t')[0], " : ", type(row[0].split('\t')[0]), "\n"
            if (row[0].split('\t')[0]).split(' ')[1] == 'Subject:':
                    print "\nThis is participant number:\t", row[0].split('\t')[1]
                    PARTICIPANTNUMBER = float(row[0].split('\t')[2])
        except:
            pass
            #print "Error at line :" , i , "\n", row , '\n'
    #First: Order of events: 1. Get participant number 2. Make Sub-Folder for subject information
    # 3. Write the information into a information file for each participant
    # 4. Make a text file for all the relevant data by using
###############Starting Main Function######################
if __name__ == '__main__':
#Look for eye tracking file in Data folder
    os.chdir('Data/EyeTrackingData/')
    print "In current folder!"
    #Listing all files in folder
    files = os.listdir('.')
    print "\nAll files in current folder:\n",files
    for f in files:
        try:
            file  = open(f, 'r')
            print "\nOperating on File:\n" , f
            csv_file = csv.reader(file)
            #Function to clean the file. It stores file in a separate file
            FileCleaner(csv_file)
            file.close()
        except:
            sys.exit("Unknown Error Encountered!")
