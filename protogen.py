import config
from protogenMood import *
import time
import board
import digitalio
import analogio
from adafruit_max7219 import matrices
from collections import OrderedDict
import asyncio
import keypad
import neopixel

def getNumMats(mat):
    return  len(mat[0])

def flipSide(mat, actualyFlip):
    retmat = [None] * 8
    for i in range(8):
            retmat[i] = list(reversed(mat[i])) if actualyFlip else list(mat[i])
    return retmat

def matConv(inmat, vflip, hflip):
    numMats = getNumMats(inmat)
    retmat = [[0 for col in range(numMats*8)] for row in range(8)]
    for row in range(8):
        for mat in range(numMats):
            for bit in range(8):
                if (inmat[row][mat] & (1<<(7-bit))):
                    retmat[row][bit+(8*(mat))] = 1
                else:
                    retmat[row][bit+(8*(mat))] = 0
    if vflip == True:
        retmat.reverse()
    if hflip == True:
        for row in retmat:
            row.reverse()
    return retmat

def createFullMat(rightMouth, rightEye, rightNose, leftMouth=None, leftEye=None, leftNose=None, flipSymetry=True):

    outMat = []
    matricies = {
            "rightMouth": matConv(rightMouth, config.vFlipRMouth, config.hFlipRMouth),
            "rightEye": matConv(rightEye, config.vFlipREye, config.hFlipREye),
            "rightNose": matConv(rightNose, config.vFlipRNose, config.hFlipRNose)}

    if (leftMouth != None):
        matricies.update({"leftMouth": matConv(leftMouth, config.vFlipLMouth, config.hFlipLMouth)})
    else:
        matricies.update({"leftMouth": flipSide(matConv(rightMouth, config.vFlipLMouth, config.hFlipLMouth), flipSymetry)})
    if (leftEye != None):
        matricies.update({"leftEye" : matConv(leftEye, config.vFlipLEye, config.hFlipLEye)})
    else:
        matricies.update({"leftEye" : flipSide(matConv(rightEye, config.vFlipLEye, config.hFlipLEye), flipSymetry)})
    if (leftNose != None):
        matricies.update({"leftNose" : matConv(leftNose, config.vFlipLNose, config.hFlipLNose)})
    else:
        matricies.update({"leftNose" : flipSide(matConv(rightNose, config.vFlipLNose, config.hFlipLNose), flipSymetry)})

    sortedMats = []
    for i in config.matOrder:
        sortedMats.append(matricies[i])
    
    for row in range(8):
        outMat.append([])
    for i in sortedMats:
        for row in range(8):
            outMat[row]+=i[row]
    return outMat

def smartUpdate(protogen, newMat):
    startTime = time.monotonic()
    for row in range(8):
        for col in range(14*8):
            if protogen.currentDisplayed[row][col] != newMat[row][col]:
                protogen.display.pixel(col,row, newMat[row][col])
                protogen.currentDisplayed[row][col] = newMat[row][col]
    protogen.display.show()
    

def smartFill(protogen, onOff):
    for row in range(8):
        for col in range(14*8):
            checkval = 1 if onOff==True else 0
            if protogen.currentDisplayed[row][col] != checkval:
                protogen.display.pixel(col,row, checkval)
                protogen.currentDisplayed[row][col] = checkval
    protogen.display.show()

async def buttonCheck(protogen):
    with keypad.Keys(
        (config.moodButtonPin, board.D6), value_when_pressed=False, pull=True) as buttons:
        while True:
            buttonsEvent = buttons.events.get()
            if buttonsEvent and buttonsEvent.pressed:
                buttonNumber = buttonsEvent.key_number
                if buttonNumber == 0:
                    protogen.gotoNextMood()
            await asyncio.sleep(0)

async def hallCheck(protogen):
    protogen.magSense = analogio.AnalogIn(board.A1)
    while True:
        inval = protogen.magSense.value
        if (inval >= 35000 or inval <= 30000):
            protogen.gotoNextMood()
        await asyncio.sleep(.1)

async def animationCheck(protogen):
    while True:
        if ((time.monotonic() > protogen.currentMood.nextRun) and (protogen.currentMood.animFunc != None)):
            protogen.currentMood.doAnimation()
        await asyncio.sleep(0)

async def rgbCheck(protogen):
    while True:
        rgbRainbowCycle(protogen)
        await asyncio.sleep(0)

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

