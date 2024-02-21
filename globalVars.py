import time
import board
import digitalio
from adafruit_max7219 import matrices



def init(spi, cs):
    global currentMatrixState
    global matDisplay
    global matOrder
    global matInfo
    global sizeIndex
    global orderIndex
    global offsetIndex
    global vFlipLEye
    global hFlipLEye
    global vFlipLMouth
    global hFlipLMouth
    global vFlipLNose
    global hFlipLNose
    global vFlipRNose
    global hFlipRNose
    global vFlipRMouth
    global hFlipRMouth
    global vFlipREye
    global hFlipREye
    global currentProtoState
    vFlipLEye   = False
    hFlipLEye   = False
    vFlipLMouth = True
    hFlipLMouth = True
    vFlipLNose  = False
    hFlipLNose  = False
    vFlipRNose  = False
    hFlipRNose  = False
    vFlipRMouth = True
    hFlipRMouth = True
    vFlipREye   = False
    hFlipREye   = False
    currentProtoState = None
    sizeIndex = 0
    orderIndex = 1
    offsetIndex = 2
    matOrder = ["leftEye", "leftMouth", "leftNose", "rightNose", "rightMouth", "rightEye"]
    currentMatrixState = [[0 for col in range(14*8)] for row in range(8)]
    matDisplay = matrices.CustomMatrix(spi, cs, 14*8, 8, rotation=1)
    
    # -1 is temporary until we set the actual offset below
    matInfo = {"leftEye": [2, matOrder.index("leftEye"), -1],
               "leftMouth": [4, matOrder.index("leftMouth"), -1],
               "leftNose": [1, matOrder.index("leftNose"), -1],
               "rightNose": [1, matOrder.index("rightNose"), -1],
               "rightMouth": [4, matOrder.index("rightMouth"), -1],
               "rightEye": [2, matOrder.index("rightEye"), -1]}

    # set the offsets now that we've gotten the order
    matInfo[matOrder[0]][offsetIndex] = 0 #first one will always be 0
    runningSum = matInfo[matOrder[0]][sizeIndex]*8
    for mat in matOrder[1:]:
        matInfo[mat][offsetIndex] = runningSum
        runningSum += matInfo[mat][sizeIndex]*8