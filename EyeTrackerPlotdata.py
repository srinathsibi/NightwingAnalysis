# Srinath Sibi (ssibi@stanford.edu)
#Purpose: To analyze Eyetracker Data
import glob, os, csv
import matplotlib as plt
import numpy as np




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
            file  = open(f)
            print "\nOperating on File:\n" , f
            csv_file = csv.reader(file)
            #function to process the files
            file.close()
        except:
            sys.exit("Unknown Error Encountered!")
