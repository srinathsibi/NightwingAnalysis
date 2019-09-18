#Author: Srinath Sibi , Email : ssibi@stanford.edu
#Purpose : Plot the heat maps for the physilogical data
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
import plotly.graph_objects as go
#import seaborn as sb
CSV_COLUMNS = ['Participant', 'Baseline1', 'Baseline2', 'Baseline3', 'Baseline4', 'Baseline5', 'Baseline6', 'Baseline7', 'Baseline8', 'Baseline9', 'Baseline10', 'SECTION0', 'SECTION1', 'SECTION2', 'SECTION3', 'SECTION4', 'SECTION5', 'SECTION6', 'SECTION7', 'SECTION8', 'SECTION9', 'SECTION10', 'SECTION11', 'SECTION12', 'SECTION13', 'SECTION14', 'SECTION15', 'SECTION16', 'SECTION17', 'SECTION18', 'SECTION19', 'SECTION20', 'SECTION21', 'SECTION22', 'SECTION23', 'SECTION24', 'SECTION25', 'SECTION26', 'SECTION27', 'SECTION28', 'SECTION29', 'SECTION30', 'SECTION31', 'SECTION32', 'SECTION33', 'SECTION34', 'SECTION35', 'SECTION36', 'SECTION37', 'SECTION38', 'SECTION39', 'SECTION40', 'SECTION41', 'SECTION42', 'SECTION43', 'SECTION44', 'SECTION45', 'SECTION46', 'SECTION47', 'SECTION48', 'SECTION49', 'SECTION50', 'SECTION51', 'SECTION52', 'SECTION53', 'SECTION54', 'SECTION55', 'SECTION56', 'SECTION57', 'SECTION58', 'SECTION59', 'SECTION60', 'SECTION61', 'SECTION62', 'SECTION63', 'SECTION64', 'SECTION65', 'SECTION66', 'SECTION67', 'SECTION68', 'SECTION69', 'SECTION70', 'SECTION71', 'SECTION72', 'SECTION73', 'SECTION74', 'SECTION75', 'SECTION76', 'SECTION77', 'SECTION78', 'SECTION79', 'SECTION80', 'SECTION81', 'SECTION82', 'SECTION83', 'SECTION84', 'SECTION85', 'SECTION86', 'SECTION87', 'SECTION88', 'SECTION89', 'SECTION90', 'SECTION91', 'SECTION92', 'SECTION93', 'SECTION94', 'SECTION95', 'SECTION96', 'SECTION97', 'SECTION98', 'SECTION99', 'SECTION100', 'SECTION101', 'SECTION102', 'SECTION103', 'SECTION104', 'SECTION105', 'SECTION106', 'SECTION107', 'SECTION108', 'SECTION109', 'SECTION110', 'SECTION111', 'SECTION112', 'SECTION113', 'SECTION114', 'SECTION115', 'SECTION116', 'SECTION117', 'SECTION118', 'SECTION119', 'SECTION120', 'SECTION121', 'SECTION122', 'SECTION123', 'SECTION124', 'SECTION125', 'SECTION126', 'SECTION127', 'SECTION128', 'SECTION129', 'SECTION130', 'SECTION131', 'SECTION132', 'SECTION133', 'SECTION134', 'SECTION135', 'SECTION136', 'SECTION137', 'SECTION138', 'SECTION139', 'SECTION140', 'SECTION141', 'SECTION142', 'SECTION143', 'SECTION144', 'SECTION145', 'EndSectionData1', 'EndSectionData2', 'EndSectionData3', 'EndSectionData4', 'EndSectionData5', 'EndSectionData6', 'EndSectionData7', 'EndSectionData8', 'EndSectionData9', 'EndSectionData10', 'EndSectionData11','EndSectionData12','EndSectionData13', 'EndSectionData14','EndSectionData15','EndSectionData16','EndSectionData17','EndSectionData18','EndSectionData19','EndSectionData20']
LOGFILE = os.path.abspath('.') + '/OutputFileForHeatMaps.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
FiletoRead = MAINPATH + '/GSRDEC_Cleaned.csv'#Change the file here for other files
DEBUG = 0;#DEBUG data flag
SUPERVISIONLIST = []
#Main Function
if __name__ == '__main__':
    try:
        #LOGFILE init
        file = open(LOGFILE, 'wb')
        writer = csv.writer(file)
        writer.writerow(['Error Log for Heat Maps production.'])
        file.close()
        #Opening the source file
        file = open(FiletoRead,'r')
        reader = csv.reader(file)
        #header file has 'Participants'+SECTION list
        header = next(reader)
        header.remove(header[0])
        data = list(reader)
        file.close()
        if DEBUG == 1:
            print " Header row: \n" , header , "\n\nData line:\n", data[3][0]
        participantlist = []
        for list in data:
            participantlist.append(list[0])
        if DEBUG == 1:
            print "\nParticipant List : ", participantlist
        zdata =[]#Initializing the data
        i = 1
        for list in data:
            list.remove(list[0])#Remove the participant number
            temp = []#Create an empty array for the float type data
            zdata.append(list)
        print " Compiled Data : \n", zdata
        fig = go.Figure( data = go.Heatmap( z = zdata[35:36] , x = header , y = participantlist[35:36] ))
        fig.show()
    except Exception as e:
        print "Exception in Heat Maps Main File", "\n Exception: " ,e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at Main Function for Heat Maps File', 'Exception' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
