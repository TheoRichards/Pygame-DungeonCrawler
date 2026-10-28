import pygame,random
from weaponsforplayer import *

"""Name: Gold
    Purpose: It allows the player to pick up the gold and it will add the players gold currency"""
class Gold(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,amount = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the Gold object with the necessary information"""
    def __init__(self,amount,x,y):
        super(Gold, self).__init__()
        self.amount = amount
        self.image = pygame.Surface((10,10))
        self.image.fill((255, 223, 0))
        pygame.draw.rect(self.image, (255, 223, 0), [0, 0, 10,10])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """Name:remove_self
            Parameter: self,group = pygame.sprite.Group
            Return: None
            Purpose: It removes itself from the group
            """

    def remove_self(self,group):
        group.remove(self)

"""Name: Hearts
    Purpose: This allows the player to pick the hearts and heal the player"""
class Hearts(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,amount = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the Hearts object with the necessary information"""
    def __init__(self,amount,x,y):
        super(Hearts, self).__init__()
        self.amount = amount
        self.image = pygame.Surface((15,15))
        self.image.fill((255,0,0))
        pygame.draw.rect(self.image, (255, 0, 0), [0, 0, 15, 15])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """Name:remove_self
            Parameter: self,group
            Return: None
            Purpose: It removes itself from the group
            """

    def remove_self(self,group):
        group.remove(self)

"""Name: Shop_Keeper
    Purpose: It allows the player to set buy weapons with money."""
class Shop_Keeper(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,width = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the Shop_Keeper object with the necessary information"""
    def __init__(self,width,x,y):
        super(Shop_Keeper, self).__init__()
        self.type_of_shopkeeper = "Normal"
        self.option1 = dictonary_for_weapon[str(random.randint(1,6))]
        self.option2 = dictonary_for_weapon[str(random.randint(1,6))]
        while self.option2 == self.option1:
            self.option2 = dictonary_for_weapon[str(random.randint(1, 6))]
        self.option3 = dictonary_for_weapon[str(random.randint(1,6))]
        while self.option3 == self.option1 or self.option3 == self.option2:
            self.option3 = dictonary_for_weapon[str(random.randint(1, 6))]
        self.centrex = x + round(width/2)
        self.centrey = y + round(width/2)
        self.amplifers = {"Cost":{}}
        self.width = width
        self.image = pygame.Surface((self.width, self.width))
        self.image.fill((156, 156, 156))
        pygame.draw.rect(self.image, (156, 156, 156), [0, 0, self.width, self.width])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """Name:remove_self
        Parameter: self,group = pygame.sprite.Group
        Return: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

"""Name: XP_Shop_Keeper
    Purpose: It allows the player to buy stuff with Xp to get boosts"""
class XP_Shop_Keeper(Shop_Keeper):
    """Name: __init__
        Parameter: self,width = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the XP_Shop_Keeper object with the necessary information and sends some of the information
        to the parent class Shop_Keeper"""
    def __init__(self,width,x,y):
        super(XP_Shop_Keeper, self).__init__(width,x,y)
        self.type_of_shopkeeper = "XP"
        self.option1 = dictonary_for_boosts[str(random.randint(1, 4))]
        self.option2 = dictonary_for_boosts[str(random.randint(1, 4))]
        while self.option2 == self.option1:
            self.option2 = dictonary_for_boosts[str(random.randint(1, 4))]
        self.option3 = dictonary_for_boosts[str(random.randint(1, 4))]
        while self.option3 == self.option1 or self.option3 == self.option2:
            self.option3 = dictonary_for_boosts[str(random.randint(1, 4))]

"""Name: boosters
    Purpose: It sets the boosts the player can buy from the xp shop """
class boosters():
    """Name: __init__
        Parameter: self,boost_type = string,name = string,boost = float
        Return: None
        Purpose: This sets up the boosters object with the necessary information"""
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