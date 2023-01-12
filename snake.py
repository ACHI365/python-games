import random

import pygame


class food:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class snake:
    def __init__(self):
        self.length = 5
        self.size = 15
        self.cells = [(600, 345), (585, 345), (570, 345), (555, 345), (540, 345)]
        self.direction = "RIGHT"
        self.color = pygame.Color("green")
        self.score = 0
        self.food = None

    def addBlock(self):
        self.score += 1
        self.length += 1
        self.spawnFood()

    def canEat(self, head):
        return head[0] == self.food.x and head[1] == self.food.y

    def spawnFood(self):
        x = random.randint(2, 76) * self.size
        y = random.randint(4, 41) * self.size
        self.food = food(x, y)
        while any(list(map(lambda x: self.canEat(x), self.cells[1:]))):
            x = random.randint(2, 76) * self.size
            y = random.randint(4, 41) * self.size
        self.food = food(x, y)

    def render(self, screen):
        pygame.draw.circle(screen, pygame.Color('green'), (self.cells[0][0], self.cells[0][1]), 7.5)
        for cell in self.cells[1:]:
            pygame.draw.circle(screen, pygame.Color('green'), (cell[0], cell[1]), 7.5)
        if self.food is not None:
            pygame.draw.circle(screen, pygame.Color('red'), (self.food.x, self.food.y), 7.5)

    def hitMyself(self):
        return self.cells[0] in self.cells[1:]

    def collision_check(self):
        head = self.cells[0]
        if head[0] >= 1185 or head[0] <= 0 or head[1] < 50 or head[1] > 680 or self.hitMyself():
            self.size = 0
            return True
        return False

    def changeDir(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = direction
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = direction
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = direction
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = direction

    def changeCells(self):
        if self.direction == "RIGHT":
            new_head = (self.cells[0][0] + self.size, self.cells[0][1])
            self.cells = [new_head] + self.cells
        elif self.direction == "LEFT":
            new_head = (self.cells[0][0] - self.size, self.cells[0][1])
            self.cells = [new_head] + self.cells
        elif self.direction == "DOWN":
            new_head = (self.cells[0][0], self.cells[0][1] + self.size)
            self.cells = [new_head] + self.cells
        elif self.direction == "UP":
            new_head = (self.cells[0][0], self.cells[0][1] - self.size)
            self.cells = [new_head] + self.cells

        if len(self.cells) > self.length:
            self.cells.pop(len(self.cells) - 1)


class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.gameOver = False
        self.gameStart = True

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        if self.snake is not None:
            self.snake.changeCells()
            self.gameOver = self.snake.collision_check()
            if self.snake.canEat(self.snake.cells[0]):
                self.snake.addBlock()

    def events(self):
        for event in pygame.event.get():
            flag = event.type == pygame.KEYUP
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()
            # Movement with WASD
            if keys[pygame.K_SPACE] and (self.gameStart or self.gameOver):
                self.gameStart = False
                self.gameOver = False
                self.snake = snake()
                self.snake.spawnFood()

            if self.snake is not None:
                if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.snake.direction != "DOWN":
                    self.snake.changeDir("UP")
                elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.snake.direction != "UP":
                    self.snake.changeDir("DOWN")
                elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.snake.direction != "RIGHT":
                    self.snake.changeDir("LEFT")
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.snake.direction != "LEFT":
                    self.snake.changeDir("RIGHT")

    def render(self):
        if self.gameStart:
            self.screen.fill((0, 0, 0))
            self.StartScreen()
            pygame.display.flip()
            self.clock.tick(30)
        elif self.gameOver:
            self.screen.fill((0, 0, 0))
            self.gameOverScreen()
            pygame.display.flip()
            self.clock.tick(30)
        else:
            self.screen.fill((0, 0, 0))
            self.drawMenu()
            self.snake.render(self.screen)
            pygame.display.flip()
            self.clock.tick(12)

    def StartScreen(self):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Drawing Text
        self.screen.blit(
            font.render('To start the Game press Space', False, pygame.Color("Yellow"))
            , (400, 300))

    def gameOverScreen(self):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Drawing Text
        self.screen.blit(
            font.render('Game Over, If you wanna retry press SPACE', False, pygame.Color("Yellow"))
            , (250, 300))
        self.screen.blit(
            font.render('Your Score: ' + str(self.snake.score), False, pygame.Color("Yellow"))
            , (250, 350))

    def drawMenu(self):
        pygame.draw.line(self.screen, pygame.Color("white"), [0, 40],
                         [1200, 40], 10)
        pygame.draw.line(self.screen, pygame.Color("white"), [0, 700],
                         [1200, 700], 10)
        pygame.draw.line(self.screen, pygame.Color("white"), [5, 45],
                         [5, 700], 10)
        pygame.draw.line(self.screen, pygame.Color("white"), [1196, 45],
                         [1196, 700], 10)
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        self.screen.blit(font.render("Score: " + str(self.snake.score), True, pygame.Color("Yellow")), (5, 0))

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
