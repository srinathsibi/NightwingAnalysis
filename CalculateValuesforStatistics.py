#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose:
#   1. In each interval we extract the HR, PupilDiameter, GSR, Steer, Brake, Accel and other relevant data into a individual csv files and single averaged values for each interval
#   2. Single out the participants that are relevant and usable. Might have to revisit the pick sheet to see which ones are usable. This might be differnet from Dave's Criteria
#   3. Employ Signal processing for HR and GSR.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
def HRExtract(filename, infofilename, subfolder, folder):
    print " Extracting Heart Rate in Section :", subfolder, " for : ", folder
def GSRExtract(filename, infofilename, subfolder, folder):
    print " Extracting GSR in Section :", subfolder, " for : ", folder
def PupilDiaExtract(filename, infofilename, subfolder, folder):
    print " Extracting PupilDiameter in Section :", subfolder, " for : ", folder
def PERCLOSExtract(filename, subfolder, folder):
    print  " Estimating PERCLOS in Section :", subfolder, " for : ", folder
#Main Function
if __name__ == '__main__':
    outputfile = open(LOGFILE,'wb')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(['Output file and exception recorder for Python Script to '])
    outputfile.close()
    os.chdir(MAINPATH+'/Data/')
    listoffolders = os.listdir(MAINPATH+'/Data')
    print "List of folders in Data : \n" , listoffolders
    for folder in listoffolders:
        try:
            print " Analyzing Clipped Data Folder for :", folder
            #navigate to the Clipped Data Folder and locate all the subfolders that contain "SECTION??", "EndSectionData", "Baseline" in their name
            os.chdir(MAINPATH+'/Data/'+folder+'/ClippedData/')
            listofsubfolders = os.listdir('.')
            result = []
            print " List of elements in the ClippedData Folder\n" ,listofsubfolders
            for item in listofsubfolders:
                if 'SECTION' in item or 'Baseline' in item or 'EndSectionData' in item:
                    result.append(item)
            result.sort()#Doesn't sort the list the way we want, but it works for now and so we will keep it
            listofsubfolders = result
            print "End result of filtering the Folder names is : \n", listofsubfolders, "\n\n\n"
            for subfolder in listofsubfolders:
                #For each subfolder we now have one function per data column of interest. Passing the appropriate
                HRExtract('iMotionsFile.csv', 'iMotionsinfo.csv', subfolder, folder)
                GSRExtract('iMotionsFile.csv', 'iMotionsinfo.csv', subfolder, folder)
                PERCLOSExtract(glob.glob('PERCLOS*'), subfolder, folder)
                PupilDiaExtract('EyetrackingFile.csv', 'EyeTrackingInfo.csv', subfolder, folder)
                print "End of Section :", subfolder,  "\n"
        except Exception as e:
            print "Main Exception Catcher"
            file = open(LOGFILE,'a')
            writer = csv.writer(file)
            writer.writerow([' Main Function Exception Catcher '])
            file.close()
