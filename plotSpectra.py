#script to check run1 4353 of the LANL test beam
###############################################
# scripting for quick analysis of the LANL test beam from April 15-22
# Patrick Freeman
# UCSB
# pmfreeman@ucsb.edu
###############################################
import ROOT as r
import argparse
import array
from datetime import datetime
import LANLTB as LANL
#################################################################################################
start =  datetime.now()
cal = "./data/Run4307.root"
for ch in LANL.chs:
    j=0
    print(j)
    for run in LANL.runs:
        testRun = "./data_wfm/"+run#LANL.runDir+run
        defaultRun= LANL.runDir+cal
        print("Plotting spectra for file "+testRun+" with comparison run "+str(defaultRun))
        LANL.plotWfms(testRun, ch)
        #LANL.plotRun(cal, testRun, ch, 1.0, False)
        j=j+1

stop =  datetime.now()

print ("start time: "+str(start))
print("end time: "+str(stop))
