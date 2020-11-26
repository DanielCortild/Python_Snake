from pygame.locals import *

FPS = 30

CELLSIZE = 20
NB_CELL_WIDTH = 10
NB_CELL_HEIGHT = 10
WINDOW_WIDTH = NB_CELL_WIDTH * CELLSIZE
WINDOW_HEIGHT = NB_CELL_HEIGHT * CELLSIZE

STARTING_DIRECTION = 'right'
STARTING_SNAKE = [
	{'x': 5, 'y': 5},
	{'x': 5, 'y': 5},
	{'x': 5, 'y': 5},
	{'x': 5, 'y': 5},
	{'x': 5, 'y': 5},
]

MOVE_VECTORS = {
	'left': (-1, 0),
	'right': (1, 0),
	'up': (0, -1),
	'down': (0, 1)
}
 
ACTIONS_DICT = {
  K_UP: 0,
  K_DOWN: 1,
  K_LEFT: 2,
  K_RIGHT: 3
}
ACTIONS = {
	0: 'up',
	1: 'down',
	2: 'left',
	3: 'right'
}
OPPOSITE_ACTIONS = {
	0: 'down',
	1: 'up',
	2: 'right',
	3: 'left'
}
MOVING_ACTIONS = [
	{ # STRAIGHT
		0: 0,
		1: 1,
		2: 2,
		3: 3
	},
	{ # RIGHT
		0: 3,
		1: 2,
		2: 0,
		3: 1
	},
	{ # LEFT
		0: 2,
		1: 3,
		2: 1,
		3: 0
	}
]

OBSERVATION_DIRECTIONS = {
	'left': [
		(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1),	
	],
	'right': [
		(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), 
	],
	'up': [
		(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), 
	],
	'down': [
		(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), 
	]
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)

# Costum Colors
BG_COLOR = BLACK
GRID_COLOR = DARKGRAY
APPLE_COLOR = RED
SNAKE_COLOR = DARKGREEN
SCORE_COLOR = WHITE
GAMEOVER_COLOR = RED