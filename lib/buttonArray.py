from typing import Dict
from gpiozero import Button

class ButtonArray:
    def __init__(self):
        Button.was_held = False
        self.buttons: Dict[str, Button] = {}

    def addButton(self, label: str, pin: int,was_held = False, when_pressed = None, when_held = None, when_released = None):
        if label in self.buttons:
            return

        self.buttons[label] = Button(pin)

        
        self.buttons[label].was_held = was_held

        if when_pressed:
            self.buttons[label].when_pressed = when_pressed
        if when_held:
            self.buttons[label].when_held = when_held
        if when_released:
            self.buttons[label].when_released = when_released

        return self

    def getButton(self, label: str):
        return self.buttons[label]