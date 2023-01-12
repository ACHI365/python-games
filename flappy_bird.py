import pygame


class Bird:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = 10
        self.jump = 10

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # rendering pipes
        pygame.draw.line(screen, pygame.Color("green"), [150, 400],
                         [150, 700], 30)
        pygame.draw.line(screen, pygame.Color("green"), [375, 47.5],
                         [375, 400], 30)
        pygame.draw.line(screen, pygame.Color("green"), [600, 350],
                         [600, 700], 30)
        pygame.draw.line(screen, pygame.Color("green"), [900, 47.5],
                         [900, 400], 30)
        pygame.draw.line(screen, pygame.Color("green"), [1150, 300],
                         [1150, 700], 30)

    def update(self):
        self.y -= self.jump
        self.jump -= 1.5
        self.x += self.speed

    def game_winner(self):
        return self.x > 1185

    def collision_check(self):
        return self.y < 55 or self.y > 700 - 10 \
               or ((150 - self.radius <= self.x <= 150 + self.radius + 15) and 400 <= self.y <= 700) \
               or ((375 - self.radius <= self.x <= 375 + self.radius + 15) and 47.5 + self.radius <= self.y <= 415) \
               or ((600 - self.radius <= self.x <= 600 + self.radius + 15) and 340 <= self.y <= 715) \
               or ((900 - self.radius <= self.x <= 900 + self.radius + 15) and 47.5 + self.radius <= self.y <= 415) \
               or ((1150 - self.radius <= self.x <= 1150 + self.radius + 15) and 300 <= self.y <= 1165)


class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bird = Bird(20, 300, pygame.Color("yellow"), 20)
        self.gameOver = False
        self.gameStart = True
        self.jump_flag = False
        self.clicked_space = False
        self.winner = False

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        if self.bird is not None:
            self.gameOver = self.bird.collision_check()
            if not self.gameStart and not self.gameOver and not self.winner:
                self.bird.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_r] and (self.gameOver or self.winner):
                self.bird = Bird(20, 300, pygame.Color("yellow"), 20)
                self.winner = False
                self.gameOver = False
                self.gameStart = True

            if keys[pygame.K_p] and self.gameStart:
                self.gameStart = False

            if self.bird is not None and not self.gameStart and not self.gameOver and not self.winner:
                if keys[pygame.K_SPACE]:
                    self.bird.jump = 15
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump = 15

    def render(self):
        if self.gameStart:
            self.screen.fill((0, 0, 0))
            self.StartScreen()
            self.drawMenu()
            self.bird.render(self.screen)
            self.pipeRender()
            pygame.display.flip()
            self.clock.tick(30)
        elif self.gameOver:
            self.screen.fill((0, 0, 0))
            self.gameOverScreen()
            pygame.display.flip()
            self.clock.tick(30)
        elif self.bird.game_winner():
            self.winner = True
            self.screen.fill((0, 0, 0))
            self.winnerScreen()
            pygame.display.flip()
            self.clock.tick(30)
        else:
            self.screen.fill((0, 0, 0))
            self.drawMenu()
            self.bird.render(self.screen)
            self.pipeRender()
            pygame.display.flip()
            self.clock.tick(24)

    def StartScreen(self):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Drawing Text
        self.screen.blit(
            font.render('To start the Game press P', False, pygame.Color("Yellow"))
            , (400, 300))

    def pipeRender(self):
        pass

    def gameOverScreen(self):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Drawing Text
        self.screen.blit(
            font.render('Game Over, If you wanna retry press R', False, pygame.Color("Yellow"))
            , (250, 300))

    def drawMenu(self):
        pygame.draw.line(self.screen, pygame.Color("white"), [0, 40],
                         [1200, 40], 15)

    def winnerScreen(self):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Drawing Text
        self.screen.blit(
            font.render('You Won, If you wanna retry press R', False, pygame.Color("Yellow"))
            , (250, 300))

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
