#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose : This script is meant to copy files to the external hard drive or any other drive that the user choses.
import csv, os, shutil
PATH = '/media/srinathsibi/Seagate Backup Plus Drive/ProcessedData/'
#Function to check if the folder already exists in the External Drive ProcessedData Folder
def checkandcopy(folder):
    print "Checking for folder : ", folder
    if not os.path.exists(PATH+folder):
        #os.makedirs(PATH+folder)#Create the folder for the first time
        shutil.copytree(folder+'/ClippedData',PATH+folder)#Copying the Data from the processing folder
    else:
        shutil.rmtree(PATH+folder)
        shutil.copytree(folder+'/ClippedData',PATH+folder)#Copying the Data from the processing folder
#Main Function
if __name__=='__main__':
    print " Copying ClippedData Folders to the external Drive"
    #NOTE: The ClippedData Folder in each participant will be copied to the External Drive under the ProcessedData folder.
    #Shifting to the Data Folder
    os.chdir('Data/')
    listoffolders = os.listdir('.')
    for folder in listoffolders:
        if int(folder[1:4]) <= 100 and int(folder[1:4])>=0:#Way to curtail the folders that are copied
            checkandcopy(folder)
