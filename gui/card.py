from gui.gui import GUI
import pygame as py

class CardManager(GUI):
    def __init__(self):
        super().__init__()

        ### VARIABLES ###
        self.cards = {"sun":self.spm.LoadSprite("PlantCard2",SCALEBY=4.4) }
        self.inv = [] #Format: {"Type": "sun", "Card Object" : OBJ, "ID":0}

        self.CARD_SIZE = self.cards["sun"].get_rect() 
        self.MAX_CARDS = 5
        self.WAVE_FACTOR = 3

        self.newCard = False
        self.cardPicked = False
        self.selectedCard = None
        self.deckBoundingRect = py.rect.Rect(0,0,0,0)

    #Handles Everything; Called Every Frame
    def update(self):
        #Mouse Ins
        mPos = self.ut.getMousePos()
        mClick = py.mouse.get_pressed(3)

        #If There are Cards in INV; create a Rect that Encapsulates Card Deck Area
        if len(self.inv) > 0:
            firstCard = self.inv[0]["Object"].rect
            self.deckBoundingRect = py.rect.Rect(firstCard.left,firstCard.top,
                                    self.CARD_SIZE.w*len(self.inv),  self.CARD_SIZE.h)
   
        for x in self.inv:
            currCardType = x["Type"]
            currCardRect = x["Object"].rect
            currCardPosition = (currCardRect.left,currCardRect.top)

            #If Mouse NOT near the Card Deck; Draw it!
            if not self.ut.IntersectsBounds(self.deckBoundingRect,mPos) or self.cardPicked: 
                self.win.blit(self.cards[currCardType],currCardPosition) 
            else:
                if self.ut.IntersectsBounds(currCardRect,mPos):
                    
                    if not self.cardPicked:
                        temp = abs((x["ID"]-len(self.inv)))
                        #Wave Effect Left
                        for j in range( len(self.inv)-temp+1 ):
                            tempCard = self.inv[(x["ID"])-j]
                            tempCardType = tempCard["Type"]
                            tempCardRect = tempCard["Object"].rect

                            self.win.blit(self.cards[tempCardType],( tempCardRect.left,tempCardRect.top-self.CARD_SIZE.height/(self.WAVE_FACTOR*(j+1)) ))
                            
                        #Wave Effect Right
                        for j in range(temp):
                            tempCard = self.inv[(x["ID"])+j]
                            tempCardType = tempCard["Type"]
                            tempCardRect = tempCard["Object"].rect

                            self.win.blit(self.cards[tempCardType],( tempCardRect.left,tempCardRect.top-self.CARD_SIZE.height/(self.WAVE_FACTOR*(j+1)) ))
                        
                    else:
                        self.win.blit(self.cards[currCardType],currCardPosition)

                    
                    #Clicked & Selected A Card
                    if mClick[0] and not self.cardPicked:
                        self.cardPicked = True
                        self.selectedCard = x
                        self.selectACard(x)
                    
                        
        #If we Have a Card Picked, Highlight It
        if self.cardPicked:
            self.selectACard(self.selectedCard)
        
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
        cardRect = card["Object"].rect

        self.win.blit(selectedSprite,(cardRect.left,cardRect.top-self.CARD_SIZE.height/3))

    #Sets The Position Of Each Card in Deck If Deck Is Altered
    def rearrangeCards(self):
        for x in self.inv:
            tPos = py.Vector2( (x["ID"]*self.CARD_SIZE.w), self.screenRes.y-self.CARD_SIZE.h/2)

            x["Object"].rect.top = tPos.y
            x["Object"].rect.left = tPos.x + (self.screenRes.x - (len(self.inv)*self.CARD_SIZE.width))/2
            
    #Creates A New Card Object 
    def createNewCard(self,cardType,ID):
        newCard = Card(cardType,ID)
        newCard.rect.w = self.CARD_SIZE.w
        newCard.rect.h = self.CARD_SIZE.h

        return newCard


class Card():
    def __init__(self,cardType,ID):
        self.pos = py.Vector2(0,0)
        self.type = cardType
        self.ID = ID
        self.sprite = py.surface.Surface((0,0))
        self.rect = self.sprite.get_rect()
     

    
    