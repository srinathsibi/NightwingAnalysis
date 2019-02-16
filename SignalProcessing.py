#Author : Srinath Sibi ssibi@stanford.edu
#Purpose : This code is meant to signal process the Physiological signals in the data set and
# weed out the spikes in the data. We also have to resample the data. We have to resample the data and
# and put it into a folder that has just the fitered data.
# It is important to note that each measure needs a different method of filtering.
# 1. GSR: As such needs no filtering. It seems relatively easy to read with some spikes
# but they are usually significant
# 2. PPG: Needs a lot of work:
#   a) First replace the parts that have zeroes with previous values
#   b) Then apply the resampling with butterworth bandpass filter
# 3. Pupil Diameter: Needs some work:
#   a)Pupil diamter data goes to zero very often. Need to replace the zero values with previous value
#   b)Need for more filters might come after. Bandpass filters might be unnecessary, Maybe even a
#    simple moving average filter.
# 4. PERCLOS is derived from Category Binocular. We have an extracted PERCLOS file, but the underlying
# catbin data might need some filtering. Investigate when you are done with all other filters.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
#Function to filter GSR
def FilterGSR():
    print "Filtering GSR"
#Function to filter PPG
def FilterHR():
    print "Filtering HR"
#Function to filter PupDia
def FilterPupilDiameter():
    print "Filtering Pupil Diameter"
#Function to filter Catbin
def FilterCategoryBinocular():
    print "Filtering Category Binocular"
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
        FilterGSR()
        FilterHR()
        FilterPupilDiameter()
        FilterCategoryBinocular()
        os.chdir('../../')
    print "\n\n################# END OF SIGNAL PROCESSING! #################\n\n"
