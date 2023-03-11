from lib.max7219.matrix import LedMatrix


ledMat = LedMatrix(0, 0)

ledMat.show("AB", delay=1)
ledMat.CLEAR_DISPLAY()

ledMat.close()