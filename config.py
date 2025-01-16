import board
def init():
    global moodSwitchOnButtonPress
    global moodSwitchOnHallEffect
    global moodSwitchRemoteEnable
    global moodButtonPin
    global hallEffectPin
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
    global numRGBLEDs
    global maxRGBBrightness
    global rgbStripAnimationRate
    global rgbStripAnimation
    global rgbStripSolidColor
    global stateLedEnable
    global stateLedPins
    global oledScreenEnable
    global battSensePin
    global rgbStripPin
    global buttonEnable
    global hallEffectEnable
    global microphonePin
    global microphoneEnable
    global talkAnimationOnMicrophone


    # hardware configuration

    # set to True if you want to have a button directly hooked up to the board to change the mood, otherwise False
    moodSwitchOnButtonPress = False # <True or False>
    # set the following to True if you wish to use a hall effect sensor
    moodSwitchOnHallEffect = True # True or False
    # Set the following to true if you want to have a button to switch moods
    buttonEnable = False # True or False
    # Set the following to true if you want to have a hall effect sensor and magnet to switch moods
    hallEffectEnable = True
    # Pin that one of the leads on the button above is connected to (the other is connected to gnd)
    # ignored if moodSwitchOnButtonPress is False
    moodButtonPin = board.D5 # <board.<pin identifier>> ie board.D5
    # Pin the sense pin of the hall effect sensor is connected to
    # ignored if moodSwitchOnHallEffect is False
    hallEffectPin = board.A1
    # Set to True if using my BLE remote control. Link to github repo to be added when done
    moodSwitchRemoteEnable = False # <True or False>

    # optional 3 led's to display state number
    stateLedPins = [board.D12, board.D11, board.D10]
    # Set to True if using the LED's to show state number, otherwise set to False
    stateLedEnable = False # <True or False>

    # optional enable SSD1306 OLED screen, hooked up to the SCL and SDA pins on the RP2040
    oledScreenEnable = True
    # if screen is enabled, you'll want to hook up a resistor network to the following pin to read the voltage
    battSensePin = board.A3

    # Order of the matrix groups. Rearrange them in the order that they are wired
    matOrder = ["leftEye", "leftMouth", "leftNose", "rightNose", "rightMouth", "rightEye"]

    # Specify the pin for a microphone
    microphonePin = board.A0
    # enable the microphone in general
    microphoneEnable = False # <True or False>
    # do a talk animation when enabled
    talkAnimationOnMicrophone = False # <True or False>

    # horizontal/vertical flip control. Change these if the orientation needs to be changed
    # <True or False> for all of the following:
    vFlipLEye   = True
    hFlipLEye   = True
    vFlipLMouth = True
    hFlipLMouth = True
    vFlipLNose  = True
    hFlipLNose  = True
    vFlipRNose  = True
    hFlipRNose  = True
    vFlipRMouth = True
    hFlipRMouth = True
    vFlipREye   = True
    hFlipREye   = True
    
    # optional RGB Strip

    # Set to true to enable 
    rgbStripEnable = True # <True or False>
    #Set to pin used for RGB strip control
    rgbStripPin = board.D9
    # Number of LED's on the strip <integer>
    numRGBLEDs = 50
    # Maximum brightness for the RGB strip <number between 0.0 and 1.0>
    maxRGBBrightness = .4
    # "Animation" to run on the strip <"solid", "breathe", "rainbowCycle", "wheel">
    rgbStripAnimation = "rainbowCyle"
    # Rate for the RGB strip animation <number of seconds the animation should take to cycle>
    rgbStripAnimationRate = 20
    # Solid color for RGB Strip (required if solid or breathing animation) <(<redValue0-255>, <greenValue0-255>, <blueValue0-255>)>
    rgbStripSolidColor = (128,128,128)
