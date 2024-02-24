import config
from protogenMood import *
import time
import board
import digitalio
from adafruit_max7219 import matrices
from collections import OrderedDict

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


class protogen:
    def __init__(self, moods):
        self.moods = moods
        for mood in moods.values():
            mood.protogen = self
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D4)
        self.currentDisplayed = [[0 for col in range(14*8)] for row in range(8)]
        self.display = matrices.CustomMatrix(spi, cs, 14*8, 8, rotation=1)
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
        self.currentMood = self.moods[next(iter(self.moods.keys()))]
        self.currentMood.enterMood()
    
    def gotoNextMood(self):
        l = list(self.moods.keys())
        i = l.index(self.currentMood.name)
        if i < len(l)-1:
            self.moods[l[i+1]].enterMood()
        else:
            self.moods[next(iter(self.moods.keys()))].enterMood()
