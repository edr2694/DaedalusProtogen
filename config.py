def init():
    global matOrder
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

    # Order of the matrix groups. Rearrange them in the order that they are wired
    matOrder = ["leftEye", "leftMouth", "leftNose", "rightNose", "rightMouth", "rightEye"]

    # horizontal/vertical flip control. Change these if the orientation needs to be changed
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
