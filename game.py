import pygame, sys
from config import *
from apple import Apple
from snake import Snake
import numpy as np
import math

class Game():
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Snake')

  def drawGrid(self):
    for x in range(0, WINDOW_WIDTH, CELLSIZE):
      pygame.draw.line(self.screen, GRID_COLOR, (x,0), (x, WINDOW_HEIGHT))

    for y in range(0, WINDOW_HEIGHT, CELLSIZE):
      pygame.draw.line(self.screen, GRID_COLOR, (0,y), (WINDOW_WIDTH, y))

  def drawSnake(self):
    for snakeCoord in self.snake.coordinates:
      x = snakeCoord['x']*CELLSIZE
      y = snakeCoord['y']*CELLSIZE

      snakeRectangle = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
      pygame.draw.rect(self.screen, SNAKE_COLOR, snakeRectangle)

  def drawApple(self):
    x = self.apple.x*CELLSIZE
    y = self.apple.y*CELLSIZE

    appleRectangle = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(self.screen, APPLE_COLOR, appleRectangle)

  def drawScore(self):
    score = len(self.snake.coordinates) - len(STARTING_SNAKE)
    scoreSurf = pygame.font.Font(None, 20).render('Score : %s' % (score), True, SCORE_COLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
    self.screen.blit(scoreSurf, scoreRect)

  def render(self):
    self.screen.fill(BG_COLOR)
    self.drawGrid()
    self.drawApple()
    self.drawSnake()
    self.drawScore()

    pygame.display.update()
    self.clock.tick(FPS)

  def handleAction(self, action):
    if(self.snake.direction != OPPOSITE_ACTIONS[action]):
      self.snake.direction = ACTIONS[action]

  def isGameOver(self):
    if self.snake.coordinates[0]['x'] < 0 or\
        self.snake.coordinates[0]['x'] >= NB_CELL_WIDTH or\
        self.snake.coordinates[0]['y'] < 0 or\
        self.snake.coordinates[0]['y'] >= NB_CELL_HEIGHT:
      return True

    for snakeBody in self.snake.coordinates[1:]:
      if snakeBody['x'] == self.snake.coordinates[0]['x'] and\
          snakeBody['y'] == self.snake.coordinates[0]['y']:
        return True
    
    if self.snake.lastAte >= 50:
      return True

  def resetGame(self):
    self.apple = Apple()
    self.snake = Snake()
    self.grid = np.zeros((NB_CELL_WIDTH+2, NB_CELL_HEIGHT+2))

  def updateGrid(self):
    # 0 is empty, 1 is apple, 2 is snake, 3 is border
    self.grid = np.zeros((NB_CELL_HEIGHT+2, NB_CELL_WIDTH+2))
    self.grid[[0, -1], :] = 3
    self.grid[:, [0, -1]] = 3
    self.grid[self.apple.y+1, self.apple.x+1] = 1
    for pos in self.snake.coordinates[1:]:
      self.grid[pos['y']+1, pos['x']+1] = 2

  def step(self, action):
    self.handleAction(action)
    self.snake.update(self.apple)
    self.updateGrid()
    return self.getObservation(), self.snake.reward, self.isGameOver()


  def getObservation(self):
    def loop(x_increment, y_increment, head_x, head_y):
        distance = 0
        food = -1
        body = -1
        wall = -1
        base_distance = math.sqrt(x_increment**2 + y_increment**2)
        x = head_x+x_increment+1
        y = head_y+y_increment+1
        while (x > -1) and (y > -1) and (x < len(self.grid[0])) and (y < len(self.grid)):
            if self.grid[y, x] == 1 and food == -1: food = distance
            if self.grid[y, x] == 2 and body == -1: body = distance
            if self.grid[y, x] == 3 and wall == -1: wall = distance
            distance += base_distance
            x += x_increment
            y += y_increment
        max_dist = math.sqrt(NB_CELL_WIDTH**2 + NB_CELL_HEIGHT** 2)
        if body == -1: body = max_dist
        if food == -1: food = max_dist
        return [wall, food, body]

    observation = np.array([loop(lx, ly, self.snake.coordinates[0]['x'], self.snake.coordinates[0]['y']) for (lx, ly) in OBSERVATION_DIRECTIONS[self.snake.direction]])
    observation.shape = (24,)
    observation = 1-2*observation/math.sqrt(NB_CELL_WIDTH**2 + NB_CELL_HEIGHT**2)
    return observation