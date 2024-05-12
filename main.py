import pygame
import pymunk
import pymunk.pygame_util
import math
from params import *
import socket
import asyncio

def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    body.mass = 2
    body.moment = 5
    
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8

    space.add(body, shape)
    
    return shape


def create_player(size, pos):
    body = pymunk.Body()
    body.position = pos
    body.mass = 2
    body.moment = math.inf
    body.friction = 1
    
    shape = pymunk.Poly.create_box(body, size)
    
    space.add(body, shape)
    
    return shape


def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 1
    shape.friction = 5
    
    space.add(body, shape)
    
    return shape


def pygame_coords(x, y, size):
    return (x - size/2, y - size/2)


def distance(x, y):
    return abs(x - y)


def kick(player, ball):
    if (distance(player.body.position[0] + side/2, ball.body.position[0] - diam/2) < 3 or\
        distance(player.body.position[0] - side/2, ball.body.position[0] + diam/2) < 3) and\
        distance(player.body.position[1] + side/2, ball.body.position[1] + diam/2) < 3:
        ball.body.apply_impulse_at_local_point((0, -2000))


def frame(left, right, ball):
    screen.fill(BG)
    pygame.draw.rect(screen, FLOOR_COLOR, FLOOR_RECT)
    screen.blit(right_goal_image, RIGHT_GOAL_POS)
    screen.blit(left_goal_image, LEFT_GOAL_POS)
    screen.blit(ball_image, pygame_coords(ball.body.position[0],
                                          ball.body.position[1],
                                          diam))
    screen.blit(right_player_image, pygame_coords(right.body.position[0],
                                                  right.body.position[1],
                                                  side))
    screen.blit(left_player_image, pygame_coords(left.body.position[0],
                                                 left.body.position[1],
                                                 side))


def reset_speed(element):
    element.body.velocity = (0, element.body.velocity[1])
    return False


def set_speed(player, left, right, up):
    if left and player.body.position[0] - side/2 > 0:
        player.body.velocity = (-500, player.body.velocity[1])
    if right and player.body.position[0] + side/2 < SCREEN_WIDTH:
        player.body.velocity = (500, player.body.velocity[1])
    if up:
        player.body.velocity = (0, -400)


def goal(ball, left, right):
    coords = ball.body.position
    
    ball.body.velocity = (0, 0)
    left.body.position = LEFT_PLAYER_START_POS
    right.body.position = RIGHT_PLAYER_START_POS
    ball.body.position = BALL_START_POS
    
    if coords[0] < GOAL_WIDTH:
        return True
    return False
        


def check_goal(ball):
    coords = ball.body.position
    if (coords[0] < GOAL_WIDTH or coords[0] > SCREEN_WIDTH - GOAL_WIDTH) and\
    coords[1] > SCREEN_HEIGHT - GOAL_HEIGHT:
        return True
    return False
    

def create_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        return client
    except ConnectionRefusedError:
        print("server isn't available")
        exit(1)


def send_state(client, left, right, up):
    message = str(int(left)) + str(int(right)) + str(int(up))
    client.send(message.encode(FORMAT))
    
    
async def accept_state(client):
    data = client.recv(SIZE).decode(FORMAT)
    if len(str(data)) != 3:
        return False 
    return bool(int(data[0])), bool(int(data[1])), bool(int(data[2]))


async def request(client, left, right, up):
    send_state(client, left, right, up)
    data = await accept_state(client)
    
    return data

client = create_client()
player_number = int.from_bytes(client.recv(SIZE), "little")

if player_number == 1:
    print("Waiting second player")
    client.recv(SIZE)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + FLOOR_HEIGHT))
pygame.display.set_caption("HeadBall")

font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

space = pymunk.Space()
space.gravity = (0, 1000)
static_body = space.static_body

draw_options = pymunk.pygame_util.DrawOptions(screen)

clock = pygame.time.Clock()

ball_image = pygame.transform.scale(pygame.image.load("images/ball.png"), (diam, diam)).convert_alpha()
right_goal_image = pygame.transform.scale(pygame.image.load("images/right_goal.png"), (GOAL_WIDTH, GOAL_HEIGHT)).convert_alpha()
left_goal_image = pygame.transform.scale(pygame.image.load("images/left_goal.png"), (GOAL_WIDTH, GOAL_HEIGHT)).convert_alpha()
right_player_image = pygame.transform.scale(pygame.image.load("images/right_player.png"), (side, side)).convert_alpha()
left_player_image = pygame.transform.scale(pygame.image.load("images/left_player.png"), (side, side)).convert_alpha()

floor = create_cushion(FLOOR_SIZE)
right_wall = create_cushion(RIGHT_WALL_SIZE)
left_wall = create_cushion(LEFT_WALL_SIZE)
ceiling = create_cushion(CEILING_SIZE)
right_goal = create_cushion(RIGHT_GOAL_SIZE)
left_goal = create_cushion(LEFT_GOAL_SIZE)


async def main():
    
    game_ball = create_ball(diam/2, BALL_START_POS)
    right_player = create_player((side, side), RIGHT_PLAYER_START_POS)
    left_player = create_player((side, side), LEFT_PLAYER_START_POS)

    player_motion_left = False
    player_motion_right = False
    player_motion_up = False

    opponent_motion_left = False
    opponent_motion_right = False
    opponent_motion_up = False
    
    left_left, left_right, left_up = False, False, False
    right_left, right_right, right_up = False, False, False

    left_goals = 0
    right_goals = 0
    is_goal = False

    run = True
    
    while run:

        clock.tick(FPS)
        space.step(1 / FPS)
        
        is_goal = check_goal(game_ball)
        
        if is_goal:
            if goal(game_ball, left_player, right_player):
                right_goals += 1
            else:
                left_goals += 1 

        frame(left_player, right_player, game_ball)
        
        text = font.render(f'{left_goals}:{right_goals}', False, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, 0))
        
        player_motion_up = reset_speed(left_player)
        opponent_motion_up = reset_speed(right_player)
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_motion_right = True
                if event.key == pygame.K_LEFT:
                    player_motion_left = True
                if event.key == pygame.K_UP:
                    player_motion_up = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player_motion_right = False
                if event.key == pygame.K_LEFT:
                    player_motion_left = False
                if event.key == pygame.K_UP:
                    player_motion_up = False
            if event.type == pygame.QUIT:
                run = False
        
        data = await request(client, player_motion_left, player_motion_right, player_motion_up)
        
        if not data:
            print("Opponent exit")
            return
        
        opponent_motion_left, opponent_motion_right, opponent_motion_up = data
        
        if player_number == 1:
            left_left, left_right, left_up =\
            player_motion_left, player_motion_right, player_motion_up
            right_left, right_right, right_up =\
            opponent_motion_left, opponent_motion_right, opponent_motion_up
        else:
            right_left, right_right, right_up =\
            player_motion_left, player_motion_right, player_motion_up
            left_left, left_right, left_up =\
            opponent_motion_left, opponent_motion_right, opponent_motion_up
        
        set_speed(left_player, left_left, left_right, left_up)
        set_speed(right_player, right_left, right_right, right_up)
            
        kick(left_player, game_ball)
        kick(right_player, game_ball)
        
        #space.debug_draw(draw_options)
        pygame.display.update()


if __name__ == "__main__":
    asyncio.run(main())
    client.close()
    pygame.quit()