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



bellSound = sa.WaveObject.from_wave_file("./static/bell.wav") # Bell sound
startupSound = sa.WaveObject.from_wave_file("./static/startup.wav") # Startup sound


fc = FaceRecognition() # Facerecogntion Library
pattern = Pattern("1234") # Passcode Library

buttonArrray = ButtonArray() # Button Array



def match_found(user:str):
    # Log the user name and entry time
    print(user)

    # Display approval graphics on 8x8 matrix
    pass


# Handle Face Detecte on button push
def face_detect():
    # Play the bell
    bellSound.play()

    # TODO: Display graphics on 8x8 matrix

    # Start the face recognition process
    fc.run_recognition(onMatchFound=match_found,
                       cancelButton=buttonArrray.getButton("FaceDetect"))

buttonArrray.addButton("FaceDetect", CONSTANTS.HOME_BUTTON, when_pressed=face_detect) # Add button with handler to the button on GPIO PIN 2





startupSound.play()
pause()
