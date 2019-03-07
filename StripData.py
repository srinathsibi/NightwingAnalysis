# Author: Srinath Sibi ssibi@stanford.edu
#Purpose: The goal is to strip the relevant columns of data from the existing files and plot the relevant streams of data.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 3.5})
#Create and save plots of relevant data to peruse and make sure that there are no problems before analysis.
def PlotParticipantData():
    #chosenfolder = raw_input("\n\nPlease enter the name of the participant whose data we need to plot (e.g. P006/P010/P027...)\n\n")
    for chosenfolder in listoffolders:
        #chosenfolder = raw_input("\n\nPlease enter an acceptable folder name!\n\n")
        os.chdir(chosenfolder+'/ClippedData/')#Navigating in to the participant subfolder.
        #print "\n ****** Plotting for participant:", chosenfolder, " Opening all stripped files *******\n"
        #Wondering if I should sim data. There is nothing there that we need now for now.
        #simfile = open('StrippedSimData.csv','r')
        #simreader = csv.reader(simfile)
        #skiplines(simreader,1)
        #simdata = list(simreader)
        try:
            #Plotting imotions Data
            imofile = open('StrippediMotionsData.csv','r')
            imoreader = csv.reader(imofile)
            skiplines(imoreader,1)
            imodata = list(imoreader)
            time = [float(imodata[i][0]) for i in range(len(imodata))]
            eventmarker = [float(imodata[i][2]) for i in range(len(imodata))]
            steer = [float(imodata[i][3]) for i in range(len(imodata))]
            throttle = [float(imodata[i][4]) for i in range(len(imodata))]
            brake = [float(imodata[i][5]) for i in range(len(imodata))]
            PPG = [float(imodata[i][6]) for i in range(len(imodata))]
            speed = [float(imodata[i][7]) for i in range(len(imodata))]
            GSR = [float(imodata[i][8]) for i in range(len(imodata))]
            #Locating indices and respective times for vertical marker placement
            # Markers for participants under 61
            if int(chosenfolder[1:4])<=61:
                xi = [eventmarker.index(1)]
                xi.append(eventmarker.index(21))
                xi.append(eventmarker.index(5))
                xi.append(eventmarker.index(10))
                xc = [time[xi[0]]]
                for i in xi:
                    xc.append(time[i])
                print "x coordinates: ", xc ,'\n'
            # Markers for participants over 62
            if int(chosenfolder[1:4])>=61:
                xi = [eventmarker.index(1)]
                xi.append(eventmarker.index(5))
                xi.append(eventmarker.index(10))
                xc = [time[xi[0]]]
                for i in xi:
                    xc.append(time[i])
                print "x coordinates: ", xc ,'\n'
            #Starting the iMotions Figure here.
            imofig1 = plt.figure(1)
            imofig1.tight_layout()
            plt.subplot(411)
            plt.title('Driving Data Plot (Steer/Throttle/Brake)')
            plt.plot(time, steer, 'r-', label = 'Steer')
            plt.xlabel('Time (sec)')
            plt.ylabel('Steer')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j, linewidth = 0.25)
            plt.subplot(412)
            plt.plot(time, throttle, 'b-', label = 'Throttle')
            plt.xlabel('Time (sec)')
            plt.ylabel('Throttle')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j , linewidth = 0.25)
            plt.subplot(413)
            plt.plot(time, brake, 'g-', label = 'Brake')
            plt.xlabel('Time (sec)')
            plt.ylabel('Brake')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j , linewidth = 0.25)
            plt.subplot(414)
            plt.plot(time, speed, 'b-', label = 'Speed')
            plt.xlabel('Time (sec)')
            plt.ylabel('Speed')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j , linewidth = 0.25)
            imofig1.savefig("iMotionsDrivingData.pdf",bbox_inches = 'tight')
            plt.close()
            #END OF FIGURE 1
            imofig2 = plt.figure(1)
            imofig2.tight_layout()
            plt.subplot(211)
            plt.title('Physiological Data Plot (PPG/GSR)')
            plt.plot(time, PPG , 'r-', label = 'PPG')
            plt.legend(loc = 'upper right')
            plt.xlabel('Time (sec)')
            plt.ylabel('PPG/HR')
            for j in xc:
                plt.axvline(x = j , linewidth = 0.25)
            plt.subplot(212)
            plt.plot(time, GSR, 'g-', label = 'GSR')
            plt.xlabel('Time (sec)')
            plt.ylabel('GSR')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j , linewidth = 0.25)
            imofig2.savefig("iMotionsPhysioData.pdf", bbox_inches = 'tight')
            plt.close()
            #END OF FIGURE 2
        except:
            print "Participant : ", chosenfolder ," has bad data. Please exclude from analysis."
            '''if os.path.isfile('BadData.txt'):
                pass
            else:
                markerfile = open('BadData.csv','wb')
                markerwriter = csv.writer(markerfile)
                markerfile.close()'''
            pass
        #Plotting Eye Tracker Data
        try:
            etfile = open('StrippedEyeTrackingFile.csv','r')
            etreader = csv.reader(etfile)
            skiplines(etreader,1)
            etdata = list(etreader)
            # Plotting the marker using counter in the indexbinocular column.
            time = [float(etdata[i][0]) for i in range(len(etdata))]
            catbin =  [etdata[i][3] for i in range(len(etdata))]
            pupdia =[];indexbin = []#initializing to populate them later
            for i in range(len(etdata)):
                try:
                    pupdia.append(float(etdata[i][2]))
                except ValueError:
                    pupdia.append(0)
                try:
                    indexbin.append(etdata[i][15])
                except ValueError:
                    indexbin.append('-')
            # Function to calculate PERCLOS stats from catbin variable and time variable
            perclos_array = PERCLOS(time, catbin)
            #print "PERCLOS: \n", len(perclos_array)," \n\n\n", perclos_array
            if perclos_array[0][0] != 0:
                perclos_file = open('PERCLOS.csv', 'wb')
                percloswriter = csv.writer(perclos_file)
                percloswriter.writerow(['Time','PERCLOS'])
                percloswriter.writerows([ perclos_array[i][1], perclos_array[i][0] ] for i in range(len(perclos_array)))
                perclos_file.close()
            #x = [ time[i] for i in range(len(etdata)) if catbin[i] == 'User Event']# This produces the same results as xc from above
            #Starting the eyetracker Figure here.
            etfig = plt.figure(1)
            etfig.tight_layout()
            plt.subplot(211)
            plt.title('Eye Tracking Data Plot (Pupil Diameter/Blinks)')
            plt.plot(time, pupdia, 'r-', label = 'Pupil Diameter')
            plt.xlabel('Time (sec)')
            plt.ylabel('Pupil Diameter (mm)')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j, linewidth = 0.25)
            plt.subplot(212)
            plt.plot([perclos_array[i][1]for i in range(len(perclos_array))] , [perclos_array[i][0] for i in range(len(perclos_array))] , 'b--', label = 'PERCLOS')
            plt.xlabel('Time (sec)')
            plt.ylabel('PERCLOS ( 0 - 1 )')
            plt.legend(loc = 'upper right')
            for j in xc:
                plt.axvline(x = j, linewidth = 0.25)
            etfig.savefig("EyeTrackerData.pdf",bbox_inches = 'tight')
            plt.close()
            #END OF FIGURE 3
        except IOError:
            print "Eye tracker data for: ", chosenfolder ,"is not available to plot. This participant has an error with markers or the eye tracker data wasn't recorded."
            '''if os.path.isfile('BadData.txt'):
                pass
            else:
                markerfile = open('BadData.csv','wb')
                markerwriter = csv.writer(markerfile)
                markerfile.close()'''
            pass
        os.chdir('../../')#Navigating back to the main folder now.
