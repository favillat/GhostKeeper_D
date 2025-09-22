import pygame as py
from gui.gui import GUI


class Button():
    def __init__(self, text, x, y, width, height, color, event):
        super().__init__()

        self.gui = GUI()

        #Variables
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.event = event
        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        self.drawButton()

    def drawButton(self):
        py.draw.rect(self.win,self.color,self.rect)
        textSurface = self.gui.font.render(self.text, True, (202,202,202))
        self.win.blit(self.font,((self.screenRes.x/2)-(self.font.get_rect().width/2),300))

