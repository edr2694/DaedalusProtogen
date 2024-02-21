#backup 2/10/2024

import time
import board
import digitalio
from adafruit_max7219 import matrices
from sprites import *
from protoStates import *
from collections import OrderedDict
import globalVars
import animations

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D4)
globalVars.init(spi, cs)
# You may need to change the chip select pin depending on your wiring

# set up frame array for angry

angryFrameList = [createFullMat(angryMouth1, angryEye, regularNose),
                  createFullMat(angryMouth2, angryEye, regularNose),
                  createFullMat(angryMouth3, angryEye, regularNose)]

happyState = protoState("happy", happyMouth, happyEye, regularNose, period=5, animFunc=animations.blink)
spookedState = protoState("spooked", spookedMouth, spookedEye, regularNose)
angryState = protoState("angry", angryMouth1, angryEye, regularNose, period=.05, animFunc=animations.cycleFrames, animData=angryFrameList)
errorState = protoState("error", errorMouth, errorEye, errorNose, flipSymetry=False)
testPat    = protoState("test", TestPatMouth, TestPatEyes, regularNose, flipSymetry=False)



states = OrderedDict()
states.update({happyState.name: happyState})
states.update({spookedState.name: spookedState})
states.update({angryState.name: angryState})
states.update({errorState.name: errorState})
states.update({testPat.name: testPat})

smartFill(True)
time.sleep(0.5)
smartFill(False)
angryState.enterState()

while True:
    if (time.monotonic() > globalVars.currentProtoState.nextRun):
        globalVars.currentProtoState.doAnimation()
    time.sleep(.05)
    #for state in states:
    #    print(str(state))
    #    states[state].enterState()
    #    time.sleep(5)
