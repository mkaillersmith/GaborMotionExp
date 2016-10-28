from __future__ import division # so that 1/3 = 0.33 instead of 1/3 = 0
# GaborMotion Exp 1
 
#1)Generates the list containing randomized trial order with stimulus values
#2)Creates Moving Gabors
#3)Presents a random auditory amplitude modulation
#4)Allows participant to adjust the auditory amplitude modulation rate then move to next trial when satisfied
from psychopy import visual
import math, datetime, numpy as np, random, os
import scipy.signal
from threading import Thread
from psychopy import prefs
prefs.general['audioLib'] = ['pygame'] # Windows = pygame mac = pyo
from psychopy import sound
from psychopy import *

randomizer = 1


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

# Gabor Values
gratingSize = (400, 400) # scalar in cm, can chage to x,y pair
gratingOpacity = 1.0 # The value should be a single float ranging 1.0 (opaque) to 0.0 (transparent).
gratingPos = [0,0] # [0,0] is the center of the screen
gratingOri = 0 # degrees
# Fixation Stim Vaues
fixationPos = [0,0]

# Window 
size = (1920, 1080)


#Create a window and stimuli
#mywin = visual.Window(size = size, units='pix')# monitor='testMonitor', size = (800, 800), units='cm', allowGUI=False)

# Keys
allowedKeys = ['a', 's', 'd','esc', 'space']

# Spatial Frequencies
#1 is equivalent to one cycle per 'cm','deg', or 'pixel' depending on units value 
lowSpatialFreq = .009
medSpatialFreq = .04
highSpatialFreq = .09
#Temporal Frequencies # Figure out the cycles/cm and cycles/period
lowTempFreq = .1 # 1 cycle per second
medTempFreq = .4
highTempFreq = .8
# Direction
left = '-'
right = '+'

# Adjust 
minStartFreqMod = .5
maxStartFreqMod = 4

adjustIncrement = .5

minFreqModRate = .5
maxFreqModRate = 10


# Instructions
instructions = """You will be presented with contrasting lines and asked to adjust the auditory frequency to correspond with the moving contrasting lines
The Right Key or D Key will make the auditory frequency faster.
The Left Key or A Key will make the auditory frequency slower.
Press the S Key when you have finished adjusting. 

Please Press Any Key to Begin
"""

# Add participant GUI Here

def showInstructions(text): # uses psychopy textStim to show the task instructions
    win= visual.Window(size)
    instructions = visual.TextStim(win, text, pos=(0,0), color='white', height=0.085)
    while True:
        instructions.draw()
        win.flip()
        keys = event.getKeys()
        if len(keys)> 0:
            break
        

def createGratingStim(spatialFreq):
#    global mywin
    grating = visual.GratingStim(win=mywin, size=gratingSize, mask='gauss', pos=gratingPos, ori=gratingOri, sf=float(spatialFreq))
#    print grating
    return grating

def makeSound(freq):
    clock = core.Clock()

    print 'initial frequency = ', freq
    duration = 0.5 # 500ms
    fs = 10000 # frequency sample rate 
    f = 110 # the frequency of the signal
    ft = 1 # this is the varuable that needs to be adjusted
    A = .45 # amplitude
    modulationRate = freq # modulation frequency
    modulationIndex = 1 # 100% modulation

    waveLength = np.arange(fs) # the points on the x axis for plotting

    # Computes the value (amplitude) of the sin wave at the for each sample
    carrierWave = np.array([A*math.sin(2*np.pi*f * (i/fs)) for i in np.arange(fs)]) # i/fs = time
    modulationWave = np.array([modulationIndex*math.sin(2*np.pi*modulationRate*(i/fs)) for i in np.arange(fs)])

#    print waveLength.shape
#    print modulationWave.shape
#    print carrierWave.shape

    #Calculates Amplitude Modulated Sound
    samples = carrierWave*modulationWave

    # White Noise
    return samples


def showMovingGrating(grating,TempFreq,direction, freq):
#    global mywin 
    toneOn = 0
    while True:
        keys = event.getKeys(allowedKeys)
        grating.setPhase(float(TempFreq), direction) 
        grating.draw()
        mywin.flip() 
        if toneOn == 0:
            snd = sound.Sound(freq, loops=-1)
            snd.play()
            core.wait(.1)
            toneOn = 1
        elif 'a' in keys:
            snd.stop()
            adjust = 'lower'
            return adjust
            break
        elif 'd' in keys:
            snd.stop()
            adjust = 'higher'
            return adjust
            break
        elif 's' in keys:
            snd.stop()
            adjust = 'done'
            return adjust
            break
    event.clearEvents

