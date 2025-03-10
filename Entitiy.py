from Utils import SpriteManager
from Utils import utils
import pygame as py

class Entity:
    def __init__(self):
        self.spm = SpriteManager()
        self.ut = utils()
        self.health = 100
        self.damage = 10
        self.speed =  20
        self.pos = py.Vector2(0,0)
        self.states = ["IDLE","RUN","ATTACK"]
        self.curState = self.states[0];
        self.sprite = py.surface.Surface((0,0))


        self.animations = 0

        
    def takeDamage(self,damage):
        self.health -= damage

    def heal(self,healAmount):
        self.health += healAmount
        
    def loadAnimation(self,img,name,DURRATION = 0.1):
        self.spm.loadAnim(img,name,DURRATION)
        self.animations = self.spm.animations

        
