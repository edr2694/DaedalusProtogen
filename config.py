import board
def init():
    global moodSwitchOnButtonPress
    global moodSwitchRemoteEnable
    global moodButtonPin
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
    global rgbStripEnable
    global rgbStripPin
    global numRGBLEDs
    global maxRGBBrightness
    global rgbStripAnimationRate
    global rgbStripAnimation
    global rgbStripSolidColor


    # hardware configuration

    # set to True if you want to have a button directly hooked up to the board to change the mood, otherwise False
    moodSwitchOnButtonPress = True # <True or False>
    # Pin the one of the leads on the button above is connected to (the other is connected to gnd)
    # ignored if moodSwitchOnButtonPress is False
    moodButtonPin = board.D5 # <board.<pin identifier>> ie board.D5
    # Set to True if using my BLE remote control. Link to github repo to be added when done
    moodSwitchRemoteEnable = False # <True or False>

    # Order of the matrix groups. Rearrange them in the order that they are wired
    matOrder = ["leftEye", "leftMouth", "leftNose", "rightNose", "rightMouth", "rightEye"]

    # horizontal/vertical flip control. Change these if the orientation needs to be changed
    # <True or False> for all of the following:
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

    # optional RGB Strip

    # Set to true to enable 
    rgbStripEnable = False # <True or False>
    # Pin that the data line for the RGB strip is connected to
    rgbStripPin = board.D6
    # Number of LED's on the strip <integer>
    numRGBLEDs = 25
    # Maximum brightness for the RGB strip <number between 0.0 and 1.0>
    maxRGBBrightness = .3
    # "Animation" to run on the strip <"solid", "breathe", "rainbowCycle", "wheel">
    rgbStripAnimation = "rainbowCyle"
    # Rate for the RGB strip animation <number of seconds the animation should take to cycle>
    rgbStripAnimationRate = 20
    # Solid color for RGB Strip (required if solid or breathing animation) <(<redValue0-255>, <greenValue0-255>, <blueValue0-255>)>
    rgbStripSolidColor = (128,128,128)
