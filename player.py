import pygame as py
import numpy as np
import math
from entitiy import Entity
from gui import GUI


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 1.45
        self.damage = 10
        self.health = 100
        self.pos = py.math.Vector2(300,200)
        #self.sprite = py.surface.Surface((0,0))
        self.facingR = True

        #LOADS ANIMATIONS 
        self.runSS = self.spm.LoadSprite("GraveKeepRunSpritePlayerGrid")
        self.idleSS = self.spm.LoadSprite("GraveKeeperIdleSpritePlayer")
        self.shovelSprite = self.spm.LoadSprite("ShovelLone",SCALE=90,KEY=(255,255,255))
        self.shovelSprite = py.transform.scale(self.shovelSprite,(16,32))
        self.shovelSprite = py.transform.scale_by(self.shovelSprite,3)
        self.shovelSprite = py.transform.rotate(self.shovelSprite,-90)


        super().loadAnimation(self.runSS,"RUN",0.1)
        super().loadAnimation(self.idleSS,"IDLE",0.35)

        self.curSprite = 0
        self.maxSprite = (self.spm.ssDimensions * self.spm.ssDimensions)-1

        self.gui = GUI()
     
    def move(self,keys):    
        up = keys[py.K_w] or keys[py.K_UP]
        down = keys[py.K_s] or keys[py.K_DOWN]
        left = keys[py.K_a] or keys[py.K_LEFT]
        right = keys[py.K_d] or keys[py.K_RIGHT]

        # unit vector of movement? idk if thats the right term - julian
        self.vect = py.math.Vector2(right - left, down - up)
        if self.vect.length_squared() > 0:
            # gives unit vector a magnitude equal to speed variable, should allow for modularity in future updates
            self.vect.scale_to_length(self.speed)
            self.pos += self.vect
            self.facingR = self.vect.x > 0
            # position is now a sum of the new vector
            self.curState = "RUN"
        else:
            self.curState = "IDLE"
    
    def getPos(self):
        return self.pos
    
    def update(self):
        if self.ut.Timer(self.animations[self.curState][1]) == 0:
            if(self.curSprite < self.maxSprite):
                self.sprite = self.animations[self.curState][0][self.curSprite]
                self.curSprite += 1

                if(not self.facingR):
                    self.sprite = py.transform.flip(self.sprite,True,False)
                
                        
            else:
                self.curSprite = 0
                self.sprite = self.animations[self.curState][0][self.curSprite]

                if(not self.facingR):
                    self.sprite = py.transform.flip(self.sprite,True,False)

        self.gui.updateHealthBar(self.health)


    
