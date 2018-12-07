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
    print "In all folder common actions. This is a function to strip the iMotions, Eyetracking and the Sim Data. \
The stripped files will be stored in the ClippedData Folder as well."
    for folder in listoffolders:
        os.chdir(folder+'/ClippedData/')
        print "################# In folder : " , folder , " ####################"
        strip_imotions_data()
        strip_sim_data()
        strip_eyetracking_data()
        os.chdir('../../')
#iMotions data stripper function
def strip_imotions_data():
    print "\niMotions Stripping begun.\n"
#Sim data stripper function
#NOTE: The clipped Sim file is kinda weird. I added a column that indicated relative time ahead of all the other columns when clipping.
# As a result the row structure is weird; the first columsn is comma separateed and the rest are space separated. A row looks like this
# ['-179.9928 ', '832.716689999436 1 0 0 -0.29072093963623 -0.94616311788559 0 0.801034569740295 3 87.3806454483458 0.00137846119818993 10000 685.723448583853 -1 -0.630452023804135 -1.16954792851215 0.131464287638664 10000 685.723448583853 14.5829992294312 -0.0311381593346596 -0.0566742084920406 -3900.9013671875 526.386901855469 -0.533323347568512 0.424907571862279 -0.229437248585732 87.3191455874348 1432.11218261719 0.00977549608796835 0.00960742868483067 0.00513751804828644 0.00514872372150421 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1487556507 0 -1 0 1 8 8']
def strip_sim_data():
    print "\nSim Stripping begun.\n"
    headerkey = { 'RelativeTime': 0, 'SimTime': 1, 'EndAutonomousMode':2 , 'SitAwOnTab':3 , 'TakeOverOnTab':4, 'LonAccel':5 , 'LatAccel':6 , 'ThrottlePedal':7 ,'BrakePedal':8\
'Gear':9 ,'heading':10 , 'headingerror':11, 'headwaydist':12, 'headwaytime':13 ,'lanenumber':14 ,'laneoffset':15,'roadoffset':16, 'steeringwheelpos':17 ,\
'tailwaydist':18 , 'tailwaytime':19 , 'velocity':20, 'lateralvel':21 , 'verticalvel':22 , 'xpos':23 , 'ypos':24 , 'zpos':25, 'roll':26 , 'pitch':27\
'yaw':28, 'enginerpm':29 , 'slip1':30 , 'slip2':31 , 'slip3':33, 'slip4':34,'SubId' :54, 'DriveID' : 53, 'AutomationType':52 , 'ModeSwitch': 51 , 'EventMarker': 50 \
, 'SteerTouch': 49 , 'UnixTime':48 , ''}#Total of 55 columns in the row [index 0 - 54]. The first three columns after SimTime are SitAw options
# that were left behind a long time ago. Ignore them.
#Eyetracking data stripper function
def strip_eyetracking_data():
    print "\nEyetracking Stripping begun.\n"
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
