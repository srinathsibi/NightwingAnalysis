#Author : Srinath Sibi ssibi@stanford.edu
#Purpose :
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
#Function to filter GSR
def FilterGSR():
    print "Filtering GSR"
#Function to filter PPG
def FilterHR():
    print "Filtering HR"
#Function to filter PupDia
def FilterPupilDiameter():
    print "Filtering Pupil Diameter"
#Function to filter Catbin
def FilterCategoryBinocular():
    print "Filtering Category Binocular"
#Function to skip lines in the csv files
def skiplines(fr, lines):
    #fp is file reader and lines is the number of lines to skip
    i = 1
    while i<=lines:
        i = i+1
        row = next(fr)
