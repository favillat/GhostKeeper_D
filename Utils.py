import pygame as py
import math
import os 
import time as t

SCALAR = 90
SCALAR_HALF = SCALAR/2
SCALAR_QUART = SCALAR/4

class utils:
    def __init__(self):
        self.SCALAR = SCALAR
        self.SCALAR_HALF = SCALAR/2
        self.SCALAR_QUART = SCALAR/4

        self.screenRes = py.display.get_surface().get_size()
        self.screenRes = py.Vector2(self.screenRes[0],self.screenRes[1])

        self.curtime = 0
        #self.clock = py.time.Clock()
        self.t0 = t.time()

        print("TIME STARTED ", self.t0/1000)
        
    #Takes Grid Coordinates and Converts Them to Screen Coordinates
    def MapToScreen(self,x,y):
        screenX = (((x-y)*self.SCALAR_HALF) - self.SCALAR_HALF) + self.screenRes.x/2
        screenY = ((x+y)*self.SCALAR_QUART) +(self.screenRes.y/4)#+np.sin((py.time.get_ticks()/1000)*.5*np.pi)*5    
        return py.Vector2(screenX,screenY)

    #Takes Screen Coordinates and Converts Them to Grid Coordinates
    def ScreenToMap(self,x,y):
        x -= self.screenRes.x/2
        y -= self.screenRes.y/4

        d = (self.SCALAR_HALF*self.SCALAR_QUART)-(-self.SCALAR_HALF*self.SCALAR_QUART)
        mapX = ((x * self.SCALAR_QUART) + (y * self.SCALAR_HALF))//d
        mapY = ((x * -self.SCALAR_QUART) + (y * self.SCALAR_HALF))//d
        return py.Vector2(math.floor(mapX),math.floor(mapY))
    
    #Simple Timer
    def Timer(self, waitTime):
        self.curtime = (t.time()-self.t0)
        timeLeft = ((waitTime-self.curtime))
        #print ("CURRENT TIME: ", str(math.floor(self.curtime)), " TIME LEFT: ", str(math.floor(timeLeft)),"INPUT: ",str(waitTime))
        if(self.curtime > waitTime):
            self.t0 = t.time()
            return 0
            
        return timeLeft
    
    #Returns Current Mouse Position
    def getMousePos(self):
        return py.Vector2(py.mouse.get_pos()[0],py.mouse.get_pos()[1])

    #True or False based on Intersect between Rect and Point
    def IntersectsBounds(self,rect = py.rect.Rect(0,0,0,0), point = py.Vector2(0,0)):
        return rect.collidepoint((point.x,point.y))   
    
    #Returns Distance Between Points
    def GetDistance(self,m1,m2):
        return m2-m1
    
    #True or False If the Point is in or out of Bounds
    def pointInBounds(self,gridPosition = py.Vector2(0,0),bound = 10):
        if(gridPosition.x >= 0 and gridPosition.y >= 0 and 
               gridPosition.x < bound and gridPosition.y < bound):
            return True
        else: return False
    

class SpriteManager:
    def __init__(self):
        self.ut = utils()
        self.ssDimensions = 3
        self.spriteSizes = 30
        self.animations = {} #Format: { Animation Name: [ [Sprite1,Sprite2,Sprite3],Duration] }

    #Loads A Sprite
    def LoadSprite(self,NAME="bg3", SCALE=90,SCALEBY = 0, KEY=(0,0,0), ALPHA=255):
        try:
            self.SCALAR = SCALE
            img = py.image.load("./assets/sprites/"+str(NAME)+'.png').convert()

            if SCALEBY > 0:
                img = py.transform.scale_by(img,SCALEBY)
            else:
                img = py.transform.scale(img,(self.SCALAR,self.SCALAR))
            
            img.set_alpha(ALPHA)
            img.set_colorkey(KEY)

            print(str(NAME)," SPRITE LOADED")
            return img
        except:
            print("FAILED TO LOAD: ",str(NAME)," SPRITE")

    #Loads An Animation From A SS and Saves it Into 'Animations' List W/ Name and Duration
    def loadAnim(self,img,animationName,DURATION,framesInSheet = 9,):
        j = 0
        k = 0

        frames = []
        for i in range(1,framesInSheet):
            tempRect = img.subsurface(py.Rect(j*self.spriteSizes,k*self.spriteSizes,self.spriteSizes,self.spriteSizes))
            tempRect = py.transform.scale_by(tempRect,4)
            frames.append(tempRect)
            k+=1

            if (i == self.ssDimensions or i == self.ssDimensions*2):
                j += 1
                
                k = 0

        self.animations.update( {animationName:[frames, DURATION]} )
        self.frames = []
