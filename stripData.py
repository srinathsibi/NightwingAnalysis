#New file to strip the sim data into individual components based on the excel file given by dave
# We are going to try and build a plot function to plot and extract the specific columns of data as needed.
# NOTE: We are going to build it to be recursive with reagrds to the choice of
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
# The sigle participant folder actions have only plotting options for individual participant data. Make sure to run the AllParticipantFolderActions()
# at least once before you run the plot functions in this function
def SingleParticipantFolderActions():
    print "In single participant folder actions"
#This function is to strip the relevant data from the three major participant data files (iMotions, Sim and Eye Tracking)
def AllParticipantFolderActions():
    #print "In all folder common actions. This is a function to strip the iMotions, Eyetracking and the Sim Data. \
#The stripped files will be stored in the ClippedData Folder as well."
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        print "################# In folder : " , folder , " ####################"
        #Stripping the files in individual functions
        strip_imotions_data(folder)
        strip_sim_data(folder)
        strip_eyetracking_data(folder)
        MoveFiles(folder)
        os.chdir('../../')
#iMOTIONS DATA STRIPPING FUNCTION
def strip_imotions_data(foldername):
    print "\niMotions Stripping begun.\n"
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
    relevantcols = ['RelativeTime', 'UTCTimestamp', 'SimulatorEvent (0.0)', 'Steer (0.0)', 'Throttle (0.0)', 'Brake (0.0)', 'Cal InternalAdc13 (Shimmer Sensor)', \
'Speed (0.0)', 'Cal GSR (Shimmer Sensor)', 'Raw InternalAdc13 (Shimmer Sensor)', 'Raw GSR (Shimmer Sensor)']
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
    print "\nSim Stripping begun.\n"
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
    print "\nEyetracking Stripping begun.\n"
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
        print ' There are no clipped eye tracking files for this participant. Ingoring this participant\
        and moving on.'
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
#Function to move the files to the ProcessedData Folder
def MoveFiles(foldername):
    print "\nMoving Files to ProcessedData folder\n"
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
#Start of main function
if __name__ == '__main__':
    os.chdir('Data/')#Moving to the data folder6
    listoffolders = os.listdir('.')
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    endflag = False
    options = {1: SingleParticipantFolderActions, 2: AllParticipantFolderActions}
    while not endflag:
        input = raw_input("\n\n\n\nChoose an option from here : \n\n1. Participant Number (Enter the number here) \
\n\n2. Common Operation to all participant folders (Type 'All') \n\n3.Exit (Type 'exit')\n\n")
        if input == 'Exit' or input =='exit':
            endflag = True
            print "Ending Now! Goodbye!"
        elif input in listoffolders:
            print "This is the folder you chose : ", input
            choice  = 1
            options[choice]()
            pass
        elif input == 'All' or input == 'all':
            print "Processing all participants"
            choice = 2
            options[choice]()
            pass
        else:
            print "Enter a valid participant folder name or option in the list provided!"
            pass
    os.chdir('../')#Moving out of the Data folder
