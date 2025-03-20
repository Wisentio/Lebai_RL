import numpy as np
import logging
from logging import info, basicConfig as logging_confing

logging_confing(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    datefmt="%H:%M:%S"
)
SIZE = 2
DSIZE = 0.1
HM_EPISODES = 2500
MOVE_PENALTY = 1  # feel free to tinker with these!
ENEMY_PENALTY = 300  # feel free to tinker with these!
FOOD_REWARD = 25  # feel free to tinker with these!
epsilon = 0.5  # randomness
EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = HM_EPISODES / 10  # how often to play through env visually.
DISPLAY_EVERY = 50
PROXIMITY_THREASHOLD = 0.05
LEARNING_RATE = 0.1
DISCOUNT = 0.95

x_coordinates = np.arange(-SIZE, SIZE+DSIZE, DSIZE)
x_coordinates = [0 if x==0 else round(x,1) for x in x_coordinates]
y_coordinates = np.arange(-SIZE, SIZE+DSIZE, DSIZE)
y_coordinates = [0 if y==0 else round(y,1) for y in y_coordinates]
z_coordinates = np.arange(-SIZE/2, SIZE/2+DSIZE, DSIZE)
z_coordinates = [0 if z==0 else round(z,1) for z in z_coordinates]


coordinates = np.arange(0, SIZE/2, DSIZE)
coordinates = [0 if x==0 else round(x,1) for x in coordinates]

if __name__ == '__main__':
    print(x_coordinates)
    print(z_coordinates)
