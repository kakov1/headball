SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FLOOR_HEIGHT = 40

GOAL_WIDTH = 120
GOAL_HEIGHT = 300

FONT_SIZE = 200

diam = 50
side = 100

FPS = 60

BG = (0, 191, 255)

FLOOR_SIZE = [(0, SCREEN_HEIGHT),
              (SCREEN_WIDTH, SCREEN_HEIGHT),
              (0, SCREEN_HEIGHT+FLOOR_HEIGHT),
              (SCREEN_WIDTH, SCREEN_HEIGHT+FLOOR_HEIGHT)]
RIGHT_WALL_SIZE = [(0,0), 
                   (0, SCREEN_HEIGHT)]
LEFT_WALL_SIZE = [(SCREEN_WIDTH, 0),
                  (SCREEN_WIDTH, SCREEN_HEIGHT)]
CEILING_SIZE = [(0, 0),
                (SCREEN_WIDTH, 0)]
RIGHT_GOAL_SIZE = [(0, SCREEN_HEIGHT - GOAL_HEIGHT),
                   (GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT),
                   (0, SCREEN_HEIGHT - GOAL_HEIGHT*14/15),
                   (GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15)]
LEFT_GOAL_SIZE = [(SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT),
                  (SCREEN_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT),
                  (SCREEN_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15),
                  (SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15)]

BALL_START_POS = (SCREEN_WIDTH/2, SCREEN_HEIGHT - diam/2)
RIGHT_PLAYER_START_POS = (SCREEN_WIDTH - GOAL_WIDTH - side/2, SCREEN_HEIGHT - side/2)
LEFT_PLAYER_START_POS = (GOAL_WIDTH + side/2, SCREEN_HEIGHT - side/2)

FLOOR_RECT = (0, SCREEN_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)
FLOOR_COLOR = (51,102,0)
RIGHT_GOAL_POS = (0, SCREEN_HEIGHT - GOAL_HEIGHT)
LEFT_GOAL_POS = (SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT)
