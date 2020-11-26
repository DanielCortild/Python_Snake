import random
from config import *

class Apple():
  def __init__(self):
    self.newCell()

  def newCell(self):
    self.x = random.randint(1, NB_CELL_WIDTH - 2)
    self.y = random.randint(1, NB_CELL_HEIGHT - 2)