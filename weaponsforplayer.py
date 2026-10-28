import pygame
import random
""" Name: spear
    Purpose: This allows the user to fire a weapon that has a longer bullet """
class spear():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the spear object with the necessary information"""
    def __init__(self):
        self.type = "spear"
        self.attack = 3
        self.original_damage = 3
        self.range = 75
        self.width = 20
        self.height = 50
        self.time = 0.1
        self.enemy_time = 1
        self.speed = 2
        self.cost = 7
        self.amplified_damage = 3
        self.number = "4"

""" Name: dagger
    Purpose: This allows the user to fire a weapon that has a smaller bullet"""
class dagger():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the dagger object with the necessary information"""
    def __init__(self):
        self.type = "dagger"
        self.attack = 5
        self.original_damage = 5
        self.range = 50
        self.width = 20
        self.height = 15
        self.time = 0.1
        self.enemy_time = 1
        self.speed = 2
        self.cost = 8
        self.amplified_damage = 5
        self.number = "5"

""" Name: longsword
    Purpose: This allows the user to fire a weapon that has the same size bullet as a sword but takes a longer cooldown"""
class longsword():
    """Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the longersword object with the necessary information"""
    def __init__(self):
        self.type = "longsword"
        self.attack = 7
        self.original_damage = 7
        self.range = 50
        self.width = 40
        self.height = 30
        self.time = 0.75
        self.enemy_time = 1.25
        self.speed = 2
        self.cost = 11
        self.amplified_damage = 7
        self.number = "6"

""" Name: sniper
    Purpose: This allows the user to fire a weapon that has a smaller bullet"""
class sniper():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the sniper object with the necessary information"""
    def __init__(self):
        self.type = "sniper"
        self.attack = 5
        self.original_damage = 5
        self.range = 200
        self.width = 10
        self.height = 10
        self.time = 2
        self.enemy_time = 2
        self.speed = 5
        self.cost = 5
        self.amplified_damage = 5
        self.number = "1"

""" Name: minigun
    Purpose: This allows the user to fire a weapon that has a even smaller bullet"""
class minigun():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the minigun object with the necessary information"""
    def __init__(self):
        self.type = "minigun"
        self.attack = 2
        self.original_damage = 2
        self.range = 100
        self.width = 3
        self.height = 3
        self.time = 0.05
        self.enemy_time = 1.5
        self.speed = 2
        self.cost = 5
        self.amplified_damage = 2
        self.number = "2"

""" Name: sword
    Purpose: This allows the user to fire a weapon that has a larger bullet"""
class sword():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the sword object with the necessary information"""
    def __init__(self):
        self.type = "sword"
        self.attack = 1
        self.original_damage = 1
        self.range = 50
        self.width = 40
        self.height = 30
        self.time = 0.1
        self.enemy_time = 1
        self.speed = 2
        self.cost = 4
        self.amplified_damage = 1
        self.number = "3"

dictonary_for_weapon = {"1":sniper(),
                        "2":minigun(),
                        "3":sword(),
                        "4":spear(),
                        "5":dagger(),
                        "6":longsword()}

""" Name: mega_fireball
    Purpose: This allows the user to use the special ability that has a very large bullet"""
class mega_fireball():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the mega_fireball object with the necessary information"""
    def __init__(self):
        self.type = "megafireball"
        self.attack = 20
        self.range = 150
        self.width = 50
        self.height = 50
        self.time = 5
        self.speed = 1

    """ Name: special_ability
        Parameters: self,player_1 = Character class,Bullet = Bullet class,player_shots = pygame.sprite.Group,player_2 = Character class
        Returns: None
        Purpose: This creates the bullet for the fireball and then it will send the information over the sever to tell
        the other player to shoot the fireball"""

    def special_ability(self,player_1,Bullet,player_shots,player_2):
        Bullet_Sprite = Bullet(player_1.rect.x, player_1.rect.y, player_1.direction, player_1.Special_Ability.width,
                               player_1.Special_Ability.height
                               , player_1.Special_Ability.range, player_1.Special_Ability.speed, "player1",
                               player_1.Special_Ability.attack)
        player_shots.add(Bullet_Sprite)
        player_1.tell_server("special", 0, 0, Bullet_Sprite.direction)
        player_1.set_regen_health()

""" Name: dash
    Purpose: This allows the user to use a special ability that has allows the player to dash"""
class dash():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the dash object with the necessary information"""
    def __init__(self):
        self.type = "dash"
        self.time = 0.5
        self.range = 45

    """ Name: special_ability
        Parameters: self,player_1 = Character class,Bullet = Bullet class,player_shots = pygame.sprite.Group,player_2 = Character class
        Returns: None
        Purpose: This sees the direction that the player is facing and then calls the function to dash that way"""

    def special_ability(self,player_1,Bullet,player_shots,player_2):
        if player_1.direction == "R":
            player_1.move_right(self.range, "Dash")
        elif player_1.direction == "L":
            player_1.move_left(self.range, "Dash")
        elif player_1.direction == "U":
            player_1.move_up(self.range, "Dash")
        elif player_1.direction == "D":
            player_1.move_down(self.range, "Dash")

class healing_aura():
    """ Name: __init__
        Parameter: self
        Return: None
        Purpose: This sets up the healing_aura object with the necessary information"""
    def __init__(self):
        self.type = "healing_aura"
        self.time = 10
        self.range = 15000

    """ Name: special_ability
        Parameter: self,player_1 = Character class,Bullet = Bullet class,player_shots = pygame.sprite.Group,player_2 = Character class
        Return: None
        Purpose: This activates a special ability which checks to see if the player is at a certain and if they are it will
        heal them"""
    def special_ability(self,player_1,Bullet,player_shots, player_2):
        range_between_players_x = ((player_1.rect.x + (player_1.width/2)) - (player_2.rect.x + player_2.width/2))**2
        range_between_players_y = ((player_1.rect.y + (player_1.width/2)) - (player_2.rect.y + player_2.width/2))**2
        total_range_between_players = range_between_players_x + range_between_players_y
        if total_range_between_players < self.range:
            player_2.heal_through_aura(True)

