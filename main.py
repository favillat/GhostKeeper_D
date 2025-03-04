import pygame as py
import numpy as np
import math
from Utils import utils as utils 
import gui
import World
import Player

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

        # Sprites
        
        self.ut = utils()
        self.gui = gui.GUI()
        self.world = World.World()
        self.world.popWorld()
        self.plr = Player.Player()
        #self.spm = spm()
    
        #CAMERA SETTINGS
        
        self.halfWinH = self.win.get_size()[1]//2
        self.halfWinW = self.win.get_size()[0]//2
        self.offset = py.Vector2(self.plr.getPos().x - self.halfWinW,self.plr.getPos().y - self.halfWinH)

        self.plantedPlants = [] #{"type": ,"pos": }}
        self.constructAlpha = 190

        
    def run(self):
        self.worldTiles = self.world.tiles
        self.isMoving = False

        self.newWave = False
        self.text = None

        #Game Loop
        self.angle = 0
        while self.running:
            msPos = (self.ut.getMousePos().x + self.offset.x,self.ut.getMousePos().y + self.offset.y)
            gridPos = py.Vector2(self.ut.ScreenToMap(*msPos))
            highlighting = False

            # Event Polling
            for event in py.event.get(): 
                if event.type == py.QUIT:
                    self.running = False
                
                if event.type == py.MOUSEBUTTONUP:
                    if gridPos.x >= 0 and gridPos.y >= 0 and gridPos.x < self.world.gridSize and gridPos.y < self.world.gridSize: 
                        if self.gui.cardPicked:
                            t = self.world.plant
                            
                            tPos = self.ut.MapToScreen(gridPos.x,gridPos.y)
                            
                            self.plantedPlants.append({"img": t, "pos": (tPos.x,tPos.y-(self.ut.SCALAR-self.ut.SCALAR_QUART))})
                            print("PLACED",self.gui.selectedCard["type"], "AT: ",gridPos)
                            self.gui.cardPicked = False   
                                    
            keys = py.key.get_pressed()
            self.plr.move(keys)
            self.offset = py.Vector2(self.plr.getPos().x -self.halfWinW,self.plr.getPos().y - self.halfWinH)

            if keys:
                

                if keys[py.K_SPACE]:
                    if(self.ut.Timer(.2) == 0):
                        self.gui.addCard("plant")
                    
                if keys[py.K_1]:
                    self.newWave = True
                           

            # Clear
            self.win.fill("#202020")

            #Draw Background
            for x in range(10):
                for y in range(10):            
                    self.win.blit(self.world.bg,(x*self.ut.SCALAR,y*self.ut.SCALAR))
            
           
            # Process Tiles
            for x in range(self.world.gridSize):
                for y in range(self.world.gridSize):
                    
                    #Get Selected Grid Tile
                    curTile = py.Vector2(self.worldTiles[x][y].x - self.offset.x, self.worldTiles[x][y].y - self.offset.y)

                    #If We're Selecting A Valid Tile On The Grid
                    if gridPos.x >= 0 and gridPos.y >= 0 and gridPos.x < self.world.gridSize and gridPos.y < self.world.gridSize:      
                        if gridPos.x == x and gridPos.y == y and self.gui.cardPicked:
                            curTile.y -= 5
                            highlighting = True
                        else:
                            highlighting = False

                    #Draw Tiles
                    self.win.blit(self.world.tileSprite,curTile)

                    if highlighting:
                        self.win.blit(self.world.tileHSprite,curTile)
                        if self.gui.cardPicked:
                            t = self.world.plant.copy()
                            t.set_alpha(self.constructAlpha)
                            tPos = self.ut.MapToScreen(gridPos.x,gridPos.y)
                            self.win.blit(t,(tPos.x-self.offset.x,tPos.y-(self.ut.SCALAR-self.ut.SCALAR_QUART)-self.offset.y))

            #Render Plants
            for x in range(len(self.plantedPlants)):
                    self.win.blit(self.plantedPlants[x]["img"],self.plantedPlants[x]["pos"]-self.offset)


            #Draw Player
            self.plr.update()
            #py.draw.circle(self.win,(200,200,200,200),(self.plr.getPos().x+100,self.plr.getPos().y+100),100)
            self.win.blit(self.plr.sprite,(self.plr.pos.x,self.plr.pos.y)) 

            msPos = (self.ut.getMousePos().x,self.ut.getMousePos().y)
            self.angle = (-math.atan2((msPos[1]-self.plr.pos.y),(msPos[0]-self.plr.pos.x)))
            print(self.angle )

            radius = 100
            tangent_x = self.plr.pos.x + 100 + radius * math.cos(-self.angle)
            tangent_y = self.plr.pos.y+ 100 + radius * math.sin(-self.angle)

            self.plr.shovelSpriteRotated = py.transform.rotate(self.plr.shovelSprite,math.degrees(self.angle))
            self.tempSizeX =  self.plr.shovelSpriteRotated.get_width()/2
            self.tempSizeY =  self.plr.shovelSpriteRotated.get_height()/2

           
            self.win.blit(self.plr.shovelSpriteRotated,(tangent_x-self.tempSizeX,tangent_y-self.tempSizeY)) 
            
            
            if self.newWave:
                self.text = self.gui.Popup("NEW WAVE",3)
                if self.text.get_rect().width == 0:
                    self.newWave = False
    
            self.gui.update()

            # Draw
            py.display.flip()

            self.dt = self.clock.tick(120) / 1000 

        py.quit()

Game().run()