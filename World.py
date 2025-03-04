import pygame as pg
import numpy as np
from Utils import utils as ut
from Utils import SpriteManager as spm

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
        self.plant = self.spm.LoadSprite("Plant")

        self.tiles = []


    def popWorld(self):
        for x in range(self.gridSize):
            temp = []
            for y in range(self.gridSize):
                tilePos = self.ut.MapToScreen(x,y)
                temp.append(tilePos)
            self.tiles.append(temp)