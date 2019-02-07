#Author : David Mengyun
from io import StringIO
import csv
import numpy as np
import pandas as pd
from datetime import datetime
import scipy.signal as signal
import matplotlib.pyplot as plt
df = pd.read_csv("IgnoreThisFolder/ProcessedData/P008/iMotionsData.csv")
hr = df['Cal InternalAdc13 (Shimmer Sensor)']
time = df['RelativeTime']
#To convert a pandas dataframe (df) to a numpy ndarray, use this code:
hr_arry = hr.values
time_arry = time.values
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Plotting imotions Data
imofile = open('IgnoreThisFolder/ProcessedData/P008/iMotionsData.csv','r')
imoreader = csv.reader(imofile)
skiplines(imoreader,1)
imodata = list(imoreader)
time = [float(imodata[i][0]) for i in range(len(imodata))]
eventmarker = [float(imodata[i][2]) for i in range(len(imodata))]

#Locating indices and respective times for vertical marker placement
xi = [eventmarker.index(1)]
xi.append(eventmarker.index(21))
xi.append(eventmarker.index(5))
xi.append(eventmarker.index(10))
xc = [time[xi[0]]]
for i in xi:
    xc.append(time[i])
#print "x coordinates: ", xc ,'\n'
# First, design the Buterworth filter
N  = 1    # Filter order
Wn = 0.00006#0.00005 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')

# Second, apply the filter to HR
hrf = signal.filtfilt(B,A, hr_arry)

# Make plots
fig = plt.figure()
ax1 = fig.add_subplot(211)
plt.plot(time_arry,hr_arry, 'b-')
plt.plot(time_arry,hrf, 'r-',linewidth=2)
plt.ylabel("PPG/HR")
plt.legend(['Original','Filtered'])

#vertical marker
for j in xc:
    plt.axvline(x = j, linewidth = 0.25)

plt.title("Physiological Data Plot (PPG)")
ax1.axes.get_xaxis().set_visible(True)


fig.savefig("FilteredPhysioData1.pdf",bbox_inches = 'tight')
plt.close()
