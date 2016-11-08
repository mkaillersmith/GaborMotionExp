#!/usr/bin/env python2

from __future__ import division # so that division produces float 

__author__ = "Max Smith - mkaillersmith@gmail.com"


import os, sys, random, datetime, time, psychopy
from psychopy import core, data, event, logging, gui
import numpy as np
import math
from psychopy import visual
from psychopy import prefs
prefs.general['audioLib'] = ['pygame'] # Windows = pygame mac = pyo
from psychopy import sound
import matplotlib.pyplot as plt

#Test screenSize
screenSize = (800, 600)

#Actual screenSize 
#screenSize = (1920, 1080)
win = visual.Window([1024,768], monitor='LenovoT460s')

# SoundStimulus
snd = sound.Sound('whiteNoiseBurst10ms.wav')
snd.setVolume(.01)
snd.play()
snd.setVolume(1.0)
# Magic Numbers 

framesPerStim = 10

radius = 15
circleRadius = 2
circleColor = 'black'
fixationRadius = 6
fixationColor = 'red'
degreesIncrement = 22.5
radians = math.radians(0)
radianIncrement = math.radians(degreesIncrement)

rotateSpeed = .25
rotateStimLength = 40
ambiguousStimLength = 20
ITI = .5

fixPos = (0,0)
fixation = visual.TextStim(win=win, text='+', color=fixationColor, pos=fixPos)
centerCirclePos = (0,0)
centerCircle = visual.Circle(win=win, radius=radius, edges=1200, lineColor=circleColor, pos=centerCirclePos)

xList = []
yList = []
for i in range(16):
    radians += radianIncrement
    x = radius*(math.sin(radians))
    y = radius*(math.cos(radians))
#    print x * 10
    xList.append(x)
    yList.append(y)
#    print 'x', x
#    print 'y', y
xPosList = xList*100
yPosList = yList*100
#print len(xPosList)
#print len(yPosList)

def showRotateCircle(direction):
    soundPlay = 0
    rotateDirection = direction
    i = -1
    clock = core.Clock()
    startTime = clock.getTime()
    while True:
        if clock.getTime() - startTime >= 5:
            break
        for frame in range(60):
            print 'frame / framesPerStim = ', frame%framesPerStim
            print 'frame Num: ', frame
            print 'i: ', i
            pos1 = (xPosList[i], yPosList[i])
            pos2 = (xPosList[i+4], yPosList[i+4])
            pos3 = (xPosList[i+8], yPosList[i+8])
            pos4 = (xPosList[i+12], yPosList[i+12])
            circle1 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos1) # circleColor
            circle2 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos2)
            circle3 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos3)
            circle4 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos4)
                    
            if frame%framesPerStim == framesPerStim-1:
                soundPlay = 1
                if rotateDirection == 'clockwise':
                    i += 1
                elif rotateDirection == 'counterClockwise':
                    i -= 1
                pos1 = (xPosList[i], yPosList[i])
                pos2 = (xPosList[i+4], yPosList[i+4])
                pos3 = (xPosList[i+8], yPosList[i+8])
                pos4 = (xPosList[i+12], yPosList[i+12])
                circle1 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos1) # circleColor
                circle2 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos2)
                circle3 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos3)
                circle4 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos4)
                
            centerCircle.draw()
            fixation.draw()
            circle1.draw()
            circle2.draw()
            circle3.draw()
            circle4.draw()

            win.flip()
            if frame%framesPerStim == framesPerStim-(framesPerStim/2):
                soundDuation = snd.getDuration()
#                print soundDuration
                print 'play Sound'
                snd.play()
            soundPlay = 0




def showAmbiguousCircle():
    z = 0
    counter2 = 0
    switcher = 0
    while True:

        counter2+= 1
        if counter2 >= ambiguousStimLength:
            break
        if switcher == 0:
            pos1 = (xPosList[-1], yPosList[-1])
            pos2 = (xPosList[3], yPosList[3])
            pos3 = (xPosList[7], yPosList[7])
            pos4 = (xPosList[11], yPosList[11])
            switcher = 1
            
        elif switcher == 1:
            pos1 = (xPosList[1], yPosList[1])
            pos2 = (xPosList[5], yPosList[5])
            pos3 = (xPosList[9], yPosList[9])
            pos4 = (xPosList[13], yPosList[13])
            switcher = 0
            
        circle1 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos1)
        circle2 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos2)
        circle3 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos3)
        circle4 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos4)
        
        centerCircle.draw()
        fixation.draw()
        circle1.draw()
        circle2.draw()
        circle3.draw()
        circle4.draw()
        
        win.flip()
        core.wait(rotateSpeed)
def showBlank():
    centerCircle.draw()
    fixation.draw()
    win.flip()
    core.wait(ITI)
    
def showITI():
    centerCircle.draw()
    fixation.draw()
    win.flip()
    core.wait(1)
    
    

#fakeTrialList = ['clockwise', 'counterClockwise', 'clockwise', 'counterClockwise']

#for trial in fakeTrialList:
#    print trial
trialClock = core.Clock()
startTime = trialClock.getTime()
showRotateCircle('clockwise')
endTime = trialClock.getTime()
print 'End time:', endTime-startTime
#showBlank()
#showAmbiguousCircle()
#showITI()

#
#clock = core.Clock()
#let's draw a stimulus for 200 frames, drifting for frames 50:100
#for frameN in range(200):#for exactly 200 frames
#    if 10 <= frameN < 150:  # present fixation for a subset of frames
#        fixation.draw()
#    if 50 <= frameN < 100:  # present stim for a different subset
#        gabor.setPhase(0.1, '+')  # increment by 10th of cycle
#        gabor.draw()
#    win.flip()



#Plot AMSound
#plt.plot(waveLength, samples)
#plt.show()

