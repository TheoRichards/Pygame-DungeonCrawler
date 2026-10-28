import pygame,random,time,math
from permament_variables import Boss_Enemy_ID,Enemy_ID,preview_attack_Group,Boss_attack_Group
"""Name: slime_boss
    Purpose: This summons the boss slime which separates when it dies into smaller version of itself """
class slime_boss(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer,size = tuple,health = integer,xadjustment = integer, yadjustment = integer, time_extender = integer
        Return: None
        Purpose: This sets up the slime_boss object with the necessary information"""
    def __init__(self,x,y,size,health,xadjustment,yadjustment,time_extender):
        super(slime_boss, self).__init__()
        global Boss_Enemy_ID
        self.size = size
        self.image = pygame.Surface((self.size,self.size))
        self.image.fill((124,252,0))
        pygame.draw.rect(self.image, (124, 252, 0), [0, 0, 200, 200])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orignial_health = health
        self.hp = health
        self.damage = 5
        self.Enemy_ID = Boss_Enemy_ID
        Boss_Enemy_ID += 2
        self.__x_adjustment = xadjustment
        self.__y_adjustment = yadjustment
        self.base_Xp = 30
        self.Xp = 30
        self.__rest_time = False
        self.__current_time_rest = 0
        self.__time_elapsed_rest = 0
        self.__last_time_rest = 0
        self.__time_since_last_rest = 0
        self.__time_for_rest = 15
        self.__contact_time = True
        self.__current_time_contact = 0
        self.__time_elapsed_contact = 0
        self.__last_time_contact = 0
        self.__time_since_last_contact = 0
        self.__time_for_contact = time_extender
        self.type = "slime"

    """Name:check_alive
        Parameter: self, Boss_Group = pygame.sprite.Group, Boss_health_bar_Group = pygame.sprite.Group, staircase = staircase Class
        staircase_group = pygame.sprite.Group, player_1 = Character class, players_bar_group = pygame.sprite.Group,
        x_adj_for_slimes = integer, y_adj_for_slimes = integer, xadjustment = integer, yadjustment = integer
        Return: None
        Purpose: This checks to see if the enemies health is less than or equal to 0 and if it is it will check to see
        the size of the enemy and if its larger than a certain number it will spawn 2 more slime enemy but if its 
        less than the certain number it will just destroy"""

    def check_alive(self,Boss_Group,Boss_health_bar_Group,staircase,staircase_group,player_1,players_bar_group,x_adj_for_slimes,y_adj_for_slimes,xadjustment,yadjustment):
        counter = 0
        if self.hp <= 0:
            if round(self.size / 2) > 25:
                for i in range(2):
                    self.where_to_spawn_slimes(player_1,Boss_Group)
            for i in Boss_Group:
                counter += 1
            if counter <= 1 and round(self.size/2) <= 25:
                for i in Boss_health_bar_Group:
                    i.kill()
                staircase_group.add(staircase(500 +xadjustment+x_adj_for_slimes, -100 + yadjustment+y_adj_for_slimes))
                player_1.xp += math.ceil(self.Xp * player_1.xp_boosts_multiplied_together)
                for i in players_bar_group:
                    if i.type == "blue":
                        size_xp_level_up = player_1.get_players_xp_level_up()
                        i.change_size((0, 191, 255), size_xp_level_up, player_1.xp)
                player_1.did_player_level_up()
            self.kill()
        else:
            for i in Boss_health_bar_Group:
                if i.type == "red":
                    i.change_size(self.orignial_health,self.hp)

    """Name: where_to_spawn_slimes
        Parameter: self,player_1 = Character class, Boss_Group = pygame.sprite.Group
        Return: None
        Purpose: This works at where to spawn the next 2 slimes and it will then tell the server so the other player
        can spawn the slimes in the same location."""

    def where_to_spawn_slimes(self,player_1,Boss_Group):
        time_extender = self.__time_for_contact + self.__time_for_contact
        if player_1.PlayerNumber == "player1" and self.Enemy_ID % 2 == 0:
            random_number_x = random.randint(-100,100)
            random_number_y = random.randint(-100,100)
            if self.rect.x + random_number_x <= -50 or self.rect.x + random_number_x >= 1000:
                random_number_x = -random_number_x
            if self.rect.y + random_number_y <= -450 or self.rect.y + random_number_y >= 500:
                random_number_y = -random_number_y
            slime_boss_character = slime_boss(self.rect.x + random_number_x+self.__x_adjustment,self.rect.y + random_number_y+self.__y_adjustment, self.size / 2,round(self.orignial_health / 2), self.__x_adjustment, self.__y_adjustment,time_extender)
            Boss_Group.add(slime_boss_character)
            player_1.tell_server("slime_spawn",info = [self.rect.x + random_number_x,self.rect.y + random_number_y,self.size/2,round(self.orignial_health / 2),self.__x_adjustment,self.__y_adjustment,time_extender])
        if player_1.PlayerNumber == "player2" and self.Enemy_ID % 2 == 1:
            random_number_x = random.randint(-100,100)
            random_number_y = random.randint(-100,100)
            if self.rect.x + random_number_x <= -50 or self.rect.x + random_number_x >= 1000:
                random_number_x = -random_number_x
            if self.rect.y + random_number_y <= -450 or self.rect.y + random_number_y >= 500:
                random_number_y = -random_number_y
            slime_boss_character = slime_boss(self.rect.x + random_number_x+self.__x_adjustment,self.rect.y + random_number_y + self.__y_adjustment, self.size / 2,round(self.orignial_health / 2), self.__x_adjustment, self.__y_adjustment,time_extender)
            Boss_Group.add(slime_boss_character)
            player_1.tell_server("slime_spawn",info=[self.rect.x + random_number_x, self.rect.y + random_number_y, self.size / 2,round(self.orignial_health / 2),self.__x_adjustment,self.__y_adjustment,time_extender])

    """Name: change_x_y_adjustment
        Parameter: self,x = boolean, number = integer
        Return : Nome
        Purpose: This will change the x and y adjustment so the staircase will still spawn in the center of the floor"""

    def change_x_y_adjustment(self,x,number):
        if x:
            self.__x_adjustment += number
        else:
            self.__y_adjustment += number

    """Name: who_does_movement
        Parameter: self, player_1 = Character class, player_2 = Character class
        Return: None
        Purpose: This decides which player will control the boss so that the movement is synchronized"""

    def who_does_movement(self,player_1,player_2):
        if self._rest_time:
            if self.Enemy_ID % 2 == 1 and player_1.PlayerNumber == "player1":
                self.__movement(player_1,player_2)
            if self.Enemy_ID % 2 == 0 and player_1.PlayerNumber != "player1":
                self.__movement(player_1,player_2)

    """Name: movement
        Parameter: self, player_1 = Character class, player_2 = Character class
        Return: None
        Purpose: This decides which player is the closest but if both players are the same distance it will flip a coin
        to see whop to move towards. Theres also a 1 in 5 chance that it wont move that means that the players can move
        faster than the boss"""

    def __movement(self,player_1,player_2):
        distance_from_player_1 = (((self.rect.x - player_1.rect.x) ** 2) + (self.rect.y - player_1.rect.y) ** 2)
        distance_from_player_2 = (((self.rect.x - player_2.rect.x) ** 2) + (self.rect.y - player_2.rect.y) ** 2)
        new_random_number = random.randint(1, 5)
        if new_random_number != 1:
            if distance_from_player_2 > distance_from_player_1:
                self.__move_to_player(player_1,player_1)
            elif distance_from_player_1 > distance_from_player_2:
                self.__move_to_player(player_2,player_1)
            else:
                random_number = random.randint(1, 2)
                if random_number == 1:
                    self.__move_to_player(player_1,player_1)
                else:
                    self.__move_to_player(player_2,player_1)

    """Name: move_to_player
        Parameter: self,player = Character class, player_1 = Character class
        Return: None
        Purpose: If the player is above the enemy in the x axis it will make the boss move in that direction and the 
        opposite way as well. It also does this with the y axis"""

    def __move_to_player(self,player,player_1):
        if self.rect.x > player.rect.x:
            self.rect.x -= 1
            player_1.tell_server("enemy_move",-1,0,"L",self.Enemy_ID)
        elif self.rect.x < player.rect.x:
            self.rect.x += 1
            player_1.tell_server("enemy_move",1,0,"R",self.Enemy_ID)
        if self.rect.y > player.rect.y:
            self.rect.y -= 1
            player_1.tell_server("enemy_move",0,-1,"U",self.Enemy_ID)
        elif self.rect.y < player.rect.y:
            self.rect.y += 1
            player_1.tell_server("enemy_move",0,1,"D",self.Enemy_ID)

    """Name: rest_for_movement
        Parameter: self
        Return: None
        Purpose: This makes it so the enemy will move for certain amount of seconds and then stop for the same amount of
        seconds"""

    def rest_for_movement(self):
        if not self.__rest_time:
            self.__current_time_rest = time.time()
            self.__time_elapsed_rest = self.__current_time_rest - self.__last_time_rest
            self.__last_time_rest = self.__current_time_rest
            if not self.__rest_time:
                self.__time_since_last_rest += self.__time_elapsed_rest
            if self.__time_since_last_rest >= self.__time_for_rest:
                self._rest_time = True
                self._time_since_last_rest = 0
        if self._rest_time:
            self.__current_time_rest = time.time()
            self.__time_elapsed_rest = self.__current_time_rest - self.__last_time_rest
            self.__last_time_rest = self.__current_time_rest
            if self.__rest_time:
                self.__time_since_last_rest += self.__time_elapsed_rest
            if self.__time_since_last_rest >= self.__time_for_rest:
                self.__rest_time = False
                self.__time_since_last_rest = 0

    """Name: stop_contact_damage
        Parameter: self
        Return: None
        Purpose: This makes it so each time the enemy interacts with the player it will only damage the player by 1 
        every second"""

    def stop_contact_damage(self):
        if self.__contact_time:
            self.__current_time_contact = time.time()
            self.__time_elapsed_contact = self.__current_time_contact - self.__last_time_contact
            self.__last_time_contact = self.__current_time_contact
            if self.__contact_time:
                self.__time_since_last_contact += self.__time_elapsed_contact
            if self.__time_since_last_contact >= self.__time_for_contact:
                self.__contact_time = False
                self.__time_since_last_contact = 0

"""Name: slime_boss_spawn
    Parameter:xadjustment = integer,yadjustment = integer,room = integer
    Return: slime_boss_character
    Purpose: It will return the enemy class to the main program"""

def slime_boss_spawn(xadjustment,yadjustment,room):
    slime_boss_character = slime_boss(300+ xadjustment,100+yadjustment,200,50,xadjustment,yadjustment,1)
    return slime_boss_character

"""Name: slime_boss_spawn_from_other_player
    Parameter: Boss_Group = pygame.sprite.Group, data = dictionary, xadjustment = integer, yadjustment = integer, x_adj_for_slime = integer, y_adj_for_slime = integer
    Return: Boss_Group
    Purpose: This creates the slime boss from information from the other player"""

def slime_boss_spawn_from_other_player(Boss_Group,data,xadjustment,yadjustment,x_adj_for_slime,y_adj_for_slime):
    Boss_Group.add(slime_boss(data["Xpos"]+xadjustment+x_adj_for_slime,data["Ypos"]+yadjustment+y_adj_for_slime,data["size"],data["health"],data["xadj"],data["yadj"],data["time_ext"]))
    return Boss_Group

"""Name: ghost_boss
    Purpose: This is a boss that will disappear from one player but will show on another player"""
class ghost_boss(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer,size = tuple,health = integer,xadjustment = integer, yadjustment = integer
        boost = integer
        Return: None
        Purpose: This sets up the ghost_boss object with the necessary information"""
    def __init__(self,x,y,size,health,xadjustment,yadjustment,boost):
        global Enemy_ID
        super(ghost_boss, self).__init__()
        self._size = size
        self.image = pygame.Surface((self._size, self._size))
        self.image.fill((211, 211, 211))
        pygame.draw.rect(self.image, (211, 211, 211), [0, 0, self._size, self._size])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orignial_health = round(health * boost)
        self.hp = round(health * boost)
        self.Enemy_ID = Enemy_ID
        Enemy_ID += 1
        self.base_Xp = 30
        self.Xp = 30
        self.__x_adjustment = xadjustment
        self.__y_adjustment = yadjustment
        self.__rest_time = False
        self.__current_time_rest = 0
        self.__time_elapsed_rest = 0
        self.__last_time_rest = 0
        self.__time_since_last_rest = 0
        self.__time_for_rest = 15
        self.__preview_attack = True
        self.__current_time_preview_attack = 0
        self.__time_elapsed_preview_attack = 0
        self.__last_time_preview_attack = 0
        self.__time_since_last_preview_attack = 0
        self.__time_for_preview_attack = 10
        self.type = "ghost"
        self.location = 5

    """Name:check_alive
        Parameter:self, Boss_Group = pygame.sprite.Group, Boss_health_bar_Group = pygame.sprite.Group, staircase = staircase Class
        staircase_group = pygame.sprite.Group, player_1 = Character class, players_bar_group = pygame.sprite.Group,
        x_adj_for_slimes = integer, y_adj_for_slimes = integer, xadjustment = integer, yadjustment = integer
        Return: None
        Purpose: It will see if the health is less than or equal to 0 and if it is it will remove itself and it will
        also summon the staircase at the center of the room"""

    def check_alive(self,Boss_Group,Boss_health_bar_Group,staircase,staircase_group,player_1,players_bar_group,x_adj_for_slimes,y_adj_for_slimes,xadjustment,yadjustment):
        if self.hp > 0:
            for i in Boss_health_bar_Group:
                if i.type == "red":
                    i.change_size(self.orignial_health,self.hp)
        else:
            for i in Boss_health_bar_Group:
                i.kill()
            staircase_group.add(staircase(500 + self.__x_adjustment, -100 + self.__y_adjustment))
            player_1.xp += math.ceil(self.Xp * player_1.xp_boosts_multiplied_together)
            for i in players_bar_group:
                if i.type == "blue":
                    size_xp_level_up = player_1.get_players_xp_level_up()
                    i.change_size((0, 191, 255), size_xp_level_up, player_1.xp)
            player_1.did_player_level_up()
            self.kill()

    """Name: change_x_y_adjustment
        Parameter: self,x = boolean, number = integer
        Return : Nome
        Purpose: This will change the x and y adjustment so the staircase will still spawn in the center of the floor"""

    def change_x_y_adjustment(self,x,number):
        if x:
            self.__x_adjustment += number
        else:
            self.__y_adjustment += number

    """Name: movement
        Parameter: self,player_1 = Character class
        Return: None
        Purpose: This randomly teleports the boss around the 4 corners of the room and the middle and tells the server
        so that the other player has the same boss location, it also creates the new random number for the next time
        the boss wants to teleport"""

    def movement(self,player_1):
        if self.__rest_time:
            self.__rest_time = False
            player_1.tell_server("move_boss",info = [self.location])
            if self.location == 1:
                self.rect.x = 50 + self.__x_adjustment
                self.rect.y = -300 + self.__y_adjustment
                self.location = random.randint(1,4)
                if self.location == 1:
                    self.location = 5
            elif self.location == 2:
                self.rect.x = 50 + self.__x_adjustment
                self.rect.y = 400 + self.__y_adjustment
                self.location = random.randint(1,4)
                if self.location == 2:
                    self.location = 5
            elif self.location == 3:
                self.rect.x = 800 + self.__x_adjustment
                self.rect.y = -300 + self.__y_adjustment
                self.location = random.randint(1,4)
                if self.location == 3:
                    self.location = 5
            elif self.location == 4:
                self.rect.x = 800 + self.__x_adjustment
                self.rect.y = 400 + self.__y_adjustment
                self.location = random.randint(1,4)
                if self.location == 4:
                    self.location = 5
            elif self.location == 5:
                self.rect.x = 400 + self.__x_adjustment
                self.rect.y = -100 + self.__y_adjustment
                self.location = random.randint(1,4)

    """Name: movement_from_other_player
        Parameter: self,data = dictionary
        Return: None
        Purpose: This gets information from the other player to where to spawn the boss by changing the x and y coordinates
        so it teleports to that location"""

    def movement_from_other_player(self,data):
        if data["Location"] == 1:
            self.rect.x = 50 + self.__x_adjustment
            self.rect.y = -300 + self.__y_adjustment
        elif data["Location"] == 2:
            self.rect.x = 50 + self.__x_adjustment
            self.rect.y = 400 + self.__y_adjustment
        elif data["Location"] == 3:
            self.rect.x = 800 + self.__x_adjustment
            self.rect.y = -300 + self.__y_adjustment
        elif data["Location"] == 4:
            self.rect.x = 800 + self.__x_adjustment
            self.rect.y = 400 + self.__y_adjustment
        elif data["Location"] == 5:
            self.rect.x = 400 + self.__x_adjustment
            self.rect.y = -100 + self.__y_adjustment

    """Name: rest_for_movement
        Parameter: self
        Return: None
        Purpose: This makes a timer so every 15 seconds the boss will teleport around the room"""

    def rest_for_movement(self):
        if not self.__rest_time:
            self.__current_time_rest = time.time()
            self.__time_elapsed_rest = self.__current_time_rest - self.__last_time_rest
            self.__last_time_rest = self.__current_time_rest
            if not self.__rest_time:
                self.__time_since_last_rest += self.__time_elapsed_rest
            if self.__time_since_last_rest >= self.__time_for_rest:
                self.__rest_time = True
                self.__time_since_last_rest = 0

    """Name: spawn_preview_attack_timer
        Parameter: self
        Return: None
        Purpose: This makes it so each time the enemy interacts with the player it will only damage the player by 1 
        every second"""

    def spawn_preview_attack_timer(self):
        if self.__preview_attack:
            self.__current_time_preview_attack = time.time()
            self.__time_elapsed_preview_attack = self.__current_time_preview_attack - self.__last_time_preview_attack
            self.__last_time_preview_attack = self.__current_time_preview_attack
            if self.__preview_attack:
                self.__time_since_last_preview_attack += self.__time_elapsed_preview_attack
            if self.__time_since_last_preview_attack >= self.__time_for_preview_attack:
                self.__preview_attack = False
                self.__time_since_last_preview_attack = 0

    """Name: spawn_preview_attacks
        Parameter: self, location = string
        Return: None
        Purpose: This creates the prewarning to where the attacks is by calling the class preview_attack and it will
        get the string from the parameter to say if it is vertical, horizontal or spots attack"""

    def __spawn_preview_attacks(self,location):
        if location == "horizontal":
            placement_y = random.randint(-400,400)
            preview_attack_Group.add(preview_atack(-650+self.__x_adjustment,placement_y+self.__y_adjustment,[3000,50]))
        elif location == "vertical":
            placement_x = random.randint(0, 900)
            preview_attack_Group.add(
                preview_atack(placement_x + self.__x_adjustment, -1050 + self.__y_adjustment, [50, 3000]))
        elif location == "spots":
            placement_x = random.randint(0, 900)
            placement_y = random.randint(-400, 400)
            preview_attack_Group.add(
                preview_atack(placement_x + self.__x_adjustment, placement_y + self.__y_adjustment, [100, 100]))

    """Name: how_many_attacks_to_load
        Parameter: self
        Return: None
        Purpose: This creates the amount of where the damaging spots are with the less health the boss the more damaging
        places will appear"""

    def how_many_attacks_to_load(self):
        if not self.__preview_attack:
            self.__preview_attack = True
            if self.hp/self.orignial_health >= 0.66:
                for i in range(5):
                    self.__spawn_preview_attacks("spots")
            elif self.hp/self.orignial_health >= 0.33 and self.hp/self.orignial_health < 0.66:
                for i in range(7):
                    self.__spawn_preview_attacks("spots")
                for i in range(3):
                    self.__spawn_preview_attacks("horizontal")
            elif self.hp/self.orignial_health >= 0 and self.hp/self.orignial_health < 0.33:
                for i in range(12):
                    self.__spawn_preview_attacks("spots")
                for i in range(5):
                    self.__spawn_preview_attacks("horizontal")
                    self.__spawn_preview_attacks("vertical")

"""Name: ghost_boss_spawn
    Parameter: xadjusment = integer, yadjustment = integer, room = integer
    Return: ghost_boss_character = ghost_boss
    Purpose: It will return the enemy class to the main program"""
def ghost_boss_spawn(xadjustment,yadjustment,room):
    ghost_boss_character = ghost_boss(400+xadjustment,-100+yadjustment,75,150,xadjustment,yadjustment,1.15**(round(room/2)-1))
    return ghost_boss_character

"""Name: boss_health_bar
    Purpose: This shows the health that the boss has"""
class boss_health_bar(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,Id = intger
        Return: None
        Purpose: This sets up the boss_health_bar object with the necessary information"""
    def __init__(self,Id):
        super(boss_health_bar, self).__init__()
        self.image = pygame.Surface((500,10))
        self.image.fill((255,0,0))
        pygame.draw.rect(self.image,(255,0,0),[0,0,200,50])
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 100
        self.__base_length = 500
        self.__base_height = 10
        self.type = "red"
        self.ID = Id

    """Name: change_size
        Parameter: self,base_stat = integer, new_stat = integer
        Return: None
        Purpose: This changes the size of the healthbar so it is representative of the bosses health"""
    def change_size(self,base_stat,new_stat):
        self.image = pygame.transform.scale(self.image,[self.__base_length * (new_stat / base_stat),self.__base_height])
        pygame.draw.rect(self.image,(255,0,0),[0,0,200,50])

"""Name: boss_border_for_health
    Purpose: This shows the max health that the boss health and it also shows the minium health required to kill it"""
class boss_border_for_health(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,width = integer,height = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the boss_border_for_health object with the necessary information"""
    def __init__(self, width, height, x, y):
        super(boss_border_for_health, self).__init__()
        self.image = pygame.Surface((width, height))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "black"

"""Name: spawn_boss_health_bar
    Parameter: Boss_health_bar_Group = pygame.sprite.Group, ID = integer
    Return: None
    Purpose: It will draw the health bar and the border around the health bar for the enemy"""

def spawn_boss_health_bar(Boss_health_bar_Group,ID):
    boss_health_bar_spawn = boss_health_bar(ID)
    Boss_health_bar_Group.add(boss_health_bar_spawn)
    Boss_health_bar_Group.add(boss_border_for_health(501,1,149,100))
    Boss_health_bar_Group.add(boss_border_for_health(1, 11, 149, 100))
    Boss_health_bar_Group.add(boss_border_for_health(501, 1, 149, 110))
    Boss_health_bar_Group.add(boss_border_for_health(1, 11, 650, 100))

"""Name: boss_group_actions
    Parameter: Boss_Group = pygame.sprite.Group, player_1 = Character class, player_2 = Character class
    Return: None
    Purpose: This makes it so the bosses can perform and do actions which include them moving setting off all the 
    necessary timers so that the attacks and the contact damage actually happen"""

def boss_group_actions(Boss_Group,player_1,player_2):
    for i in Boss_Group:
        if i.type == "slime":
            i.who_does_movement(player_1,player_2)
            i.rest_for_movement()
            i.stop_contact_damage()
        elif i.type == "ghost":
            if i.Enemy_ID % 2 == 1 and player_1.PlayerNumber == "player1":
                i.rest_for_movement()
                i.movement(player_1)
            elif i.Enemy_ID % 2 == 0 and player_1.PlayerNumber != "player1":
                i.rest_for_movement()
                i.movement(player_1)
            i.spawn_preview_attack_timer()
            i.how_many_attacks_to_load()
    for i in preview_attack_Group:
        i.turn_to_attack_timer()
        i.turn_into_attack()
    for i in Boss_attack_Group:
        i.contact_damage()
        i.existance()

"""Name: preview_attack
    Purpose: This shows where the attacking areas will spawn and gives prewarning to the players"""

class preview_atack(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer, y = integer, size = list
        Return: None
        Purpose: This sets up the preview_attack with the necessary information"""
    def __init__(self,x,y,size):
        super(preview_atack, self).__init__()
        self.size = size
        self.image = pygame.Surface((self.size[0], self.size[1]))
        self.image.fill((241, 128, 126))
        pygame.draw.rect(self.image, (241, 128, 126), [0, 0, 200, 200])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__turn_to_attack = True
        self.__current_time_turn_to_attack = 0
        self.__time_elapsed_turn_to_attack = 0
        self.__last_time_turn_to_attack = 0
        self.__time_since_last_turn_to_attack = 0
        self.__time_for_turn_to_attack = 5
        self.__counter = 0

    """Name: turn_to_attack_timer
        Parameter: self
        Return: None
        Purpose: This does a timer so when it reaches the end of timer it will turn the prewarning into an actual
        damaging area"""

    def turn_to_attack_timer(self):
        if self.__turn_to_attack:
            self.__current_time_turn_to_attack = time.time()
            self.__time_elapsed_turn_to_attack = self.__current_time_turn_to_attack - self.__last_time_turn_to_attack
            self.__last_time_turn_to_attack = self.__current_time_turn_to_attack
            if self.__turn_to_attack:
                self.__time_since_last_turn_to_attack += self.__time_elapsed_turn_to_attack
            if self.__time_since_last_turn_to_attack >= self.__time_for_turn_to_attack:
                self.__turn_to_attack = False
                self.__time_since_last_turn_to_attack = 0

    """Name: turn_into_attack
        Parameter: self
        Return: Nome
        Purpose: This calls the boss attack class so that the prewarning turns into an actual attack it will the delete
        itself."""

    def turn_into_attack(self):
        if not self.__turn_to_attack:
            self.__counter += 1
            self.__turn_to_attack = True
            if self.__counter >= 2:
                Boss_attack_Group.add(Boss_attack(self.rect.x,self.rect.y,self.size))
                self.kill()

"""Name: Boss_attack
    Purpose: This creates damaging zones for the boss fight """
class Boss_attack(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer, y = integer, size = list
        Return: None
        Purpose: This sets up the Boss_attack object with the necessary information"""
    def __init__(self,x,y,size):
        super(Boss_attack, self).__init__()
        self.size = size
        self.image = pygame.Surface((self.size[0], self.size[1]))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (255, 0, 0), [0, 0, 200, 200])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 1
        self.contact_time = True
        self._current_time_contact = 0
        self._time_elapsed_contact = 0
        self._last_time_contact = 0
        self._time_since_last_contact = 0
        self._time_for_contact = 1
        self.existance_time = True
        self._current_time_existance = 0
        self._time_elapsed_existance = 0
        self._last_time_existance = 0
        self._time_since_existance = 0
        self._time_for_existance = 5
        self.counter = 0

    """Name: contact_damage
        Parameter: self
        Return: None
        Purpose: this does a timer so every second it will damage the player if they are in the damaging zone"""

    def contact_damage(self):
        if self.contact_time:
            self._current_time_contact = time.time()
            self._time_elapsed_contact = self._current_time_contact - self._last_time_contact
            self._last_time_contact = self._current_time_contact
            if self.contact_time:
                self._time_since_last_contact += self._time_elapsed_contact
            if self._time_since_last_contact >= self._time_for_contact:
                self.contact_time = False
                self._time_since_last_contact = 0

    """Name: existance
        Parameter: self
        Return: None
        Purpose: This sets a timer so after 5 seconds it will use the kill command and get rid of itself"""

    def existance(self):
        if self.existance_time:
            self._current_time_existance = time.time()
            self._time_elapsed_existance = self._current_time_existance - self._last_time_existance
            self._last_time_existance = self._current_time_existance
            if self.existance_time:
                self._time_since_existance += self._time_elapsed_existance
            if self._time_since_existance >= self._time_for_existance:
                self.existance_time = False
                self._time_since_existance = 0
        if not self.existance_time:
            self.existance_time = True
            self.counter += 1
        if self.counter >= 2:
            self.kill()