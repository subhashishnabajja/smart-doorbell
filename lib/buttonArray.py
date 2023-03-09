from typing import Dict
from gpiozero import Button

class ButtonArray:
    def __init__(self):
        self.buttons: Dict[str, Button] = {}

    def addButton(self, label: str, pin: int, when_pressed):
        if label in self.buttons:
            return

        self.buttons[label] = Button(pin)

        self.buttons[label].when_pressed = when_pressed

        return self

    def getButton(self, label: str):
        return self.buttons[label]