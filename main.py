import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FLOOR_HEIGHT = 40

GOAL_WIDTH = 120
GOAL_HEIGHT = 300

diam = 200
side = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + FLOOR_HEIGHT))
pygame.display.set_caption("HeadBall")

space = pymunk.Space()
space.gravity = (0, 1000)
static_body = space.static_body

draw_options = pymunk.pygame_util.DrawOptions(screen)

clock = pygame.time.Clock()
FPS = 60

BG = (0, 191, 255)

ball_image = pygame.transform.scale(pygame.image.load("images/ball.png"), (diam, diam)).convert_alpha()
right_goal_image = pygame.transform.scale(pygame.image.load("images/right_goal.png"), (GOAL_WIDTH, GOAL_HEIGHT)).convert_alpha()
left_goal_image = pygame.transform.scale(pygame.image.load("images/left_goal.png"), (GOAL_WIDTH, GOAL_HEIGHT)).convert_alpha()
right_player_image = pygame.transform.scale(pygame.image.load("images/right_player.png"), (side, side)).convert_alpha()
left_player_image = pygame.transform.scale(pygame.image.load("images/left_player.png"), (side, side)).convert_alpha()


def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    body.mass = 5
    body.moment = math.inf
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8


    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000


    space.add(body, shape)
    return shape


def create_player(size, pos):
    body = pymunk.Body()
    body.position = pos
    body.mass = 2
    body.moment = math.inf
    shape = pymunk.Poly.create_box(body, size)
    #shape.elasticity = 0.8
    space.add(body, shape)
    return shape


def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.2
    space.add(body, shape)
    return shape
    
floor = create_cushion([(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT),
                        (0, SCREEN_HEIGHT+FLOOR_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT+FLOOR_HEIGHT)])
right_wall = create_cushion([(0,0),(0, SCREEN_HEIGHT)])
left_wall = create_cushion([(SCREEN_WIDTH, 0),(SCREEN_WIDTH, SCREEN_HEIGHT)])
ceiling = create_cushion([(0, 0), (SCREEN_WIDTH, 0)])
right_goal = create_cushion([(0, SCREEN_HEIGHT - GOAL_HEIGHT), (GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT),
                             (0, SCREEN_HEIGHT - GOAL_HEIGHT*14/15), (GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15)])
right_goal = create_cushion([(SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT),
                             (SCREEN_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15), (SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT*14/15)])

ball = create_ball(diam/2, (SCREEN_WIDTH/2, SCREEN_HEIGHT - diam/2))
right_player = create_player((side, side), (SCREEN_WIDTH - GOAL_WIDTH - side/2, SCREEN_HEIGHT - side/2))
left_player = create_player((side, side), (GOAL_WIDTH + side/2, SCREEN_HEIGHT - side/2))


run = True
left_f = False
right_f = False

while run:

    clock.tick(FPS)
    space.step(1 / FPS)

    screen.fill(BG)
    pygame.draw.rect(screen, (51,102,0), (0, SCREEN_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT))
    screen.blit(right_goal_image, (0, SCREEN_HEIGHT - GOAL_HEIGHT))
    screen.blit(left_goal_image, (SCREEN_WIDTH - GOAL_WIDTH, SCREEN_HEIGHT - GOAL_HEIGHT))
    screen.blit(ball_image, (ball.body.position[0]-diam/2, ball.body.position[1] - diam/2))
    screen.blit(right_player_image, (right_player.body.position[0]-side/2,
                                     right_player.body.position[1] - side/2))
    screen.blit(left_player_image, (left_player.body.position[0]-side/2,
                                     left_player.body.position[1] - side/2))
    
    left_player.body.velocity = (0, left_player.body.velocity[1])
 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right_f = True
            if event.key == pygame.K_LEFT:
                left_f = True
            if event.key == pygame.K_UP:
                left_player.body.apply_impulse_at_local_point((0, -1000))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right_f = False
            if event.key == pygame.K_LEFT:
                left_f = False
        if event.type == pygame.QUIT:
            run = False
    if left_f and left_player.body.position[0] -side/2 > 0:
        left_player.body.velocity = (-1000, left_player.body.velocity[1])
    if right_f and left_player.body.position[0] + side/2 < SCREEN_WIDTH:
        left_player.body.velocity = (1000, left_player.body.velocity[1])
        
    #space.debug_draw(draw_options)
    pygame.display.update()


pygame.quit()