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
import wave

print 'importing wav'
snd = sound.Sound('whiteNoiseBurst10ms.wav')
print 'playing sound'
snd.play()
core.wait(4)