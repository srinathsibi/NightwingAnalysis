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
#iMotions data: Both HR and GSR extracted here.
def iMotionsExtract(filename, infofilename, subfolder, folder):
    print " Extracting Heart Rate in Section :", subfolder, " for : ", folder
    try:
        HRCOL = 6#7th column in file
        GSRCOL = 8#9th column in file
        file = open(subfolder+'/iMotionsFile.csv','r')
        filereader = csv.reader(file)
        headerrow_ = next(filereader)
        #print " Header row in Imotions file is :", headerrow_ ,"\n"
        data = list(filereader)
        file.close()
        #print "First row : \n", data[0]
        #Writing the heart rate file #############################
        hrfile = open(subfolder+'/HeartRate.csv','wb')
        hrwriter = csv.writer(hrfile)
        hrwriter.writerow([headerrow_[0],headerrow_[HRCOL]])#Writing the header column for the heart rate file
        for row in data:
            hrwriter.writerow([row[0],row[HRCOL]])
        hrfile.close()
        #Writing the GSR file ####################################
        gsrfile = open(subfolder+'/GSR.csv','wb')
        gsrwriter = csv.writer(gsrfile)
        gsrwriter.writerow([headerrow_[0],headerrow_[GSRCOL]])#Writing the header column for the GSR file
        for row in data:
            gsrwriter.writerow([row[0],row[GSRCOL]])
        gsrfile.close()
    except Exception as e:
        print " Exception discovered at the iMotions Processing : ", e
        file = open(LOGFILE,'a')
        writer = csv.writer(file)
        writer.writerow([' iMotions Data Extraction Exception Catcher ', e, ' ' ,subfolder , ' ' , folder])
        file.close()
def PupilDiaExtract(filename, infofilename, subfolder, folder):
    print " Extracting PupilDiameter in Section :", subfolder, " for : ", folder
    try:
        CATBINCOL = 3#4th column in file
        PUPDIACOL = 2#3rd column in file
        file = open(subfolder+'/EyetrackingFile.csv','r')
        filereader = csv.reader(file)
        headerrow_ = next(filereader)
        data = list(filereader)
        file.close()
        #Writing the Pupil Diameter file ######################
        Pupdiafile = open(subfolder+'/PupilDiameter.csv','wb')
        Pupdiawriter = csv.writer(Pupdiafile)
        Pupdiawriter.writerow([headerrow_[0],headerrow_[PUPDIACOL]])
        for row in data:
            Pupdiawriter.writerow([row[0],row[PUPDIACOL]])
        Pupdiafile.close()
        #Writing the CategoryBinocular file ##################
        catbinfile = open(subfolder+'/CategoryBinocular.csv','wb')
        catbinwriter = csv.writer(catbinfile)
        catbinwriter.writerow([headerrow_[0], headerrow_[CATBINCOL]])
        for row in data:
            catbinwriter.writerow([row[0], row[CATBINCOL]])
        catbinfile.close()
    except Exception as e:
        print "Exception discovered at the Eye tracking Processing : ", e
        file = open(LOGFILE,'a')
        writer = csv.writer(file)
        writer.writerow([' Eyetracking Data extraction exception catcher ', e ,' ', subfolder , ' ' , folder])
        file.close()
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
                iMotionsExtract('iMotionsFile.csv', 'iMotionsinfo.csv', subfolder, folder)
                PERCLOSExtract(glob.glob('PERCLOS*'), subfolder, folder)
                PupilDiaExtract('EyetrackingFile.csv', 'EyeTrackingInfo.csv', subfolder, folder)
                print "End of Section :", subfolder,  "\n"
        except Exception as e:
            print "Main Exception Catcher"
            file = open(LOGFILE,'a')
            writer = csv.writer(file)
            writer.writerow([' Main Function Exception Catcher ', folder , e])
            file.close()
