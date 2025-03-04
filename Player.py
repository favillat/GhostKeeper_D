import pygame as py
import numpy as np
import math
from Entitiy import Entity


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 1.1
        self.damage = 10
        self.health = 100
        self.pos = py.math.Vector2(300,200)
        self.sprite = py.surface.Surface((0,0))
        self.facingR = True
        self.changeDir = False

        print("NEW PLAYER CREATED")

        self.runSS = self.spm.LoadSprite("GraveKeepRunSpritePlayerGrid")
        self.idleSS = self.spm.LoadSprite("GraveKeeperIdleSpritePlayer")
        self.shovelSprite = self.spm.LoadSprite("ShovelLone",SCALE=90,KEY=(255,255,255))
        self.shovelSprite = py.transform.scale(self.shovelSprite,(56,32))
        self.shovelSprite = py.transform.scale_by(self.shovelSprite,3)
        self.shovelSprite = py.transform.rotate(self.shovelSprite,-90)


        super().loadAnimation(self.runSS,"RUN",0.1)
        super().loadAnimation(self.idleSS,"IDLE",0.35)

        self.curSprite = 0;
        self.maxSprite = (self.spm.ssDimensions * self.spm.ssDimensions)-1

        

    def move(self,keys):
              
        if keys:
            
            if keys[py.K_w]:
                self.curState = self.states[1]
                self.pos.y -= self.speed 
            elif keys[py.K_s]:
                self.curState = self.states[1]

                self.pos.y += self.speed
            elif keys[py.K_a]:
                self.pos.x -= self.speed 
                self.curState = self.states[1]

                if(self.facingR):
                    self.facingR = False
               
            elif keys[py.K_d]:
                self.curState = self.states[1]

                self.pos.x += self.speed 

                if(not self.facingR):
                    self.facingR = True
            else:
                self.curState = self.states[0]
        #print("CURRENT FRAME: ",self.sprite)
    
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


    