def rgbRainbowCycle(protogen):
    for i in range(len(protogen.rgbLights)):
        idx = int((i * 256 / len(protogen.rgbLights)) + protogen.rgbIndex)
        protogen.rgbLights[i] = rgbHelper(idx & 255)
    protogen.rgbLights.show()
    period = 2
    protogen.rgbIndex = (255 * (time.monotonic() % period) / period)


rgbVals = [255, 0, 0]
rgbDirs = [-1, 1, 1]

def rgbColorShift(pixels): #shift all pixels at once for hopefully better performance
    for i in range(0, 2, 1):
        nextVal = rgbVals[i] + rgbDirs[i]
        if ((nextVal == 0) or (nextVal == 255)):
            rgbDirs[i] = rgbDirs[i]*-1
        rgbVals[i] = nextVal
    pixels.fill((rgbVals[0], rgbVals[1], rgbVals[2]))
    pixels.show()

class protogen:
    def __init__(self, moods):
        self.moods = moods
        for mood in moods.values():
            mood.protogen = self
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D24)
        self.onesLed = digitalio.DigitalInOut(config.stateLedPins[0])
        self.onesLed.direction = digitalio.Direction.OUTPUT
        self.onesLed.value = True
        self.twosLed = digitalio.DigitalInOut(config.stateLedPins[1])
        self.twosLed.direction = digitalio.Direction.OUTPUT
        self.twosLed.value = True
        self.foursLed = digitalio.DigitalInOut(config.stateLedPins[2])
        self.foursLed.direction = digitalio.Direction.OUTPUT
        self.foursLed.value = True
        self.displayedStateNum = 1
        self.display = matrices.CustomMatrix(spi, cs, 14*8, 8, rotation=1)
        self.asyncList = []
        self.currentDisplayed = [[0 for col in range(14*8)] for row in range(8)]
        self.matInfo = {"leftEye": {"numPanels": 2, "offset": -1},
                        "leftMouth": {"numPanels": 4, "offset": -1},
                        "leftNose": {"numPanels": 1, "offset": -1},
                        "rightNose": {"numPanels": 1, "offset": -1},
                        "rightMouth": {"numPanels": 4, "offset": -1},
                        "rightEye": {"numPanels": 2, "offset": -1}}
        self.matInfo[config.matOrder[0]]["offset"] = 0 #first one will always be 0
        runningSum = self.matInfo[config.matOrder[0]]["numPanels"]*8
        for mat in config.matOrder[1:]:
            self.matInfo[mat]["offset"] = runningSum
            runningSum += self.matInfo[mat]["numPanels"]*8
        self.currentMood = None
        # before we enter the first state, flash the display to indicate reboot
        smartFill(self, True)
        time.sleep(.5)
        smartFill(self, False)
        self.twosLed.value = False
        self.foursLed.value = False
        self.moods[next(iter(self.moods.keys()))].enterMood()
        if (config.rgbStripEnable):
            self.rgbLights = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, config.numRGBLEDs, auto_write=False)
            self.rgbLights.brightness = config.maxRGBBrightness
            self.rgbLastRun = time.monotonic()
            self.rgbIndex = 0
            external_power = digitalio.DigitalInOut(board.EXTERNAL_POWER)
            external_power.direction = digitalio.Direction.OUTPUT
            external_power.value = True
    
    def gotoNextMood(self):
        l = list(self.moods.keys())
        i = l.index(self.currentMood.name)
        if i < len(l)-1:
            self.moods[l[i+1]].enterMood()
            self.displayedStateNum += 1
        else:
            self.moods[next(iter(self.moods.keys()))].enterMood()
            self.displayedStateNum = 1
        self.onesLed.value = self.displayedStateNum & 0b1
        self.twosLed.value = self.displayedStateNum & 0b10
        self.foursLed.value = self.displayedStateNum & 0b100
    
    async def beginLoop(self):
        animTask = asyncio.create_task(animationCheck(self))
        self.asyncList.append(animTask)
        if (config.moodSwitchOnHallEffect):
            hallTask = asyncio.create_task(hallCheck(self))
            self.asyncList.append(hallTask)
        if (config.moodSwitchOnButtonPress):
            buttonTask = asyncio.create_task(buttonCheck(self))
            self.asyncList.append(buttonTask)
        if(config.rgbStripEnable):
            rgbTask = asyncio.create_task(rgbCheck(self))
            self.asyncList.append(rgbTask)
        results = await asyncio.gather(*self.asyncList)


