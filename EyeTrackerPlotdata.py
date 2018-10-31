# Srinath Sibi (ssibi@stanford.edu)
#Purpose: To analyze Eyetracker Data
import glob, os, csv, sys
import matplotlib as plt
import numpy as np
#Line of intro block end is at 31 using enumerate function on rows
#There are empty lines in the eye tracker export file. Check README.md for
#more information.
def FileCleaner(filereader):
    for i,row in enumerate(filereader):
        try:
            if row[0].split('\t')[0] == '##':
                print "\nEnd of Intro Block at line: ", i, "\n"
                print row[0].split('\t')[0], " : ", type(row[0].split('\t')[0]), "\n"
        except:
            print "Error at line :" , i , "\n", row , '\n'
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
