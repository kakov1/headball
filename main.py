import pygame
from geometry import intersection
from math import ceil


class GameSession:
    def __init__(self, gravity, images):
        self.window = None
        self.goal1 = None
        self.goal2 = None
        self.player1 = None
        self.player2 = None
        self.ball = None
        self.gravity = gravity
        self.images = images

    def AddWindow(self, window):
        self.window = window

    def AddGoal1(self, goal):
        self.goal1 = goal

    def AddGoal2(self, goal):
        self.goal2 = goal

    def AddPlayer1(self, player):
        self.player1 = player

    def AddPlayer2(self, player):
        self.player2 = player
    
    def AddBall(self, ball):
        self.ball = ball

    def hit(self, player):
        for CoordX in [player.x + player.width, player.x]:
            if intersection(1, 0, CoordX,
                        self.ball.x + self.ball.width/2, self.ball.y + self.ball.height/2, self.ball.rad,
                        player.y, player.y + player.height) != (-1,-1):
                if self.ball.vx != 0 and self.ball.motionx != player.motionx != 0:
                    self.ball.motionx = -self.ball.motionx
                    self.ball.vx = -self.ball.vx
                else:
                    self.ball.vx = player.speed/2
                    self.ball.motionx = player.motionx


    def running(self):
        clock = pygame.time.Clock()

        running = True
        
        while running:
            self.frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player1.motionx = 1
                    if event.key == pygame.K_LEFT:
                        self.player1.motionx = -1
                    if event.key == pygame.K_UP:
                        if self.player1.y == self.window.height - self.player1.height:
                            self.player1.motiony = True
                            self.player1.vy = 50
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player1.motionx = 0
                    if event.key == pygame.K_LEFT:
                        self.player1.motionx = 0

            pygame.display.update()
            
            clock.tick(60)

    def frame(self):
        self.hit(self.player1)
        self.player1.moving((self.window.width, self.window.height), self.gravity)
        self.player2.moving((self.window.width, self.window.height), self.gravity)
        self.ball.moving((self.window.width, self.window.height))
        self.window.screen.fill((0, 191, 255))
        self.window.screen.blit(self.images["goal1"], (0, 400))
        self.window.screen.blit(self.images["goal2"], (1180, 400))
        self.window.screen.blit(self.images["player1"], (self.player1.x, self.player1.y))
        self.window.screen.blit(self.images["player2"], (self.player2.x, self.player2.y))
        self.window.screen.blit(self.images["ball"], (self.ball.x, self.ball.y))


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])


class Goal:
    def __init__(self, width, height):

       self.width = width
       self.height = height


class Player:
    def __init__(self, width, height, StartPosX, StartPosY, speed):

       self.width = width
       self.height = height
       self.x = StartPosX
       self.y = StartPosY
       self.vy = 0
       self.motionx = 0
       self.motiony = False
       self.speed = speed
    
    def moving(self, FieldSize, gravity):
        if (self.x > 0 or self.motionx != -1) and\
            (self.x < FieldSize[0] - self.width or self.motionx != 1):
            self.x += self.motionx*self.speed
        if self.motiony == True:
            if self.y > FieldSize[1] - self.height:
                self.motiony = False
                self.y = FieldSize[1] - self.height
                self.vy = 0
                return
            self.y -= self.vy
            self.vy -= gravity
    

class Ball:
    def __init__(self, width, height, StartPosX, StartPosY):
        self.width = width
        self.height = height
        self.x = StartPosX
        self.y = StartPosY
        self.vy = 0
        self.vx = 0
        self.motionx = 0
        self.motiony = False
        self.rad = self.width/2

    def moving(self, FieldSize):
        if self.x < 0 or self.x > FieldSize[0] - self.width:
            self.vx = -self.vx
            self.motionx = -self.motionx
        self.x += self.vx

def main():
    images = {"player1": pygame.transform.scale(pygame.image.load("images/player1.png"), (100, 100)),
              "player2": pygame.transform.scale(pygame.image.load("images/player2.png"), (100, 100)),
              "goal1": pygame.transform.scale(pygame.image.load("images/goal1.png"), (120, 300)),
              "goal2": pygame.transform.scale(pygame.image.load("images/goal2.png"), (120, 300)),
              "ball": pygame.transform.scale(pygame.image.load("images/ball.png"), (150, 150))}

    pygame.init()

    game = GameSession(5, images)
    window = Window(1300, 700)

    goal1 = Goal(120, 300)
    goal2 = Goal(60, 150)
    player1 = Player(100, 100, 120, 600, 5)
    player2 = Player(100, 100, 1080, 600, 5)
    ball = Ball(150, 150, 575, 550)

    game.AddWindow(window)
    game.AddGoal1(goal1)
    game.AddGoal2(goal2)
    game.AddPlayer1(player1)
    game.AddPlayer2(player2)
    game.AddBall(ball)

    pygame.display.update()

    game.running()

    pygame.quit()


if __name__ == "__main__":
    main()