#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose: This file is to convert the values that are signal processed into the values for statistics
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import pandas as pd
from statistics import mean
from PlottingFunctions import *
LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
DEBUG = 1# To print statements for debugging
def ConvertHRToStats(hrheader,hrdata, participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert HR to stats for ", participant, " in ", section
            print "Test Print \n", "Header: " , hrheader , "\nData Sample:",hrdata[0:3]
    except Exception as e:
        print "Exception in HR processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the HR Data to Statistics.', 'Participant', particpant , 'Section' , section , 'Exception' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
def ConvertGSRToStats(gsrheader, gsrdata , participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert GSR to Stats for ", participant , " in ", section
            print "Test Print \n", "Header: " , gsrheader , "\nData Sample:",gsrdata[0:3]
    except Exception as e:
        print "Exception in GSR processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the GSR data to Statistics.' , 'Participant' , participant , 'Section', section , 'Exception', e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
def ConvertPDToStats(pdheader, pddata, participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert PD Data to Stats for ", participant , " in ", section
            print " Test Print\n", "Header: ", pdheader , "\nData Sample:" , pddata[0:3]
    except Exception as e:
        print "Exception in PD data processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the PD data to Statistics.' , 'Participant' , participant , 'Section', section , 'Exception', e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
def ConvertPERCLOSToStats(perclosheader, perclosdata, participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert PERCLOS Data to Stats for ", participant , " in ", section
            print " Test Print\n", "Header: ", perclosheader , "\nData Sample:" , perclosdata[0:3]
    except Exception as e:
        print "Exception in PERCLOS data processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the PERCLOS data to Statistics.' , 'Participant' , participant , 'Section', section , 'Exception', e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
if __name__ == '__main__':
    try:
        #output file prep
        file = open(LOGFILE, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Statistics Values Calculation.'])
        file.close()
        #Get all the participant folders in the Data folder
        listoffolders = os.listdir(MAINPATH+'/Data/')
        for folder in listoffolders:
            try:
                #Get list of subfolders in each participants ClippedData folder
                temp = os.listdir(MAINPATH+'/Data/'+folder+'/ClippedData/')
                listofsubfolders =[]
                for item in temp:
                    if 'SECTION' in item or 'Baseline' in item or 'EndSectionData' in item:
                        listofsubfolders.append(item)
                #listofsubfolders = listofsubfolders.sort()
                if DEBUG == 1:
                    print " \n\n\nList of subfolders for participant ", folder , " is: \n", listofsubfolders
                for subfolder in listofsubfolders:
                    Section_path = MAINPATH+'/Data/'+folder+'/ClippedData/'+subfolder+'/'
                    #Load the data
                    ###########################################Loading Data for analysis ######################################################
                    #Loading GSR data
                    try:
                        file = open(Section_path+'DSP_GSR.csv', 'r')
                        reader = csv.reader(file)
                        gsrheader = next(reader)
                        gsrdata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the GSR data : ", e
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the GSR data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                        file.close()
                    #Loading HR data
                    try:
                        file = open(Section_path+'DSP_FOR_HR.csv','r')
                        reader = csv.reader(file)
                        hrheader = next(reader)
                        hrdata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the HR data : ", e
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the HR data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                        file.close()
                    #Loading the Eye tracking Data
                    ETDATAFLAG = 1#ET data available
                    #Loading the PupilDiameter data
                    try:
                        file = open(Section_path+'DSP_FOR_PD.csv','r')
                        reader = csv.reader(file)
                        pdheader = next(reader)
                        pddata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the PD data : ", e
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the Eyetracking data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e, 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                        file.close()
                        ETDATAFLAG = 0
                    #Loading the PERCLOS Data
                    PERCLOSFLAG = 1# PERCLOS data available
                    try:
                        file = open(Section_path+'PERCLOS.csv', 'r')
                        reader = csv.reader(file)
                        perclosheader = next(reader)
                        perclosdata = list(reader)
                        file.close()
                    except Exception as e:
                        print "Exception at loading the PERCLOS data: " , e
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        file = open(LOGFILE, 'a')
                        writer = csv.writer(file)
                        writer.writerow(['Exception at loading the PERCLOS data.', 'Participant' , folder , 'Section' , subfolder , 'Exception:' , e, 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                        file.close()
                        PERCLOSFLAG= 0
                    #All the data is now loaded
                    #Test Print
                    #if DEBUG == 1:
                    #    print " GSR Data : ", gsrheader , "HR Header : " , hrheader
                    #    if ETDATAFLAG==1:
                    #        print " PD Data : ", pdheader
                    #Calling the individual Functions
                    ConvertHRToStats(hrheader, hrdata, folder, subfolder)
                    ConvertGSRToStats(gsrheader, gsrdata, folder, subfolder)
                    if ETDATAFLAG==1:
                        ConvertPDToStats(pdheader, pddata, folder, subfolder)
                    if PERCLOSFLAG==1:
                        ConvertPERCLOSToStats(perclosheader, perclosdata, folder, subfolder)
            except Exception as e:
                print " Participant level exception catcher :", # -*- coding: utf-8 -*-
                print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                file = open(LOGFILE, 'a')
                writer = csv.writer(file)
                writer.writerow(['Exception at participant level', 'Participant' , folder ,'Exception:' , e, 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                file.close()
    except Exception as e:
        print " Main Function Exception Catcher : " , e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at loading the Main Functio Level' , 'Exception:' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
