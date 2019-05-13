#Author : Srinath Sibi
#Email : ssibi@stanford.edu
#Purpose :
#1. For each section folder, we need plots for PupilDiameter, PERCLOS, GSR, HR , catbin
#2. We need to save the plots in the SECTION FOLDER
import glob, os, sys, shutil
import matplotlib as plt
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
DEBUG = 1#Variable to identify what if anything is wrong with the PERCLOS calcuator
