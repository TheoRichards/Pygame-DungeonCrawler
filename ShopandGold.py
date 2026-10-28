import pygame,random
from weaponsforplayer import *

class Gold(pygame.sprite.Sprite):
    def __init__(self,amount,x,y):
        super(Gold, self).__init__()
        self.amount = amount
        self.image = pygame.Surface((10,10))
        self.image.fill((255, 223, 0))
        pygame.draw.rect(self.image, (255, 223, 0), [0, 0, 10,10])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_rid_off_self(self,group):
        group.remove(self)

class boosters():
    def __init__(self,boost_type,name,boost):
        self.name = name
        self.cost = 1
        self.boost = boost
        self.type = boost_type

Health_Boost_Permanence = boosters("health","Health",1.5)
Damage_Boost_Permanence = boosters("damage","Damage",1.2)
XP_Boost_Permanence = boosters("xp_boost","EXP Increase",1.2)
Money_Boost_Permanence = boosters("money_boost","Money Increase",1.5)
dictonary_for_boosts = {"1":Damage_Boost_Permanence,
                        "2":Health_Boost_Permanence,
                        "3":XP_Boost_Permanence,
                        "4":Money_Boost_Permanence}