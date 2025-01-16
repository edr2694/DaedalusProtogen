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
import asyncio
import keypad


config.init()

# You may need to change the chip select pin depending on your wiring

# set up frame array for angry


angryFrameList = [createFullMat(angryMouth1, angryEye, regularNose),
                  createFullMat(angryMouth2, angryEye, regularNose),
                  createFullMat(angryMouth3, angryEye, regularNose)]

happyState = protogenMood("happy", happyMouth, happyEye, regularNose, period=5, animFunc=animations.blink)
spookedState = protogenMood("spooked", spookedMouth, spookedEye, regularNose, period=3, animFunc=animations.blink)
angryState = protogenMood("angry", angryMouth1, angryEye, regularNose, period=.1, animFunc=animations.cycleFrames, animData=angryFrameList)
errorState = protogenMood("error", errorMouth, errorEye, errorNose, flipSymetry=False, period=.25, animFunc=animations.flashEyes)
#testPat    = protogenMood("test", rightMouth=TestPatMouthR, leftMouth=TestPatMouthL, rightEye=TestPatEyesR, leftEye=TestPatEyesL, leftNose=TestPatNoseL, rightNose=TestPatNoseR, flipSymetry=False)



states = OrderedDict()
#states.update({testPat.name: testPat})
states.update({happyState.name: happyState})
states.update({spookedState.name: spookedState})
states.update({angryState.name: angryState})
states.update({errorState.name: errorState})




proto = protogen(states)
asyncio.run(proto.beginLoop())