#This function is to strip the relevant data from the three major participant data files (iMotions, Sim and Eye Tracking)
def StripData():
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        #print "################# In folder : " , folder , " ####################"
        #Stripping the files in individual functions
        strip_imotions_data(folder)
        strip_sim_data(folder)
        strip_eyetracking_data(folder)
        os.chdir('../../')
#PERCLOS CALCULATION function
def PERCLOS(t , CategoryBinocular):
    try:
        #print "Calculating PERCLOS"
        #PARAMETERS FOR
        WINDOWSIZE = 60# 60 second window size
        STEPSIZE = 10# 10 second step size
        windowstart = t[0]# Initialized to the start of the time variable
        perclos = []# Perclos array to be sent back to the
        # we proceed till the windowstart variable reaches the end of the CategoryBinocular length
        while windowstart < t[len(t) - 10]:
            windowstop = min(t, key =lambda x:abs(x-(windowstart + 60)))
            #print " Window start : ", windowstart, " Window stop: ", windowstop, "\n\n"
            startindex = t.index(windowstart)
            stopindex = t.index(windowstop)
            t_ = t[startindex:stopindex]
            cbwindow = CategoryBinocular[startindex:stopindex]
            #We are going to change the 'Blink' and '-' values to 1 and setting the rest to 0. Easier to calculate PERCLOS this way
            eyeclosure = [ 1 if cbwindow[i] in ['Blink', '-'] else 0 for i in range(len(cbwindow))]
            #PERCLOS is calculated as time(t_ variable) weighted average of the eyeclosure variable.
            sum =0# To calculate average
            for i in range(len(t_)-1):
                sum = sum + (eyeclosure[i]*abs(t_[i+1]-t_[i]))
            perclos_result = sum / abs(t_[len(t_)-1] - t_[0])
            perclos.append([perclos_result, (t_[len(t_)-1] + t_[0])/2 ])
            windowstart = min(t, key =lambda x:abs(x-(windowstart + 10))) #windowstart + 10;# 10 sec time step.
        return perclos
    except IndexError:
        print " Empty array for eye tracking => Empty eye tracking file. Consider fixing."
        '''if os.path.isfile('BadData.txt'):
            pass
        else:
            markerfile = open('BadData.csv','wb')
            markerwriter = csv.writer(markerfile)
            markerfile.close()'''
        return [[0,0]]
