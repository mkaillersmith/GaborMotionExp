
from psychopy import visual
import numpy as np
import random
import scipy.signal
from threading import Thread
from psychopy import prefs
# prefs.general['audioLib'] = ['pygame'] # Windows = pygame mac = pyo
# from psychopy import sound
from psychopy import *



# Set Gabor Values
gratingSize = (400, 400) # scalar in cm, can chage to x,y pair
gratingOpacity = 1.0 # The value should be a single float ranging 1.0 (opaque) to 0.0 (transparent).
gratingPos = [0,0] # [0,0] is the center of the screen
gratingOri = 0 # degrees
# Fixation Stim Vaues
fixationPos = [0,0]

size = (800, 800)

mywin = visual.Window(size = size, units='pix')

def createGratingStim(spatialFreq):
#    global mywin
    grating = visual.GratingStim(win=mywin, size=gratingSize, mask='gauss', pos=gratingPos, ori=gratingOri, sf=float(spatialFreq))
#    print grating
    return grating

def showGrating(grating):
#    global mywin
    grating.draw()
    mywin.flip()   
    core.wait(3)
    if len(event.getKeys())>0:
        event.clearEvents()
        mywin.close()
        core.quit() 
       
y = createGratingStim(.09) # maybe does it by pixel length change the values to compensate
showGrating(y)
