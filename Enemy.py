import pygame as py
import numpy as np
import math
import random as rand
import Utils as ut 
from Entity import Entity

class EnemyManager():
    def __init__(self):
        pass

    def newEnemy(self,enemyType):
        return Enemy(enemyType)
    
    def pathfind(self, pos):
        dX = pos.x - self.pos.x
        dY = pos.y - self.pos.y
        self.pos 
    

class Enemy(Entity):
    def __init__(self,enemyType = "ghost"):
        super().__init__()

        match(enemyType):
            case "ghost":
                self.sprite = self.spm.LoadSprite("GraveKeepHurtSpritesBooGhost")
                self.sprite = self.sprite.subsurface((0,0,30,32))
                self.health = 100
                self.speed = 0.5

        
            
        self.sprite = py.transform.scale(self.sprite,(200,200))
        self.pos = py.Vector2(rand.randint(100,700),rand.randint(100,600))