#iMOTIONS DATA STRIPPING FUNCTION
def strip_imotions_data(foldername):
    #print "\niMotions Stripping begun.\n"
    infofile = open('iMotionsInfo.csv', 'r')
    file = open('iMotionsClipped.csv','r')
    inforeader = csv.reader(infofile)
    filereader = csv.reader(file)
    skiplines(inforeader,5)
    headerrow = next(inforeader)
    #Ensuring that the first column is identical for all stripped files
    del headerrow[0]
    headerrow.insert(0,'RelativeTime')
    headerkey = {headerrow[i]:i for i in range((len(headerrow)))}
    if int(foldername[1:4])<=61:
        relevantcols = ['RelativeTime', 'UTCTimestamp', 'SimulatorEvent (0.0)', 'Steer (0.0)', 'Throttle (0.0)', 'Brake (0.0)', 'Cal InternalAdc13 (Shimmer Sensor)', \
'Speed (0.0)', 'Cal GSR (Shimmer Sensor)', 'Raw InternalAdc13 (Shimmer Sensor)', 'Raw GSR (Shimmer Sensor)']
    if int(foldername[1:4])>=62:
        relevantcols = ['RelativeTime', 'UTCTimestamp', 'SimulatorEvent (0.0)', 'Steer (0.0)', 'Throttle (0.0)', 'Brake (0.0)', 'Heart Rate PPG  (Beats/min) (2)', \
'Speed (0.0)', 'GSR CAL (\xc2\xb5Siemens) (2)', 'Internal ADC A13 PPG CAL (mVolts) (2)', 'GSR CAL (kOhms) (2)']
    #print headerkey, '\n'
    strippediMotionsfile = open('StrippediMotionsData.csv' , 'wb')
    strippediMotionswriter = csv.writer(strippediMotionsfile)
    strippediMotionswriter.writerow(relevantcols)
    for row in filereader:
        strippedrow = [ row[headerkey[i]] for i in relevantcols ]
        strippediMotionswriter.writerow(strippedrow)
    infofile.close()
    strippediMotionsfile.close()
    file.close()
    #print "************** Participant " , foldername , " iMotions file stripped to essential data!**************"
