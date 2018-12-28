#Specific data extraction
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
from moviepy.editor import *
#Main function
if __name__=='__main__':
    os.chdir('IgnoreThisFolder/ProcessedData/P023/')
    time_to_start_clipping = 1727.0
    time_to_stop_clipping = 1801.0
    #Video file clipping
    clip_ = VideoFileClip('File0.mp4')
    clip = clip_.subclip(time_to_start_clipping, time_to_stop_clipping)
    clip.write_videofile('ForWendy/File0.mp4', fps = clip_.fps , audio_bitrate="1000k")
    clip_ = VideoFileClip('File1.mp4')
    clip = clip_.subclip(time_to_start_clipping, time_to_stop_clipping)
    clip.write_videofile('ForWendy/File1.mp4', fps = clip_.fps , audio_bitrate="1000k")
    #iMotions File Clipping
    file = open('iMotionsData.csv','r')
    filereader = csv.reader(file)
    outfile = open('ForWendy/iMotionsDataSnap.csv','wb')
    outfile_writer = csv.writer(outfile)
    row_ = next(filereader)#header row
    print row_
    outfile_writer.writerow(row_)
    for row in filereader:
        #print row
        if float(row[0]) >= (time_to_start_clipping -180) and float(row[0]) <= (time_to_stop_clipping -180):
            outfile_writer.writerow(row)
    #Sim File Clipping
    file = open('SimData.csv','r')
    filereader = csv.reader(file)
    outfile = open('ForWendy/SimDataSnap.csv','wb')
    outfile_writer = csv.writer(outfile)
    row_ = next(filereader)#header row
    print row_
    outfile_writer.writerow(row_)
    for row in filereader:
        #print row
        if float(row[0]) >= (time_to_start_clipping -180) and float(row[0]) <= (time_to_stop_clipping -180):
            outfile_writer.writerow(row)
    #ET File Clipping
    file = open('EyeTrackingdata.csv','r')
    filereader = csv.reader(file)
    outfile = open('ForWendy/EyeTrackingdata.csv','wb')
    outfile_writer = csv.writer(outfile)
    row_ = next(filereader)#header row
    print row_
    outfile_writer.writerow(row_)
    for row in filereader:
        #print row
        if float(row[0]) >= (time_to_start_clipping -180) and float(row[0]) <= (time_to_stop_clipping -180):
            outfile_writer.writerow(row)
    #Plotting Data
