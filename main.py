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
        self.STATE = "IDLE"

        self.bellSound = sa.WaveObject.from_wave_file("./static/bell.wav") # Bell sound
        self.startupSound = sa.WaveObject.from_wave_file("./static/startup.wav") # Startup sound

        self.led = LedMatrix(0, 0) # Led Matrix
        self.buttonArray = ButtonArray() # Button Array

        self.fc = FaceRecognition() # Face recognition library
        self.pattern = Pattern("1234", display = self.led) # Pattern library

        # Initialize buttons
        self.buttonArray.addButton("HomeButton", CONSTANTS.HOME_BUTTON, when_held=self.when_held, when_released=self.when_pressed)
        self.buttonArray.addButton("UpButton", CONSTANTS.UP_BUTTON, when_pressed=self.upHandler)
        self.buttonArray.addButton("DownButton", CONSTANTS.DOWN_BUTTON, when_pressed=self.downHandler)
        self.buttonArray.addButton("RightButton", CONSTANTS.RIGHT_BUTTON, when_pressed=self.rightHandler)


    # Function to differentiate between hold and press
    def when_held(self, btn):
        btn.was_held = True
        # When the button is held
        if self.pattern.STATE == "STARTED":
            self.pattern.end_session()

            # Play the bell
            self.bellSound.play()
            self.STATE = "FACE_RECOGNITION_STARTED"

            # Display camera frame on display
            self.led.setBitmap(bitMap=CONSTANTS.FRAME_CAMERA)

            # Start the face recognition process
            result = self.fc.run_recognition(onMatchFound=self.onMatchFound,
                cancelButton=self.buttonArray.getButton("HomeButton"))
        
            if not result:
                self.onMatchNotFound()

            print(result)

        # If the machine is in the pattern recognition mode then exit pattern recognition mode and start face detection
        

    def when_pressed(self, btn):
        if not btn.was_held:
            if self.pattern.STATE == "STARTED":
                return self.pattern.left()

            # Play the bell
            self.bellSound.play()
            self.STATE = "FACE_RECOGNITION_STARTED"

            # Display camera frame on display
            self.led.setBitmap(bitMap=CONSTANTS.FRAME_CAMERA)

            # Start the face recognition process
            result = self.fc.run_recognition(onMatchFound=self.onMatchFound,
                cancelButton=self.buttonArray.getButton("HomeButton"))
        
            if not result:
                self.onMatchNotFound()

            print(result)

        

        btn.was_held = False
      

    def onMatchFound(self, user:str):
        self.STATE = "FACE_RECOGNITION_SUCCESS"

        # Log the user name and entry time
        print(user)


        # Display approval graphics on 8x8 matrix
        self.led.setBitmap(CONSTANTS.FRAME_TICK)

        self.STATE = "IDLE"

    def onMatchNotFound(self):

        # Display approval graphics on 8x8 matrix
        self.led.show("X")

        self.STATE = "IDLE"

    def onCancel(self):
        self.STATE = "FACE_RECOGNITION_CANCELLED"

        # Dislay graphich on display
        self.led.show("X")

        self.STATE= "IDLE"

    def homeHandler(self, btn:Button): # Also the left handler
        # Play the bell
        self.bellSound.play()
        self.STATE = "FACE_RECOGNITION_STARTED"

        # Display camera frame on display
        self.led.setBitmap(bitMap=CONSTANTS.FRAME_CAMERA)

        # Start the face recognition process
        result = self.fc.run_recognition(onMatchFound=self.onMatchFound,
            cancelButton=self.buttonArray.getButton("HomeButton"))
        
        if not result:
            self.onMatchNotFound()

        print(result)

        if self.pattern.STATE == "STARTED":
            return self.pattern.left()

        
        
    def upHandler(self):
        if self.pattern.STATE == "PATTERN_RECOGNITION_STARTED":
            self.pattern.up()
        else:
            self.pattern.start_session()
            self.pattern.up()

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
            self.pattern.right()


    def start(self):
        self.startupSound.play()

    def close(self):
        self.led.CLEAR_DISPLAY()
        self.led.close()


if __name__ == "__main__":
    db = DoorBell()
    try:
        db.start()
        pause()
    finally:
        db.close()