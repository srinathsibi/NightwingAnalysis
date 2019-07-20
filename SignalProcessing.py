#Author : Srinath Sibi ssibi@stanford.edu
#Purpose : House the primary functions for signal processing for all the SECTION data (HR, GSR AND PUPDIA). This script is meant to be imported into the CalculateValuesforStatistics.py script
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import pandas as pd
from math import factorial
from scipy.signal import butter, lfilter, freqz
from statistics import mean
import scipy.signal as signal
from PlottingFunctions import Plot3Data
LOGFILE = os.path.abspath('.') + '/OutputFileForSignalProcessing.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
DEBUG = 1# To print statements dor debugging
#The plan is to identify all the points where the HR goes to 0. These points will be substituted with previous non zero values
def ZeroElimination(raw_signal,lowestvalue =0):
    print "Eliminating Zeros in signal"
    temp = raw_signal
    for i in range(len(temp)):
        if temp[i] <= lowestvalue and i!=0 :
            temp[i] = temp[i-1]
        elif temp[i] <= lowestvalue  and i ==0 :
            temp[i] = mean(temp)
    return temp
#savitzky_golay filter
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
#Low pass filter functions
def LowPass(order , cutoff , input):
    #Designing the filter first
    N = order #Filter order
    Wn = cutoff #Cutoff frequency
    B, A = signal.butter(N, Wn, output = 'ba')
    output = signal.filtfilt(B,A,input).tolist()
    return output
# Sudden change detection function.
# Purpose : To detect suddent changes in the HR data and generate a second array that has ones when there is a sudden change in the HR values
def SuddenChangeDetection(Input,change = 0):
    #Create an index for recording the points at which there are sharp changes in the input data stream
    changeindex = [0]*(len(Input))
    for i in range(len(Input)):
        if i>1 and ( abs(Input[i] - Input[i-1]) >= change ):
            changeindex[i] = 1
    return changeindex
#Function to replace the spikes in the data further based on markers. I am replacing the erroneous data around the spikes with None
#First we remove the band around the spikes as indicated by the markers and then remove the outliers by removing data 2*SDs away from mean
def RemoveErrData(input, markers, bandsize):#bandsize is in indices not in time interval
    print "In function to remove erroneous data."
    output = input
    try:
        for i in range(len(output)):
            if markers[i] == 1:
                for j in range(i-bandsize,i+bandsize):
                    output[j] = None
        #Create a temporary list with no None values
        temp = []
        for k in range(len(output)):
            if output[k]!=None:
                temp.append(output[k])
        #Remove data outside the 2*SD band
        mean = np.mean(temp)
        sd = np.std(temp)
        print " Mean :", mean, " standadrd deviation: ", sd, "\n"
        for i in range(len(output)):
            if output[i]>= (mean+2*sd) or output[i]<=(mean-2*sd):
                if output[i]!= None:
                    output[i] = None
        #Now adding the interpolation function using the pandas interpolation using the interpolation function
        #First replace the None with Nan
        df = pd.DataFrame( output, index = range(len(output)) , columns=['PupilDiameter'] )
        df.fillna(value=pd.np.nan, inplace=True)
        #print check for dataframe creation
        #for col in df.columns:
        #    print "Column :" , col
        df['A'] = df.PupilDiameter.interpolate(method='spline', order = 5)
        output = df.A.tolist()
        #print "Interpolated PD: ", output
    except Exception as e:
        print "************** Exception ************** : ", e
        pass
    return output
