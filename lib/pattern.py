import threading
import random
import string
import time

# User libraries
from lib.max7219.matrix import LedMatrix
import CONSTANTS

def generate_string(length: int):
    return [*''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=length))]

class Pattern:
    def __init__(self, pin: str, display:LedMatrix):
        self.STATE = "IDLE"  # Track the state of the pattern machine
        self.display = display
        self.pin = pin  # Store the user entered pin
        self.matrix = []  # Store the randomly generated matrix
        self.cursors = {  # Store the current location of the cursor
            "row": 0,
            "col": 0
        }
        self.tries = 0 # Store the number of user attempts
        # Store the saved location, default is set to 0
        self.saved_locations = [0 for i in range(len(self.pin))]
        

    def generate_matrix(self):
        for i in range(len(self.pin)):
            string = generate_string(5)
            string[random.randint(0, 5 - 1)] = self.pin[i]
            self.matrix.append(string)

    def get_current_password(self):
        entered_pin = []
        # Iterate through the all the rows of the matrix
        for i in range(len(self.pin)):
            entered_pin.append(self.matrix[i][self.saved_locations[i]])

        print(entered_pin)
        return entered_pin

    def start_session(self):
        self.STATE = "STARTED"  # Change the state of the machine

        threading.Timer(120, self.end_session).start()  # Set timer

        self.generate_matrix()  # Generate and store a randomly generated password
        self.update_display() # Update the display to show characters

    def end_session(self):
        self.STATE = "ENDED"  # Change the state of the machine
        print("Session Ended")
        # Reset the cursors
        self.cursors["row"] = 0
        self.cursors["col"] = 0

        # Reset the saved location
        self.saved_locations = [0 for i in range(len(self.pin))]

        # Reset the matrix
        self.matrix = []

        # Reset the number of attempts
        self.tries = 0

        # Clear the display
        self.display.CLEAR_DISPLAY()

    def down(self):
        if self.STATE == "ENDED":
            return

        # Move the cursor in the horizontal axis (+ 1)
        self.cursors["col"] = min(self.cursors["col"] + 1, 4)
        # Update the saved locations
        self.saved_locations[self.cursors["row"]] = self.cursors["col"]

        self.get_current_password()  # Print the updated password
        self.display.setBitmap(CONSTANTS.FRAME_ARROW_DOWN)
        time.sleep(2)
        self.update_display()  # Print the updated password

    def up(self):
        if self.STATE == "ENDED":
            return
        # Move the cursor in the horizontal axis (+ 1)
        self.cursors["col"] = max(0, self.cursors["col"] - 1)
        # Update the saved locations
        self.saved_locations[self.cursors["row"]] = self.cursors["col"]

        self.get_current_password()  # Print the updated password
        self.display.setBitmap(CONSTANTS.FRAME_ARROW_UP)
        time.sleep(0.75)
        self.update_display()  # Print the updated password

    def right(self):
        if self.STATE == "ENDED":
            return

        if self.cursors["row"] == 3:
            return self.check_password()

        # Move the cursor in the vertical axis (+ 1)
        self.cursors["row"] = min(self.cursors["row"] + 1, 3)

        # Move the col cursor to the save location
        self.cursors["col"] = self.saved_locations[self.cursors["row"]]

        # Update the saved locations

        self.get_current_password()  # Print the updated password
        self.display.setBitmap(CONSTANTS.FRAME_ARROW_RIGHT)
        time.sleep(0.75)
        self.update_display() 

    def left(self):
        if self.STATE == "ENDED":
            return
        # Move the cursor in the vertical axis (+ 1)
        self.cursors["row"] = max(self.cursors["row"] - 1, 0)

        # Move the col cursor to the save location
        self.cursors["col"] = self.saved_locations[self.cursors["row"]]

        # Update the saved locations

        self.get_current_password()  # Print the updated password
        self.display.setBitmap(CONSTANTS.FRAME_ARROW_LEFT)
        time.sleep(0.75)
        self.update_display() 

    def check_password(self):
        if self.tries >= 3:
            self.display.show("Please try again", delay=.5)

            return self.end_session()
        if "".join(self.get_current_password()) == self.pin:
            self.display.show("Access granted")
            self.display.setBitmap(CONSTANTS.FRAME_TICK)
            time.sleep(0.75)
            self.end_session()
        else:
            print("Access denied")
            self.tries += 1

    def update_display(self):
        self.display.show(self.matrix[self.cursors["row"]][self.cursors["col"]])

    def parse_command(self, command: str):
        if command == "D":
            self.down()
        elif command == "U":
            self.up()
        elif command == "R":
            self.right()
        elif command == "L":
            self.left()