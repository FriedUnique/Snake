from utils import Button

import pygame
pygame.init()

class Text:
    """
    Displays the text when the 'draw(surface)' method is called.
    """
    def __init__(self, position = (0, 0), color = (255, 255, 255), font = pygame.font.Font(None, 32), text = "", active=True):
        self.text = text
        self.color = color
        self.font = font
        self.position = position

        self.isActive = active

        self.txt_surface = font.render(self.text, True, self.color) #change
        self.rect = self.txt_surface.get_rect(center=(self.position[0], self.position[1]))

    def draw(self, surface):
        if not self.isActive: return

        surface.blit(self.txt_surface, self.rect) #blit a image
    
    def changeText(self, newText: str):
        self.text = newText
        self.txt_surface = self.font.render(self.text, True, self.color) #change
        self.rect = self.txt_surface.get_rect(center=(self.position[0], self.position[1]))
    
    def SetActive(self, activate):
        self.isActive = activate


class SplashText:
    def __init__(self, sWidth, sHeight):
        self.sDim = (sWidth, sHeight)
        w, h = int(sWidth/2), int(sHeight/2)

        self.bgColor = (0, 0, 0)
        self.textColor = (255, 0, 0)

        self.text = Text((w, h), color=self.textColor, active=False, font=pygame.font.Font(None, 40))
        self.closeButton = Button("okButton", (w, sHeight-50), (15, 6), text="MENU", onClicked=self.accept, active=False)

        self.isToggled = False
        self.acceptFunction = None

    def update(self, _screen):
        if(self.isToggled):
            pygame.draw.rect(_screen, self.bgColor, (0, 0, self.sDim[0], self.sDim[1]))

            self.text.draw(_screen)
            self.closeButton.draw(_screen)
            self.closeButton.handleEvents()

    def accept(self, _b):
        # close popup 
        if self.acceptFunction != None: self.acceptFunction()

        self.text.SetActive(False)
        self.closeButton.SetActive(False)
        
        self.isToggled = False

    def loadInfo(self, msg: str, bText: str, f = None):
        self.text.color = self.textColor

        if f != None: self.acceptFunction = f

        self.closeButton.changeText(bText)
        self.closeButton.SetActive(True)

        self.text.changeText(msg)
        self.text.SetActive(True)
        self.isToggled = True

