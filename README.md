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

