#backup 2/10/2024

import time
import board
import digitalio
from adafruit_max7219 import matrices
from sprites import *
from protoStates import *
from collections import OrderedDict
import globalVars

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D4)
globalVars.init(spi, cs)
# You may need to change the chip select pin depending on your wiring

happyState = protoState("happy", happyMouth, happyEye, regularNose)
spookedState = protoState("spooked", spookedMouth, spookedEye, regularNose)
angryState = protoState("angry", angryMouth1, angryEye, regularNose)
errorState = protoState("error", errorMouth, errorEye, errorNose, flipSymetry=False)
testPat    = protoState("test", TestPatMouth, TestPatEyes, regularNose, flipSymetry=False)

states = OrderedDict()
states.update({happyState.name: happyState})
states.update({spookedState.name: spookedState})
states.update({angryState.name: angryState})
states.update({errorState.name: errorState})
states.update({testPat.name: testPat})

while True:
    print("Cycle Start")
    # all lit up
    smartFill(True)
    time.sleep(0.5)
    smartFill(False)
    for state in states:
        print(str(state))
        states[state].enterState()
        time.sleep(5)
