import time
import board
import digitalio
from protogenMood import *
from protogen import *
from adafruit_max7219 import matrices
from sprites import *
import config
import neopixel

def blink(mood, delay=None, animData=None, animIndex=None):
    originalMat = [x[:] for x in mood.protogen.currentDisplayed]
    left  = mood.protogen.matInfo["leftEye"]
    right = mood.protogen.matInfo["rightEye"]
    depth = 6 
    leftRange = list(range(depth)) if (config.vFlipLEye == False) else list(range(7, 7-depth, -1))
    rightRange = list(range(depth)) if (config.vFlipREye == False) else list(range(7, 7-depth, -1))
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

def flashEyes(mood, delay=None, animData=None, animIndex=None):
    if (animData == None):
        mood.animData = 0
    if (animData == 1):
        mood.animData = 0
    else:
        mood.animData = 1
    left  = mood.protogen.matInfo["leftEye"]
    right = mood.protogen.matInfo["rightEye"]
    nextMat = [x[:] for x in mood.fullDefaultMat]
    for i in range(8):
        for j in range(left["numPanels"]*8): #columns
            nextMat[i][(left["offset"]+j)] = (0 if (mood.animData == 0) else mood.fullDefaultMat[i][(left["offset"]+j)])
            nextMat[i][(right["offset"]+j)] = (0 if (mood.animData == 0) else mood.fullDefaultMat[i][(right["offset"]+j)])
    smartUpdate(mood.protogen, nextMat)

def rgbHelper(pos):
    # Input a value 0 to 255 to get a color value.
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rgbRainbowCycle(pixels):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j)
            pixels[i] = rgbHelper(idx & 255)
        pixels.show()