from typing import Dict

from gpiozero import Button
from signal import pause
import simpleaudio as sa
from threading import Thread
import string
import random

# Constant
import CONSTANTS

# User libraries
from lib.face_recognition import FaceRecognition
from lib.buttonArray import ButtonArray
from lib.pattern import Pattern
from lib.max7219.matrix import LedMatrix

class DoorBell:
    def __init__(self):
        self.bellSound = sa.WaveObject.from_wave_file("./static/bell.wav") # Bell sound
        self.startupSound = sa.WaveObject.from_wave_file("./static/startup.wav") # Startup sound

        self.led = LedMatrix(0, 0) # Led Matrix
        self.buttonArray = ButtonArray() # Button Array

        self.fc = FaceRecognition() # Face recognition library
        self.pattern = Pattern("1234", display = self.led) # Pattern library

        # Initialize buttons
        self.buttonArray.addButton("HomeButton", CONSTANTS.HOME_BUTTON, when_pressed=self.homeHandler)
        self.buttonArray.addButton("UpButton", CONSTANTS.UP_BUTTON, when_pressed=self.upHandler)
        self.buttonArray.addButton("DownButton", CONSTANTS.DOWN_BUTTON, when_pressed=self.downHandler)
        self.buttonArray.addButton("RightButton", CONSTANTS.RIGHT_BUTTON, when_pressed=self.rightHandler)

    def onMatchFound(self, user:str):
         # Log the user name and entry time
        print(user)


        # Display approval graphics on 8x8 matrix
        self.led.setBitmap(CONSTANTS.FRAME_TICK)

    def homeHandler(self): # Also the left handler
        if self.pattern.STATE == "STARTED":
            return self.pattern.left()

        # Play the bell
        self.bellSound.play()

        # Display camera frame on display
        self.led.setBitmap(bitMap=CONSTANTS.FRAME_CAMERA)

        # Start the face recognition process
        self.fc.run_recognition(onMatchFound=self.onMatchFound,
                        cancelButton=self.buttonArray.getButton("HomeButton"))
        
    def upHandler(self):
        if self.pattern.STATE == "STARTED":
            self.pattern.up()
        else:
            self.pattern.start_session()

    def downHandler(self):
        if self.pattern.STATE == "STARTED":
            self.pattern.down()
        else:
            self.pattern.start_session()

    def rightHandler(self):
        if self.pattern.STATE == "STARTED":
            self.pattern.right()
        else:
            self.pattern.start_session()


    def start(self):
        self.startupSound.play()

    def close(self):
        self.led.CLEAR_DISPLAY()
        self.led.close()

# bellSound = sa.WaveObject.from_wave_file("./static/bell.wav") # Bell sound
# startupSound = sa.WaveObject.from_wave_file("./static/startup.wav") # Startup sound


# fc = FaceRecognition() # Facerecogntion Library
# pattern = Pattern("1234") # Passcode Library

# buttonArrray = ButtonArray() # Button Array

# led = LedMatrix(0, 0)



# def match_found(user:str):
   
#     pass


# # Handle Face Detecte on button push
# def face_detect():
#     pass

# buttonArrray.addButton("FaceDetect", CONSTANTS.HOME_BUTTON, when_pressed=face_detect) # Add button with handler to the button on GPIO PIN 2





# startupSound.play()
# pause()


if __name__ == "__main__":
    db = DoorBell()
    try:
        db.start()
        pause()
    finally:
        db.close()