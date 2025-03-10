import pygame as pg
import numpy as np
from Utils import utils as ut
from Utils import SpriteManager as spm
from Plant import PlantManager

class World:
    def __init__(self):
        ## Variables ##
        self.gridSize = 10
        self.spm = spm()
        self.ut = ut()

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