#Function to filter GSR
def FilterGSR(data, header , participant , section , LOGFILE= os.path.abspath('.') + '/OutputFileForSignalProcessing.csv'):
    try:
        gsr_raw = [ float(data[i][1]) for i in range(len(data)) ]
        time_raw = [ float(data[i][0]) for i in range(len(data)) ]
        if DEBUG == 1:
            print "\nFiltering GSR for participant :", participant, " in section : " , section
            print " GSR header", header , " data sample : ", gsr_raw[0:3]
        #data loaded
        #LowPass filter #ADD Other signal processing things here if needed
        gsr_lp = LowPass(3, 0.002, gsr_raw)
        gsr_raw = [ float(data[i][1]) for i in range(len(data)) ]
        #Data plot and save
        savepath = (MAINPATH+'/Data/'+participant+'/ClippedData/'+section+'/')
        Plot3Data( time_raw, gsr_raw , gsr_lp , ' Raw GSR Data ' , ' Low Passed GSR ' , 'GSR Signal Processing' , 'DSP_FOR_GSR.pdf' , LOGFILE , participant , section , savepath, [] , 0 )#No need for grids here
        #Save Data
        file = open( savepath+'/DSP_GSR.csv' , 'wb')
        writer = csv.writer(file)
        writer.writerow([header[0] , header[1] , 'Filtered GSR'])
        for i in range(len(gsr_raw)):
            writer.writerow([ time_raw[i] , gsr_raw[i] , gsr_lp[i] ])
        file.close()
    except Exception as e:
        print "Exception discovered at the GSR filtering function ", e
        file = open( LOGFILE , 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception discovered at the GSR filtering function for ', participant , 'at section', section , ' Exception : ', e])
        file.close()
#Function to filter PPG
def FilterHR(data, header , participant , section , LOGFILE= os.path.abspath('.') + '/OutputFileForSignalProcessing.csv'):
    try:
        hr_raw = [ float(data[i][1]) for i in range(len(data)) ]
        time_raw = [ float(data[i][0]) for i in range(len(data)) ]
        if DEBUG == 1:
            print "\nFiltering HR for participant :", participant, " in section : " , section
            print " HR header : ", header , " Data Sample : ", hr_raw[0:3]
        #data loaded
        #Signal Processing
        hr_nz = ZeroElimination(hr_raw, 40)
        hr_raw = [ float(data[i][1]) for i in range(len(data)) ]
        HRChangeIndex = SuddenChangeDetection(hr_raw, 15)
        hr_lp = LowPass(3, 0.002 , hr_nz)
        hr_raw = [ float(data[i][1]) for i in range(len(data)) ]
        #Plot and Save Data
        savepath = (MAINPATH+'/Data/'+participant+'/ClippedData/'+section+'/')
        Plot3Data ( time_raw, hr_raw, hr_lp , ' Raw HR ' , ' Low Passes HR ' , ' HR Signal Processing ', 'DSP_FOR_HR.pdf' , LOGFILE , participant , section , savepath, HRChangeIndex )
        #Save Data
        file = open( savepath+'/DSP_FOR_HR.csv' , 'wb')
        writer = csv.writer(file)
        writer.writerow([ header[0] , header[1] , 'Filtered HR', ' Sudden Change Indicators'])
        for i in range(len(hr_raw)):
            writer.writerow([ time_raw[i] , hr_raw[i] , hr_lp[i] , HRChangeIndex[i] ])
        file.close()
    except Exception as e:
        print " Exception discovered at the GSR filtering function ", e
        file = open (LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception discovered at the HR filtering function for ', participant, 'at section', section , ' Exception: ', e])
        file.close()
#Function to filter PupDia
def FilterPupilDiameter(data, header , participant, section , LOGFILE= os.path.abspath('.') + '/OutputFileForSignalProcessing.csv'):
    try:
        print "Filtering Pupil Diameter for participant :", participant, " in section : " , section
    except Exception as e:
        print " Exception discovered at the Pupil Diameter filtering function", e
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerrow(['Exception discovered at the Pupil Diamter filtering function for ', participant, 'at section', section, 'Exception:',e])
        file.close()
#Function to filter Catbin
#Not sure, we need it. The perclos function extracts the relevant data pretty well.
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
if __name__ == '__main__':
    outputfile = open(LOGFILE,'wb')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerow(['Output file and exception recorder for Python Script to signal process and eliminate bad data.'])
    outputfile.close()
    DataFolder_path = MAINPATH+'/Data/'
    os.chdir(DataFolder_path)
    listoffolders = os.listdir(MAINPATH+'/Data/')
    print "List of folders in Data : \n" , listoffolders
    for folder in listoffolders:
        try:
            print " \n\n\nSignal Processing for participant :" , folder
            ClippedData_path = MAINPATH+'/Data/'+folder+'/ClippedData/'
            #print " List of subfolders in the Clipped Data folder \n", os.listdir(ClippedData_path)
            listofsubfolders = os.listdir(ClippedData_path)
            result =[]
            for item in listofsubfolders:
                if 'SECTION' in item or 'Baseline' in item or 'EndSectionData' in item:
                    result.append(item)
            result.sort()#Doesn't sort the list the way we want, but it works for now and so we will keep it
            listofsubfolders = result
            print " Relevant subfolders in the Clipped Data folder\n " , listofsubfolders
            for subfolder in listofsubfolders:
                try:
                    print " \n\nIn SECTION: ", subfolder
                    Section_path = ClippedData_path+subfolder+'/'
                    ###########################################Loading Data and processing them for analysis ######################################################
                    #Loading GSR data
                    try:
                        file = open(Section_path+'GSR.csv', 'r')
                        reader = csv.reader(file)
                        gsrheader = next(reader)
                        gsrdata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the GSR data : ", e
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the GSR data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e])
                        file.close()
                    #Loading HR data
                    try:
                        file = open(Section_path+'HeartRate.csv','r')
                        reader = csv.reader(file)
                        hrheader = next(reader)
                        hrdata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the HR data : ", e
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the HR data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e])
                        file.close()
                    #Loading the Eye tracking Data
                    ETDATAFLAG = 1#ET data available
                    #Loading the PupilDiameter data
                    try:
                        file = open(Section_path+'PupilDiameter.csv','r')
                        reader = csv.reader(file)
                        pdheader = next(reader)
                        pddata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the PD data : ", e
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the Eyetracking data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e])
                        file.close()
                        ETDATAFLAG = 0
                    #All the data is now loaded
                    #Test Print
                    if DEBUG == 1:
                        print " GSR Data : ", gsrheader , "HR Header : " , hrheader
                        if ETDATAFLAG==1:
                            print " PD Data : ", pdheader
                    #Now calling Individual functions for signal processing.
                    FilterGSR(gsrdata, gsrheader , folder , subfolder)
                    FilterHR(hrdata , hrheader , folder, subfolder)
                    if ETDATAFLAG == 1:
                        FilterPupilDiameter(pddata, pdheader, folder, subfolder)
                    #All the files in individual sections should be analyzed and plotted.
                    #################################################################################################################################################
                except Exception as e:
                    print "Participant Level Exception Catcher" ,e
                    file = open(LOGFILE,'a')
                    writer = csv.writer(file)
                    writer.writerow(['Participant Level Exception Catcher.', 'Participant:', folder , 'Section:', subfolder, 'Exception:', e])
                    file.close()
        except Exception as e:
            print "Main Exception Catcher" ,e
            file = open(LOGFILE,'a')
            writer = csv.writer(file)
            writer.writerow([' Main Function Exception Catcher ', folder , e])
            file.close()
