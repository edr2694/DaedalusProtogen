from sprites import *
import time
from adafruit_max7219 import matrices
import config
from protogen import *


class protogenMood:
    def __init__(self, name, rightMouth, rightEye, rightNose, leftMouth=None, leftEye=None, leftNose=None, period=None, flipSymetry=True, animFunc=None, animDelay=None, animData=None):

        self.name   = name
        self.flipSymetry = flipSymetry
        self.fullDefaultMat = createFullMat(rightMouth, rightEye, rightNose, leftMouth, leftEye, leftNose, flipSymetry)

        self.animFunc = animFunc
        self.period = period
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period
        self.animData = animData
        self.animIndex = 0
        self.animDelay = animDelay
        self.protogen = None

    def enterMood(self):
        self.nextRun = -1 if (self.period == None) else time.monotonic()+self.period
        smartFill(self.protogen, False)
        smartUpdate(self.protogen, self.fullDefaultMat)
        self.protogen.currentMood = self
    
    def doAnimation(self):
        if self.period == None or self.animFunc == None or time.monotonic() < self.nextRun:
            return
        else:
            self.animFunc(self, delay=self.animDelay, animData=self.animData, animIndex=self.animIndex)
            self.nextRun += self.period