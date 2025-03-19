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

        if not x:
            self.x += random.choice([-DSIZE, 0, DSIZE])
        else:
            self.x += x
        self.x = round(self.x, 1)

        if not y:
            self.y += random.choice([-DSIZE, 0, DSIZE])
        else:
            self.y += y
        self.y = round(self.y, 1)

        if not z:
            self.z += random.choice([-DSIZE, 0, DSIZE])
        else:
            self.z += z
        self.z = round(self.z, 1)

        if self.x < -SIZE/2:
            self.x = -SIZE/2
        elif self.x > SIZE/2:
            self.x = SIZE/2
        if self.y < -SIZE/2:
            self.y = -SIZE/2
        elif self.y > SIZE/2:
            self.y = SIZE/2 
        if self.z < 0:
            self.z = 0
        elif self.z > SIZE/2:
            self.z = SIZE/2 

if __name__ == '__main__':
    gripper = Player()
    target = Player()
    print(gripper)
    print(target)
    print(gripper-target)
