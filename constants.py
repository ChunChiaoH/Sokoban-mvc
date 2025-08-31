DEST = '0'
WALL = '+'
EMPTY = ' '
GLASS = 'G'
BROKEN_GLASS = 'B'
CAT = 'C'
MOVEABLE_ENTITY = '_'

#UP = 'w'
#DOWN = 's'
#LEFT = 'a'
#RIGHT = 'd'

UP=87 #'w'
UP_ARROW=38

DOWN=83 #'s'
DOWN_ARROW = 40

LEFT = 65 #'d'
LEFT_ARROW = 37

RIGHT = 68 #'a'
RIGHT_ARROW = 39

# Unified movement system
MOVE_DIRECTIONS = {
    'UP': {
        'delta': (-1, 0),
        'keys': [UP, UP_ARROW],
        'char': 'w'
    },
    'DOWN': {
        'delta': (1, 0),
        'keys': [DOWN, DOWN_ARROW],
        'char': 's'
    },
    'LEFT': {
        'delta': (0, -1),
        'keys': [LEFT, LEFT_ARROW],
        'char': 'a'
    },
    'RIGHT': {
        'delta': (0, 1),
        'keys': [RIGHT, RIGHT_ARROW],
        'char': 'd'
    }
}


END_GAME = 'end'

DEFAULT_TIREDNESS = 1000

TITLE = 'SOKOBAN'
PROMPT_TEXT = 'Enter a move(w,a,s,d) or "end" to quit:'
DEFAULT_GAMES = 'games/default'
DIR_NOT_EXIST = 'Directory does not exist, play default games.'
PRESS_ANY = 'This room is messed. Press any key to continue.'
GAMEFILE_TEXT = 'Enter game directory:'
WIN_TITLE = 'Won!'
WIN = 'Miao! All rooms are messed.'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
ROOM_CANVAS_WIDTH, ROOM_CANVAS_HEIGHT = 600, 600
KEY_EVENT = "<Key>"

IMAGE_FOLDER = 'images/'
TILE_IMAGES = {
    WALL: 'wall.png',
    EMPTY: 'empty.png',
    DEST: 'dest.png'
}

MOVEABLE_ENTITY_IMAGES = {
    CAT: 'cat.png',
    GLASS: 'glass.png',
    BROKEN_GLASS: 'broken_glass.png'
}

# AI Solver Messages
AI_SOLVER_TITLE = 'AI Solver'
AI_HINT_TITLE = 'AI Hint'
AI_SOLVING_MSG = 'Solving puzzle... This may take a moment.'
AI_NO_SOLUTION_MSG = 'No solution found!'
AI_ALREADY_SOLVED_MSG = 'Puzzle is already solved!'
AI_SOLUTION_FOUND_MSG = 'Solution found in {} moves! Watch the AI play.'
AI_SOLUTION_COMPLETE_MSG = 'Solution complete!'
AI_PUZZLE_SOLVED_MSG = 'Puzzle solved by AI!'
AI_TRY_MOVING_MSG = 'Try moving {}'
