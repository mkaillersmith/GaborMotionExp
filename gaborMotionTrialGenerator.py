import numpy as np
import scipy
import os

dir = os.getcwd()
print dir
#curr = os.chdir('C:/Users/maxkails/Documents/GaborMotionEXP ')
#print curr

trialfile = open('gaborMotionTrials.txt', 'w')
trialfile.close

# Spatial Frequencies
#1 is equivalent to one cycle per 'cm','deg', or 'pixel' depending on units value 
lowSpatialFreq = .009
medSpatialFreq = .04
highSpatialFreq = .9 #.09
#Temporal Frequencies # Figure out the cycles/cm and cycles/period
lowTempFreq = .1 # 1 cycle per second
medTempFreq = .4
highTempFreq = .8
# Direction
left = '-'
right = '+'

# All Conditions
conLLL = [lowSpatialFreq, lowTempFreq, left] #1
conLLR = [lowSpatialFreq, lowTempFreq, right] #2
conLML = [lowSpatialFreq, medTempFreq, left] #3
conLMR = [lowSpatialFreq, medTempFreq, right] #4
conLHL = [lowSpatialFreq, highTempFreq, left] #5
conLHR = [lowSpatialFreq, highTempFreq, right] #6
conMLL = [medSpatialFreq, lowTempFreq, left] #7
conMLR = [medSpatialFreq, lowTempFreq, right] #8
conMML = [medSpatialFreq, medTempFreq, left] #9
conMMR = [medSpatialFreq, medTempFreq, right] #10
conMHL = [medSpatialFreq, highTempFreq, left] #11
conMHR = [medSpatialFreq, highTempFreq, right] #12
conHLL = [highSpatialFreq, lowTempFreq, left] #13
conHLR = [highSpatialFreq, lowTempFreq, right] #14
conHML = [highSpatialFreq, medTempFreq, left] #15
conHMR = [highSpatialFreq, medTempFreq, right] #16
conHHL = [highSpatialFreq, highTempFreq, left] #17
conHHR = [highSpatialFreq, highTempFreq, right] #18
masterList = [conLLL, conLLR, conLML, conLMR, conLHL, conLHR, conMLL, conMLR, conMML, conMMR, conMHL, conMHR,
conHLL, conHLR, conHML, conHMR, conHHL, conHHR]
# Spatial Frequency Conditions
lowSF = 'lowSpatialFreq'
medSF = 'medSpatialFreq'
highSF = 'highSpatialFreq'
# TemporalFrequency Conditions
lowTF = 'lowTempFreq'
medTF = 'medTempFreq'
highTF = 'highTempFreq'
# Direction Conditions
leftDir = 'left'
rightDir ='right'

trialfile = open('gaborMotionTrials.txt', 'a')
for trialCondition in masterList:
    for i in range(4):
        print trialCondition
        trialfile.write('%s %s %s\n' % (trialCondition[0], trialCondition[1], trialCondition[2]))

trialfile.close()
