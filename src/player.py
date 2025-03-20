import numpy as np
from constants import *
import random
from logging import error

class Player:

    def __init__(self):
        self.x = random.choice(z_coordinates)
        self.y = random.choice(z_coordinates)
        self.z = random.choice(coordinates)

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'

    def __sub__(self, other):
        return (round(self.x - other.x, 1), round(self.y - other.y, 1), round(self.z - other.z, 1))
    
    def action(self, choice):

        if choice == 0:
            self.move(x=DSIZE, y=DSIZE, z=DSIZE)
        elif choice == 1:
            self.move(x=-DSIZE, y=DSIZE, z=DSIZE)
        elif choice == 2:
            self.move(x=-DSIZE, y=-DSIZE, z=DSIZE)
        elif choice == 3:
            self.move(x=DSIZE, y=-DSIZE, z=DSIZE)
        elif choice == 4:
            self.move(x=DSIZE, y=DSIZE, z=-DSIZE)
        elif choice == 5:
            self.move(x=-DSIZE, y=DSIZE, z=-DSIZE)
        elif choice == 6:
            self.move(x=-DSIZE, y=-DSIZE, z=-DSIZE)
        elif choice == 7:
            self.move(x=DSIZE, y=-DSIZE, z=-DSIZE)
        else:
            error("NOT CORRECT CHOICE")

    def move(self, x=False, y=False, z=False):

        self.x += x if x else random.choice([-DSIZE, 0, DSIZE])
        self.y += y if y else random.choice([-DSIZE, 0, DSIZE])
        self.z += z if z else random.choice([-DSIZE, 0, DSIZE])

        self.x = round(self.x, 1)
        self.y = round(self.y, 1)
        self.z = round(self.z, 1)

        # Workspace bounds
        self.x = min(max(self.x, -SIZE/2), SIZE/2)
        self.y = min(max(self.y, -SIZE/2), SIZE/2)
        self.z = min(max(self.z, 0), SIZE/2)

        # Avoid middle
        if -0.1 <= self.x <= 0.1 and -0.1 <= self.y <= 0.1:
            self.x = -0.2 if self.x < 0 else 0.2
            self.y = -0.2 if self.y < 0 else 0.2

if __name__ == '__main__':
    gripper = Player()
    target = Player()
    print(gripper)
    print(target)
    print(gripper-target)
