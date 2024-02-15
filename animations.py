import time
import board
import digitalio
from protoStates import *
from adafruit_max7219 import matrices
from sprites import *
import globalVars

def blink():
    originalMat = [x[:] for x in globalVars.currentMatrixState]
    left  = globalVars.matInfo["leftEye"]
    right = globalVars.matInfo["rightEye"]
    depth = 6
    leftRange = list(range(depth)) if (globalVars.vFlipLEye == False) else list(range(15, 15-depth, -1))
    rightRange = list(range(depth)) if (globalVars.vFlipREye == False) else list(range(15, 15-depth, -1))
    for i in range(depth):
        nextMat = [x[:] for x in globalVars.currentMatrixState]
        for j in range(left[globalVars.sizeIndex]*8):
            nextMat[leftRange[i]][(left[globalVars.offsetIndex]+j)] = 0
        for j in range(right[globalVars.sizeIndex]*8):
            nextMat[rightRange[i]][(right[globalVars.offsetIndex]+j)] = 0
        smartUpdate(nextMat)
    smartUpdate(originalMat)