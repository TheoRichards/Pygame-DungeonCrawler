import math
from Shop_Gold_Heart import *
"""Name:Create_Starting_Area
    Parameter: xadjustment = integer, yadjustment = integer, Walls = None or pygame.sprite.Group, wall = none or
    wall class, StairCase_Group = None or pygame.sprite.Group, StairCase = None or Staircase, Shops_Group = 
    pygame.sprite.Group or None, Shop_Keeper = Shop_Keeper class or None, Melee_Enemy = Melee_Enemy or None, 
    enemies = pygame.sprite.Group or none
    Return: None
    Purpose: This creates the starting floor where the players will spawn into in"""
def Create_Starting_Area(xadjustment,yadjustment,Walls=None,wall=None,StairCase_Group= None,StairCase=None,Shops_Group=None,
                         Shop_Keeper=None,Melee_Enemy= None,enemies = None):
    if Walls != None:
        Walls.add(wall(300 + xadjustment,(500 + yadjustment),(600,50)))
        Walls.add(wall(250 + xadjustment,(150 + yadjustment),(50,300)))
        Walls.add(wall(250 + xadjustment, (400 + yadjustment), (50, 150)))
        Walls.add(wall(900 + xadjustment,(150 + yadjustment), (50, 150)))
        Walls.add(wall(900 + xadjustment, (400 + yadjustment), (50, 150)))
        Walls.add(wall(250 + xadjustment, (100 + yadjustment), (300, 50)))
        Walls.add(wall(650 + xadjustment,(100 + yadjustment), (300, 50)))
        Walls.add(wall(900 + xadjustment, (250 + yadjustment), (200, 50)))
        Walls.add(wall(900 + xadjustment, (400 + yadjustment), (200, 50)))
        Walls.add(wall(1100 + xadjustment, (200 + yadjustment), (50, 100)))
        Walls.add(wall(1100 + xadjustment, (400 + yadjustment), (50, 100)))
        Walls.add(wall(1100 + xadjustment, (450 + yadjustment), (250, 50)))
        Walls.add(wall(1100 + xadjustment, (200 + yadjustment), (250, 50)))
        Walls.add(wall(1350 + xadjustment, (200 + yadjustment), (50, 300)))
        Walls.add(wall(1100 + xadjustment, (450 + yadjustment), (200, 50)))
        Walls.add(wall(500 + xadjustment, (-50 + yadjustment), (50, 200)))
        Walls.add(wall(650 + xadjustment, (-50 + yadjustment), (50, 200)))
        Walls.add(wall(500 + xadjustment, (-50 + yadjustment), (150, 50)))
        StairCase_Group.add(StairCase(562+xadjustment,0+yadjustment))
        Shop_Sprite = XP_Shop_Keeper(40, 1275 + xadjustment, 325 + yadjustment)
        Shops_Group.add(Shop_Sprite)

"""Name: Playground
    Parameter: xadjustment = integer, yadjustment = integer, Walls = None or pygame.sprite.Group, wall = none or
    wall class, StairCase_Group = None or pygame.sprite.Group, StairCase = None or Staircase, Shops_Group = 
    pygame.sprite.Group or None, Shop_Keeper = Shop_Keeper class or None, Melee_Enemy = Melee_Enemy or None, 
    enemies = pygame.sprite.Group or none, player_1 = None or player_1 class, player_2 = None or player_2 class
    Return: None
    Purpose: This has no affect on the actual program but i used it to quickly generate the maps to see where the walls
    would be placed and where the enemies would spawn"""

def Playground(xadjustment,yadjustment,Walls=None,wall=None,StairCase_Group= None,StairCase=None,Shops_Group=None,
                         Shop_Keeper=None,Melee_Enemy= None,enemies = None,player_1 = None,player_2 = None):
    if player_1.PlayerNumber == "player1":
        player_2.rect.x = player_1.rect.x + 100
        player_2.rect.y = player_1.rect.y
    else:
        player_2.rect.x = player_1.rect.x - 100
        player_2.rect.y = player_1.rect.y
        xadjustment = -100
    Walls.add(wall(-50 + xadjustment, (500 + yadjustment), (1000, 50)))
    Walls.add(wall(-50 + xadjustment, (-450 + yadjustment), (50, 950)))
    Walls.add(wall(0 + xadjustment, (-450 + yadjustment), (1000, 50)))
    Walls.add(wall(950 + xadjustment, (-400 + yadjustment), (50, 950)))
    Shop_Sprite = XP_Shop_Keeper(100, 400 + xadjustment, -100 + yadjustment)
    Shops_Group.add(Shop_Sprite)

