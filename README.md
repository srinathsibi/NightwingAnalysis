Nightwing Data Analysis

Author: Srinath Sibi (ssibi@stanford.edu)

User: Srinath Sibi (ssibi@stanford.edu)

Purpose: Personal Python Repo for Analysis of Data.

Description and Notes:
This section contains individual notes made by Srinath Sibi during the data cleanup process.

1. Eye tracker files are named reliably. But they have subject information in the first few lines of each file.

2. In order to make the files more readable for the creation of a data set, we have to clear up the header information in each file.

3. We might create a separate subfolder for each participant, clip the relevant time stamp information and save as the eye tracker 
data for analysis.

4. Each row of information in the file is structured in the following order left to right (coder left to right):
Time	Type	Trial	L Dia X [px]	L Dia Y [px]	L Pupil Diameter [mm]	R Dia X [px]	R Dia Y [px]	R Pupil Diameter [mm]	B POR X [px]	B POR Y [px]	L POR X [px]	L POR Y [px]	R POR X [px]	R POR Y [px]	B Event Info	Stimulus

5. There are empty lines in each eye tracker file export around points which look like this (excerpt below) :
11824399892	SMP	1	125.00	99.00	5.28	124.00	100.00	5.32	655.20	280.30	597.04	307.77	699.00	322.05	Saccade	11-2-recording.avi

11824403000	MSG	1	Marker:1.00



11824419000	MSG	1	Marker:1.00



11824433215	SMP	1	118.00	95.00	5.16	116.00	100.00	5.18	796.33	259.47	736.62	281.97	841.02	307.71	Saccade	11-2-recording.avi

11824436000	MSG	1	Marker:1.00

<end of excerpt>

	For now, I have ignored empty lines in processing the files. But I need to find out what these are from Dave Miller.

6. In order to make sure that all participant numbers are in fact the actual participant numbers, I had to manually edit a few files so that Subject value at the top of the file was a integer and not anything else. Short recordings with less than a MB of data were deleted.

7. The time codes on the eye tracker files seem confusing. For example, consider participant 50, the duration of the recording is 26min 30 secs. However, the time stamp corresponding to the start and end seem off.

Time start :
      Timestamp: 549333000, Time in recording: ~ 06:26.016
Time end:
      Timestamp: 2141049000, Time in recording: ~33:00.576

I can't seem to reconcile the time stamps and the clock times. 

8. Eye Tracker Data Marker Information:
	Marker 1 : When the participant enters the highway.
	Marker 2 : When the automation is engaged in the car.
	Marker 3 : 5 seconds at current speed before the car runs into the fallen truck.

9. iMotions files were not organized correctly in the NAS, I had to reorg them while analyzing them. Please ensure that the column called Name has the right participant number before placing them in individual participant folders.

10. Each participant folder should contain an iMotionsClipped.csv and iMotionsInfo.csv file which contain the clipped iMotions and the top sheet information from the iMotions file. They have separated before clipping to make the csv files easier to process.

11. Each iMotionsClipped.csv file has a "Time (in seconds)" column as its first column. This column starts at -180 seconds. Marker 1 placement time is considered 0 time. I clipped the file 3 minutes before that to make sure that there is sufficient time before the start for a baseline.

12. stripData.py file is made to ensure that the relevant data from the three major files (eye tracking, sim, iMotions) are stripped to the bare essentials. This means that only the relevant columns are gathered. The stripped files should be considerably smaller than the source cliiped file.

13. StripData.py has a function to extract, move and plot the relevant data.

14. The relevant columns in the the sim file are : { 'RelativeTime': 0, 'SimTime': 1, 'EndAutonomousMode':2 , 'SitAwOnTab':3 , 'TakeOverOnTab':4, 'LonAccel':5 , 'LatAccel':6 , 'ThrottlePedal':7 ,'BrakePedal':8\
'Gear':9 ,'heading':10 , 'headingerror':11, 'headwaydist':12, 'headwaytime':13 ,'lanenumber':14 ,'laneoffset':15,'roadoffset':16, 'steeringwheelpos':17 ,\
'tailwaydist':18 , 'tailwaytime':19 , 'velocity':20, 'lateralvel':21 , 'verticalvel':22 , 'xpos':23 , 'ypos':24 , 'zpos':25, 'roll':26 , 'pitch':27\
'yaw':28, 'enginerpm':29 , 'slip1':30 , 'slip2':31 , 'slip3':33, 'slip4':34,'SubId' :54, 'DriveID' : 53, 'AutomationType':52 , 'ModeSwitch': 51 , 'EventMarker': 50 \
, 'SteerTouch': 49 , 'UnixTime':48 }. Columns not mentioned here are empty. Please ignore them)

< For more on the relevant columns please go through the python script comments >

15. In order to run the StripData.py , just run the ./CleanAndMoveData.sh bash script.

16. I attempted to perform fourier transform to understand the frequency of signal changes to understand where the noise comes from and I discovered that the sampling rate and the frequency don't match. For a frequency of 1024 Hz, the number of samples don't match because of the way iMotions exports its files based on triggers, so we have to employ linear interpolation to resolve this issue.

17. For linear interpolation for time step use 0.001 (Resample to 1000 Hz for all signals). We cannot use cubic interpolation since the time steps are not always monotonically increasing (again because of the iMotions export method) . We will employ linear interpolation for all the signals. I have added an image in this repository to show that the resampling to a 1000 Hz doesn't alter the overall HR signal.

18. Participant 013 has some problems, there are 21 markers before 1 , these are shown in pictures in the Affiliated Images folder.
