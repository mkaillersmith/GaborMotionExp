from __future__ import division # so that 1/3 = 0.33 instead of 1/3 = 0

from psychopy import visual
from psychopy import prefs
prefs.general['audioLib'] = ['pygame'] # Windows = pygame mac = pyo
from psychopy import sound
from psychopy import core
import numpy as np
import math


freq = 500

mywin = visual.Window(size=(400,400))

print 'playing sound'
snd = sound.Sound(value=freq, loops=-1)
snd.play()
print 'sound played'

core.wait(3)

win.close()