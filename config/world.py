import pygame as py
import numpy as np
from config.utils import utils as ut
from config.utils import SpriteManager as spm
from entity.plant import PlantManager

class World:
    def __init__(self):
        ## Variables ##
        self.gridSize = 12
        self.spm = spm()
        self.ut = ut()
        self.win = py.display.get_surface()

        ## Sprites ##
        self.tileSprite = self.spm.LoadSprite("IsoFarmTile7")
        self.bg = self.spm.LoadSprite("bg3")
        self.tileHSprite = self.spm.LoadSprite("IsoFarmTileH")
        self.plantMan = PlantManager()
        
        self.tiles = []
        self.plantedPlants = self.plantMan.planted

    #Returns List Of Current Plants On Map, Along With Position and Sprite
    def getPlanted(self):
        self.plantedPlants = self.plantMan.planted
        return self.plantedPlants
    
    #Simple Map Generation; A Symmetric Grid is Created
    def popWorld(self):
        
        for x in range(self.gridSize):
            temp = []
            for y in range(self.gridSize):
                tilePos = self.ut.MapToScreen(x,y)
                temp.append(tilePos)
            self.tiles.append(temp)

    #Draws Background Grid
    def drawBG(self):
         for x in range(10):
                for y in range(10):            
                    self.win.blit(self.bg,(x*self.ut.SCALAR,y*self.ut.SCALAR))

    #Draws Planted Plants
    def drawPlants(self,camOffset = py.Vector2(0,0)):
        for x in range(len(self.plantedPlants)):
                    tempPlant = self.plantedPlants[x]
                    tempSprite = tempPlant["Object"].sprite
                    tempPos = tempPlant["Object"].pos
                    tempPos = (tempPos.x-camOffset.x,tempPos.y-camOffset.y-(self.ut.SCALAR-self.ut.SCALAR_QUART))
                    self.win.blit(tempSprite,tempPos)


  
        
