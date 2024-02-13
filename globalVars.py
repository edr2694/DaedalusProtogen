import time
import board
import digitalio
from adafruit_max7219 import matrices
def init(spi, cs):
    global currentMatrixState
    global matDisplay
    currentMatrixState = [[0 for col in range(14*8)] for row in range(8)]
    matDisplay = matrices.CustomMatrix(spi, cs, 14*8, 8, rotation=1)