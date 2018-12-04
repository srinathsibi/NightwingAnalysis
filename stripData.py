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
    print "In all folder common actions"

#Start of main function
if __name__ == '__main__':
    os.chdir('Data/')#Moving to the data folder6
    listoffolders = os.listdir('.')
    print "\nInside Data Folder, these are the particpant folders located here :\n" , listoffolders, '\n'#, "\ntype: ", type(listoffolders[0])
    endflag = False
    options = {1: SingleParticipantFolderActions, 2: AllParticipantFolderActions}
    while not endflag:
        input = raw_input("\n\n\n\nChoose an option from here : \n\n1. Participant Number (Enter the number here) \n\n2. Common Operation to all participant folders (Type 'All') \n\n3.Exit (Type 'exit')\n\n")
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
