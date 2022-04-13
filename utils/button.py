from utils import roundTupleValues

import pygame
from enum import Enum

pygame.init()


class Button:
    """
    Custom Button Class. Kinda shit but it does the job.
    """
    class ButtonStates(Enum):
        Idle = 1
        Hover = 2
        Pressing = 3

    def __init__(self, name = "Button", position = (0, 0), scale = (1, 1), text = "Button", textColor = (0, 0, 0), fontSize = 32,
                normalBackground = (255, 255, 255), onHoverBackground = (220, 230, 235), onPressedBackground = (220, 230, 235), onClicked=None, active=True):

        self.position = (position[0] - int(10*scale[0]/2), position[1] - int(10*scale[1]/2))
        self.scale = scale
        self.name = name
        self.isActive = active
        self.state: Button.ButtonStates = Button.ButtonStates.Idle

        self.buttonRect = pygame.Rect((self.position[0], self.position[1], 10*scale[0], 10*scale[1]))

        self.textColor = textColor
        self.font = pygame.font.Font(None, fontSize)

        self.textPos = (position[0], position[1])
        self.listener = onClicked
        
        #customization
        self.text = text
        self.changeText(self.text)

        self.colors = {
            Button.ButtonStates.Idle: normalBackground,
            Button.ButtonStates.Hover: onHoverBackground,
            Button.ButtonStates.Pressing: onPressedBackground
        }

        
    def alignText(self):
        textW, textH = self.font.size(self.text)
        x = self.position[0]
        y = self.position[1]
        w = self.scale[0] * 10
        h = self.scale[1] * 10

        self.textPos = (x + w/2 - textW/2, y + h/2 - textH/2)

        self.textPos = roundTupleValues(self.textPos)

    def draw(self, surface):
        if not self.isActive: return
        
        pygame.draw.rect(surface, self.colors[self.state], self.buttonRect)
        surface.blit(self.txt_surface, self.textPos)
    
    def handleEvents(self):
        if not self.isActive: return

        try:
            if pygame.mouse.get_pressed()[0]:
                if self.buttonRect.collidepoint(pygame.mouse.get_pos()):
                    self.state = Button.ButtonStates.Pressing

                    if self.listener != None: self.listener(self) # feeds one positional argument, the button object

                else:
                    self.state = Button.ButtonStates.Idle
            elif not pygame.mouse.get_pressed()[0]:
                if self.buttonRect.collidepoint(pygame.mouse.get_pos()):
                    self.state = Button.ButtonStates.Hover
                else:
                    self.state = Button.ButtonStates.Idle
        except AttributeError:
            pass

    def changeText(self, newText: str):
        self.text = newText
        self.alignText()
        self.txt_surface = self.font.render(self.text, True, self.textColor)

    def SetActive(self, activate):
        self.isActive = activate

