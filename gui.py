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
        self.screenRes = py.Vector2(self.win.get_size()[0],self.win.get_size()[1])

        self.font = py.font.Font("./assets/fonts/PixelifySans-Regular.ttf",50)
        self.cursor = self.spm.LoadSprite("Cursor-1",SCALE=40)

        

    #Creates A Pop Up Message For The User at the Top of the Screen
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

 


class CardManager(GUI):
    def __init__(self):
        super().__init__()

        #Cards + Settings
        self.cards = {"sun":self.spm.LoadSprite("PlantCard2",SCALEBY=5) }
        self.inv = [] #Format: {"Type": "sun", "Card Object" : OBJ, "ID":0}

        self.CARD_SIZE = self.cards["sun"].get_rect() 
        self.MAX_CARDS = 5
        self.WAVE_FACTOR = 3

        self.newCard = False
        self.cardPicked = False
        self.selectedCard = None

   #Function That Handles Everything; Called Every Frame
    def update(self):
        #Mouse Ins
        mPos = self.ut.getMousePos()
        mClick = py.mouse.get_pressed(3)

        #If we Have a Card Picked, Highlight It
        if self.cardPicked:
            self.selectACard(self.selectedCard)

        #If There are Cards in INV; create a Rect that Encapsulates Card Deck Area
        if len(self.inv) > 0:
            firstCard = self.inv[0]["Object"].rect
            deckBoundingRect = py.rect.Rect(firstCard.left,firstCard.top,
                                    self.CARD_SIZE.w*len(self.inv),  self.CARD_SIZE.h)
        
                  
        for x in self.inv:
            currCardType = x["Type"]
            currCardRect = x["Object"].rect
            currCardPosition = (currCardRect.left,currCardRect.top)

            if not self.ut.IntersectsBounds(deckBoundingRect,mPos): #If Mouse NOT near the Card Deck
                self.win.blit(self.cards[currCardType],currCardPosition) #Draw it!
            else:
                if self.ut.IntersectsBounds(currCardRect,mPos):
                    currCardRect.top = self.screenRes.y - self.CARD_SIZE.height
                    temp = abs((x["ID"]-len(self.inv)))
                    
                    if not self.cardPicked:
                        #Wave Effect Left
                        for j in range( len(self.inv)-temp+1 ):
                            try:
                                tX = self.inv[(x["ID"])-j]
                                self.win.blit(self.cards[tX["Type"]],(tX["Sprite"].left,tX["Sprite"].top-self.CARD_SIZE.height/(self.WAVE_FACTOR*j)))
                            except:
                                self.win.blit(self.cards[currCardType],currCardPosition)

                        #Wave Effect Right
                        for j in range(temp):
                            try:
                                tX = self.inv[(x["ID"])+j]
                                self.win.blit(self.cards[tX["Type"]],(tX["Sprite"].left,tX["Sprite"].top-self.CARD_SIZE.height/(self.WAVE_FACTOR*j)))  
                            except:
                                self.win.blit(self.cards[currCardType],currCardPosition)
                    else:
                        self.win.blit(self.cards[currCardType],currCardPosition)

                    
                    #Clicked & Selected A Card
                    if mClick[0] and not self.cardPicked:
                        self.cardPicked = True
                        self.selectedCard = x
                        self.selectACard(x)
                    else: 
                        self.win.blit(self.cards[currCardType],currCardPosition)
                        
                currCardRect.top = self.screenRes.y - self.CARD_SIZE.height/2     

    #Adds A Card to 'inv' list if Possible
    def addCard(self,cardType):
        if len(self.inv) < self.MAX_CARDS:
            newCard = self.createNewCard(cardType,len(self.inv))
            newCard.sprite = self.cards[cardType]
            newCard.pos = py.Vector2( (len(self.inv)*self.CARD_SIZE.width), self.screenRes.y-self.CARD_SIZE.height/2)
            newCard = {"Type" : newCard.type, "Object" : newCard, "ID" : newCard.ID }
            self.inv.append(newCard)

        self.rearrangeCards()

    #Emphezises Selected Card by Rasing and Card    
    def selectACard(self,card = None):
        selectedSprite = self.cards[card["Type"]]
        cardRect = card["Sprite"]

        self.win.blit(selectedSprite,(cardRect.left,cardRect.top-20))
        #py.draw.rect(self.win,"#CACACA",(py.rect.Rect(x["rect"].left,x["rect"].top-20,x["rect"].w,x["rect"].h)),4)          

    #Sets The Position Of Each Card in Deck If Deck Is Altered
    def rearrangeCards(self):
        for x in self.inv:
            tPos = py.Vector2( (x["ID"]*self.CARD_SIZE.w), self.screenRes.y-self.CARD_SIZE.h/2)

            x["Object"].rect.top = tPos.y
            x["Object"].rect.left = tPos.x + (self.screenRes.x - (len(self.inv)*self.CARD_SIZE.width))/2
    
    #Creates A New Card Object 
    def createNewCard(self,cardType,ID):
        return Card(cardType,ID)


class Card():
    def __init__(self,cardType,ID):
        self.pos = py.Vector2(0,0)
        self.type = cardType
        self.ID = ID
        self.sprite = py.surface.Surface((0,0))
        self.rect = self.sprite.get_rect()

    
    