#SIM DATA STRIPPING FUNCTION
#NOTE: The clipped Sim file is kinda weird. I added a column that indicated relative time ahead of all the other columns when clipping.
# As a result the row structure is weird; the first columsn is comma separateed and the rest are space separated. A row looks like this
# ['-179.9928 ', '832.716689999436 1 0 0 -0.29072093963623 -0.94616311788559 0 0.801034569740295 3 87.3806454483458 0.00137846119818993 10000 685.723448583853 -1 -0.630452023804135 -1.16954792851215 0.131464287638664 10000 685.723448583853 14.5829992294312 -0.0311381593346596 -0.0566742084920406 -3900.9013671875 526.386901855469 -0.533323347568512 0.424907571862279 -0.229437248585732 87.3191455874348 1432.11218261719 0.00977549608796835 0.00960742868483067 0.00513751804828644 0.00514872372150421 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1487556507 0 -1 0 1 8 8']
def strip_sim_data(foldername):
    #print "\nSim Stripping begun.\n"
    if int(foldername[1:4])<=61:
        headerkey = { 'RelativeTime': 0, 'SimTime': 1, 'EndAutonomousMode':2 , 'SitAwOnTab':3 , 'TakeOverOnTab':4, 'LonAccel':5 , 'LatAccel':6 , 'ThrottlePedal':7 ,'BrakePedal':8 ,\
    'Gear':9 ,'Heading':10 , 'HeadingError':11, 'HeadwayDistance':12, 'HeadwayTime':13 ,'LaneNumber':14 , 'LaneOffset':15 , 'RoadOffset':16, 'SteeringWheelPos':17 ,\
    'TailwayDistance':18 , 'TailwayTime':19 , 'Velocity':20, 'LateralVelocity':21 , 'verticalvel':22 , 'xpos':23 , 'ypos':24 , 'zpos':25, 'Roll':26 , 'Pitch':27 ,\
    'Yaw':28, 'enginerpm':29 , 'slip1':30 , 'slip2':31 , 'slip3':33, 'slip4':34,'SubId' :54, 'DriveID' : 53, 'AutomationType':52 , 'ModeSwitch': 51 , 'EventMarker': 50 , \
    'SteerTouch': 49 , 'UnixTime':48 }#Total of 55 columns in the row [index 0 - 54]. The first three columns after SimTime are SitAw options
    # that were left behind a long time ago. Ignore them.
        #relevantcols is meant to contain the relevant columns for stripping data. I might add functionality to choose the columns as needed.
        relevantcols = ['RelativeTime' , 'SimTime' , 'LonAccel' , 'LatAccel' , 'ThrottlePedal','BrakePedal'\
    ,'Heading' , 'HeadingError', 'HeadwayDistance', 'HeadwayTime' ,'LaneNumber' ,'LaneOffset' , 'RoadOffset', 'SteeringWheelPos',\
    'TailwayDistance' , 'TailwayTime' , 'Velocity', 'LateralVelocity','Roll' , 'Pitch' , 'Yaw', 'EventMarker' , 'UnixTime']
    #The columns are different for participants over 62 (control case)
    if int(foldername[1:4])>=62:
        headerkey = { 'RelativeTime': 0, 'SimTime': 1, 'LonAccel':2 , 'LatAccel':3 , 'ThrottlePedal':4 ,'BrakePedal':5 ,\
    'Gear':6 ,'Heading':7 , 'HeadingError':8, 'HeadwayDistance':9, 'HeadwayTime':10 ,'LaneNumber':11 , 'LaneOffset':12 , 'RoadOffset':13, 'SteeringWheelPos':14 ,\
    'TailwayDistance':15 , 'TailwayTime':16 , 'Velocity':17, 'LateralVelocity':18 , 'verticalvel':19 , 'xpos':20 , 'ypos':21 , 'zpos':22, 'Roll':23 , 'Pitch':24 ,\
    'Yaw':25, 'enginerpm':26 , 'slip1':27 , 'slip2':28 , 'slip3':30, 'slip4':31,'SubId' :51, 'DriveID' : 50, 'AutomationType':49 , 'ModeSwitch': 48 , 'EventMarker': 47 , \
    'SteerTouch': 46 , 'UnixTime':45 }# The first three columns after SimTime are SitAw options that were removed from the automation condition(Participants 006-061). Hence the number of columns is different.
        #relevantcols is meant to contain the relevant columns for stripping data. I might add functionality to choose the columns as needed.
        relevantcols = ['RelativeTime' , 'SimTime' , 'LonAccel' , 'LatAccel' , 'ThrottlePedal','BrakePedal'\
    ,'Heading' , 'HeadingError', 'HeadwayDistance', 'HeadwayTime' ,'LaneNumber' ,'LaneOffset' , 'RoadOffset', 'SteeringWheelPos',\
    'TailwayDistance' , 'TailwayTime' , 'Velocity', 'LateralVelocity','Roll' , 'Pitch' , 'Yaw', 'EventMarker' , 'UnixTime']
    simfile = open('ClippedSimData.csv','r')
    simreader = csv.reader(simfile)
    strippedsimfile = open('StrippedSimData.csv' , 'wb')
    strippedsimwriter = csv.writer(strippedsimfile)
    strippedsimwriter.writerow(relevantcols)
    for row in simreader:
        simline = row[1].split(' ')
        del row[-1]
        row = row + simline
        strippedrow = [ row[headerkey[i]] for i in relevantcols ]
        strippedsimwriter.writerow(strippedrow)
    strippedsimfile.close()
    simfile.close()
    #print "************** Participant " , foldername , " sim file stripped to essential data!**************"
