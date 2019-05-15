#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose :
#1. For each section folder, we need plots for PupilDiameter, PERCLOS, GSR, HR , catbin
#2. We need to save the plots in the SECTION FOLDER
# We might need to write a function to get to the bottom of what the dimensions of the
#This function is used to plot the data:
#1. plotdata : 2 dimensional list of data that needs to be plotted
#2. xlabel and ylabel : axes labels for x and y axes , type : strings
#3. plottitle : The title of the plot at the top center of the plot, type : string
#4. savename : The name of the plot when saved, type : string, note: use pdf extension
#5. LOGFILE : Use the LOGFILE with absolute path, type : string
#6. participant : Participant folder, type: string
#7. section : section folder name , type : string
#8. savepath : the absolute location of the saved plot, type : string
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
plt.rcParams.update({'font.size': 3.5})
DEBUG = 0#Variable to identify what if anything is wrong with the PERCLOS calcuator
def PlotAndSaveData( plotdata, xlabel, ylabel, plottitle, savename, LOGFILE, participant, section, savepath ):
    print "Plotting function called in PlottingFunctions.py"
    try:
        x_data = [ float(plotdata[i][0]) for i in range(len(plotdata)) ]
        y_data = [ float(plotdata[i][1]) for i in range(len(plotdata)) ]
        #starting the plot
        fig = plt.figure()
        fig.tight_layout()
        plt.title(plottitle)
        plt.plot(x_data, y_data, 'r-', label = ylabel )
        if DEBUG == 1:
            print "First few elements of the x and y data are : ", x_data[0:3] ,'\n', y_data[0:3]
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc = 'upper right')
        plt.savefig(savepath + savename, bbox_inches = 'tight')
        plt.close()
    except Exception as e:
        print "Exception at the plotting function in PlottingFunctions.py : ", e
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow([' Exception in the plotting function ',  ' Participant: ' , participant , ' Section : ', section , '  ' , ' Exception: ', e])
        file.close()
