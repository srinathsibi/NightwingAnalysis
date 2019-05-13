#Author: Srinath Sibi Email: ssibi@stanford.edu
#Purpose: This script contains a PERCLOS function that take in the category Binocular, time and Window
#size and step information.
#Output of the file is no longer a returned array, it is instead a PERCLOS.csv file saved at the SECTION folder
# Variable description :
# t : This is the relative time variable at the start of all the extracted data
# catbin : Category Binocular column of data that contains whether the participant blinked or not
# LOGFILE : Absolute path to the log file for the program we are using
# participant : folder name for the participant we are running
# section : subfolder within the ClippedData folder that we are analyzing
# savepath : Abspath + participant + ClippedData + section (or the location where the file to be saved )
# WINDOWSIZE : Size of each window to be analyzed (default at 30 sec)
# WINDOWSTEP : Increment to the start of the window to calculate the perclos value, default at 10
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
DEBUG = 0#Variable to identify what if anything is wrong with the PERCLOS calcuator
def PERCLOSCal( t , catbin , LOGFILE, participant, section, savepath, WINDOWSIZE = 30, WINDOWSTEP =10):
    try:
        print "PERCLOS calcuator called."
        perclos = []#empty array into which perclos is calculated and stored.
        #set loop variables before the start of calcaulation for the first loop. Other requisite variables
        #set in the arguments list
        windowstart = t[0]
        #Loop start
        while windowstart < ((t[len(t)-1]-WINDOWSIZE) + 3):#I am trying to make it 4 windows and measures of PERCLOS from CATBIN data rather than 3, hence the +3
            windowstop = min(t, key=lambda x: abs(x - (windowstart+WINDOWSIZE)))
            if DEBUG ==1:
                print "Top of loop\n Window Start: ",windowstart, " Window Stop : ", windowstop
            startindex = t.index(windowstart)
            stopindex = t.index(windowstop)
            timewindow = t[startindex:stopindex]#Separating out the time variable for calculation purposes
            cbwindow = catbin[startindex:stopindex]#Separating the category binocular
            #Now calculate the requisite variable from the segregated raw variables
            eyeclosure = [1 if cbwindow[i] in ['Blink' , '-'] else 0 for i in range(len(cbwindow))]
            #PERCLOS is the weighted avg of the time interval with corresponding eyeclosure variables
            sum = 0#just a holding variable to calculate the weighted avg
            for i in range(len(timewindow)):
                if(i<1):
                    pass
                elif(i>=1):
                    sum = sum + (eyeclosure[i]*abs(t[i]-t[i-1]))
            weightedavg = sum / (abs( timewindow[len(timewindow)-1] - timewindow[0] ))
            perclos.append( [ (abs( timewindow[len(timewindow)-1] + timewindow[0] ) )/2 , weightedavg] )#Mid point of the time window
            #End condition
            windowstart = min(t, key=lambda x: abs(x - (windowstart+WINDOWSTEP)))
            if DEBUG ==1:
                print "Bottom of loop\n Window Start: ",windowstart, " Window Stop : ", windowstop
        # we now need to write the perclos array into a file at the section folder
        file = open(savepath+'/PERCLOS.csv','wb')
        writer = csv.writer(file)
        writer.writerow(['RelativeTime','PERCLOS'])
        writer.writerows([perclos[i][0] , perclos[i][1]] for i in range(len(perclos)))
        file.close()
    except Exception as e:
        print "Exception recorded here at the PERCLOS--------------\n",e
        file = open(LOGFILE,'a')
        writer = csv.writer(file)
        writer.writerow(['Exception recorded at the PERCLOS calculator for ', folder , ' at ', section, ' Exception : ', str(e)])
        file.close()
