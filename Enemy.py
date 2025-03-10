import pygame as py
import numpy as np
import math
import random as rand
import Utils as ut 
from Entitiy import Entity

class Enemy(Entity):
    def __init__(self):
        super().__init__()

        self.sprite = self.spm.LoadSprite("GraveKeepHurtSpritesBooGhost")
        self.sprite = self.sprite.subsurface(0,0,30,32)
        self.sprite = py.transform.scale(self.sprite,(200,200))

        self.pos = py.Vector2(rand.randint(100,700),rand.randint(100,600))


