#Author: Srinath Sibi ssibi@stanford.edu
#Purpose: To create windowed data like Dave's End Section Creation File, but instead of Multiple Windows, we create 1 baseline window from -180 to 0 and several
# WINDOWSIZE windows, each window's start time a fixed STEPSIZE ahead of the previous window's start time.
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from moviepy.editor import *
from StripData import PERCLOS
#Function to load the data to the
#Main Function
if __name__=='__main__':
    os.chdir('Data/')#Moving to the folder containing the data
    listoffolders = os.listdir('.')
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        print " Inside folder : ", ClippedData
        LoadData(folder)
        os.chdir('../../')