"""Name: Create_First_Floor
    Parameter: xadjustment = integer, yadjustment = integer, Walls = None or pygame.sprite.Group, wall = none or
    wall class, StairCase_Group = None or pygame.sprite.Group, StairCase = None or Staircase, Shops_Group = 
    pygame.sprite.Group or None, Shop_Keeper = Shop_Keeper class or None, Melee_Enemy = Melee_Enemy or None, 
    enemies = pygame.sprite.Group or none, player_1 = None or player_1 class, player_2 = None or player_2 class
    Return: None
    Purpose: This creates the first floor and shows where the enemies will spawn"""
def Create_First_Floor(xadjustment,yadjustment,Walls=None,wall=None,player_1= None,player_2= None,
                         enemies=None,Melee_Enemy= None, StairCase_Group = None,StairCase = None):
    if Walls != None:
        if player_1.PlayerNumber == "player1":
            player_2.rect.x = player_1.rect.x + 200
            player_2.rect.y = player_1.rect.y
        else:
            player_2.rect.x = player_1.rect.x - 200
            player_2.rect.y = player_1.rect.y
        Walls.add(wall(300 + xadjustment, (500 + yadjustment), (400, 50)))
        Walls.add(wall(250 + xadjustment, (400 + yadjustment), (50, 150)))
        Walls.add(wall(100 + xadjustment, (350 + yadjustment), (200, 50)))
        Walls.add(wall(50 + xadjustment, (200 + yadjustment), (50, 200)))
        Walls.add(wall(0 + xadjustment, (150 + yadjustment), (100, 50)))
        Walls.add(wall(-50 + xadjustment, (-50 + yadjustment), (50, 250)))
        Walls.add(wall(-50 + xadjustment, (-100 + yadjustment), (350, 50)))
        Walls.add(wall(250 + xadjustment, (-100 + yadjustment), (50, 300)))
        Walls.add(wall(200 + xadjustment, (150 + yadjustment), (50, 50)))
        Walls.add(wall(200 + xadjustment, (200 + yadjustment), (50, 100)))
        Walls.add(wall(250 + xadjustment, (250 + yadjustment), (450, 50)))
        Walls.add(wall(700 + xadjustment, (250 + yadjustment), (50, 300)))
        Enemy = Melee_Enemy((50 + xadjustment), 50, (0, 0, 255), 50,sniper())
        enemies.add(Enemy)
        if player_1.difficulty == "Easy":
            Enemy.add_amplifiers_to_dictionary("Damage","Dungeon1",1.15)
            Enemy.add_amplifiers("Damage")
        if player_1.difficulty == "Medium":
            Enemy.add_amplifiers_to_dictionary("Damage","Dungeon1",1.3)
            Enemy.add_amplifiers("Damage")
        if player_1.difficulty == "Hard":
            Enemy.add_amplifiers_to_dictionary("Damage","Dungeon1",1.5)
            Enemy.add_amplifiers("Damage")
        StairCase_Group.add(StairCase(150 + xadjustment, 0 + yadjustment))

"""Name: Create_Boss_Room
    Parameter:xadjustment = integer, yadjustment = integer, Walls = None or pygame.sprite.Group, wall = none or
    wall class, StairCase_Group = None or pygame.sprite.Group, StairCase = None or Staircase, Shops_Group = 
    pygame.sprite.Group or None, Shop_Keeper = Shop_Keeper class or None, Melee_Enemy = Melee_Enemy or None, 
    enemies = pygame.sprite.Group or none, player_1 = None or player_1 class, player_2 = None or player_2 class
    Return: xadjustment = integer
    Purpose: This creates the room where the boss will spawn"""

def Create_Boss_Room(xadjustment,yadjustment,Walls=None,wall=None,StairCase_Group= None,StairCase=None,Shops_Group=None,
                         Shop_Keeper=None,Melee_Enemy= None,enemies = None,player_1 = None,player_2 = None):
    if player_1.PlayerNumber == "player1":
        player_2.rect.x = player_1.rect.x + 100
        player_2.rect.y = player_1.rect.y
    else:
        player_2.rect.x = player_1.rect.x - 100
        player_2.rect.y = player_1.rect.y
        xadjustment = -100
    Walls.add(wall(-50 + xadjustment, (500 + yadjustment), (1000, 50)))
    Walls.add(wall(-50 + xadjustment, (-450 + yadjustment), (50, 950)))
    Walls.add(wall(0 + xadjustment, (-450 + yadjustment), (1000, 50)))
    Walls.add(wall(950 + xadjustment, (-400 + yadjustment), (50, 950)))
    return xadjustment