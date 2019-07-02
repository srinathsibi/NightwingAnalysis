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
def ZeroElimination(HR):
    print "Eliminating zeros in the HR data"
    HRone = HR
    for i in range(len(HRone)):
        if HRone[i] <= 40 and i!=0 :
            HRone[i] = HRone[i-1]
        elif HRone[i] <= 40 and i == 0 :
            HRone[i] = mean(HRone)
    return HRone
#Writing a shorter version of the plot function from PlottingFunctions.py script for quicker testing
def PlotData(x_data , y_data , z_data , ylabel , zlabel , plottitle , xlabel = 'Time (in Seconds)'):
    print "Plotting function called for : ", ylabel
    try:
        #starting the plot
        fig = plt.figure()
        fig.tight_layout()
        plt.title(plottitle)
        plt.plot(x_data, y_data, 'r-', label = ylabel)
        plt.plot(x_data, z_data, 'g--', label = zlabel)
        plt.xlabel(xlabel)
        plt.ylabel(str(ylabel) + ' and ' + str(zlabel))
        plt.legend(loc = 'upper right')
        plt.grid()
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
"""def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y"""
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
        #Loading the PupilDiameter data
        file = open('PupilDiameter.csv','r')
        reader = csv.reader(file)
        pdheader = next(reader)
        pddata = list(reader)
        file.close()
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
        N  = 3    # Filter order
        Wn = 0.002 # Cutoff frequency
        B, A = signal.butter(N, Wn, output='ba')
        gsr_lp = signal.filtfilt(B, A, gsr_raw).tolist()
        print type(gsr_lp), len(gsr_raw), len(gsr_lp)
        #PlotData(time_raw, gsr_raw, gsr_lp, 'Raw GSR', 'Low Pass Filtered GSR' , 'GSR Data Processing')
        #Move on to the HR data.
        time_raw = [ float(hrdata[i][0]) for i in range(len(hrdata)) ]
        hr_raw = [ float(hrdata[i][1]) for i in range(len(hrdata)) ]
        print " HR values :", hr_raw[0:10],"\n"
        hr_nz = ZeroElimination(hr_raw)
        hr_raw = [ float(hrdata[i][1]) for i in range(len(hrdata)) ]
        PlotData(time_raw, hr_raw, hr_nz, 'RAW HR', ' HR with no zeros' , 'Comparing HR processes')
    except Exception as e :
        print " Exception recorded here :", e
