from __future__ import division # so that 1/3 = 0.33 instead of 1/3 = 0
# GaborMotion Exp 1
 
#1)Generates the list containing randomized trial order with stimulus values
#2)Creates Moving Gabors
#3)Presents a random auditory amplitude modulation
#4)Allows participant to adjust the auditory amplitude modulation rate then move to next trial when satisfied

import numpy as np
import random
import scipy.signal
from threading import Thread
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import sound
from psychopy import *

# play a tone to initialize

# Sound Values
duration = 0.5 # 500ms
frequencySampleRate = 10000 # Sample rate in Hz
fadeTime = 50 # Sets duration of fade function (ms)
soundTime = np.arange(0, duration+.0001, (1/frequencySampleRate)) # Creates a list of consisting of
#all time between 0 and 0.5 by 0.0001 steps
nrchannels = 1 # this may just be for MatLab but it is used to designate mono as opposed to stereo
repitions = 0 # number of repitions of the sound
toneFrequencyValue = 500 # equivalent to tone in Matlab
time = 3
phase = 0
sampleRate = 10000 # in HZ

#Or by giving an Nx2 numpy array of floats (-1:1) you can specify the sound yourself as a waveform
# sampleRate (= 44100): if the psychopy.sound.init() function has been
#called or if another sound has already been created then this argument will be ignored and the previous setting will be used
#bits: has no effect for the pyo backend hamming: whether to apply a Hamming window (5ms) for generated tones.
#Not applied to sounds from files. 
# Once you know how to modulate the pitch and Amplitude Modulation Rate figure out how to link its duration to key press

# Set Gabor Values
gratingSize = 15 # scalar in cm, can chage to x,y pair
gratingOpacity = 1.0 # The value should be a single float ranging 1.0 (opaque) to 0.0 (transparent).
gratingPos = [0,0] # [0,0] is the center of the screen
gratingOri = 0 # degrees
# Fixation Stim Vaues
fixationPos = [0,0]

#Window 
size = (800, 800)

# Keys
allowedKeys = ['a', 's', 'd','esc', 'space']

# Spatial Frequencies
#1 is equivalent to one cycle per 'cm','deg', or 'pixel' depending on units value 
lowSpatialFreq = .09 # .009
medSpatialFreq = .4 # .04
highSpatialFreq = .9 # .09
#Temporal Frequencies # Figure out the cycles/cm and cycles/period
lowTempFreq = .1 # 1 cycle per second
medTempFreq = .4
highTempFreq = .8
# Direction
left = '-'
right = '+'

# testSound
#snd = sound.Sound(toneFrequencyValue)
#snd.play()

# Instructions
instructions = """You will be presented with contrasting lines and asked to adjust the auditory freqquency to correspond with the moving contrasting lines
The Right Key or D Key will make the auditory frequency faster.
The Left Key or A Key will make the auditory frequency slower.
Press the S Key when you have finished adjusting. 

Please Press Any Key to Begin
"""

#Create a window and stimuli
mywin = visual.Window(monitor='testMonitor', size = (800, 800), units='cm', allowGUI=False)# makes a window based on testMonitor Calibration

# Add participant GUI Here

def createGratingStim(spatialFreq):
#    global mywin
    grating = visual.GratingStim(win=mywin, size=gratingSize, mask='gauss', pos=gratingPos, ori=gratingOri, sf=float(spatialFreq))
#    print grating
    return grating

def showGrating(grating):
#    global mywin
    grating.draw()
    mywin.flip()   
    if len(event.getKeys())>0:
        event.clearEvents()
        mywin.close()
        core.quit() 

def showMovingGrating(grating,TempFreq,direction):
#    global mywin 
    toneOn = 0
    while True:
        if toneOn == 0:
            playSound(500)
            toneOn = 1
        grating.setPhase(float(TempFreq), direction) 
        grating.draw()
        mywin.flip()   
        keys = event.getKeys(allowedKeys)
        if 's' in keys:
            break
    event.clearEvents
#    mywin.close()
#    core.quit() 
#def adjustSound(freq, snd): # only play sound as long as needed
#    while True:
#        keys = event.getKeys(allowedKeys)
#        if 'a' in keys:
#            snd.stop()
#            snd = sound.Sound(value=freq + 100, loops=-1)
#            return snd
#            
def playSound(freq):
    snd = sound.Sound(value=freq, loops=-1)
    snd.play()
#    adjustSound(freq, snd)
#    while True:
#        keys = event.getKeys(allowedKeys)
#        if 'a' in keys:
#            snd.stop()
#            snd = sound.Sound(value=freq + 100, loops=-1)
#            break 
    snd.play()

def showStim(trialStim):
#    mywin = visual.Window(monitor='testMonitor', size = (800, 800), units='cm', allowGUI=False)# makes a window based on testMonitor Calibration
    grating =createGratingStim(trialStim[0])
#    playSound(500)
    showMovingGrating(grating, trialStim[1], trialStim[2])


def showInstructions(text):
    win = visual.Window(size)
    instruction = visual.TextStim(win, text, pos=(0,0), color='white') # height=0.038
    instruction.draw()
    win.flip
    if len(event.getKeys())>0:
        event.clearEvents()
        win.close()
        core.quit() 
        
#Test Grating Presentation
#x = [lowSpatialFreq, lowTempFreq, left]
#showStim(x)

# Test Sound Presentation
#playSound(500)

trialfile = open('gaborMotionTrials.txt', 'r')
trialList = []
print trialfile
for line in trialfile:
    trials = line.split()
    print trials
    trialList.append(trials)
print len(trialList)
random.shuffle(trialList) # replace with predetermined trial order list

#showInstructions(instructions)


#Experiment Engine
for trial in trialList:
    print trial
    showStim(trial)

##Graveyard

# Moving Gratings!
#def showBistableGratingMotion(gratingLeft, gratingRight, grating1, grating2): # 
#    while True:
#        gratingLeft.setPhase(phaser, '-')
#        gratingRight.setPhase(phaser, '+')
#        grating1.setPhase(phaser, '-') 
#        grating2.setPhase(phaser, '+')
#        gratingLeft.draw()
#        gratingRight.draw()
#        grating1.draw()
#        grating2.draw()
#        mywin.flip()   
#        if len(event.getKeys())>0: break
#    event.clearEvents()
#    mywin.close()
#    core.quit() 
#    
#def showBistableGratings(gratingLeft, gratingRight, grating1, grating2): # 
#    while True:
#        gratingLeft.draw()
#        gratingRight.draw()
#        grating1.draw()
#        grating2.draw()
#        mywin.flip()   
#        if len(event.getKeys())>0: break
#    event.clearEvents()
#    mywin.close()

#showBistableGratingMotion(gratingLeft, gratingRight, grating1, grating2)  
#showBistableGratings(gratingLeft, gratingRight, grating1, grating2) #  
