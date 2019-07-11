#Author: Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose : Testing the GSR and HR data signal processing for a single participant section. Choice : P028, Section : SECTION2
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from math import factorial
from scipy.signal import butter, lfilter, freqz
from statistics import mean
import scipy.signal as signal
#Function to eliminate the zero values in the HR data
#The plan is to identify all the points where the HR goes to 0. These points will be substituted with previous non zero values
def ZeroEliminationHR(HR):
    print "Eliminating zeros in the HR data"
    HRone = HR
    for i in range(len(HRone)):
        if HRone[i] <= 40 and i!=0 :
            HRone[i] = HRone[i-1]
        elif HRone[i] <= 40 and i == 0 :
            HRone[i] = mean(HRone)
    return HRone
def ZeroElimination(raw_signal,lowestvalue =0):
    print "Eliminating Zeros in signal"
    temp = raw_signal
    for i in range(len(temp)):
        if temp[i] <= lowestvalue and i!=0 :
            temp[i] = temp[i-1]
        elif temp[i] <= lowestvalue  and i ==0 :
            temp[i] = mean(temp)
    return temp
#Writing a shorter version of the plot function from PlottingFunctions.py script for quicker testing
def PlotData(x_data , y_data , z_data , ylabel , zlabel , plottitle , verticallineindices=[0] , xlabel = 'Time (in Seconds)'):
    print "Plotting function called for : ", ylabel
    try:
        #starting the plot
        fig = plt.figure()
        fig.tight_layout()
        plt.title(plottitle)
        plt.plot(x_data, y_data, 'r-', label = ylabel)
        plt.plot(x_data, z_data, 'g--', label = zlabel)
        if len(verticallineindices) > 1:#Meaning the verticallineindices array is not empty
            for i in range(len(verticallineindices)):
                if verticallineindices[i]==1:
                    plt.axvline(x = x_data[i], linewidth = '1')
        plt.xlabel(xlabel)
        plt.ylabel(str(ylabel) + ' and ' + str(zlabel))
        plt.legend(loc = 'upper right')
        plt.grid(color = 'b' , linestyle = '-.', linewidth = 0.25 )
        plt.show()
    except Exception as e:
        print "Exception at the plotting function in PlottingFunctions.py : ", e
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
    N = 5 #Filter order
    Wn = 0.002 #Cutoff frequency
    B, A = signal.butter(N, Wn, output = 'ba')
    output = signal.filtfilt(B,A,input).tolist()
    return output
# Sudden change detection function.
# Purpose : To detect suddent changes in the HR data and generate a second array that has ones when there is a sudden change in the HR values
def SuddenChangeDetection(Input):
    #Create an index for recording the points at which there are sharp changes in the input data stream
    changeindex = [0]*(len(Input)-1)
    for i in range(len(Input)):
        if i>1 and ( abs(Input[i] - Input[i-1]) >= 15 ):
            changeindex[i] = 1
    return changeindex
#main function
if __name__ == '__main__':
    try:
        print "Testing the signal processing"
        #Set Working Directory
        os.chdir(os.path.abspath('.') + '/Data/P028/ClippedData/SECTION3/')
        #verify
        print 'Files here are ', os.listdir('.')
        #Loading GSR data
        file = open('GSR.csv', 'r')
        reader = csv.reader(file)
        gsrheader = next(reader)
        gsrdata = list(reader)
        file.close()
        #Loading HR data
        file = open('HeartRate.csv','r')
        reader = csv.reader(file)
        hrheader = next(reader)
        hrdata = list(reader)
        file.close()
        ETDATAFLAG = 1#ET data available
        #Loading the PupilDiameter data
        try:
            file = open('PupilDiameter.csv','r')
            reader = csv.reader(file)
            pdheader = next(reader)
            pddata = list(reader)
            file.close()
        except Exception as e:
            print "There is no eye tracker data here :", # -*- coding: utf-8 -*-
            ETDATAFLAG = 0#ET data not available
            pass
        #All the data is now loaded
        #Use the PlotData function to plot as needed
        gsr_raw = [ float(gsrdata[i][1]) for i in range(len(gsrdata)) ]
        time_raw = [ float(gsrdata[i][0]) for i in range(len(gsrdata)) ]
        print " GSR values : ",gsr_raw[0:5],"\n"
        #Using Savitzky-Golay filter on the GSR data
        gsr_sg = savitzky_golay( np.array(gsr_raw), int(1001) , int(3) ).tolist()
        print type(gsr_sg), len(gsr_sg), len(gsrdata)
        #PlotData(time_raw, gsr_raw, gsr_sg, 'Raw GSR', 'Savitzky-Golay GSR', 'GSR Data Processing')
        #Using the simple low pass filter on the GSR data
        # First, design the Buterworth filter
        gsr_lp = LowPass(3, 0.002, gsr_raw)#signal.filtfilt(B, A, gsr_raw).tolist()
        print type(gsr_lp), len(gsr_raw), len(gsr_lp)
        #PlotData(time_raw, gsr_raw, gsr_lp, 'Raw GSR', 'Low Pass Filtered GSR' , 'GSR Data Processing')
        #Processing the HR data.
        time_raw = [ float(hrdata[i][0]) for i in range(len(hrdata)) ]
        hr_raw = [ float(hrdata[i][1]) for i in range(len(hrdata)) ]
        print " HR values :", hr_raw[0:10],"\n"
        hr_nz = ZeroElimination(hr_raw,40)
        hr_raw = [ float(hrdata[i][1]) for i in range(len(hrdata)) ]# For some reason, the values in the main function get edited though I pass arguments by value and not reference#FIX LATER
        #Detect the changes in the heart rate data
        HRChangeIndex = SuddenChangeDetection(hr_nz)
        PlotData(time_raw, hr_raw, hr_nz, 'RAW HR', ' HR with no zeros' , 'Comparing HR processes',HRChangeIndex)
        hr_lp = LowPass(3, 0.002, hr_nz)#signal.filtfilt(B,A,hr_nz).tolist()
        PlotData(time_raw, hr_nz, hr_lp ,'No zero HR', 'LP HR', 'Applying Low Pass Filter')
        #Processing eye tracking data. Depends on the availability of the Eye tracker data
        if ETDATAFLAG==1:
            pd_raw = [ float(pddata[i][1]) for i in range(len(pddata)) ]
            time_raw = [ float(pddata[i][0]) for i in range(len(pddata)) ]
            print " Pupil Diameter values : ", pd_raw[0:10], "\n"
            pd_nz = ZeroElimination(pd_raw)
            pd_raw = [ float(pddata[i][1]) for i in range(len(pddata)) ]
            PlotData( time_raw , pd_raw , pd_nz, ' Pupil Diameter', 'Zero Eliminated PD' , 'Plotting Raw Pupil Diameter ')
            #Based on observation, Pupil Diameter needs zero elimination and the low pass filter
    except Exception as e :
        print " Exception recorded here :", e