#Eyetracking data stripper function
def strip_eyetracking_data(foldername):
    #print "\nEyetracking Stripping begun.\n"
    try:
        infofile = open('EyeTrackingInfo.csv','r')
        inforeader = csv.reader(infofile)
        eyetrackingfile = open('EyetrackingClipped.csv','r')
        eyetrackingreader = csv.reader(eyetrackingfile)
        strippedETfile = open('StrippedEyeTrackingFile.csv' , 'wb')
        strippedETwriter = csv.writer(strippedETfile)
        skiplines(inforeader,4)
        headerrow = next(inforeader)
        #Ensuring that the first column is identical for all stripped files
        del headerrow[0]
        headerrow.insert(0,'RelativeTime')
        headerkey = {headerrow[i]:i for i in range((len(headerrow)))}
        #print headerkey , '\n'
        relevantcols = ['RelativeTime', 'Time of Day [h:m:s:ms]', 'Pupil Diameter Right [mm]', 'Category Binocular', 'Point of Regard Binocular Y [px]' , 'Point of Regard Left Y [px]' , 'Pupil Diameter Left [mm]', 'Gaze Vector Left Y', 'Gaze Vector Left X', 'Gaze Vector Left Z'\
        , 'Point of Regard Left X [px]', 'Gaze Vector Right Y', 'Gaze Vector Right X', 'Gaze Vector Right Z', 'Tracking Ratio [%]', 'Index Binocular' ,  'Point of Regard Right Y [px]', 'Point of Regard Binocular X [px]' , 'Point of Regard Right X [px]']
        strippedETwriter.writerow(relevantcols)
        for row in eyetrackingreader:
            strippedrow = [ row[headerkey[i]] for i in relevantcols ]
            strippedETwriter.writerow(strippedrow)
        infofile.close()
        eyetrackingfile.close()
        strippedETfile.close()
        #print "************** Participant " , foldername , " eye tracking file stripped to essential data!**************"
    except IOError:
        print ' There are no clipped eye tracking files for participant : ', foldername, '\n'
        '''if os.path.isfile('BadData.txt'):
            pass
        else:
            markerfile = open('BadData.csv','wb')
            markerwriter = csv.writer(markerfile)
            markerfile.close()'''
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#This function is to only move data after stripping and plotting them
def MoveData():
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        MoveFiles(folder)
        os.chdir('../../')
