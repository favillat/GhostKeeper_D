import pygame as py
from gui.gui import GUI


class Button(GUI):
    def __init__(self, text,x,y, color, padding=20):
        super().__init__()

        self.gui = GUI()

        #Variables
        self.text = text
        self.x = x
        self.y = y
        self.padding = padding
        self.color = color
        self.drawButton()

    def drawButton(self):
        textSurface = self.gui.font.render(self.text, True, (202,202,202))

        width = textSurface.get_rect().width + self.padding
        height = textSurface.get_rect().height + self.padding
        self.rect = py.Rect(self.x, self.y, width, height)

        py.draw.rect(self.win,self.color,self.rect)
        self.win.blit(textSurface,(self.x + self.padding/2,self.y + self.padding/2 ))

