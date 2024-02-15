from sprites import *
import time
from adafruit_max7219 import matrices
import globalVars

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

def smartUpdate(newMat):
    for row in range(8):
        for col in range(14*8):
            if globalVars.currentMatrixState[row][col] != newMat[row][col]:
                globalVars.matDisplay.pixel(col,row, newMat[row][col])
                globalVars.currentMatrixState[row][col] = newMat[row][col]
    globalVars.matDisplay.show()
    

def smartFill(onOff):
    for row in range(8):
        for col in range(14*8):
            checkval = 1 if onOff==True else 0
            if globalVars.currentMatrixState[row][col] != checkval:
                globalVars.matDisplay.pixel(col,row, checkval)
                globalVars.currentMatrixState[row][col] = checkval
    globalVars.matDisplay.show()
    #update current globalVars.matDisplay state

class protoState:
    def __init__(self, name, rightMouth, rightEye, rightNose, leftMouth=None, leftEye=None, leftNose=None, period=None, animFunc=None, flipSymetry=True):

        self.name   = name
        self.flipSymetry = flipSymetry
        matricies = {
            "rightMouth": matConv(rightMouth, globalVars.vFlipRMouth, globalVars.hFlipRMouth),
            "rightEye": matConv(rightEye, globalVars.vFlipREye, globalVars.hFlipREye),
            "rightNose": matConv(rightNose, globalVars.vFlipRNose, globalVars.hFlipRNose)}



        if (leftMouth != None):
            matricies.update({"leftMouth": matConv(leftMouth, globalVars.vFlipLMouth, globalVars.hFlipLMouth)})
        else:
            matricies.update({"leftMouth": flipSide(matConv(rightMouth, globalVars.vFlipLMouth, globalVars.hFlipLMouth), self.flipSymetry)})

        if (leftEye != None):
            matricies.update({"leftEye" : matConv(leftEye, globalVars.vFlipLEye, globalVars.hFlipLEye)})
        else:
            matricies.update({"leftEye" : flipSide(matConv(rightEye, globalVars.vFlipLEye, globalVars.hFlipLEye), self.flipSymetry)})

        if (leftNose != None):
            matricies.update({"leftNose" : matConv(leftNose, globalVars.vFlipLNose, globalVars.hFlipLNose)})
        else:
            matricies.update({"leftNose" : flipSide(matConv(rightNose, globalVars.vFlipLNose, globalVars.hFlipLNose), self.flipSymetry)})

        # order dicrionary based on the configuration

        sortedMats = []
        for i in globalVars.matOrder:
            sortedMats.append(matricies[i])
        self.fullDefaultMat = []
        for row in range(8):
            self.fullDefaultMat.append([])
        for i in sortedMats:
            for row in range(8):
                self.fullDefaultMat[row]+=i[row]

        self.period = period

        self.animFunc = animFunc
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period

    def enterState(self):
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period
        # we need to make sure we tell the global current globalVars.matDisplay of this update
        smartFill(False)
        smartUpdate(self.fullDefaultMat)
    
    def doAnimation(self):
        if self.period == None or self.animFunc == None or time.monotonic() < self.nextRun:
            return
        else:
            self.animFunc()
            self.nextRun += self.period




