#backup 2/10/2024

import time
import board
import digitalio
from adafruit_max7219 import matrices
import asyncio
from sprites import *
from protogenMood import *
from collections import OrderedDict
from protogen import *
import config
import animations


config.init()

# You may need to change the chip select pin depending on your wiring

# set up frame array for angry

angryFrameList = [createFullMat(angryMouth1, angryEye, regularNose),
                  createFullMat(angryMouth2, angryEye, regularNose),
                  createFullMat(angryMouth3, angryEye, regularNose)]

happyState = protogenMood("happy", happyMouth, happyEye, regularNose, period=5, animFunc=animations.blink)
spookedState = protogenMood("spooked", spookedMouth, spookedEye, regularNose)
angryState = protogenMood("angry", angryMouth1, angryEye, regularNose, period=.05, animFunc=animations.cycleFrames, animData=angryFrameList)
errorState = protogenMood("error", errorMouth, errorEye, errorNose, flipSymetry=False)
testPat    = protogenMood("test", TestPatMouth, TestPatEyes, regularNose, flipSymetry=False)



states = OrderedDict()
states.update({happyState.name: happyState})
states.update({spookedState.name: spookedState})
states.update({angryState.name: angryState})
states.update({errorState.name: errorState})
states.update({testPat.name: testPat})

proto = protogen(states)

smartFill(proto, True)
time.sleep(0.5)
smartFill(proto, False)
happyState.enterMood()

while True:
    if (time.monotonic() > proto.currentMood.nextRun):
        proto.currentMood.doAnimation()
    time.sleep(.05)
    #for state in states:
    #    print(str(state))
    #    states[state].enterState()
    #    time.sleep(5)