#Function to move the files to the ProcessedData Folder
def MoveFiles(foldername):
    #print "\nMoving Files to ProcessedData folder\n"
    path = '../../../IgnoreThisFolder/ProcessedData/'
    if not os.path.exists(path+foldername):
        os.mkdir(path+foldername)
    if not os.path.exists(path+foldername+'/RawData/'):#Path to the raw data folder created. Moving the data to the
        os.mkdir(path+foldername+'/RawData/')
    path = path+foldername +'/'
    #Moving the stripped files now
    try:
        shutil.copy('StrippedSimData.csv', path+'SimData.csv')
    except IOError:
        print "Sim File not here for  : "+foldername
        pass
    try:
        shutil.copy('StrippediMotionsData.csv' , path+'iMotionsData.csv')
    except IOError:
        print "iMotions file not here for  : "+foldername
        pass
    try:
        shutil.copy('File1.mp4', path+'File1.mp4')
    except IOError:
        print "File1.mp4 not here for  : "+foldername
        pass
    try:
        shutil.copy('File0.mp4', path+'File0.mp4')
    except IOError:
        print "File0.mp4 not here for  : "+foldername
        pass
    try:
        shutil.copy('StrippedEyeTrackingFile.csv', path+'EyeTrackingdata.csv')
    except IOError:
        print "Eye tracking file not here for  : "+foldername
        pass
    try:
        shutil.copy('EyeTrackingInfo.csv', path+'EyeTrackingInfo.csv')
    except IOError:
        print "Eye tracking Info file not here for  : "+foldername
        pass
    try:
        shutil.copy('iMotionsInfo.csv', path+'iMotionsInfo.csv')
    except IOError:
        print " iMotions Info File is not here for ", foldername
        pass
    try:
        shutil.copy('PERCLOS.csv', path+'PERCLOS.csv')
    except IOError:
        print " PERCLOS File is not here for ", foldername
        pass
    try:#plot 1
        shutil.copy('EyeTrackerData.pdf', path+'EyeTrackerDataPlot.pdf')
    except IOError:
        print " EyeTracker Plot File is not here for ", foldername
        pass
    try:#plot 2
        shutil.copy('iMotionsPhysioData.pdf', path+'iMotionsDataPlot.pdf')
    except IOError:
        print " iMotions Plot File is not here for ", foldername
        pass
    try:#plot 3
        shutil.copy('iMotionsDrivingData.pdf', path+'DrivingDataPlot.pdf')
    except IOError:
        print " Diving Data Plot File is not here for ", foldername
        pass
#Start of main function
if __name__ == '__main__':
    os.chdir('Data/')#Moving to the data folder6
    listoffolders = os.listdir('.')#['P062','P063','P064','P065','P066','P067','P068','P069','P070','P071','P072','P073','P074','P075','P076','P077','P078','P079','P080','P081','P082','P083','P084','P085']#
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    options = {1: StripData, 2: PlotParticipantData, 3: MoveData}
    options[1]()
    options[2]()
    options[3]()
    os.chdir('../')#Moving out of the Data folder
