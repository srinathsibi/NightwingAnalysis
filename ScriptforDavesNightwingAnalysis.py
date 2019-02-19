#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: This script is to extract the data from Sim, iMotions and Eye tracking data from
# 3 minutes before marker 3 (start of marker value 5) and 1 minute after the marker 4 (start of
# marker 10)
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
def ExtractData(foldername):
    print "In only function for study\n"
    iMotionsFile = open()
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Main Function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the folder containing the data
    listoffolders = os.listdir('.')#Getting the list of folders
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'
    for folder in listoffolders:
        os.chdir(folder + '/ClippedData/')
        #print "List of Contents in ClippedData Folder : \n", os.listdir('.')
        ExtractData(folder)
        os.chdir('../../')
    print "\n\n################# END OF SIGNAL PROCESSING! #################\n\n"
