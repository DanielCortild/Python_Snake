from game import Game as game
import pygame
from config import *
from pygame.locals import *

def playAsHuman():
  env = game()
  env.resetGame()
  action = 3
  while True:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        action = ACTIONS_DICT[event.key]
  
    env.render()
    obs, reward, done = env.step(action)
    if done: env.resetGame()


