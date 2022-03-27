from time import sleep
import pygame
import random
from math import ceil, floor

from utils import Vector2, SplashText, Text

pygame.init()

GRIDSIZE = 10  # how many cells are in the grid
CELLSIZE = 30    # visual grid size

screenX, screenY = (CELLSIZE*GRIDSIZE, CELLSIZE*GRIDSIZE)
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

scoreText = Text("scoreText", Vector2(25, 30), (13, 13, 26), text="0", font=pygame.font.Font(None, 42))
splash = SplashText(screenX, screenY)
splash.textColor = (156, 50, 50)

THEME = "blue"
cellColors = {"blue": [(93, 216, 228), (84, 194, 205), (233, 163, 49)], "green": [(170, 215, 81), (155, 200, 73), (156, 50, 50)]} #(108, 156, 50), (184, 80, 70, )

splash.bgColor = cellColors[THEME][1]

# directions 
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [[0 * CELLSIZE, int(GRIDSIZE/2) * CELLSIZE]]
        self.snakeLength = 1
        #self.dir = random.choice([UP, DOWN, LEFT, RIGHT])
        self.dir = RIGHT
        self.color = (17, 24, 47)

        self.moved = True

    def head_pos(self):
        return self.positions[0]

    def turn(self, targetDir):
        if self.moved == False:
            return

        if self.snakeLength > 1 and (targetDir[0] * -1, targetDir[1] * -1) == self.dir:
            return
        else:
            self.dir = targetDir
            self.moved = False

    def move(self):
        head = self.head_pos()
        #newPos = (((head[0] + (x*GRIDSIZE)) % screenX), (head[1] + (y*GRIDSIZE)) % screenY) # % screen so you can move indefinitly
        newPos = ((head[0] + (self.dir[0]*CELLSIZE)), head[1] + (self.dir[1]*CELLSIZE))

        # test if collided with wall
        if newPos[0] > screenX - CELLSIZE or newPos[0] < 0 or newPos[1] > screenY - CELLSIZE or newPos[1] < 0:
            splash.loadInfo("You died!", "RESET", self.reset)
            return

        # test if crash into you self
        if len(self.positions) > 2 and newPos in self.positions[2:]:
            splash.loadInfo("You died!", "RESET", self.reset)
            return
            

        self.positions.insert(0, newPos)
        if len(self.positions) > self.snakeLength:
            self.positions.pop() # default last
        self.moved = True

    def reset(self):
        global scoreText, score
        scoreText.changeText("0")

        sleep(0.2)
        score = 0
        self.snakeLength = 1
        self.positions = [[2 * CELLSIZE, int(GRIDSIZE/2) * CELLSIZE]]
        self.dir = RIGHT

    def draw(self):
        for body in self.positions:
            r = pygame.Rect((body[0], body[1]), (CELLSIZE, CELLSIZE))
            pygame.draw.rect(screen, self.color, r)


class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = cellColors[THEME][2]
        self.random_pos()
    
    def random_pos(self):
        self.position = (random.randint(0, GRIDSIZE-1) * CELLSIZE, random.randint(0, GRIDSIZE-1) * CELLSIZE)

    def draw(self):
        r = pygame.Rect(self.position, (CELLSIZE, CELLSIZE))
        pygame.draw.rect(screen, self.color, r)


def drawGrid(surface):
    for y in range(0, GRIDSIZE):
        for x in range(0, GRIDSIZE):
            r = pygame.Rect((x*CELLSIZE, y*CELLSIZE), (CELLSIZE, CELLSIZE))
            pygame.draw.rect(surface, cellColors[THEME][1], r)

score = 0
snake = Snake()
def main():
    global splash, score, snake

    apple = Apple()

    isRunning = True
    snake.reset()

    while isRunning:
        if splash.toggled:
            clock.tick(30)
        else:
            clock.tick(8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    snake.snakeLength += 1
                    score += 1

                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)

                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        if not splash.toggled:
            snake.move()

        screen.fill((255, 255, 255))
        drawGrid(screen)
        
        # check food
        if snake.head_pos() == apple.position:
            snake.snakeLength += 1
            score += 1
            scoreText.changeText(str(score))
            apple.random_pos()
        
        # check won
        if snake.snakeLength == CELLSIZE**2:
            splash.loadInfo("You won!", "RESET", snake.reset)

        snake.draw()
        apple.draw()

        scoreText.draw(screen)

        splash.update(screen)
        pygame.display.update()

main()

