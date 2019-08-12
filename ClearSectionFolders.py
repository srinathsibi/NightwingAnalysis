#Author: Srinath Sibi
#Purpose: To remove the section folders in the ClippedData path
import shutil, os, sys, csv
LOGFILE = os.path.abspath('.') + '/OutputForClearingSectionFolders.csv'
MAINPATH = os.path.abspath('.')#Always specify absolute path for all path specification and file specifications
#Main Function
if __name__=='__main__':
    file = open(LOGFILE, 'wb')
    writer = csv.writer(file)
    writer.writerow([' The log file for the program to remove all section folders in the ClippedData folder.'])
    file.close()
    try:
        print " Clearing the section folders in the Clipped Data folder."
        listoffolders = os.listdir(MAINPATH+'/Data/')
        for folder in listoffolders:
            #Get list of subfolders in each participants ClippedData folder
            temp = os.listdir(MAINPATH+'/Data/'+folder+'/ClippedData/')
            listofsubfolders =[]
            for item in temp:
                if 'SECTION' in item:
                    listofsubfolders.append(item)
            print "\n\n\nList of all the subfolders for: ", folder, " are: \n" , listofsubfolders
            for subfolder in listofsubfolders:
                shutil.rmtree(MAINPATH+'/Data/'+folder+'/ClippedData/'+subfolder)
    except Exception as e:
        print " Main Function Exception Catcher : " , e
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        file = open(LOGFILE, 'a')
        writer = csv.writer(file)
        writer.writerow(['Exception at loading the Main Functio Level' , 'Exception:' , e , 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)])
        file.close()
