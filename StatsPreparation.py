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
LISTOFPARTICIPANTS =[]#This is the list of all participants in the Data folder
LISTOFSECTIONS =[]# List of all sections for a participant
DEBUG = 0# To print statements for debugging
CSV_COLUMNS = ['Baseline', 'SECTION0', 'SECTION1', 'SECTION2' ,'SECTION3', 'SECTION4', 'SECTION5' , 'SECTION6', 'SECTION7', 'SECTION8', 'SECTION9', 'SECTION10', 'SECTION11', 'SECTION12', 'SECTION13', 'SECTION14', 'SECTION15', 'SECTION16', 'SECTION17', 'SECTION18', 'SECTION19', 'SECTION20', 'SECTION21' , 'SECTION22', 'SECTION23', 'SECTION24', 'SECTION25', 'SECTION26', 'SECTION27', 'SECTION28', 'EndSectionData']
#This is the super set of all sections in the participant file in all the fields. Every participant dictionary key list should be a subset of this list
#OUTPUT FILES FOR ALL THE RELEVANT DATA
PERCLOSOUTPUT = os.path.abspath('.') + '/PERCLOSOUTPUT.csv'
HROUTPUT = os.path.abspath('.') + '/HROUTPUT.csv'
PDOUTPUT = os.path.abspath('.') + '/PDOUTPUT.csv'
GSROUTPUT = os.path.abspath('.') + '/GSROUTPUT.csv'
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
        perclos = [ float(perclosdata[i][1]) for i in range(len(perclosdata))]
        header = [ str(perclosheader[i]) for i in range(len(perclosheader)) ]
        dict = { str(section) : perclos}
        return dict
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
        writer.writerow(['Log file for Output Values Calculation to run stats on.'])
        file.close()
        #Prepare the files for aggregation for PERCLOS, HR, GSR and PD
        #PERCLOS
        file = open(PERCLOSOUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for PERCLOS values calculated .'])
        file.close()
        #HR
        file = open(HROUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for HR Values Calculation.'])
        file.close()
        #PD
        file = open(PDOUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for PD Values Calculation.'])
        file.close()
        #GSR
        file = open(GSROUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for GSR Values Calculation.'])
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
                #Initialize the dataframes for individual streams for a particpant
                participantperclosdf = pd.DataFrame()
                participantperclosdict = {}
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
                        perclosdict = ConvertPERCLOSToStats(perclosheader, perclosdata, folder, subfolder)
                        participantperclosdict.update(perclosdict)#So it looks like adding to a dictionary is better than adding to a dataframe. We can convert to a dataframe at the end of the participant loop.
                        if DEBUG == 1:
                            print " Participant:", folder, "Section: ", subfolder, " \n\nParticipant Perclos Dictionary :\n ", participantperclosdict
                if DEBUG==1:
                    print "\n\nKeys length : " , len(participantperclosdict.keys())
                    print "Participant Perclos Dictionary keys :\n" , participantperclosdict.keys()
                #Now aggregating the PERCLOS Data for all participants and printing them to previously aggregated file
                #We iterate through the section names in the CSV_COLUMNS and if the dictionary for a participant is not empty, then we fill an empty section value with [----] and move on to other participants
                #POPULATING PERCLOS
                f = open(PERCLOSOUTPUT,'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f, fieldnames = CSV_COLUMNS)
                #Final Dictionary to Write to the file
                perclosdict_new = {}
                for i,section in enumerate(CSV_COLUMNS):
                    if section in participantperclosdict.keys():
                        perclosdict_new.update( { str(section) : participantperclosdict[ str(section) ] } )
                    elif section not in participantperclosdict.keys():
                        perclosdict_new.update( { str(section) : ['No values here'] })
                if DEBUG==0:
                    print "\n\n\n\nThe ordered perclos dictionary for participant " , folder , "\nPERCLOS Dictionary :" , perclosdict_new
                w.writerow(['Participant :' + folder])
                dw.writeheader()
                dw.writerow(perclosdict_new)
                w.writerow([' '])#Blank spaces for easy reading
                w.writerow([' '])
                f.close()
            except Exception as e:
                print " Participant level exception catcher :", # -*- coding: utf-8 -*-
                print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                file = open(LOGFILE, 'a')
                writer = csv.writer(file)
                writer.writerow(['Exception at participant level', 'Participant' , folder ,'Exception:' , e, 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
                file.close()
            #print "\n\n Entire Participant perclos dataframe : ", participantperclos
    except Exception as e:
        print " Main Function Exception Catcher : " , e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at loading the Main Functio Level' , 'Exception:' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
