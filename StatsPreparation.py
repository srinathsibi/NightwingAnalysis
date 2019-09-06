#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose: This file is to convert the values that are signal processed into the values for statistics
#Conversion to values for Statistics:
# 1. PERCLOS is retained as is
# 2. HR is averaged out in the interval and the max value in the interval is also calculated
# 3. GSR decline is calculated ( positive or negative ), we also calculate the average
# 4. PD is averaged out the interval.
import glob, os, sys, shutil,re
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
import math
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
#This is hardcoded list of CSV columns, this is a backup if the dynamic computation of the CSV columns doesn't work.
#CSV_COLUMNS = ['Baseline', 'SECTION0', 'SECTION1', 'SECTION2' ,'SECTION3', 'SECTION4', 'SECTION5' , 'SECTION6', 'SECTION7', 'SECTION8', 'SECTION9', 'SECTION10', 'SECTION11', 'SECTION12', 'SECTION13', 'SECTION14', 'SECTION15', 'SECTION16', 'SECTION17', 'SECTION18', 'SECTION19', 'SECTION20', 'SECTION21' , 'SECTION22', 'SECTION23', 'SECTION24', 'SECTION25', 'SECTION26', 'SECTION27', 'SECTION28',\
#'SECTION29','SECTION30','SECTION31', 'SECTION32','SECTION33','SECTION34','SECTION35','SECTION36','SECTION37','SECTION38' ,'SECTION32', 'EndSectionData']
#This is the super set of all sections in the participant file in all the fields. Every participant dictionary key list should be a subset of this list
#OUTPUT FILES FOR ALL THE RELEVANT DATA
PERCLOSOUTPUT = os.path.abspath('.') + '/PERCLOSOUTPUT.csv'
HROUTPUT = os.path.abspath('.') + '/HROUTPUT.csv'#Contains avg HR output
PDOUTPUT = os.path.abspath('.') + '/PDOUTPUT.csv'#Contains avg PD output
GSROUTPUT = os.path.abspath('.') + '/GSROUTPUT.csv'#Contains avg GSR output
HRMAXOUTPUT = os.path.abspath('.') + '/HRMAXOUTPUT.csv'#Contains max HR output
PDMAXOUTPUT = os.path.abspath('.') + '/PDMAXOUTPUT.csv'#Contains max PD output
GSRDECOUTPUT = os.path.abspath('.') + '/GSRDECOUTPUT.csv'#Contains DECrease in tonic GSR
def SeparateListIntoPieces(inputlist , numpieces, participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG ==1:
            print " Function to split list into pieces called."
        avg = len(inputlist) / float(numpieces)
        out = []
        last = 0.0
        while last < len(inputlist):
            out.append(inputlist[int(last):int(last+avg)])
            last = last+avg
        return out
    except Exception as e:
        print "Exception in list splitting function for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception in function to cut list into pieces.', 'Participant', participant , 'Section' , section , 'Exception' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
def ConvertHRToStats(hrheader,hrdata, participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert HR to stats for ", participant, " in ", section
            print "Test Print \n", "Header: " , hrheader , "\nData Sample:",hrdata[0:3]
        if section not in ['Baseline','EndSectionData']:
            filteredhr = [ float(hrdata[i][2]) for i in range(len(hrdata)) ]
            hravg = mean(filteredhr)# we take the 10 second intervalsand average the values over it
            hrmax = max(filteredhr)
            dict = { str(section) : [hravg, hrmax] }
            return dict
        elif section in ['Baseline','EndSectionData']:
            filteredhr = [ float(hrdata[i][2]) for i in range(len(hrdata)) ]
            time = [ float(hrdata[i][0]) for i in range(len(hrdata)) ]
            hrpieces = SeparateListIntoPieces(filteredhr,  math.floor( abs(time[-1] - time[0])/20 ), participant, section)#This is done to make sure that the Baseline and EndSectionData sections don't get averaged out into a single value
            hravg = []
            hrmax = []
            for list in hrpieces:
                hravg.append(mean(list))
                hrmax.append(max(list))
            #Need to add them to different pieces of the baseline and EndSection
            dict = {}
            for i in range(len(hravg)):
                if section in ['Baseline']:
                    dict.update({ str('Baseline') + str(i+1) : [ hravg[i] , hrmax[i] ] })
                if section in ['EndSectionData']:
                    dict.update({ str('EndSectionData') + str(i+1) : [ hravg[i] , hrmax[i] ] })
            #dict = {str(section): [hravg , hrmax]}
            if DEBUG == 1:
                print "\n\n\nParticipant: ", participant, "  Section: ", section
                print "\nThe length of HRavg : " , len(hravg)
                print "\nThe length of HRmax : " , len(hrmax), '\n\n'
            return dict
    except Exception as e:
        print "Exception in HR processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the HR Data to Statistics.', 'Participant', participant , 'Section' , section , 'Exception' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
def ConvertGSRToStats(gsrheader, gsrdata , participant, section , LOGFILE = os.path.abspath('.') + '/OutputFileForStatsPreparation.csv'):
    try:
        if DEBUG==1:
            print "Convert GSR to Stats for ", participant , " in ", section
            print "Test Print \n", "Header: " , gsrheader , "\nData Sample:",gsrdata[0:3]
        if section not in ['Baseline', 'EndSectionData']:
            filteredgsr = [ float(gsrdata[i][2]) for i in range(len(gsrdata)) ]
            seperatedlists = SeparateListIntoPieces(filteredgsr, 10 , participant, section)
            decreasesinGSR = []#Array that records the decrease in GSR for the 10 intervals
            for i in range(len(seperatedlists)):
                decreasesinGSR.append( seperatedlists[i][-1]  - seperatedlists[i][0] )
            avg_decGSR = mean( decreasesinGSR )
            avg_GSR = mean ( filteredgsr )
            dict  = { str(section) : [avg_decGSR , avg_GSR] }
            return dict
        elif section in ['Baseline' , 'EndSectionData']:
            filteredgsr = [ float(gsrdata[i][2]) for i in range(len(gsrdata)) ]
            time = [ float(gsrdata[i][0]) for i in range(len(gsrdata)) ]
            separatelists = SeparateListIntoPieces(filteredgsr, math.floor( abs( time[-1] - time[0] )/20 ), participant, section)#Adjust the number of intervals formed here
            #For each interval in the Separatelists, we have
            avg_decGSR = []
            avg_GSR =[]
            for list in separatelists:
                if len(list)>5:#We ignore the really short lists that are formed as a result of the list cutting
                    temp=[]
                    index = 0
                    inc = int(len(list)/10)
                    while (index+inc+1) < len(list):
                        temp.append( ( list[index+inc] - list[index] ) )
                        index = index + inc
                    avg_decGSR.append( mean(temp) )# Mean reduction in GSR over an interval
                    avg_GSR.append( mean(list) )# Mean GSR over an interval
                elif len(list)<=5:
                    if DEBUG == 0:
                        print "There's a very short list here. "
            if DEBUG == 1:
                print "\n\n\nParticipant: ", participant, "  Section: ", section
                print "\nThe length of avg dec in GSR ", len(avg_decGSR)
                print "\nThe length of avg dec in GSR ", len(avg_GSR) , "\n\n"
            #Adding a new bit to create multiple section of Baseline and EndSectionData
            dict ={}#Empty dict
            for i in range(len(avg_GSR)):
                if section in ['Baseline']:
                    dict.update ( { 'Baseline' + str(i+1) : [avg_decGSR[i], avg_GSR[i]] } )
                elif section in ['EndSectionData']:
                    dict.update ( { 'EndSectionData' + str(i+1) : [avg_decGSR[i], avg_GSR[i]] } )
            #dict = { str(section) : [avg_decGSR , avg_GSR] }
            return dict
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
        if section not in ['Baseline','EndSectionData']:
            filteredpd = [ float(pddata[i][2]) for i in range(len(pddata)) ]
            pdavg = mean(filteredpd)# we take the 10 second intervalsand average the values over it
            pdmax = max(filteredpd)
            dict = { str(section) : [pdavg, pdmax] }
            return dict
        elif section in ['Baseline' , 'EndSectionData']:
            filteredpd = [ float(pddata[i][2]) for i in range(len(pddata)) ]
            time = [ float(pddata[i][0]) for i in range(len(pddata)) ]
            pdpieces = SeparateListIntoPieces(filteredpd , math.floor( abs(time[-1] - time[0])/20 ), participant, section)#This is done to make sure that the Baseline and EndSectionData sections don't get averaged out into a single value
            pdavg = []
            pdmax = []
            for list in pdpieces:
                pdavg.append(mean(list))
                pdmax.append(max(list))
            #Adding a new bit to create multiple sections of Baseline and EnsSectionData
            dict = {}
            for i in range(len(pdavg)):
                if section in ['Baseline']:
                    dict.update( { 'Baseline'+str(i+1): [ pdavg[i],pdmax[i] ] })
                if section in ['EndSectionData']:
                    dict.update( { 'EndSectionData'+str(i+1): [ pdavg[i],pdmax[i] ] })
            #dict = { str(section) : [pdavg, pdmax] }
            if DEBUG == 1:
                print "\n\n\nParticipant: ", participant, "  Section: ", section
                print "\nThe length of pdavg : " , len(pdavg)
                print "\nThe length of pdmax : " , len(pdmax) , "\n\n"
            return dict
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
        dict = {}
        if section not in ['Baseline','EndSectionData']:
            dict = { str(section) : perclos}
        elif section in ['Baseline','EndSection']:
            for i in range(len(perclos)):
                if section in ['Baseline']:
                    dict.update( {'Baseline'+str(i+1) : perclos[i]} )
                elif section in ['EndSectionData']:
                    dict.update( { 'EndSectionData'+str(i): perclos[i] } )
        return dict
    except Exception as e:
        print "Exception in PERCLOS data processing to stats for ", participant, " in ", section
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Converting the PERCLOS data to Statistics.' , 'Participant' , participant , 'Section', section , 'Exception', e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
#We use this function as a key to sorting a list of subfolders.
def SortFunc1(e):
    return int( re.sub('SECTION','',e) )
#We use this function as a key to sorting the list of folders (participants)
def SortFunc2(e):
    return int( re.sub('P','',e) )
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
        #HR_AVG
        file = open(HROUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Average HR Values Calculation.'])
        file.close()
        #HR_MAX
        file = open(HRMAXOUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Maximum HR Values Calculation.'])
        file.close()
        #PD_AVG
        file = open(PDOUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Average PD Values Calculation.'])
        file.close()
        #PD_MAX
        file = open(PDMAXOUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Maximum PD Values Calculation.'])
        file.close()
        #GSR_AVG
        file = open(GSROUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Average GSR Values Calculation.'])
        file.close()
        #GSR_MAX
        file = open(GSROUTPUT, 'wb')
        writer = csv.writer(file)
        writer.writerow([' Output file for Maximum GSR Values Calculation.'])
        file.close()
        #Get all the participant folders in the Data folder
        listoffolders = os.listdir(MAINPATH+'/Data/')
        #Sorting the participants list means the output will be ordered and clean rather than at random
        listoffolders.sort(key=SortFunc2)
        for folder in listoffolders:
            try:
                #Get list of subfolders in each participants ClippedData folder
                temp = os.listdir(MAINPATH+'/Data/'+folder+'/ClippedData/')
                listofsubfolders =[]
                for item in temp:
                    if 'SECTION' in item:# or 'Baseline' in item or 'EndSectionData' in item:
                        listofsubfolders.append(item)
                # We need to sort the list to make sure that the CSV columns are properly structured.
                #We add 'Baseline' and 'EndSectionData' to the list post sorting
                listofsubfolders.sort(key=SortFunc1)
                CSV_COLUMNS = ['Participant','Baseline1','Baseline2','Baseline3','Baseline4','Baseline5','Baseline6','Baseline7','Baseline8','Baseline9','Baseline10'] + listofsubfolders \
                + ['EndSectionData1','EndSectionData2','EndSectionData3','EndSectionData4','EndSectionData5','EndSectionData6','EndSectionData7','EndSectionData8','EndSectionData9','EndSectionData10']# Here we set the CSV_COlUMNS. We can either use the listofsubfolders or we can
                listofsubfolders = listofsubfolders +['EndSectionData']
                listofsubfolders = ['Baseline']+listofsubfolders

                if DEBUG == 0:
                    print " \n\n\nList of subfolders for participant ", folder , " is: \n", CSV_COLUMNS
                #Need to order the list of subfolders
                #Initialize the dataframes for individual streams for a particpant
                participantperclosdict = {}
                participanthrdict = {}
                participantpddict = {}
                participantgsrdict = {}
                #Now iterate through the subsections
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
                    participanthrdict.update(ConvertHRToStats(hrheader, hrdata, folder, subfolder))#Adding to the participant HR dictionary
                    participantgsrdict.update(ConvertGSRToStats(gsrheader, gsrdata, folder, subfolder))#Adding to the participant GSR dictionary
                    if ETDATAFLAG==1:
                        participantpddict.update(ConvertPDToStats(pdheader, pddata, folder, subfolder)) # Adding to the participant pd dictionary
                    if PERCLOSFLAG==1:
                        perclosdict = ConvertPERCLOSToStats(perclosheader, perclosdata, folder, subfolder)
                        participantperclosdict.update(perclosdict)#So it looks like adding to a dictionary is better than adding to a dataframe. We can convert to a dataframe at the end of the participant loop.
                        if DEBUG == 1:
                            print " Participant:", folder, "Section: ", subfolder, " \n\nParticipant Perclos Dictionary :\n ", participantperclosdict
                if DEBUG==1:
                    print "\n\nKeys length : " , len(participanthrdict.keys())
                #Now aggregating the PERCLOS Data for all participants and printing them to previously aggregated file
                #We iterate through the section names in the CSV_COLUMNS and if the dictionary for a participant is not empty, then we fill an empty section value with [----] and move on to other participants
                #We add participant number to all the dictionaries to be the first column instead of a separate row. We expect this to be the first column in all data rows.
                participanthrdict.update({'Participant':folder})
                participantgsrdict.update({'Participant':folder})
                participantpddict.update({'Participant':folder})
                participantperclosdict.update({'Participant':folder})
                #########################################################################################
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
                if DEBUG==1:
                    print "\n\n\n\nThe ordered perclos dictionary for participant " , folder , "\nPERCLOS Dictionary :" , perclosdict_new
                #w.writerow(['Participant :' + folder])
                dw.writeheader()
                dw.writerow(perclosdict_new)
                f.close()
                #########################################################################################
                #Populating HR Average values
                f = open(HROUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f, fieldnames = CSV_COLUMNS)
                #Final HR dictionary to write to output file
                hrdict_new ={}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participanthrdict.keys():
                        hrdict_new.update( { str(section) : participanthrdict[str(section)][0] } )
                    elif section not in participanthrdict.keys():
                        hrdict_new.update( { str(section) : ['No values here '] } )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(hrdict_new)
                f.close()
                #########################################################################################
                #Populating HR Max Values
                f = open(HRMAXOUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f, fieldnames = CSV_COLUMNS)
                #Final HR dictionary to write to output file
                hrdict_new ={}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participanthrdict.keys():
                        hrdict_new.update( { str(section) : participanthrdict[str(section)][1] } )
                    elif section not in participanthrdict.keys():
                        hrdict_new.update( { str(section) : ['No values here '] } )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(hrdict_new)
                f.close()
                #########################################################################################
                #Populating Average PD
                f= open(PDOUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f , fieldnames = CSV_COLUMNS)
                #Final PD Dictionary to write to output file
                pddict_new = {}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participantpddict.keys():
                        pddict_new.update( { str(section) : participantpddict[str(section)][0] } )
                    elif section not in participantpddict.keys():
                        pddict_new.update( {str(section) : ['No values here']} )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(pddict_new)
                f.close()
                #########################################################################################
                #Populating Maximum PD
                f= open(PDMAXOUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f , fieldnames = CSV_COLUMNS)
                #Final PD Dictionary to write to output file
                pddict_new = {}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participantpddict.keys():
                        pddict_new.update( { str(section) : participantpddict[str(section)][1] } )
                    elif section not in participantpddict.keys():
                        pddict_new.update( {str(section) : ['No values here']} )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(pddict_new)
                f.close()
                #########################################################################################
                #Populating Avg in GSR
                f = open(GSROUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f , fieldnames = CSV_COLUMNS)
                #Final GSR Dictionary to write to the output file
                gsrdict_new = {}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participantgsrdict.keys():
                        gsrdict_new.update( { str(section) : participantgsrdict[str(section)][1] } )
                    elif section not in participantgsrdict.keys():
                        gsrdict_new.update( { str(section) : ['No values here'] } )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(gsrdict_new)
                f.close()
                #########################################################################################
                #Populating Avg DECREASE in GSR
                f = open(GSRDECOUTPUT, 'a')
                w = csv.writer(f)
                dw = csv.DictWriter(f , fieldnames = CSV_COLUMNS)
                #Final GSR Dictionary to write to the output file
                gsrdict_new = {}
                for i, section in enumerate(CSV_COLUMNS):
                    if section in participantgsrdict.keys():
                        gsrdict_new.update( { str(section) : participantgsrdict[str(section)][0] } )
                    elif section not in participantgsrdict.keys():
                        gsrdict_new.update( { str(section) : ['No values here'] } )
                #w.writerow(["Participant :"+folder])
                dw.writeheader()
                dw.writerow(gsrdict_new)
                f.close()
                #########################################################################################
                print " END OF PARTICIPANT ", folder , "\n"
                print "\n\n\n\n#################################################################################################################################################################"
                print "#################################################################################################################################################################"
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
