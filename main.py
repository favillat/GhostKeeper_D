import pygame as py
import numpy as np
import math
from Utils import utils as utils 
from gui import GUI
from Card import CardManager
import World
import Player
import Enemy

class Game:
    def __init__(self):
        py.init()

        #Window
        self.screenRes = py.Vector2(900,700)
        self.win = py.display.set_mode((self.screenRes))
        py.display.set_caption('Ghost Planter!')

        # Setup
        self.clock = py.time.Clock()
        self.running = True
        self.dt = 0

        # Modules
        self.ut = utils()
        self.gui = GUI()
        self.cardManager = CardManager()
        self.world = World.World()
        self.world.popWorld()
        self.plr = Player.Player()
        self.ghost1 = Enemy.Enemy()
    
        #CAMERA SETTINGS
        self.halfWinH = self.win.get_size()[1]//2
        self.halfWinW = self.win.get_size()[0]//2
        self.camOffset = py.Vector2(self.plr.getPos().x - self.halfWinW,self.plr.getPos().y - self.halfWinH)

        #self.plantedPlants = [] #{"type": ,"pos": }}
        
    def run(self):
        self.worldTiles = self.world.tiles
        self.isMoving = False

        self.newWave = False
        self.text = None

        ## MAIN GAME LOOP ###
        py.mouse.set_visible(False)
        self.angle = 0
        while self.running:
            msPos = (self.ut.getMousePos().x + self.camOffset.x,self.ut.getMousePos().y + self.camOffset.y)
            gridPos = py.Vector2(self.ut.ScreenToMap(*msPos))
            highlighting = False

            ### EVENT POLLING ###
            for event in py.event.get(): 
                if event.type == py.QUIT:
                    self.running = False
                
                if event.type == py.MOUSEBUTTONUP:

                    #Detects Mouse Click; Plants Plant if Available 
                    if self.ut.pointInBounds(gridPosition= gridPos,bound= self.world.gridSize) and not self.ut.IntersectsBounds(self.cardManager.deckBoundingRect,self.ut.getMousePos()): 
                        if self.cardManager.cardPicked:
                            tempPlant = self.world.plantMan.createNewPlant(self.cardManager.selectedCard["Type"])
                            tempPlant.pos = self.ut.MapToScreen(gridPos.x,gridPos.y)
                           
                            self.world.plantMan.plant(tempPlant)
                            
                            self.cardManager.cardPicked = False   


            keys = py.key.get_pressed()
            self.plr.move(keys)
            self.camOffset = py.Vector2(self.plr.getPos().x -self.halfWinW,self.plr.getPos().y - self.halfWinH)

            if keys:
                if keys[py.K_SPACE]:
                    if(self.ut.Timer(.2) == 0):
                        self.cardManager.addCard("sun")
                    
                if keys[py.K_1]:
                    self.newWave = True
                           

            ### CLEAR SCREEN ###
            self.win.fill("#202020")
            self.world.drawBG()

            if(self.cardManager.cardPicked):
                self.gui.Popup((self.cardManager.selectedCard["Type"]).upper(),100)
            
            # Process Tiles
            for x in range(self.world.gridSize):
                for y in range(self.world.gridSize):
                    
                    #Get Selected Grid Tile
                    curTile = py.Vector2(self.worldTiles[x][y].x - self.camOffset.x, self.worldTiles[x][y].y - self.camOffset.y)

                    #If We're Selecting A Valid Tile On The Grid to Highlight
                    if self.ut.pointInBounds(gridPosition = gridPos,bound = self.world.gridSize): 
                        if gridPos.x == x and gridPos.y == y and self.cardManager.cardPicked:
                            curTile.y -= 5
                            highlighting = True
                        else:
                            highlighting = False

                    #Draw Tiles
                    self.win.blit(self.world.tileSprite,curTile)

                    if highlighting:
                        self.win.blit(self.world.tileHSprite,curTile)
                        if self.cardManager.cardPicked:
                            tempPlantOBJ = self.world.plantMan.createNewPlant("sun")
                            tempPlantOBJ.sprite.set_alpha(self.world.plantMan.constructAlpha)

                            tPos = self.ut.MapToScreen(gridPos.x,gridPos.y)
                            tPos = tPos.x-self.camOffset.x,tPos.y-(self.ut.SCALAR-self.ut.SCALAR_QUART)-self.camOffset.y

                            self.win.blit(tempPlantOBJ.sprite,tPos)
                    
            #Render Plants
            self.world.drawPlants(self.camOffset)

            #Draw Player
            self.plr.update()
            self.win.blit(self.plr.sprite,(self.plr.pos.x,self.plr.pos.y)) 

        ## SHOVEL LOGIC: TEMPORARY ##
            msPos = (self.ut.getMousePos().x,self.ut.getMousePos().y)
            self.angle = (-math.atan2((msPos[1]-self.plr.pos.y),(msPos[0]-self.plr.pos.x)))

            radius = 150
            tangent_x = self.plr.pos.x + 80 + radius * math.cos(-self.angle)
            tangent_y = self.plr.pos.y + 40 + radius * math.sin(-self.angle)

            self.plr.shovelSpriteRotated = py.transform.rotate(self.plr.shovelSprite,math.degrees(self.angle))
            self.tempSizeX =  self.plr.shovelSpriteRotated.get_width()
            self.tempSizeY =  self.plr.shovelSpriteRotated.get_height()/2
           ###
            
            if self.newWave:
                self.text = self.gui.Popup("NEW WAVE",3)
                if self.text.get_rect().width == 0:
                    self.newWave = False
    
            self.cardManager.update()

            # Draw
            self.win.blit(self.gui.cursor,(msPos[0] - self.gui.cursor.get_width()/2,msPos[1] - self.gui.cursor.get_height()/2,))

            py.display.flip()

            self.dt = self.clock.tick(120) / 1000 

        py.quit()

Game().run()