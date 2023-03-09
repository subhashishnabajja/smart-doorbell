import random
import string

class Pattern:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.currentCol = 0
        self.currentRow = 0

        self.cols = [[*''.join(random.choices(string.ascii_uppercase +
                                              string.digits, k=8))] for x in range(4)]

        for i in range(len(self.cols)):
            self.cols[i][random.randint(0, 7)] = self.pattern[i]

    def up(self):
        self.currentRow = min(self.currentRow + 1, 7)
        print(self.cols[self.currentCol][self.currentRow])

    def down(self):
        self.currentRow = max(self.currentRow - 1, 0)
        print(self.cols[self.currentCol][self.currentRow])