import pygame


class GameSession:
    def __init__(self):
        self.window = None
        self.goal1 = None
        self.goal2 = None
        self.player1 = None
        self.player2 = None
        self.g = 20

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


    def frame(self):
        self.player1.x += self.player1.motionx*5
        if self.player1.motiony == True:
            if self.player1.y > self.window.height - self.player1.height:
                self.player1.motiony = False
                self.player1.y = 600
                self.player1.vy = 0
            self.player1.y -= self.player1.vy/10
            self.player1.vy -= self.g/10
        self.window.screen.fill((0, 191, 255))
        self.window.screen.blit(self.goal1.image, (0, 400))
        self.window.screen.blit(self.goal2.image, (1180, 400))
        self.window.screen.blit(self.player1.image, (self.player1.x, self.player1.y))
        self.window.screen.blit(self.player2.image, (self.player2.x, self.player2.y))


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])


class Goal:
    def __init__(self, width, height, image):

       self.image = image
       self.width = width
       self.height = height


class Player:
    def __init__(self, width, height, image, x, y):

       self.image = image
       self.width = width
       self.height = height
       self.x = x
       self.y = y
       self.vy = 0
       self.motionx = 0
       self.motiony = False


def main():
    Player1Image = pygame.transform.scale(pygame.image.load("images/player1.png"), (100, 100))
    Player2Image = pygame.transform.scale(pygame.image.load("images/player2.png"), (100, 100))
    Goal1Image = pygame.transform.scale(pygame.image.load("images/goal1.png"), (120, 300))
    Goal2Image = pygame.transform.scale(pygame.image.load("images/goal2.png"), (120, 300))

    pygame.init()
    clock = pygame.time.Clock()

    game = GameSession()
    window = Window(1300, 700)

    goal1 = Goal(120, 300, Goal1Image)
    goal2 = Goal(60, 150, Goal2Image)
    player1 = Player(100, 100, Player1Image, 120, 600)
    player2 = Player(100, 100, Player2Image, 1080, 600)

    game.AddWindow(window)
    game.AddGoal1(goal1)
    game.AddGoal2(goal2)
    game.AddPlayer1(player1)
    game.AddPlayer2(player2)
    game.frame()

    pygame.display.update()

    running = True
    while running:
        game.window.screen.fill((0, 191, 255))
        game.frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.player1.motionx = 1
                if event.key == pygame.K_LEFT:
                    game.player1.motionx = -1
                if event.key == pygame.K_UP:
                    if game.player1.y == game.window.height - game.player1.height:
                        game.player1.motiony = True
                        game.player1.vy = 50
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    game.player1.motionx = 0
                if event.key == pygame.K_LEFT:
                    game.player1.motionx = 0



        pygame.display.update()
        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    main()