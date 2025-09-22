import pygame as py
import numpy as np
import math
import random as rand
import config.utils as ut 
from entity.entitiy import Entity
      
class PlantManager():
    def __init__(self):
        self.plantTypes = []
        self.planted = [] #FORMAT: {"plantType": "sun", "Object":first_Sun_Object}
        self.constructAlpha = 190

    #Creates a New Plant Object    
    def createNewPlant(self,TYPE = "sun"):
        return Plant(TYPE)

    #Places A Plant Object Into the 'Planted' List
    def plant(self,plant):
        self.planted.append( {"plantType" : plant.type, "Object" : plant}) 


class Plant(Entity):
     def __init__(self,TYPE = "sun"):
        super().__init__()
        self.type = TYPE
        self.pos = py.Vector2(0,0)

        match self.type:
            case "sun":
                self.sprite = self.spm.LoadSprite(self.type+"Plant")

