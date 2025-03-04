import pygame as py
import numpy as np
import math
from Utils import utils as ut 
from Utils import SpriteManager as spm

class GUI:
    def __init__(self):
        #Prerequisites
        self.ut = ut()
        self.spm = spm()
        self.win = py.display.get_surface()
        self.screenRes = self.win.get_size()
        self.screenRes = py.Vector2(self.screenRes[0],self.screenRes[1])
        self.font = py.font.Font("./assets/fonts/PixelifySans-Regular.ttf",50)

        #Cards + Settings
        self.cards = {"plant":self.spm.LoadSprite("PlantCard2",SCALEBY=5) }
        self.inv = [] #{"type": "plant1", "pos":(0,0)},{"type": "plant2", "pos":(300,0)}
        self.CARD_SIZE = self.cards["plant"].get_rect() 
        self.MAX_CARDS = 5
        self.WAVE_FACTOR = 3

        self.newCard = False
        self.cardPicked = False
        self.selectedCard = None

        #Menu Stuff
        self.dither = self.spm.LoadSprite("DitheringTile2",SCALE=20,KEY=(10,10,10),ALPHA=125)

    def Popup(self, alert, time, fadeOut=500, anti = False, color = (202,202,202,255)):
        t = self.ut.Timer(time)

        if(t == 0):
            print ("POP UP ENDED")
            return py.surface.Surface((0,0))
        else:
            text = self.font.render(str(alert),anti,color)
            text.set_alpha(t*fadeOut)
            self.win.blit(text,((self.screenRes.x/2)-(text.get_rect().width/2),10))

            return text

    def update(self):
        mPos = self.ut.getMousePos()
        mClick = py.mouse.get_pressed(3)

        if self.cardPicked:
            self.cardSelected(self.selectedCard)

        if self.newCard:
            for x in range(40):
                for y in range(40):
                    self.win.blit(self.dither,(x*20,y*20))

        if len(self.inv) > 0:
            self.inv[len(self.inv)-2]["rect"].width = self.CARD_SIZE.width 
            self.inv[-1]["rect"].width = self.CARD_SIZE.width

            tempRect = py.rect.Rect(self.inv[0]["rect"].left,self.inv[0]["rect"].top,
                                    self.CARD_SIZE.w*len(self.inv),self.inv[-1]["rect"].height)
                    
        for x in self.inv:
            if not self.ut.IntersectsBounds(tempRect,mPos):
                if self.cardPicked:
                    if x["id"] != self.selectedCard["id"]:
                        self.win.blit(self.cards[x["type"]],(x["rect"].left,x["rect"].top))
                else:
                    self.win.blit(self.cards[x["type"]],(x["rect"].left,x["rect"].top))
                #py.draw.rect(self.win,"red",tempRect,2)
                    
            else:
                if self.ut.IntersectsBounds(x["rect"],mPos):
                    x["rect"].top = self.screenRes.y - self.CARD_SIZE.height
                    temp = abs((x["id"]-len(self.inv)))
                    
                    if not self.cardPicked:
                        #Wave Effect Left
                        for j in range(len(self.inv)-temp+1):
                            try:
                                tX = self.inv[(x["id"])-j]
                                self.win.blit(self.cards[tX["type"]],(tX["rect"].left,tX["rect"].top-self.CARD_SIZE.height/(self.WAVE_FACTOR*j)))
                            except:
                                pass

                        #Wave Effect Right
                        for j in range(temp):
                            try:
                                tX = self.inv[(x["id"])+j]
                                self.win.blit(self.cards[tX["type"]],(tX["rect"].left,tX["rect"].top-self.CARD_SIZE.height/(self.WAVE_FACTOR*j)))  
                            except:
                                pass
                    else:
                        self.win.blit(self.cards[x["type"]],(x["rect"].left,x["rect"].top))

                    
                    #Clicked & Selected A Card
                    if mClick[0] and not self.cardPicked:
                        self.cardPicked = True
                        self.selectedCard = x
                        self.win.blit(self.cards[self.selectedCard["type"]],(self.selectedCard["rect"].left,self.selectedCard["rect"].top-20))
                    else: 
                        #pass
                        self.win.blit(self.cards[x["type"]],(x["rect"].left,x["rect"].top))
                        #py.draw.rect(self.win,"green",x["rect"],2)
                        
                    x["rect"].top = self.screenRes.y - self.CARD_SIZE.height/2
            

    def addCard(self,card):
        if len(self.inv) < self.MAX_CARDS:
            tPos = py.Vector2((len(self.inv)*self.CARD_SIZE.width), self.screenRes.y-self.CARD_SIZE.height/2)
            tRect = self.cards[str(card)].get_rect()

            tRect.top = tPos.y
            tRect.left = tPos.x + (self.screenRes.x - (self.MAX_CARDS*self.CARD_SIZE.width))/2
           
            temp = {"type": str(card), "rect":tRect,"id":len(self.inv)}#-self.CARD_SIZE.height/2)}
            self.inv.append(temp)
        self.rearrangeCards()
         
    def cardSelected(self,card = None):
        x = card
        self.win.blit(self.cards[card["type"]],(x["rect"].left,x["rect"].top-20))
        py.draw.rect(self.win,"#CACACA",(py.rect.Rect(x["rect"].left,x["rect"].top-20,x["rect"].w,x["rect"].h)),4)          

    def rearrangeCards(self):
        for x in self.inv:
            tPos = py.Vector2((x["id"]*self.CARD_SIZE.width), self.screenRes.y-self.CARD_SIZE.height/2)
            tRect = self.cards["plant"].get_rect()

            tRect.top = tPos.y
            tRect.left = tPos.x + (self.screenRes.x - (len(self.inv)*self.CARD_SIZE.width))/2
            x["rect"] = tRect
        