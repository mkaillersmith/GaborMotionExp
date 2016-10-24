from __future__ import division # so that 1/3 = 0.33 instead of 1/3 = 0
# GaborMotion Exp 1
 
#1)Generates the list containing randomized trial order with stimulus values
#2)Creates Moving Gabors
#3)Presents a random auditory amplitude modulation
#4)Allows participant to adjust the auditory amplitude modulation rate then move to next trial when satisfied

import matplotlib.pyplot as plt
from psychopy import visual
from psychopy import prefs
prefs.general['audioLib'] = ['pygame'] # Windows = pygame mac = pyo
from psychopy import sound
from psychopy import core
import numpy as np
import math
import wave


# play a tone to initialize
#freq = 500

#toneFrequency = np.array([440, 459.48, 479.82, 501.07, 523.25, 546.41, 570.61, 595.87, 622.25, 649.80, 678.57, 708.61, 739.99, 772.75, 806.96, 842.69, 880]

#intitalLevel = 0.45
allFrequencyModulations = np.arange(1.5, 19.5,.5)
possibleFrequencyModulations = np.arange(3, 9.5, .5)
print 'possible FMs: ', possibleFrequencyModulations

clock = core.Clock()

for freqModulation in allFrequencyModulations:
    print freqModulation
    duration = 0.5 # 500ms
    fs = 10000 # frequency sample rate 
    f = 110 # the frequency of the signal
    ft = 1 # this is the varuable that needs to be adjusted
    A = .45 # amplitude
    modulationRate = freqModulation # modulation frequency
    modulationIndex = 1 # 100% modulation

    waveLength = np.arange(fs) # the points on the x axis for plotting

    # Computes the value (amplitude) of the sin wave at the for each sample
    carrierWave = np.array([A*math.sin(2*np.pi*f * (i/fs)) for i in np.arange(fs)]) # i/fs = time
    modulationWave = np.array([modulationIndex*math.sin(2*np.pi*modulationRate*(i/fs)) for i in np.arange(fs)])
    
#    carrierWave = np.array([A*math.sin(2*np.pi*440 * (i/fs)) for i in np.arange(fs)]) # i/fs = time
#    modulationWave = np.array([math.sin(2*np.pi*3*(i/fs)) for i in np.arange(fs)])

    print waveLength.shape
    print modulationWave.shape
    print carrierWave.shape

    #Calculates Amplitude Modulated Sound
    AmSound = carrierWave*modulationWave



    print type(carrierWave)

    #Plot AMSound
    plt.plot(waveLength,AmSound)
    plt.show()

    mywin = visual.Window(size=(400,400))
    
    print 'playing sound'
    snd = sound.Sound(value=AmSound, loops=-1)
    startSound = clock.getTime()
    soundDuration = snd.getDuration()
    snd.play()
    print 'SoundDuration = ', soundDuration
    endSound= clock.getTime()
    print endSound-startSound
    print 'sound played'
    core.wait(3)
    snd.stop()
    mywin.close()

# Sound Values
#duration = 0.5 # 500ms
#frequencySampleRate = 10000 # Sample rate in Hz
#fadeTime = 50 # Sets duration of fade function (ms)
#soundTime = np.arange(0, duration+.0001, (1/frequencySampleRate)) # Creates a list of consisting of
#all time between 0 and 0.5 by 0.0001 steps
#print soundTime
#nrchannels = 1 # this may just be for MatLab but it is used to designate mono as opposed to stereo
#repitions = 0 # number of repitions of the sound
#toneFrequencyValue = 500 # equivalent to tone in Matlab
#sampleRate = 10000 # in HZ

#intitalLevel = 0.45
#possibleFrequencyModulations = np.arange(3, 9.5, .5)
#print 'possible FMs: ', possibleFrequencyModulations


# Keys
#allowedKeys = ['a', 's', 'd','esc', 'space']

#toneFrequency = np.array([440, 459.48, 479.82, 501.07, 523.25, 546.41, 570.61, 595.87, 622.25, 649.80, 678.57, 708.61, 739.99, 772.75, 806.96, 842.69, 880], [0.4, 0.391, 0.383, 0.375, 0.367, 0.359, 0.351, 0.344, 0.336, 0.329, 0.322, 0.315, 0.309, 0.302, 0.295, 0.289, 0.283])
# testSound
#print 'playing sound'
#snd = sound.Sound(toneFrequencyValue, loops=-1)
#snd.play()
#print 'played sound'


##############################################################################################
#########################Graveyard############################################################

#
#sampleFrequency = 22050 #sample frequency (Hz)
#duration = 1.0 #durati0n (s)
#numSamples = sampleFrequency * duration #number of samples
#
# set carrier
#carrierfrequency = 1000 #carrier frequency (Hz)
#carrierData = np.arange(1, numSamples+1) / sampleFrequency #carrier data preparation
#print 'carrierData: ', len(carrierData)
#c = 2 * math.pi * carrierfrequency * carrierData #sinusoidal modulation
#carrierList = []
#for i in range(len(carrierData)):
#    c = math.sin(2*math.pi*carrierfrequency*i)
#    print c
#    carrierList.append(c)
#print 'carrier frequency: ', carrierList
#
#set modulator
#modulatorFrequency = 5 #modulator frequency (Hz)
#modulatorIndex = 0.5 #modulator index
#modulatorData = np.arange(1, numSamples+1) / sampleFrequency #modulator data preparation
#print 'length modulatorData: ', len(modulatorData)
#modulatorList = []
#for i in range(len(modulatorData)):
#    x = 2*math.pi*modulatorFrequency*i
#    sinMod = 1+modulatorIndex*math.sin(x)
#    modulatorList.append(sinMod)
#print 'modulator list: ', modulatorList
#sinosoidalModulaiton = 1 + modulatorIndex * math.sin(2 * math.pi * modulatorFrequency * modulatorData) #sinusoidal modulation
#
#amplitude modulation
#AmSnd = np.dot(modulatorList, carrierList) #amplitude modulation
#print AmSnd

# modulation wave calculation
#t = [ math.sin(2*np.pi*ft * (i/fs)) for i in np.arange(fs)] 

# Element by Element multiplication??
#z = []
#for i in range(len(carrierWave)):
#    z.append(x[i]*carrierWave[i])
#zArray = np.array(z)





