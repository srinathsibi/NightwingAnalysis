#!/bin/bash
# This is just a test script, I will be adding a different script to run all the scripts on one .sh file
echo We will be running all the scripts one by one.
echo First the script to clip.
python ClippingData.py
wait
echo We are running the script to clean and strip the data in to relevant parts
python StripData.py
wait
echo Now extracting the End section Data for daves analysis
python ScriptforDavesNightwingAnalysis.py
wait
echo All processes done!!!!!
