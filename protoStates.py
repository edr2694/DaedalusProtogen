from sprites import *
import time
from adafruit_max7219 import matrices
import globalVars

L_EYE_OFF  = 0
R_EYE_OFF  = 12
L_NOSE_OFF = 6
R_NOSE_OFF = 7
L_MOUTH_OFF= 2
R_MOUTH_OFF= 8

order = ["leftEye", "leftMouth", "leftNose", "rightNose", "rightMouth", "rightEye"]

 

vFlipLEye = False
hFlipLEye = False
vFlipLMouth = True
hFlipLMouth = True
vFlipLNose = False
hFlipLNose = False
vFlipRNose = False
hFlipRNose = False
vFlipRMouth = True
hFlipRMouth = True
vFlipREye = False
hFlipREye = False



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
    def __init__(self, name, rightMouth, rightEye, rightNose, leftMouth=None, leftEye=None, leftNose=None, animate=False, period=None, animFunc=None, flipSymetry=True):

        self.name   = name
        self.flipSymetry = flipSymetry
        matricies = {
            "rightMouth": matConv(rightMouth, vFlipRMouth, hFlipRMouth),
            "rightEye": matConv(rightEye, vFlipREye, hFlipREye),
            "rightNose": matConv(rightNose, vFlipRNose, hFlipRNose)}



        if (leftMouth != None):
            matricies.update({"leftMouth": matConv(leftMouth, vFlipLMouth, hFlipLMouth)})
        else:
            matricies.update({"leftMouth": flipSide(matConv(rightMouth, vFlipLMouth, hFlipLMouth), self.flipSymetry)})

        if (leftEye != None):
            matricies.update({"leftEye" : matConv(leftEye, vFlipLEye, hFlipLEye)})
        else:
            matricies.update({"leftEye" : flipSide(matConv(rightEye, vFlipLEye, hFlipLEye), self.flipSymetry)})

        if (leftNose != None):
            matricies.update({"leftNose" : matConv(leftNose, vFlipLNose, hFlipLNose)})
        else:
            matricies.update({"leftNose" : flipSide(matConv(rightNose, vFlipLNose, hFlipLNose), self.flipSymetry)})

        # order dicrionary based on the configuration

        sortedMats = []
        for i in order:
            sortedMats.append(matricies[i])
        self.fullDefaultMat = []
        for row in range(8):
            self.fullDefaultMat.append([])
        for i in sortedMats:
            for row in range(8):
                self.fullDefaultMat[row]+=i[row]

        self.animate = animate

        if (animate == True):
            self.period = period
        else:
            self.period = None

        self.animFunc = animFunc
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period

    def enterState(self):
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period
        # we need to make sure we tell the global current globalVars.matDisplay of this update
        smartFill(False)
        smartUpdate(self.fullDefaultMat)



