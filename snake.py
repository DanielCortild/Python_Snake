import random
from config import *

class Snake():
  def __init__(self):
    self.direction = STARTING_DIRECTION
    self.coordinates = STARTING_SNAKE.copy()
    self.reward = 0
    self.lastAte = 0

  def update(self, apple):
    self.reward = 1
    self.lastAte += 1
    if self.coordinates[0]['x'] == apple.x and self.coordinates[0]['y'] == apple.y:
      apple.newCell()
      self.reward = 100
      self.lastAte = 0
    else:
      del self.coordinates[-1]

    self.coordinates.insert(0, {'x': self.coordinates[0]['x'] + MOVE_VECTORS[self.direction][0],
                                'y': self.coordinates[0]['y'] + MOVE_VECTORS[self.direction][1]})