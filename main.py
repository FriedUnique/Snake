import pygame
from dataclasses import dataclass
from typing import List

import random

from utils import Vector2, SplashText, Text

#region personalisation
@dataclass
class Level:
    name: str
    tickSpeed: int
    appleCount: int

@dataclass
class Colors:
    name: str
    chequered0: tuple
    chequered1: tuple
    appleColor: tuple
    snakeColor: tuple

def inputEval(s: str, d: dict):
    s = s.lower()
    lKeys = list(d.keys())
    if s in lKeys:
        return s

    print(f"Bad input! Using default: {lKeys[0]}")
    return lKeys[0]

# difficulty
levels = {"easy": Level("easy", 7, 3), "hard" : Level("hard", 10, 2), "nigger": Level("nigger", 11, 1)}
LVL = inputEval(input(f"Select difficulty {tuple(levels.keys())}: "), levels)

cellColors = {"green": Colors("green", (170, 215, 81), (155, 200, 73), (156, 50, 50), (17, 24, 47)), "blue": Colors("blue", (93, 216, 228), (84, 194, 205), (233, 163, 49), (17, 24, 47))} # [chequered0], [chequered1], [appleColor], [snakeColor]
THEME = inputEval(input(f"Select theme {tuple(cellColors.keys())}: "), cellColors)


#endregion

# region init
pygame.init()

GRIDSIZE = Vector2(20, 15)      # how many cells are in the grid
CELLSIZE = 30                   # visual grid size
fieldOffset = Vector2(100, 50)  # so the gameField is in the middle

screenX, screenY = (CELLSIZE*GRIDSIZE.x + fieldOffset.x*2, CELLSIZE*GRIDSIZE.y + fieldOffset.y*2)
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

scoreText = Text("scoreText", Vector2(25, 30), (13, 13, 26), text="0", font=pygame.font.Font(None, 42))     # will display the current score
splash = SplashText(screenX, screenY)                                                                       # will pop-up after you died
splash.textColor = (156, 50, 50)
splash.bgColor = cellColors[THEME].chequered1

# directions 
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#endregion

class Snake:
    def __init__(self):
        self.positions = []
        self.snakeLength = 1
        self.dir = RIGHT
        self.color = (17, 24, 47)

        self.moved = True

    def turn(self, targetDir):
        if self.moved == False:
            return

        if self.snakeLength > 1 and (targetDir[0] * -1, targetDir[1] * -1) == self.dir:
            return
        else:
            self.dir = targetDir
            self.moved = False

    def move(self):
        head = self.positions[0]
        newPos = ((head[0] + (self.dir[0]*CELLSIZE)), head[1] + (self.dir[1]*CELLSIZE))

        # test if collided with wall
        if newPos[0] > screenX - CELLSIZE - fieldOffset.x or newPos[0] < fieldOffset.x or newPos[1] > screenY - CELLSIZE - fieldOffset.y or newPos[1] < fieldOffset.y:
            splash.loadInfo(f"You died! Score: {score}", "RESET", self.reset)
            return

        # test if crash into you self
        if len(self.positions) > 2 and newPos in self.positions[2:]:
            splash.loadInfo(f"You died! Score: {score}", "RESET", self.reset)
            return
            

        self.positions.insert(0, newPos) # new head pos
        if len(self.positions) > self.snakeLength:
            self.positions.pop() # default last
        self.moved = True

    def reset(self):
        global scoreText, score
        scoreText.changeText("0")

        for apple in apples:
            apple.random_pos()

        score = 0
        self.snakeLength = 1
        self.positions = [[0 * CELLSIZE + fieldOffset.x, int(GRIDSIZE.x/2) * CELLSIZE + fieldOffset.y]]
        self.dir = RIGHT

    def draw(self):
        for body in self.positions:
            r = pygame.Rect((body[0], body[1]), (CELLSIZE, CELLSIZE))
            pygame.draw.rect(screen, self.color, r)

class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = cellColors[THEME].appleColor
        self.random_pos()
    
    def random_pos(self):
        self.position = ()

        while self.position == () and self.position not in snake.positions:
            self.position = (random.randint(0, GRIDSIZE.x-1) * CELLSIZE + fieldOffset.x, random.randint(0, GRIDSIZE.y-1) * CELLSIZE + fieldOffset.y)

    def draw(self):
        r = pygame.Rect(self.position, (CELLSIZE, CELLSIZE))
        pygame.draw.rect(screen, self.color, r)


def drawGrid():
    for y in range(0, GRIDSIZE.y):
        for x in range(0, GRIDSIZE.x):
            r = pygame.Rect((x*CELLSIZE + fieldOffset.x, y*CELLSIZE + fieldOffset.y), (CELLSIZE, CELLSIZE))

            if (x+y) % 2 == 0:
                pygame.draw.rect(screen, cellColors[THEME].chequered0, r)
            else:
                pygame.draw.rect(screen, cellColors[THEME].chequered1, r)

def draw():
    snake.draw()

    for apple in apples:
        apple.draw()

    scoreText.changeText(str(score))
    scoreText.draw(screen)

score = 0
snake = Snake()
apples: List[Apple] = []
def main():
    global splash, score, snake

    for i in range(levels[LVL].appleCount):
        apples.append(Apple())

    isRunning = True
    snake.reset()

    splash.loadInfo("Start Game", "START")

    while isRunning:

        # switch tickspeed so UI is not slow.
        if splash.toggled:
            clock.tick(20)
        else:
            clock.tick(levels[LVL].tickSpeed)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            #debug
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


        # draw and update
        if not splash.toggled:
            snake.move()

            # check apple collision
            for apple in apples:
                if snake.positions[0] == apple.position:
                    snake.snakeLength += 1
                    score += 1
                    apple.random_pos()
            
            # check won
            if snake.snakeLength == CELLSIZE**2:
                splash.loadInfo("You won!", "RESET", snake.reset)

            screen.fill((255, 255, 255))
            drawGrid()
            draw() # draw the rest (snake, ...)

        splash.update(screen)
        pygame.display.update()

main()