def showStim(trialStim, freq): # trialStim[0] = spatialFreq, trialStim[1] = TempFreq, trialStim[2] = Direction, trialStim[3] = intial
    grating =createGratingStim(trialStim[0])
    # play intitalsound and grating
    makeSample = 0
    while True:
        print 'frequency = ', freq
        if makeSample == 0:
            sample = makeSound(freq)
            makeSample = 1
        adjust = showMovingGrating(grating, trialStim[1], trialStim[2], sample)
        print 'adjust is:', adjust
        if adjust == 'higher':
            if freq >= maxFreqModRate: # 
                freq = freq
                makeSample = 0
            else:
                freq += adjustIncrement
                makeSample = 0
        elif adjust == 'lower':
            if freq <= minFreqModRate:
                freq = freq
                makeSample = 0
            else:
                freq -= adjustIncrement
                makeSample = 0
        elif adjust == 'done':
            responseFreq = freq
            print 'response freq = ', responseFreq
            return responseFreq

def convertTrialNum(trial):
    if trial < 10:
        trial_num = '00' +str(trial)
    elif trial >=10 and trial < 100:
        trial_num = '0'+ str(trial)
    elif trial >= 100:
        trial_num = trial
    return trial_num
    
def convertSpatialFreq(sf):
    spatialFreq = sf
    if spatialFreq == .04:
        spatialFreq = str(sf)+' '
    elif spatialFreq == .9:
        spatialFreq = str(sf)+'  '
    return spatialFreq

# Creates dialog box to enter subject number, condition, and block info
expName = 'None'  # from the Builder filename that created this script
expInfo = {'Participant': "000", 'Condition': '0', 'Block': '0'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = datetime.datetime.now().strftime("%d-%m-%y\nTime: %H:%M:%S")  # add a simple timestamp

if not os.path.isdir('data'):
    os.makedirs('data')

subj = str(expInfo['Participant'])
con = eval(expInfo['Condition'])
block = eval(expInfo['Block'])

file_log = "C:\\lab users\\GaborMotionExp-master\\logging.txt"


#Opens txt with all trial conditions
trialfile = open('gaborMotionTrials.txt', 'r')
trialList = []
print trialfile
for line in trialfile:
    trials = line.split()
    print trials
    trialList.append(trials)
print 'number of trials = ', len(trialList)
if randomizer == 1:
    random.shuffle(trialList) # replace with predetermined trial order list

#resume = expInfo['Resuming?']
resume = 0
# Writes experiment information subject log file
if resume == 0:
    print "not resuming"
    log_file = open("data\\AMSoundExp_sub%scon%1iblk%2i.txt" % (subj, con, block), 'w')
    log_file.write("Experiment Began: " + datetime.datetime.now().strftime("Experiment Ended: %H:%M:%S\n\n"))
    log_file.write('Total Trials = %i\n' % len(trialList)) # 150 trials
    log_file.write("trial_num SpatialFreq TemporalFreq Direction Response elapsed_time\n")
    log_file.close()
    trial_num = 0
elif resume == 1:
    t_log_file = open("data\\sub%scon%1i%blk%2i.txt" % (subj, con, block), 'r')
    t_log = t_log_file.readlines()
    t_log_file.close()
    t_log - t_log[-1].split(" ")
    trial_num = int(t_log[0])
    
mywin = visual.Window(size = size, units='pix')# monitor='testMonitor', size = (800, 800), units='cm', allowGUI=False)

showInstructions(instructions)


allFrequencyModulations = np.arange(1.5, 19.5,.5)
possibleFrequencyModulations = np.arange(minStartFreqMod, maxStartFreqMod, .5)
print 'possible FMs: ', possibleFrequencyModulations

#Experiment Engine
for trial in trialList:
    trial_num += 1
    trialConvert = convertTrialNum(trial_num)
#    spatialFreqConvert = convertSpatialFreq(trial[0])
    print 'Trial = ', trial
    intitialFrequency = random.choice(possibleFrequencyModulations)
    resp = showStim(trial, intitialFrequency)
    log_file = open("data\\AMSoundExp_sub%scon%1iblk%2i.txt" % (subj, con, block), 'a')
    log_file.write('%s %s %s %s %.1f\n' % (trialConvert, trial[0], trial[1], trial[2], resp))
    log_file.close()