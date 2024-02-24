import time
import board
import digitalio
from protogenMood import *
from protogen import *
from adafruit_max7219 import matrices
from sprites import *
import config

def blink(mood, delay=None, animData=None, animIndex=None):
    originalMat = [x[:] for x in mood.protogen.currentDisplayed]
    left  = mood.protogen.matInfo["leftEye"]
    right = mood.protogen.matInfo["rightEye"]
    depth = 6 
    leftRange = list(range(depth)) if (config.vFlipLEye == False) else list(range(15, 15-depth, -1))
    rightRange = list(range(depth)) if (config.vFlipREye == False) else list(range(15, 15-depth, -1))
    for i in range(depth):
        nextMat = [x[:] for x in mood.protogen.currentDisplayed]
        for j in range(left["numPanels"]*8):
            nextMat[leftRange[i]][(left["offset"]+j)] = 0
        for j in range(right["numPanels"]*8):
            nextMat[rightRange[i]][(right["offset"]+j)] = 0
        smartUpdate(mood.protogen, nextMat)
        if (delay != None):
            time.sleep(delay)
    smartUpdate(mood.protogen, originalMat)

def cycleFrames(mood, delay=None, animData=None, animIndex=None):
    # NOTE: requires a animData to be a list of frames that have been 
    # initialized using createFullMat(). This is required so that we
    # don't need to recalculate the full matricies every single time
    # the animation function is called
    smartUpdate(mood.protogen, animData[mood.protogen.currentMood.animIndex])
    if (delay != None):
        time.sleep(delay)
    mood.animIndex += 1
    if (mood.animIndex >= len(animData)):
        mood.animIndex = 0