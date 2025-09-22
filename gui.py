import pygame as py
import numpy as np
import math
from utils import utils as ut 
from utils import SpriteManager as spm

class GUI:
    def __init__(self):
        ### MODULES ###
        self.ut = ut()
        self.spm = spm()

        ### VARIABLES ###
        self.win = py.display.get_surface()
        self.screenRes = py.Vector2(self.win.get_size()[0],self.win.get_size()[1])

        self.font = py.font.Font("./assets/fonts/PixelifySans-Regular.ttf",50)
        self.cursor = self.spm.LoadSprite("Cursor-1",SCALE=40)
        self.heart = self.spm.LoadSprite("HP", SCALE = 40)
        self.heartBG = self.ut.swapColor(self.heart, (199,199,199),(23,23,23))
        self.heartBG = py.transform.scale(self.heartBG,(45,45))
        

    #Creates A Pop Up Message For The User at the Top of the Screen
    def Popup(self, alert, time, fadeOut=500, anti = False, color = (202,202,202,255)):
        t = self.ut.Timer(time)

        if(t == 0):
            print ("POP UP ENDED")
            return py.surface.Surface((0,0))
        else:
            text = self.font.render(str(alert),anti,color)
            text.set_alpha(t*fadeOut)
            self.win.blit(text,((self.screenRes.x/2)-(text.get_rect().width/2),10))

            return text

    
    def updateHealthBar(self, hp):
        maxHearts = 6
        padding = 2
        numOfHearts = hp // (100 // maxHearts)
        heartSize = self.heartBG.get_rect().h + padding

        j = 0
        for i in range(maxHearts):
            self.win.blit(self.heartBG, (11 + (i * heartSize),13))
                
            if j <= numOfHearts:
                self.win.blit(self.heart, (15 + (j * heartSize),10))
                j += 1

