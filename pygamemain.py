import pygame,time,threading,random,socket,json,math
from weaponsforplayer import *
from permament_variables import *
from Shop_Gold_Heart import Gold,Shop_Keeper,Hearts
from starting_room import Create_Starting_Area,Create_First_Floor,Playground,Create_Boss_Room
from boss_spawns import *
from procedural_generation import spawn_spawning_room
pygame.init()
screen = pygame.display.set_mode((camerax,cameray))
pygame.display.set_caption("My Game")
WAIT = True

"""Name: setup_players
    Parameters: data = dictionary ,network_connection = socket.socket
    Returns: None
    Purpose:It sets up the player by adding the coordinates that they spawn and what size they are it will also
    add the adjustment which will be used to move the enemies and walls into the right place it will also set up the
    health bar and xp bar"""

def setup_players(data,network_connection):
    global player_1
    global player_2
    global xadjustment
    global yadjustment
    if data["Player"] == 1:
        player_1 = Ranged_Character(data["PlayerX"], data["PlayerY"],(42,55,110),"player1",network_connection)
        player_2 = Melee_Character(data["EnemyX"], data["EnemyY"], (105, 25, 36),"player2")
        xadjustment = 0
        yadjustment = 0
    elif data["PlayerType"] == "Melee":
        player_1 = Melee_Character(data["PlayerX"], data["PlayerY"], (105, 25, 36),"player2",network_connection)
        player_2 = Ranged_Character(data["EnemyX"], data["EnemyY"],(42,55,110),"player1")
        xadjustment = -200
        yadjustment = 0
    characters.add(player_1)
    characters.add(player_2)
    players_bar_group.add(player_bar((255,0,0),50,700,(200,50),"red",50,200))
    players_bar_group.add(border_for_health(2,52,49,699))
    players_bar_group.add(border_for_health(202, 2, 49, 699))
    players_bar_group.add(border_for_health(2, 52, 249, 699))
    players_bar_group.add(border_for_health(202, 2, 49, 749))
    players_bar_group.add(player_bar((0,191,255),75,755,(1,10),"blue",10,150))

"""Name: move_player_2
    Parameters: data = dictionary
    Returns: None
    Purpose: It will move the second player from the data that is given from the server
    """

def move_player_2(data):
    player_2 = characters.sprites()[1]
    player_2.rect.x = player_2.rect.x + data["Xpos"]
    player_2.rect.y = player_2.rect.y + data["Ypos"]

"""Name: fire_player_2
    Parameters: data = dictionary
    Returns: None
    Purpose: It will add second players bullet to the first players screen from data from the server
    """

def fire_player_2(data):
    Bullet_Sprite = Bullet(player_2.rect.x, player_2.rect.y, data["Direction"], player_2.weapon.width, player_2.weapon.height
                           ,player_2.weapon.range,player_2.weapon.speed,"player2",player_2.weapon.attack)
    player_shots.add(Bullet_Sprite)

"""Name: special_player_2
    Parameters: data = dictionary
    Returns: None
    Purpose: This allows the second players special ability to activate on the first players from data from the server
    """

def special_player_2(data):
    Bullet_Sprite = Bullet(player_2.rect.x, player_2.rect.y, data["Direction"], player_2.Special_Ability.width,
                           player_2.Special_Ability.height, player_2.Special_Ability.range,player_2.Special_Ability.speed,"player2",player_2.Special_Ability.attack)
    player_shots.add(Bullet_Sprite)

"""Name: Enemy_Shoot_Shoot
    Parameters: data = dictionary
    Returns: None
    Purpose: This allows the synchronization of the enemy shooting from data from the server
    """

def Enemy_Shoot_Shoot(data):
    if enemies:
        for i in enemies:
            if i.Enemy_ID == data["EnemyID"]:
                EB = Bullet(i.rect.x, i.rect.y, i.direction, i.weapon.width, i.weapon.height, i.weapon.range, i.weapon.speed, None, i.weapon.amplified_damage)
                enemy_shots.add(EB)

"""Name: Enemy_Move_Move
    Parameters: data = dictionary
    Returns: None
    Purpose: This allows the synchronization of the enemy moving from data from the server
    """

def Enemy_Move_Move(data):
    for e in enemies:
        if e.Enemy_ID == data["EnemyID"]:
            e.rect.x += data["Xpos"]
            e.rect.y += data["Ypos"]
            e.direction = data["Direction"]
    for e in Boss_Group:
        if e.Enemy_ID == data["EnemyID"]:
            e.rect.x += data["Xpos"]
            e.rect.y += data["Ypos"]
            e.direction = data["Direction"]

"""Name: Make_Room_Room
    Parameter: data = dictionary
    Return: None
    Purpose: This adds the information from the server to a group to form the walls
    """

def Make_Room_Room(data):
    global Spare_Walls_Group
    Spare_Walls_Group.add(wall(data["DictionaryForPGX"]-100, (data["DictionaryForPGY"] + yadjustment), (data["DictionaryForPGL"], data["DictionaryForPGW"])))

""" Name: Make_Enemies_Enemies
    Parameter: data = dictionary
    Return: None
    Purpose: This adds the information from the server to a group to create the enemies inside the procedurally generated
    rooms"""

def Make_Enemies_Enemies(data):
    weapon_procedural = minigun()
    if data["Weapon"] == "sniper":
        weapon_procedural = sniper()
    elif data["Weapon"] == "sword":
        weapon_procedural = sword()
    Spare_Enemies_Group.add(Melee_Enemy(data["Xpos"]-100,data["Ypos"]+yadjustment,(0, 0, 255),25,weapon_procedural))

""" Name: Make_Inside_Room
    Parameter:data = dictionary
    Return = Nome
    Purpose: This adds the information from the server to a group to create the shops and staircase inside the procedurally
    generated rooms"""

def Make_Inside_Room(data):
    if data["Type"] == "shop":
        Spare_Shop_Group.add(Shop_Keeper(50, data["Xpos"] -100, data["Ypos"] + yadjustment))
    elif data["Type"] == "staircase":
        Spare_StairCase_Group.add(StairCase(data["Xpos"] -100, data["Ypos"] + yadjustment))

""" Name: Specific_Aura
    Parameter: data = dictionary
    Return: None
    Purpose: This calls the right function for whatever aura type ability the other player has"""

def Specific_Aura(data):
    if data["Type"] == "heal":
        player_1.heal_through_aura(False)

"""Name: Defeat_Enemy
    Parameter: data = dictionary
    Return: None
    Purpose: This means that if an enemy dies on the other players screen they will both die. This means that
    there is no weird desynchronisation"""

def Defeat_Enemy(data):
    for i in enemies:
        if i.Enemy_ID == data["Type"]:
            i.hp = -1
            time.sleep(0.02)
            i.check_alive(enemies,player_1)

"""Name: recv_from_client
    Parameters: client = socket.socket
    Returns:None
    Purpose:This allows the players to receive information from the server which can then be converted to information
    """

def recv_from_client(client):
    global WAIT,You_Died,Room_Generated,room,x_adjustment_for_slimes,y_adjustment_for_slimes
    while True:
        data = client.recv(1024)
        if not data:
            continue
        else:
            instruction = data.decode()
            command_list = instruction.split("#")
            for command in command_list:
                if command != '':
                    command_dct = json.loads(command)
                    if command_dct["Command"] == "SETUP":
                        setup_players(command_dct["Data"],client)
                        WAIT = False
                    elif command_dct["Command"] == "MOVE":
                        move_player_2(command_dct["Data"])
                    elif command_dct["Command"] == "FIRE":
                        fire_player_2(command_dct["Data"])
                    elif command_dct["Command"] == "SPECIAL":
                        special_player_2(command_dct["Data"])
                    elif command_dct["Command"] == "CHANGE":
                        player_2.weapon = dictonary_for_weapon[command_dct["Data"]["Weapon"]]
                    elif command_dct["Command"] == "ENEMY_SHOOT":
                        Enemy_Shoot_Shoot(command_dct["Data"])
                    elif command_dct["Command"] == "ENEMY_MOVE":
                        Enemy_Move_Move(command_dct["Data"])
                    elif command_dct["Command"] == "PLAYER_DIED":
                        room = 0
                        Room_Generated = False
                        You_Died = True
                    elif command_dct["Command"] == "MAKE_ROOMS":
                        Make_Room_Room(command_dct["Data"])
                    elif command_dct["Command"] == "CHANGE_DIFFICULTY":
                        player_2.difficulty = command_dct["Data"]["Difficulty"]
                    elif command_dct["Command"] == "CREATE_ENEMIES":
                        Make_Enemies_Enemies(command_dct["Data"])
                    elif command_dct["Command"] == "CREATE_INSIDE":
                        Make_Inside_Room(command_dct["Data"])
                    elif command_dct["Command"] == "AURA":
                        Specific_Aura(command_dct["Data"])
                    elif command_dct["Command"] == "NEW_DAMAGE":
                        player_2.weapon.attack = command_dct["Data"]["Type"]
                    elif command_dct["Command"] == "ENEMY_DEFEATED":
                        Defeat_Enemy(command_dct["Data"])
                    elif command_dct["Command"] == "SLIME_SPAWN":
                        slime_boss_spawn_from_other_player(Boss_Group,command_dct["Data"],xadjust,yadjustment,x_adjustment_for_slimes,y_adjustment_for_slimes)
                    elif command_dct["Command"] == "MOVE_BOSS":
                        for i in Boss_Group:
                            i.movement_from_other_player(command_dct["Data"])
                    else:
                        print(command_dct)

"""Name: waiting
    Parameters: None
    Returns: None
    Purpose: This just puts text on the screen to allow the player to know that they are waiting for the other player
    to join the server"""

def waiting():
    while WAIT:
        screen.fill((255,255,255))
        myFont = pygame.font.SysFont("Arial",50)
        f = myFont.render("Waiting for other player",True,(0,0,0))
        screen.blit(f,(250,400))
        pygame.display.flip()

"""Name: connect_to_server
    Parameters: None
    Returns: None
    Purpose: This allows the player to connect to the server"""

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDRESS, PORT))
    threading.Thread(target=recv_from_client, args=(s,)).start()
    waiting()

"""Name: binary_search_algorithm
    Parameters: array = array,number_that_needs_to_be_found = integer,adjustment_for_walls = integer
    Returns: "found" = string,"not found" = string
    Purpose: This searches through an array to find the specific number but it also can adjust for the movement of player
    so that the binary search is not out of sync."""

def binary_search_algorithm(array,number_that_needs_to_be_found,adjustment_for_walls = 0):
    array.sort()
    top_number = len(array) - 1
    bottom_number = 0
    while bottom_number <= top_number:
        mid_point = (bottom_number + top_number) // 2
        if array[mid_point] + adjustment_for_walls < number_that_needs_to_be_found:
            bottom_number = mid_point+1
        elif array[mid_point] + adjustment_for_walls > number_that_needs_to_be_found:
            top_number = mid_point - 1
        else:
            return "found"
    return "not found"

"""Name: wall
    Purpose: This creates a wall so that the players and enemies can not walk past it. It is the principle of each
    floor"""
class wall(pygame.sprite.Sprite):
    """Name: __init__
    Parameter: self,x = integer,y = integer,size = tuple
    Return: None
    Purpose: This sets up the wall object with the necessary information"""
    def __init__(self,x,y,size):
        super().__init__()
        self.image = pygame.Surface((size))
        self.__size = size
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image,(0,0,0),(0,0,size[0],size[1]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x1 = self.rect.x
        self.x2 = self.rect.x + size[0]
        self.y1 = self.rect.y
        self.y2 = self.rect.y + size[1]

    """Name: update_init
        Parameters: self
        Returns: None
        Purpose: This updates the coordinates so that when the player interacts it will actually interact with the 
        wall rather than an invisible wall."""

    def update_init(self):
        self.x1 = self.rect.x
        self.x2 = self.rect.x + self.__size[0]
        self.y1 = self.rect.y
        self.y2 = self.rect.y + self.__size[1]

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns:None
        Purpose: It removes itself from the group"""

    def remove_self(self,group):
        group.remove(self)

"""Name: movement
    Parameters: x = string,number = integer
    Returns: None
    Purpose: It moves everything everytime the player moves to give the illusion that the player is actually moving"""

def movement(x,number):
    global x_adjustment_for_walls,y_adjustment_for_walls,x_adjustment_for_slimes,y_adjustment_for_slimes
    if x == "x":
        characters.sprites()[1].rect.x += number
        x_adjustment_for_walls += number
        for i in Walls:
            i.rect.x += number
            i.update_init()
        for i in enemies:
            i.rect.x += number
            i.xadjustment += number
        for i in player_shots:
            i.rect.x += number
            if player_1.direction == "L" and i.direction == "L":
                i.set_bullet_range(-number)
            if player_1.direction == "R" and i.direction == "R":
                i.set_bullet_range(number)
            if player_1.direction == "R" and i.direction == "L":
                i.set_bullet_range(-number)
            if player_1.direction == "L" and i.direction == "R":
                i.set_bullet_range(number)
        for i in Dropped_Golds:
            i.rect.x += number
        for i in Dropped_Hearts:
            i.rect.x += number
        for i in Shops_Group:
            i.rect.x += number
            i.centrex += number
        for i in StairCase_Group:
            i.rect.x += number
        for i in enemy_shots:
            i.rect.x += number
            i.set_bullet_range(number)
        counter = 0
        for i in Boss_Group:
            counter += 1
            i.rect.x += number
            i.change_x_y_adjustment(True, number)
            if counter == 1:
                x_adjustment_for_slimes += number
        for i in preview_attack_Group:
            i.rect.x += number
        for i in Boss_attack_Group:
            i.rect.x += number
    if x == "y":
        characters.sprites()[1].rect.y += number
        y_adjustment_for_walls += number
        for i in Walls:
            i.rect.y += number
            i.update_init()
        for i in enemies:
            i.rect.y += number
            i.yadjustment += number
        for i in player_shots:
            i.rect.y += number
            if player_1.direction == "U" and i.direction == "U":
                i.set_bullet_range(-number)
            if player_1.direction == "D" and i.direction == "D":
                i.set_bullet_range(number)
            if player_1.direction == "D" and i.direction == "U":
                i.set_bullet_range(-number)
            if player_1.direction == "U" and i.direction == "D":
                i.set_bullet_range(number)
        for i in Dropped_Golds:
            i.rect.y += number
        for i in Dropped_Hearts:
            i.rect.y += number
        for i in Shops_Group:
            i.rect.y += number
            i.centrey += number
        for i in StairCase_Group:
            i.rect.y += number
        for i in enemy_shots:
            i.rect.y += number
        counter = 0
        for i in Boss_Group:
            i.rect.y += number
            counter += 1
            i.change_x_y_adjustment(False,number)
            if counter == 1:
                y_adjustment_for_slimes += number
        for i in preview_attack_Group:
            i.rect.y += number
        for i in Boss_attack_Group:
            i.rect.y += number
"""Name: Character
    Purpose: This is the bases of the character and it allows the player to interact with game and move around"""
class Character(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,playerno = string,colour = tuple
        Return: None
        Purpose: This sets up the Character object with the necessary information"""
    def __init__(self,playerno,colour):
        super().__init__()
        self.direction = "R"
        self.wallet = 0
        self.xp = 0
        self._level = 1
        self._xp_needed_for_level_up = 100
        self._level_points = 1
        self.boosts = {"damage":{},"health":{},"xp_boost":{},"money_boost":{}}
        self.xp_boosts_multiplied_together = 1
        self.money_boosts_multiplied_together = 1
        self.difficulty = "Medium"
        self.PlayerNumber = playerno
        self._colour = colour
        self.image = pygame.Surface((CHAR_WIDTH, CHAR_WIDTH))
        self.width = CHAR_WIDTH
        self.image.fill((colour))
        pygame.draw.rect(self.image, (colour), [0, 0, CHAR_WIDTH, CHAR_WIDTH])
        self.rect = self.image.get_rect()
        self._time_since_dmg_or_shot = 0
        self._time_for_the_regen = 30
        self._regenerate_health = False
        self._current_time_regen = 0
        self._last_time_regen = 0
        self._time_for_health_regen = 2.5
        self._time_elapsed_health = 0
        self._last_time_health = 0
        self._actual_regenerate_health = False
        self._time_since_last_heal = 0

    """Name: tell_server
        Parameters: self,command = string,x = integer,y = integer,direction = string,info = string
        Returns: None
        Purpose: It tells the server all the information needed to be able to send to the other play to allow for
        synchronization."""

    def tell_server(self,command,x=0,y=0,direction=None,info=None):
        if self.connection != None:
            if command == "move":
                msg = {"Command":"MOVE","Data":{"Xpos": x,"Ypos":y}}
            elif command == "shoot":
                msg = {"Command":"FIRE","Data":{"Direction": direction}}
            elif command == "special":
                msg = {"Command":"SPECIAL","Data":{"Direction":direction}}
            elif command == "change":
                msg = {"Command":"CHANGE","Data":{"Weapon":info}}
            elif command == "enemy_shoot":
                msg = {"Command":"ENEMY_SHOOT","Data":{"EnemyID":info}}
            elif command == "enemy_move":
                msg = {"Command":"ENEMY_MOVE","Data":{"Xpos":x, "Ypos":y,"EnemyID":info,"Direction":direction}}
            elif command == "player_died":
                msg = {"Command":"PLAYER_DIED","Data":{"Player":"Dead"}}
            elif command == "make_rooms":
                msg = {"Command":"MAKE_ROOMS","Data":{"DictionaryForPGX":info[0],"DictionaryForPGY":info[1],
                                                      "DictionaryForPGL":info[2],"DictionaryForPGW":info[3]}}
            elif command == "change_difficulty":
                msg = {"Command":"CHANGE_DIFFICULTY","Data":{"Difficulty":info}}
            elif command == "create_enemies":
                msg = {"Command":"CREATE_ENEMIES", "Data":{"Xpos":x,"Ypos":y, "EnemyID":info[0],"Weapon":info[1]}}
            elif command == "create_inside":
                msg = {"Command":"CREATE_INSIDE", "Data":{"Xpos":x,"Ypos":y,"Type":info[0]}}
            elif command == "aura":
                msg = {"Command":"AURA", "Data":{"Type":info[0]}}
            elif command == "new_damage":
                msg = {"Command":"NEW_DAMAGE", "Data": {"Type":info[0]}}
            elif command == "enemy_defeated":
                msg = {"Command":"ENEMY_DEFEATED","Data":{"Type":info}}
            elif command == "slime_spawn":
                msg = {"Command":"SLIME_SPAWN","Data":{"Xpos":info[0],"Ypos":info[1],"size":info[2],"health":info[3],"xadj":info[4],"yadj":info[5],"time_ext":info[6]}}
            elif command == "move_boss":
                msg = {"Command":"MOVE_BOSS","Data":{"Location":info[0]}}
            self.connection.send((json.dumps(msg)+"#").encode())

    """Name: move_right
        Parameters: self,distance_moved = integer,dash = string or None
        Returns: None
        Purpose: it allows the player to move right and tells the server to send the information that the player moved
        to the other player. It also allows if the player has the special ability to dash to dash moving the player
        about the dash amount. It also checks to see if the movement would make the player go into a wall if it does
        it will put the player back to where they were.
        """

    def move_right(self,distance_moved,dash=None):
        original_rect_x = self.rect.x
        self.direction = "R"
        if self.connection != None:
            movement("x",-distance_moved)
        self.tell_server("move",distance_moved)
        if self.rect.x > S_WIDTH - CHAR_WIDTH:
           self.rect.x = S_WIDTH - CHAR_WIDTH
        for check in Walls:
            if self.rect.x > check.x1 - CHAR_WIDTH and self.rect.x < check.x2 \
                    and (self.rect.y > check.y1 - CHAR_WIDTH and self.rect.y < check.y2) :
                movement("x", distance_moved)
                if dash == "Dash":
                    self.rect.x = original_rect_x
                else:
                    self.rect.x = check.x1 - CHAR_WIDTH
                self.tell_server("move",-distance_moved)

    """Name: move_left
        Parameters: self,distance_moved = integer,dash = string or None
        Returns: None
        Purpose: it allows the player to move left and tells the server to send the information that the player moved
        to the other player. It also allows if the player has the special ability to dash to dash moving the player
        about the dash amount. It also checks to see if the movement would make the player go into a wall if it does
        it will put the player back to where they were.
        """

    def move_left(self,distance_moved,dash=None):
        original_rect_x = self.rect.x
        self.direction = "L"
        if self.connection != None:
            movement("x",distance_moved)
        self.tell_server("move",-distance_moved)
        if self.rect.x < 0:
            self.rect.x = 0
        for check in Walls:
            if self.rect.x < check.x2 and self.rect.x > check.x1 \
                    and (self.rect.y > check.y1 - CHAR_WIDTH and self.rect.y < check.y2):
                movement("x", -distance_moved)
                if dash == "Dash":
                    self.rect.x = original_rect_x
                else:
                    self.rect.x = check.x2
                self.tell_server("move",distance_moved)

    """Name: move_down
        Parameters: self,distance_moved = integer,dash = string or None
        Returns: None
        Purpose: it allows the player to move down and tells the server to send the information that the player moved
        to the other player. It also allows if the player has the special ability to dash to dash moving the player
        about the dash amount. It also checks to see if the movement would make the player go into a wall if it does
        it will put the player back to where they were.
        """

    def move_down(self,distance_moved,dash=None):
        original_rect_y = self.rect.y
        self.direction = "D"
        if self.connection != None:
            movement("y",-distance_moved)
        self.tell_server("move",0,distance_moved)
        if self.rect.y > S_HEIGHT - CHAR_WIDTH:
            self.rect.y = S_HEIGHT - CHAR_WIDTH
        for check in Walls:
            if self.rect.y > check.y1 - CHAR_WIDTH and self.rect.y < check.y2 \
                    and (self.rect.x > check.x1 - CHAR_WIDTH and self.rect.x < check.x2):
                movement("y", distance_moved)
                if dash == "Dash":
                    self.rect.y = original_rect_y
                else:
                    self.rect.y = check.y1 - CHAR_WIDTH
                self.tell_server("move",0, -distance_moved)

    """ Name: move_up
        Parameters: self,distance_moved = integer,dash = string or None
        Returns: None
        Purpose: it allows the player to move up and tells the server to send the information that the player moved
        to the other player. It also allows if the player has the special ability to dash to dash moving the player
        about the dash amount. It also checks to see if the movement would make the player go into a wall if it does
        it will put the player back to where they were.
        """

    def move_up(self,distance_moved,dash=None):
        original_rect_y = self.rect.y
        self.direction = "U"
        if self.connection != None:
            movement("y",distance_moved)
        self.tell_server("move",0, -distance_moved)
        if self.rect.y < 0:
            self.rect.y = 0
        for check in Walls:
            if self.rect.y < check.y2 and self.rect.y > check.y1 \
                    and (self.rect.x > check.x1 - CHAR_WIDTH and self.rect.x < check.x2):
                movement("y", -distance_moved)
                if dash == "Dash":
                    self.rect.y = original_rect_y
                else:
                    self.rect.y = check.y2
                self.tell_server("move",0, distance_moved)

    """Name: check_alive
        Parameters: self,s_group= pygame.sprite.Group
        Returns: True = boolean
        Purpose: It checks to see if the player has died if the player has died it will return True but if the player
        hasnt died it will reduce the healthbar to show the new health
        """

    def check_alive(self,s_group):
        if self.connection != None:
            self._regenerate_health = False
            if self.hp <= 0:
                self.tell_server("player_died")
                return True
            for i in players_bar_group:
                if i.type == "red":
                    i.change_size((255,0,0),player_1.base_hp,player_1.hp)

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: it removes itself from a group
        """

    def remove_self(self,group):
        group.remove(self)

    """Name: did_player_level_up
        Parameters: self
        Returns: None
        Purpose: this checks to see if the player xp is higher than the needed to level up if it does it will then add
        one to the level and one to the level up points used in the shop and then take away the xp that was needed 
        to level up and then increase the amount of the next level up by 1.3.
        """

    def did_player_level_up(self):
        if self.xp >= self._xp_needed_for_level_up:
            self._level += 1
            self.xp -= self._xp_needed_for_level_up
            self._xp_needed_for_level_up = math.floor(self._xp_needed_for_level_up * 1.3)
            self._level_points += 1
            for i in players_bar_group:
                if i.type == "blue":
                    size_xp_level_up = player_1.get_players_xp_level_up()
                    i.change_size((0, 191, 255), size_xp_level_up, player_1.xp)

    """Name: _apply_damage_boosters
        Parameters: self
        Returns: none
        Purpose: this applies the damage amplifier to the weapon damage 
        """

    def _apply_damage_boosters(self):
        if self.boosts["damage"]:
            self.weapon.attack = self.weapon.original_damage
            for key in self.boosts["damage"]:
                self.weapon.attack = self.weapon.attack * self.boosts["damage"][key]
            self.weapon.attack = math.ceil(self.weapon.attack)
            self.tell_server("new_damage",info = [self.weapon.attack])

    """Name: _apply_xp_boosters
        Parameters: self
        Returns: None
        Purpose: This multiplies all the xp boosts together
        """

    def _apply_xp_boosters(self):
        if self.boosts["xp_boost"]:
            self.xp_boosts_multiplied_together = 1
            for key in self.boosts["xp_boost"]:
                self.xp_boosts_multiplied_together = self.xp_boosts_multiplied_together * self.boosts["xp_boost"][key]

    """ Name: _apply_health_boosters
        Parameters: self
        Returns: None
        Purpose: This adds applies the amplifiers to the health by multiplying and sets the base hp to the hp
        """

    def _apply_health_boosters(self):
        if self.boosts["health"]:
            self.hp = self.original_health
            for key in self.boosts["health"]:
                self.hp = self.hp * self.boosts["health"][key]
            self.hp = math.ceil(self.hp)
            self.base_hp = self.hp

    """Name: _apply_money_boosters
        Parameters: self
        Returns: None
        Purpose: This will apply money boosts to the player"""

    def _apply_money_boosters(self):
        if self.boosts["money_boost"]:
            self.money_boosts_multiplied_together = 1
            for key in self.boosts["money_boost"]:
                self.money_boosts_multiplied_together *= self.boosts["money_boost"][key]

    """Name: _health_regen
       Parameters: self
       Returns:None
       Purpose: This allows the user to heal but only i the players health is less than the base health"""

    def _health_regen(self):
        if self.hp < self.base_hp:
            self.hp += 1

    """Name: draw_level
       Parameters: self
       Return: None
       Purpose: This draws the level next to the xp bar"""

    def draw_level(self):
        myFont = pygame.font.SysFont("Arial", 15)
        f = myFont.render(str(self._level), True, (0, 0, 139))
        screen.blit(f, (225, 752))

    """Name:shop_boosts
        Parameters:self,Shop_hitbox_Check_2 = string
        Return: None
        Purpose: This adds the boost into a dictionary for the player and increase the cost of the boost then it will
        go to the function to apply the boost"""

    def shop_boosts(self,Shop_hitbox_Check_2):
        if self._level_points >= Shop_hitbox_Check_2.option.cost:
            self._level_points -= Shop_hitbox_Check_2.option.cost
            self.boosts[Shop_hitbox_Check_2.option.type][Shop_hitbox_Check_2.option.type + " boost from shop" + str(Shop_hitbox_Check_2.option.cost)] = Shop_hitbox_Check_2.option.boost
            Shop_hitbox_Check_2.option.cost += 1
            if Shop_hitbox_Check_2.option.type == "damage":
                self._apply_damage_boosters()
            elif Shop_hitbox_Check_2.option.type == "health":
                self._apply_health_boosters()
            elif Shop_hitbox_Check_2.option.type == "xp_boost":
                self._apply_xp_boosters()
            elif Shop_hitbox_Check_2.option.type == "money_boost":
                self._apply_money_boosters()

    """Name: get_players_xp_level_up
        Parameter: self
        Return: _xp_needed_for_level_up = integer
        Purpose: This returns xp_needed_for_level_up"""

    def get_players_xp_level_up(self):
        return self._xp_needed_for_level_up

    """Name:time_for_regen_take_place
        Parameter:self
        Return:None
        Purpose: This checks to see if the players difficulty is easy and if it will start a timer and after time it will
        set regenerate_health to true this will allow for the second timer so that every 5 seconds the player will heal
        """

    def time_for_the_regen_take_place(self):
        if self.difficulty == "Easy":
            self._current_time_regen = time.time()
            self._time_elapsed_regen = self._current_time_regen - self._last_time_regen
            self._last_time_regen = self._current_time_regen
            if not self._regenerate_health:
                self._time_since_dmg_or_shot += self._time_elapsed_regen
            if self._time_since_dmg_or_shot >= self._time_for_the_regen:
                self._regenerate_health = True
                self._time_since_dmg_or_shot = 0
            if self._regenerate_health:
                self._current_time_health = time.time()
                self._time_elapsed_health = self._current_time_health - self._last_time_health
                self._last_time_health = self._current_time_health
                if not self._actual_regenerate_health:
                    self._time_since_last_heal += self._time_elapsed_health
                if self._time_since_last_heal >= self._time_for_health_regen:
                    self._actual_regenerate_health = True
                    self._time_since_last_heal = 0
            if self._actual_regenerate_health:
                self._health_regen()
                for i in players_bar_group:
                    if i.type == "red":
                        i.change_size((255,0,0),self.base_hp,self.hp)
                self._actual_regenerate_health = False

    """Name: set_regen_health
    Parameter: self
    Return: None
    Purpose: This sets the regenerate health to False"""

    def set_regen_health(self):
        self._regenerate_health = False

    """Name: get_level_points
        Parameter: self
        Return _level_points = integer
        Purpose: This returns the level points"""

    def get_level_points(self):
        return self._level_points

    """Name: heal_through_aura,information = boolean
        Parameter: self
        Return: None
        Purpose: This allows the player to get healed from the other player ability. this checks to see if 
        the health would be over the base hp and set it to the base hp and it will tell the server to tell
        to the other player to increase their health"""

    def heal_through_aura(self,information):
        if self.hp + 2 < self.base_hp:
            self.hp += 2
        else:
            self.hp = self.base_hp
        for i in players_bar_group:
            if i.type == "red":
                i.change_size((255, 0, 0), player_1.base_hp, player_1.hp)
        if information:
            player_1.tell_server("aura",info = ["heal"])

"""Name: Ranged_Character
    Purpose: This calls Character class but it sets the player to have a sniper weapon and have the special ability 
    fireball"""
class Ranged_Character(Character):
    """Name: __init__
        Parameter: self,x = integer,y = integer ,colour = tuple,playerno = string,
        network_connection = None or socket.socket
        Return: None
        Purpose: This sets up the ranged_character object and puts some information into the parent class"""
    def __init__(self,x,y,colour,playerno,network_connection=None):
        super(Ranged_Character, self).__init__(playerno,colour)
        self.original_health = 20
        self.hp = self.original_health
        self.base_hp = self.hp
        self.weapon = sniper()
        self.Special_Ability = mega_fireball()
        self.connection = network_connection
        self.rect.x = x
        self.rect.y = y

"""Name: Melee_Character
    Purpose: This calls the Character class and it sets the player to have a sword attack and a dash special ability"""
class Melee_Character(Character):
    """Name: __init__
        Parameter: self,x = integer,y = integer,colour = tuple,playerno = string,
        network_connection = None or socket.socket
        Return: None
        Purpose: This sets up the Melee_Character object with the necessary information and passes the necessary
        information to the parent class Character"""
    def __init__(self,x,y,colour,playerno,network_connection=None):
        super(Melee_Character, self).__init__(playerno,colour)
        self.original_health = 25
        self.hp = self.original_health
        self.base_hp = self.hp
        self.weapon = sword()
        self.Special_Ability = dash()
        self.connection = network_connection
        self.rect.x = x
        self.rect.y = y

"""Name: Node
    Purpose: This sets nodes so the a star can access so it can see the parent and keep going up if necessary. It also
    holds the cooridnates and has g,h,f score which will used to work out where to go."""
class Node:
    """Name: __init__
        Parameter: self,Parent = Node,Position = Tuple
        Return: None
        Purpose: This sets up the node object with the necessary information"""
    def __init__(self,Parent=None,Position=None):
        self.Parent = Parent
        self.Position = Position
        self.g = 0
        self.h = 0
        self.f = 0

"""Name: Enemies_Class
    Purpose: This spawns in the enemy that the player can kill and the enemy can fight back this is the main obstacle
    for the player"""
class Enemies_Class(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,colour = tuple
        Return: None
        Purpose: This sets up the Enemies_Class object with the necessary information"""
    def __init__(self,colour,weapon = sniper()):
        super(Enemies_Class, self).__init__()
        self.hp = 10
        self.master_path = []
        self.test_master_path = []
        self._magnifier = 5
        self.direction = "U"
        self.available_shoot = True
        self.current_time = time.time()
        self.last_time = 0
        self.time_elapsed = self.current_time - self.last_time
        self.time_since_last_shot = 0
        self.xadjustment = 0
        self.yadjustment = 0
        self.weapon = weapon
        self.amplifiers = {"Gold":{},"Xp":{},"Health":{},"Damage":{}}
        self.Xp = 10
        self.base_Xp = 10
        self.current_time_a_star_algorithm = 0
        self.time_elapsed_a_star_algorithm = 0
        self.countdown_for_refresh_of_a_star_algorithm = 0
        self.how_long_until_it_refreshes_the_a_star_algorithm = 1.5
        self.last_time_the_a_star_pathfinding_was_used = 0
        self.redopathfinding = True
        self.amount_of_heart_dropped = 10
        global Enemy_ID
        self.colour = colour
        self.image = pygame.Surface((CHAR_WIDTH, CHAR_WIDTH))
        self.image.fill((colour))
        pygame.draw.rect(self.image, (colour), [0, 0, CHAR_WIDTH, CHAR_WIDTH])
        self.rect = self.image.get_rect()
        self.Enemy_ID = Enemy_ID
        Enemy_ID += 1
        self.start_timer_for_pathfinding = True
        self._current_time_pathfinding = 0
        self._time_elapsed_pathfinding = 0
        self._last_time_pathfinding = 0
        self._time_for_pathfinding = 1
        self._time_since_last_pathfinding = 0

    """Name: AStarAlgorithm
        Parameters: self, player = player_1 or player_2, x_distance_away_from_player = integer, 
        y_distance_away_from_player = integer
        Returns: path = list, [] = list
        Purpose: This makes it so that the enemy can pathfind to the player closest to them this is done by checking 
        if every block surrounding the current block is able to be moved into and if it is it will then go into that
        one and check again but it uses pythagoras theorem to see if the block is closer to the player or not. It will
        also see the length of the list and if its higher than the other player it will return an empty list or if the
        player is more than 500 blocks away."""

    def AStarAlgorithm(self,player,x_distance_away_from_player,y_distance_away_from_player):
        the_amount_of_routes_before_cancelling = 0 #this sets the counter which ticks up every time there is a path
        x_adjustment_for_walls_inside_astar = math.floor(x_adjustment_for_walls/self._magnifier)#this is the adjustment
        # needed as everything moves except the player
        y_adjustment_for_walls_inside_astar = math.floor(y_adjustment_for_walls/self._magnifier) #this is the adjustment
        # needed as everything moves except the player
        path = [] #this sets the path empty which will later be returned with the path in
        open_list = [] #this sets the open path list empty this list will be able to be accessed in the astar
        closed_list = [] #this sets the closed path list empty this will not will be able to be accessed in the astar
        # accept when it gets converted into the path
        x_adjustment_for_clipping = 0 #this sets the variable to 0 meaning there would not be any adjustment
        y_adjustment_for_clipping = 0 #this sets the variable to 0 meaning there would not be any adjustment
        for check in Walls: #this loops through the walls group
            if player.rect.x + CHAR_WIDTH + self._magnifier > check.x1 and player.rect.x + CHAR_WIDTH + self._magnifier < check.x2:
                #this if statement sees if the player would be in the wall if the magnifier added this makes sure that
                #if the player is hugging the bottom or left wall the enemy can still pathfind to them
                x_adjustment_for_clipping = 1 #this sets the adjustment to 1 this means the players
                # x coordinate will be one less
            if player.rect.y + CHAR_WIDTH + self._magnifier > check.y1 and player.rect.y + CHAR_WIDTH + self._magnifier < check.y2:
                y_adjustment_for_clipping = 1 #this sets the adjustment to 1 this means the players
                # y coordinate will be one less
                break #this means if the player would interact it will break out of the loop meaning less time is spent
        start_node = Node(None,(math.floor((self.rect.x/ self._magnifier)),math.floor((self.rect.y)/self._magnifier)))
        #this sets up the Node class with the cooridnates of the enemy
        end_node = Node(None,(math.floor((player.rect.x + x_distance_away_from_player) / self._magnifier - x_adjustment_for_clipping),math.floor((player.rect.y + y_distance_away_from_player) / self._magnifier) - y_adjustment_for_clipping))
        #this sets up the Node class with the corridnates of the player
        open_list.append(start_node) # it adds the node to the open list as that is where the enemy will pathfind from
        while len(open_list) > 0: #this loops through the open list until it is empty
            current_node = open_list[0] #this goes to the first Node class in the list
            current_index = 0 #this sets the current index to 0 which later could be changed
            """This sections cut off sections if the f value is higher than one in the open list this means that
            the current node is less promising to get to the end node so not much point going on with it"""
            for i in range(len(open_list)):#this iterates through the open_list
                if open_list[i].f < current_node.f: #this checks to see if the node at that index f value is less than
                    #the current node f
                    current_node = open_list[i] #this sets the current_node
                    current_index = i #this sets the current index to the number of the index
            open_list.pop(current_index) #this removes the node at that index
            closed_list.append(current_node) #this adds the current node to the closed list which means it set in stone

            if current_node.Position == end_node.Position: #this checks to see if the current node has the same
                #coordinates as the end node coordinates
                current = current_node # this sets current to the current node
                while current is not None:#this checks to see if current is none which will only be true when it has reached
                    #the starting cell
                    path.append(current.Position)#this appends the coordinates of the current node to the path
                    current = current.Parent # this sets current to the parent of the current which will be the previous
                    #one on the track
                return path[::-1] # this returns the path but reversed so it starts at the start cell and not the end cell
            children = [] #this will hold all the possible paths that the astar algorithm could go from the current node
            if the_amount_of_routes_before_cancelling == 500 / math.ceil(self._magnifier): # this means that the enemy
                #can not infitly try to pathfind to the player and will have to stop
                return [] # this will return an empty list meaning that the enemy can not pathfind to anything
            if the_amount_of_routes_before_cancelling > len(self.test_master_path) and self.test_master_path != []:
                #this checks to see if the path is longer than the pathfinding to the other player as if it there would
                #be no point carrying it on
                return [] # this will return an empty list meaning that the enemy can not pathfind to anything
            for i in range(-1,2,1): #this loops through -1 to 1 to represent the x cooridnate
                for t in range(-1,2,1): #this loops through -1 to 1 to represent the y coordinate
                    if i != 0 or t != 0:# this checks to make sure the i and j arent 1 as that would be the current node
                        true = True #this sets up true which will be used as a switch so if one of the statements is True
                        #it will put it to False
                        node_position = (current_node.Position[0] + i, current_node.Position[1] + t) #this sets up the
                        #node position with i and t being added
                        node_position_add_character_length_1 = (node_position[0] + math.ceil(32/self._magnifier), node_position[1] + math.ceil(32/self._magnifier))
                        #this sets up the node position with the width and length of the character with i and t
                        node_position_add_character_length_2 = (node_position[0], node_position[1] + math.ceil(32/self._magnifier))
                        #this sets up the node position with the length of the character with i and t
                        node_position_add_character_length_3 = (node_position[0] + math.ceil(32/self._magnifier), node_position[1])
                        #this sets up the node position with the width of the character with i and t
                        if i == -1: # this sees if the x position is -1
                            array_for_binary = list(dictionary_for_walls[str(self._magnifier)]["Left"]) #this sets the array for binary
                            found = binary_search_algorithm(array_for_binary,node_position[0]-x_adjustment_for_walls_inside_astar)#this does the binary search to see if the top would be in the wall
                            key_for_astar = node_position[0]-x_adjustment_for_walls_inside_astar#this makes the thing being searched for into a shorter variable
                            if found == "not found":#it checks to see if the number is not inside the astar
                                found = binary_search_algorithm(array_for_binary,node_position_add_character_length_2[0]-x_adjustment_for_walls_inside_astar)#this does another binary search to see if the bottom
                                #would be inside the wall
                                key_for_astar = node_position_add_character_length_2[0]-x_adjustment_for_walls_inside_astar# this makes the thing being searched for into a shorter variable
                            if found == "found": # this is the alternative if there is a number or if there wasnt is there was one with the new binary search
                                check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Left"][key_for_astar],node_position[1],y_adjustment_for_walls_inside_astar)#this does the binary search to see
                                #if the left would be in the wall
                                if check == "found":# this sees if the number was in the list
                                    true = False #this sets the switch to False meaning it cant be set back to True now
                                else:#this goes off if the number isnt in the binary
                                    check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Left"][key_for_astar],node_position_add_character_length_2[1],y_adjustment_for_walls_inside_astar)# this
                                    #binary search checks to see if the right would be in the wall
                                    if check == "found":# this sees if the enemy would in the wall
                                        true = False #this sets true to False and now true cant be set back to True
                        if i == 1: #this sees if the x position is 1
                            array_for_binary = list(dictionary_for_walls[str(self._magnifier)]["Right"]) # this puts the list into a simpilar variable
                            found = binary_search_algorithm(array_for_binary,node_position_add_character_length_1[0] - x_adjustment_for_walls_inside_astar)#this checks to see if the top of the player is in the wall
                            key_for_astar = node_position_add_character_length_1[0] - x_adjustment_for_walls_inside_astar #this makes the thing being searched for into a shorter variable
                            if found == "not found": #this sees if the number was not in the list
                                found = binary_search_algorithm(array_for_binary,node_position_add_character_length_3[0]-x_adjustment_for_walls_inside_astar)#this does a binary search to see if the bottom bit is in the wall
                                key_for_astar = node_position_add_character_length_3[0]-x_adjustment_for_walls_inside_astar#this makes the thing being searched into a shorter variable
                            if found == "found": #this is the alternative if there is a number or if there wasnt is there was one with the new binary search
                                check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Right"][key_for_astar], node_position[1],y_adjustment_for_walls_inside_astar)#this checks to see if the bottom is inside the wall
                                if check == "found":#this sees if the number is inside the list
                                    true = False#this sets true to False and now it cant be True
                                else:#this sees if the number is not in the list
                                    check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Right"][key_for_astar], node_position_add_character_length_3[1],y_adjustment_for_walls_inside_astar)#this checks to see if the right is in the wall
                                    if check == "found": #this sees if there is one to the right
                                        true = False# this sets true to False and now it cant be True
                        if t == -1 and true: #this sees if t is -1 meaning that it will check the one up from the current block it will also see if true is True as if it was False it would not be able to be True again so it would be a waste of time and effiectency to set it to False again
                            array_for_binary = list(dictionary_for_walls[str(self._magnifier)]["Up"]) #this shortens the list into a simpliar variable
                            found = binary_search_algorithm(array_for_binary,node_position[1] - y_adjustment_for_walls_inside_astar) #
                            key_for_astar = node_position[1] - y_adjustment_for_walls_inside_astar
                            if found == "not found":
                                found = binary_search_algorithm(array_for_binary,node_position_add_character_length_3[1]-y_adjustment_for_walls_inside_astar)
                                key_for_astar = node_position_add_character_length_3[1]-y_adjustment_for_walls_inside_astar
                            if found == "found":
                                check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Up"][key_for_astar], node_position[0],x_adjustment_for_walls_inside_astar)
                                if check == "found":
                                    true = False
                                else:
                                    check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Up"][key_for_astar],node_position_add_character_length_3[0],x_adjustment_for_walls_inside_astar)
                                    if check == "found":
                                        true = False
                        if t == 1 and true:
                            array_for_binary = list(dictionary_for_walls[str(self._magnifier)]["Down"])
                            found = binary_search_algorithm(array_for_binary,node_position_add_character_length_1[1] - y_adjustment_for_walls_inside_astar)
                            key_for_astar = node_position_add_character_length_1[1] - y_adjustment_for_walls_inside_astar
                            if found == "not found":
                                found = binary_search_algorithm(array_for_binary, node_position_add_character_length_2[1] - y_adjustment_for_walls_inside_astar)
                                key_for_astar = node_position_add_character_length_2[1] - y_adjustment_for_walls_inside_astar
                            if found == "found":
                                check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Down"][key_for_astar],node_position[0],x_adjustment_for_walls_inside_astar)
                                if check == "found":
                                    true = False
                                else:
                                    check = binary_search_algorithm(dictionary_for_walls[str(self._magnifier)]["Down"][key_for_astar],node_position_add_character_length_2[0],x_adjustment_for_walls_inside_astar)
                                    if check == "found":
                                        true = False
                        if true:
                            new_node = Node(current_node,node_position)
                            children.append(new_node)
            for child in children:
                for closed_child in closed_list:
                    if child.Position == closed_child.Position:
                        break
                else:
                    child.g = current_node.g + 1
                    child.h = (((child.Position[0] - end_node.Position[0])**2) + ((child.Position[1] - end_node.Position[1])**2))
                    child.f = child.g + child.h
                    for open_node in open_list:
                        if child.Position == open_node.Position and child.g > open_node.g:
                            break
                    else:
                        open_list.append(child)
            the_amount_of_routes_before_cancelling += 1#this adds one to the
        return [] #this returns an empty list

    """Name: check_alive
        Parameters: self,s_group = pygame.sprite.Group,player = string
        Returns: None
        Purpose: This checks to see if the enemies health is less or equal to 0 and if it is it will remove itself from
        the group and it will drop gold and the heart pickup as well it will give the player the xp and it will change
        the size of the experience and it will call the function to see if the player has leveled up
        """

    def check_alive(self,s_group,player):
        if self.hp <= 0:
            Gold_Sprite = Gold(self.gold,self.rect.x,self.rect.y)
            Dropped_Golds.add(Gold_Sprite)
            if player_1.difficulty != "Hard":
                Hearts_Sprite = Hearts(self.amount_of_heart_dropped,self.rect.x+10,self.rect.y+10)
                Dropped_Hearts.add(Hearts_Sprite)
            s_group.remove(self)
            self.add_amplifiers("Xp")
            if player == "player1":
                player_1.xp += math.ceil(self.Xp * player_1.xp_boosts_multiplied_together)
                for i in players_bar_group:
                    if i.type == "blue":
                        size_xp_level_up = player_1.get_players_xp_level_up()
                        i.change_size((0,191,255),size_xp_level_up,player_1.xp)
                player_1.did_player_level_up()
            s_group.remove(self)
            player_1.tell_server("enemy_defeated",info = self.Enemy_ID)

    """Name: enemy_shoot
        Parameters: self
        Returns: None
        Purpose: This means that only one player gets to control which enemy shoots so that there is synchronization 
        """

    def enemy_shoot(self):
        if player_1.PlayerNumber == "player1" and self.Enemy_ID % 2 == 0:
            self.shoot_shoot()
        elif player_1.PlayerNumber == "player2" and self.Enemy_ID % 2 == 1:
            self.shoot_shoot()

    """Name: shoot_shoot
        Parameters: self
        Returns: None
        Purpose: This sets a timer so that the enemy shoots after a certain amount of time it also sends the information
        to the other player to shoot
        """

    def shoot_shoot(self):
        self.current_time = time.time()
        self.time_elapsed = self.current_time - self.last_time
        self.last_time = self.current_time
        if not self.available_shoot:
            self.time_since_last_shot += self.time_elapsed
        if self.time_since_last_shot >= self.weapon.enemy_time:
            self.available_shoot = True
            self.time_since_last_shot = 0
        if self.available_shoot:
            self.available_shoot = False
            EB = Bullet(self.rect.x, self.rect.y, self.direction, self.weapon.width, self.weapon.height, self.weapon.range, self.weapon.speed, None, self.weapon.amplified_damage)
            enemy_shots.add(EB)
            player_1.tell_server("enemy_shoot",self.rect.x,self.rect.y,None,self.Enemy_ID)

    """Name: remove_self
        Parameters: self,group
        Returns: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

    """Name: add_amplifiers_to_dictionary
        Parameters: self,what_to_apply = string,reason = string,amplification = float
        Returns: None
        Purpose: This will add the amplifiers to a dictionary
        """

    def add_amplifiers_to_dictionary(self,what_to_apply,reason,amplification):
        true = True
        if self.amplifiers[what_to_apply]:
            for key in self.amplifiers[what_to_apply]:
                if key == reason:
                    self.amplifiers[what_to_apply][key] = amplification
                    true = False
            if true:
                self.amplifiers[what_to_apply][reason] = amplification
        else:
            self.amplifiers[what_to_apply][reason] = amplification

    """Name: add_amplifiers
        Parameters: self,what_to_apply = string
        Returns: None
        Purpose: This multiplies the amplifiers together for the health, damage and xp
        """

    def add_amplifiers(self,what_to_apply):
        if what_to_apply == "Damage":
            self.weapon.amplified_damage = self.weapon.attack
            if self.amplifiers["Damage"]:
                for key in self.amplifiers["Damage"]:
                    self.weapon.amplified_damage = self.weapon.amplified_damage * self.amplifiers["Damage"][key]
                self.weapon.amplified_damage = math.floor(self.weapon.amplified_damage)
        if what_to_apply == "Health":
            self.health = self.base_health
            if self.amplifiers["Health"]:
                for key in self.amplifiers["Health"]:
                    self.health = self.health * self.amplifiers["Health"][key]
                self.health = math.floor(self.health)
        if what_to_apply == "Xp":
            self.Xp = self.base_Xp
            if not self.amplifiers["Xp"]:
                for key in self.amplifiers["Xp"]:
                    self.Xp = self.Xp * self.amplifiers["Xp"][key]
                self.Xp = math.ceil(self.Xp)

    """Name: get_magnifier
        Parameters:self
        Return: magnifier = integer
        Purpose: This returns magnifier"""

    def get_magnifier(self):
        return self._magnifier

    """Name: the_timer_for_the_pathfinding
        Parameter: self
        Return: None
        Purpose: This is when the player is too far from the enemy it will give a certain amount of seconds before it
        will try to pathfind to the player again"""

    def the_timer_for_the_pathfinding(self):
        self._current_time_pathfinding = time.time()
        self._time_elapsed_pathfinding = self._current_time_pathfinding - self._last_time_pathfinding
        self._last_time_pathfinding = self._current_time_pathfinding
        if not self.start_timer_for_pathfinding:
            self._time_since_last_pathfinding += self._time_elapsed_pathfinding
        if self._time_since_last_pathfinding >= self._time_for_pathfinding:
            self.start_timer_for_pathfinding = True
            self._time_since_last_pathfinding = 0

"""Name: Melee_Enemy
    Purpose: This calls the enemy class but gives the enemy the sword weapon"""
class Melee_Enemy(Enemies_Class):
    """Name: __init__
        Parameter: self,x = integer ,y = integer,colour = tuple,gold = integer
        Return: None
        Purpose: This sets up the Melee_Enemy object with the necessary information and sends some information to the
        parent class Enemies_Class"""
    def __init__(self,x,y,colour,gold,weapon):
        super(Melee_Enemy, self).__init__(colour,weapon)
        self.Special_Ability = dash()
        self.rect.x = x
        self.rect.y = y
        self.gold = gold

"""Name: Bullet
    Purpose: This creates the sprite that actually deal damages to the player or enemy"""
class Bullet(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer,direction = string,SHOT_WIDTH = integer,SHOT_HEIGHT = integer,
        range = integer ,speed = integer,player = string or None,damage = integer or None
        Return: None
        Purpose: This sets up the Bullet object with the necessary information"""
    def __init__(self,x,y,direction,SHOT_WIDTH,SHOT_HEIGHT,range,speed,player=None,damage=None):
        super().__init__()
        self.direction = direction
        self.__range = range
        self.player = player
        self.damage = damage
        if direction == "R":
            self.intiation(SHOT_WIDTH,SHOT_HEIGHT)
            self.rect.x = x
            self.rect.y = y
        elif direction == "L":
            self.intiation(SHOT_WIDTH, SHOT_HEIGHT)
            self.rect.x = x - SHOT_WIDTH
            self.rect.y = y
        if direction == "D":
            self.intiation(SHOT_HEIGHT, SHOT_WIDTH)
            self.rect.x = x
            self.rect.y = y
        elif direction == "U":
            self.intiation(SHOT_HEIGHT, SHOT_WIDTH)
            self.rect.x = x
            self.rect.y = y - SHOT_HEIGHT
            self.postiony = y + self.__range
        self.direction = direction
        self.postionx = x
        self.postiony = y
        self.speed = speed
        if direction == "R":
            self.rect.x = x + CHAR_WIDTH
        elif direction != "L":
            self.rect.x = x + CHAR_WIDTH // 2 - SHOT_WIDTH // 2
        if direction == "D":
            self.rect.y = y + CHAR_WIDTH
        elif direction != "U":
            self.rect.y = y + CHAR_WIDTH // 2 - SHOT_WIDTH // 2

    """Name: update
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: This moves the the bullet in the direction it was facing and it if it goes a certain distance it will
        remove itself from every group deleting itself
        """

    def update(self,group):
        if self.direction == "R":
            self.rect.x += self.speed
        elif self.direction == "L":
            self.rect.x -= self.speed
        elif self.direction == "U":
            self.rect.y -= self.speed
        elif self.direction == "D":
            self.rect.y += self.speed
        if (self.rect.x  > self.postionx + self.__range and self.direction == "R")\
                or (self.rect.x < self.postionx - self.__range and self.direction == "L"):
            group.remove(self)
        if (self.rect.y) > self.postiony + self.__range and self.direction == "D" \
                or (self.rect.y < self.postiony - self.__range and self.direction == "U"):
            group.remove(self)

    """Name: intiation
        Parameters: self,SHOT_WIDTH = integer,SHOT_HEIGHT = integer
        Returns: None
        Purpose:This sets up a certain variables that need to be repeated
        """

    def intiation(self,SHOT_WIDTH,SHOT_HEIGHT):
        self.image = pygame.Surface((SHOT_HEIGHT, SHOT_WIDTH))
        self.image.fill((48,213,200))
        pygame.draw.rect(self.image,(48,213,200),[0,0,SHOT_HEIGHT,SHOT_WIDTH])
        self.rect = self.image.get_rect()

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

    """Name: set_bullet_range
        Parameter:self,number = integer
        Returns: None
        Purpose: It changes the range of the bullet"""

    def set_bullet_range(self,number):
        self.__range += number

"""Name: collide_check
    Parameter: None
    Return: None
    Purpose: This allows 2 objects to interact with a multitude of different reactions to the objects interacting"""

def collide_check():
    global room,Room_Generated,You_Died
    hits = pygame.sprite.groupcollide(player_shots,enemies,True,False)
    if hits != {}:
        for b,e_list in hits.items():
            for e in e_list:
                e.hp -= b.damage
                e.check_alive(enemies,b.player)
    hits = pygame.sprite.groupcollide(characters, Dropped_Golds, False, False)
    if hits != {}:
        for character_list,Dropped_Golds_list in hits.items():
            for d in Dropped_Golds_list:
                character_list.wallet += math.ceil(d.amount * player_1.money_boosts_multiplied_together)
                d.remove_self(Dropped_Golds)
    hits = pygame.sprite.groupcollide(mouse_hitbox_group,Shop_hitbox_group,True,False)
    if hits != {}:
        for i in mouse_hitbox_group:
            i.remove_self(mouse_hitbox_group)
        for t,Shop_hitbox_Check in hits.items():
            for Shop_hitbox_Check_2 in Shop_hitbox_Check:
                if Shop_hitbox_Check_2.type == "Normal":
                    if player_1.wallet >= Shop_hitbox_Check_2.option.cost:
                        if player_1.weapon.number != Shop_hitbox_Check_2.option.number:
                            player_1.wallet -= Shop_hitbox_Check_2.option.cost
                            player_1.weapon = Shop_hitbox_Check_2.option
                            player_1.tell_server("change",0,0,None,player_1.weapon.number)
                elif Shop_hitbox_Check_2.type == "XP":
                    player_1.shop_boosts(Shop_hitbox_Check_2)
    hits = pygame.sprite.groupcollide(mouse_hitbox_group,setting_hitbox_group,True,False)
    if hits != {}:
        for i in mouse_hitbox_group:
            i.remove_self(mouse_hitbox_group)
        for t,Setting_hitbox_check in hits.items():
            for Setting_hitbox_check_2 in Setting_hitbox_check:
                if Setting_hitbox_check_2.option != "Resume":
                    player_1.difficulty = Setting_hitbox_check_2.option
                    player_1.tell_server("change_difficulty",info= Setting_hitbox_check_2.option)
    hits = pygame.sprite.groupcollide(characters, StairCase_Group, False, False)
    if hits != {}:
        r = 0
        for t, StairCase_Check in hits.items():
            r += 1
            if r == 2:
                room += 1
                Room_Generated = False
    hits = pygame.sprite.groupcollide(player_shots, Walls, True, False)
    hits = pygame.sprite.groupcollide(enemy_shots,Walls,True,False)
    hits = pygame.sprite.groupcollide(enemy_shots, characters, True, False)
    if hits != {}:
        for b, c_list in hits.items():
            for c in c_list:
                c.hp -= b.damage
                check_alive = c.check_alive(characters)
                if check_alive:
                    room = 0
                    Room_Generated = False
                    You_Died = True
    hits = pygame.sprite.groupcollide(player_shots,Boss_Group,True,False)
    if hits != {}:
        for b,e_list in hits.items():
            for e in e_list:
                e.hp -= b.damage
                e.check_alive(Boss_Group,Boss_health_bar_Group,StairCase,StairCase_Group,player_1,players_bar_group,x_adjustment_for_slimes,y_adjustment_for_slimes,xadjust,yadjustment)
    hits = pygame.sprite.groupcollide(characters, Dropped_Hearts, False, True)
    if hits != {}:
        for character_list, Dropped_Hearts_list in hits.items():
            for d in Dropped_Hearts_list:
                character_list.hp += d.amount
                if character_list.hp > character_list.base_hp:
                    character_list.hp = character_list.base_hp
                for i in players_bar_group:
                    if i.type == "red":
                        i.change_size((255,0,0),player_1.base_hp,player_1.hp)
    hits = pygame.sprite.groupcollide(characters, Boss_Group, False, False)
    if hits != {}:
        for character_list,Boss_list in hits.items():
            for B in Boss_list:
                if B.type == "slime":
                    if not B.contact_time:
                        B.contact_time = True
                        character_list.hp -= 1
                        check_alive = character_list.check_alive(characters)
                        if check_alive:
                            room = 0
                            Room_Generated = False
                            You_Died = True
                        for i in players_bar_group:
                            if i.type == "red":
                                i.change_size((255, 0, 0), player_1.base_hp, player_1.hp)
    hits = pygame.sprite.groupcollide(characters,Boss_attack_Group,False,False)
    if hits != {}:
        for character_list, boss_attack_list in hits.items():
            for B in boss_attack_list:
                if not B.contact_time:
                    B.contact_time = True
                    character_list.hp -= 1
                    check_alive = character_list.check_alive(characters)
                    if check_alive:
                        room = 0
                        Room_Generated = False
                        You_Died = True
                    for i in players_bar_group:
                        if i.type == "red":
                            i.change_size((255, 0, 0), player_1.base_hp, player_1.hp)

"""Name: shop_hitboxes
    Purpose: This creates the hitbox so when the mouse hitbox interacts with it will buy the necessary boosts and items"""

class shop_hitboxes(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer,option = string,Type = string
        Return: None
        Purpose: This sets up the shop_hitboxes object with the necessary information"""
    def __init__(self,x,y,option,Type):
        super(shop_hitboxes, self).__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill((48, 213, 200))
        pygame.draw.rect(self.image, (48, 213, 200), [0, 0, 150, 150])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.option = option
        self.type = Type

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

"""Name: mouse_hitbox
    Purpose: This creates a hitbox that allows the user to interact with the setting options and shop options"""

class mouse_hitbox(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer
        Return: None
        Purpose: This sets up the mouse_hitbox object with the necessary information"""
    def __init__(self,x,y):
        super(mouse_hitbox, self).__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill((48, 213, 200))
        pygame.draw.rect(self.image, (48, 213, 200), [0, 0, 1, 1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

"""Name: create_shop_hitboxes
    Parameters: None
    Returns: None
    Purpose: It creates the hitboxes for the shops to allow the user to buy the stuff.
    """

def create_shop_hitboxes():
    Shop_hitbox_Sprite = shop_hitboxes(500,50,shop_person.option1,shop_person.type_of_shopkeeper)
    Shop_hitbox_group.add(Shop_hitbox_Sprite)
    Shop_hitbox_Sprite = shop_hitboxes(500, 250,shop_person.option2,shop_person.type_of_shopkeeper)
    Shop_hitbox_group.add(Shop_hitbox_Sprite)
    Shop_hitbox_Sprite = shop_hitboxes(500, 450,shop_person.option3,shop_person.type_of_shopkeeper)
    Shop_hitbox_group.add(Shop_hitbox_Sprite)

"""Name: StairCase
    Purpose: This creates a box that allows the players to walk into it and if both players walk into it at the 
    same time it will allow the players to go to the next floor"""

class StairCase(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,x = integer,y = integer
        Return: None
        Purpose: This sets up the StairCase object with the necessary information"""
    def __init__(self,x,y):
        super(StairCase, self).__init__()
        self.image = pygame.Surface((75, 75))
        self.image.fill((150, 75, 0))
        pygame.draw.rect(self.image, (150, 75, 0), [0, 0, 75, 75])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    """Name: remove_self
        Parameters: self,group = pygame.sprite.Group
        Returns: None
        Purpose: It removes itself from the group
        """

    def remove_self(self,group):
        group.remove(self)

"""Name: event_check
    Parameter:None
    Return: True = boolean,False = boolean
    Purpose:This does a multitude of things including pressing the x on the game making the game quit, 
    putting the left click to create a bullet, right click to activate the special ability, E to open up the shop
    if the player is in the distance, press esc to close shop if open or open and close setting, pressing down left or
    right click to spawn in a mouse hitbox to interact with settings or shops"""

def event_check():
    global available_shoot,available_shoot2,shop_open,shop_person,shop_open_2,setting_open
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                if available_shoot == True:
                    available_shoot = False
                    Bullet_Sprite = Bullet(player_1.rect.x, player_1.rect.y, player_1.direction, player_1.weapon.width,player_1.weapon.height
                                           ,player_1.weapon.range,player_1.weapon.speed,"player1",player_1.weapon.attack)
                    player_shots.add(Bullet_Sprite)
                    player_1.tell_server("shoot", 0, 0, Bullet_Sprite.direction)
                    player_1.set_regen_health()
            if mouse[2]:
                if available_shoot2 == True:
                    available_shoot2 = False
                    player_1.Special_Ability.special_ability(player_1,Bullet,player_shots,player_2)
            if keys[pygame.K_e]:
                if player_1.direction == "D":
                    for shop in Shops_Group:
                        if player_1.rect.x + (CHAR_WIDTH/2) > shop.rect.x and player_1.rect.x + (CHAR_WIDTH/2)  < shop.rect.x + shop.width \
                                and (player_1.rect.y + CHAR_WIDTH + distance_away > shop.rect.y and player_1.rect.y + CHAR_WIDTH < shop.rect.y + shop.width):
                            shop_open = True
                            shop_person = shop
                            create_shop_hitboxes()
                elif player_1.direction == "R":
                    for shop in Shops_Group:
                        if player_1.rect.x + CHAR_WIDTH + distance_away > shop.rect.x and player_1.rect.x + CHAR_WIDTH < shop.rect.x + shop.width \
                                and (player_1.rect.y + (CHAR_WIDTH/2) > shop.rect.y and player_1.rect.y + (CHAR_WIDTH/2) < shop.rect.y + shop.width):
                            shop_open = True
                            shop_person = shop
                            create_shop_hitboxes()
                elif player_1.direction == "L":
                    for shop in Shops_Group:
                        if player_1.rect.x > shop.rect.x and player_1.rect.x < shop.rect.x + shop.width + distance_away \
                                and (player_1.rect.y + (CHAR_WIDTH/2) > shop.rect.y and player_1.rect.y + (CHAR_WIDTH/2) < shop.rect.y + shop.width):
                            shop_open = True
                            shop_person = shop
                            create_shop_hitboxes()
                elif player_1.direction == "U":
                    for shop in Shops_Group:
                        if player_1.rect.x + (CHAR_WIDTH/2) > shop.rect.x and player_1.rect.x + (CHAR_WIDTH/2) < shop.rect.x + shop.width \
                                and (player_1.rect.y > shop.rect.y and player_1.rect.y < shop.rect.y + shop.width + distance_away):
                            shop_open = True
                            shop_person = shop
                            create_shop_hitboxes()
            if keys[pygame.K_ESCAPE]:
                if shop_open:
                    shop_open = False
                elif not setting_open:
                    setting_open = True
                    create_setting_hitboxes()
                elif setting_open:
                    setting_open = False
                    for group in setting_hitbox_group:
                        group.remove(setting_hitbox_group)
        if event.type == pygame.MOUSEBUTTONUP:
            for i in mouse_hitbox_group:
                i.remove_self(mouse_hitbox_group)
            pos = pygame.mouse.get_pos()
            if shop_open or setting_open:
                mouse_hitbox_sprite = mouse_hitbox(pos[0],pos[1])
                mouse_hitbox_group.add(mouse_hitbox_sprite)
    return True

"""Name:pre_running_check_event
    Parameter: None
    Return: True = boolean, False = boolean
    Purpose: This allows for the player to use the x button to exit the game and use the left click to choose the resume
    and quit
    """

def pre_running_check_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False,True
        if event.type == pygame.MOUSEBUTTONUP:
            for i in mouse_hitbox_group:
                i.remove_self(mouse_hitbox_group)
            pos = pygame.mouse.get_pos()
            mouse_hitbox_sprite = mouse_hitbox(pos[0], pos[1])
            mouse_hitbox_group.add(mouse_hitbox_sprite)

"""Name: create_setting_hitboxes
    Parameters: None
    Returns: None
    Purpose: This create the hitboxes of the resume and if the player is in the starting room it will create the hitboxes
    of the difficulties 
    """

def create_setting_hitboxes():
    setting_hitbox_Sprite = other_hitboxes(300,300,"Resume",(160, 50))
    setting_hitbox_group.add(setting_hitbox_Sprite)
    if room == 0:
        setting_hitbox_Sprite = other_hitboxes(300, 400,"Easy",(160, 50))
        setting_hitbox_group.add(setting_hitbox_Sprite)
        setting_hitbox_Sprite = other_hitboxes(300, 452,"Medium",(160, 50))
        setting_hitbox_group.add(setting_hitbox_Sprite)
        setting_hitbox_Sprite = other_hitboxes(300, 504,"Hard",(160, 50))
        setting_hitbox_group.add(setting_hitbox_Sprite)

""" Name: other_hitboxes
    Purpose: This creates a hitbox that allows the player to interact with the shop or setting options"""

class other_hitboxes(pygame.sprite.Sprite):
    """ Name: __init__
        Parameter: self,x = integer,y = integer,option = string,size = tuple
        Return: None
        Purpose: This sets up the other_hitboxes object with the necessary information"""
    def __init__(self,x,y,option,size):
        super(other_hitboxes, self).__init__()
        self.image = pygame.Surface(size)
        self.image.fill((48, 213, 200))
        pygame.draw.rect(self.image, (48, 213, 200), [0, 0, 75, 80])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.option = option

    """Name:remove_self
        Parameter:self,group =pygame.sprite.Group
        Returns:None
        Purpose: This removes itself from the group"""

    def remove_self(self,groups):
        self.remove(groups)

""" Name: setting_open_ui
    Parameter:room_id = integer
    Return:None
    Purpose: This will draw resume and then if the room id is 0 it will draw the difficulties and it will change 
    colours depending on if a player has picked it or both players have picked it"""

def setting_open_ui(room_id):
    myFont = pygame.font.SysFont("Arial", 50)
    f = myFont.render(("Resume"), True, (255, 0, 0))
    screen.blit(f, (300,300))
    if room_id == 0:
        myFont = pygame.font.SysFont("Arial", 50)
        if player_1.difficulty == "Easy":
            f = myFont.render(("Easy"), True, (0, 191, 255))
        if player_2.difficulty == "Easy":
            f = myFont.render(("Easy"), True, (255, 20, 147))
            if player_1.difficulty == "Easy":
                f = myFont.render(("Easy"), True, (93, 63, 211))
        if player_1.difficulty != "Easy" and player_2.difficulty != "Easy":
            f = myFont.render(("Easy"), True, (50, 205, 50))
        screen.blit(f, (300, 400))
        myFont = pygame.font.SysFont("Arial", 50)
        if player_1.difficulty == "Medium":
            f = myFont.render(("Medium"), True, (0, 191, 255))
        if player_2.difficulty == "Medium":
            f = myFont.render(("Medium"), True, (218, 112, 214))
            if player_1.difficulty == "Medium":
                f = myFont.render(("Medium"), True, (93, 63, 211))
        if player_1.difficulty != "Medium" and player_2.difficulty != "Medium":
            f = myFont.render(("Medium"), True, (255, 140, 0))
        screen.blit(f, (300, 450))
        myFont = pygame.font.SysFont("Arial", 50)
        if player_1.difficulty == "Hard":
            f = myFont.render(("Hard"), True, (0, 191, 255))
        if player_2.difficulty == "Hard":
            f = myFont.render(("Hard"), True, ((218, 112, 214)))
            if player_1.difficulty == "Hard":
                f = myFont.render(("Hard"), True, (93, 63, 211))
        if player_1.difficulty != "Hard" and player_2.difficulty != "Hard":
            f = myFont.render(("Hard"), True, (220, 20, 60))
        screen.blit(f, (300, 500))

"""Name: shop_open_ui
    Parameter:None
    Return: None
    Purpose:This shows the different options that the player can purchase"""

def shop_open_ui():
    list_for_shop = [shop_person.option1,shop_person.option2,shop_person.option3]
    xstart = 500
    ystart = 50
    if shop_person.type_of_shopkeeper == "Normal":
        for i in list_for_shop:
            myFont = pygame.font.SysFont("Arial", 50)
            f = myFont.render((i.type), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Cost " + str(i.cost)), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart-20))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Range: " + str(i.range)), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart+60))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Damage: " + str(i.attack)), True, (255,0, 0))
            screen.blit(f, (xstart, ystart+80))
            ystart += 200
    elif shop_person.type_of_shopkeeper == "XP":
        for i in list_for_shop:
            myFont = pygame.font.SysFont("Arial", 50)
            f = myFont.render((i.name), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Cost " + str(i.cost)), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart - 20))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Type: " + str(i.type)), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart + 60))
            myFont = pygame.font.SysFont("Arial", 20)
            f = myFont.render(("Boost: " + str(i.boost)), True, (255, 0, 0))
            screen.blit(f, (xstart, ystart + 80))
            ystart += 200

"""Name: shop_distance_away_from_player
    Parameters: None
    Returns: None
    Purpose: This sees how far the player is from the shop and if it is a certain distance away it will set shop_open
    to false and closes the shop
    """

def shop_distance_away_from_player():
    global shop_open
    if player_1.rect.x + round(CHAR_WIDTH/2) > shop_person.centrex + 100 or player_1.rect.x + round(CHAR_WIDTH/2) < shop_person.centrex - 100:
        shop_open = False
    elif player_1.rect.y + round(CHAR_WIDTH/2) > shop_person.centrey + 100 or player_1.rect.y + round(CHAR_WIDTH/2) < shop_person.centrey - 100:
        shop_open = False

"""Name: key_interface
    Parameters: None
    Returns:None 
    Purpose:This allows the user to move using the wasd it calls the function to move that direction
    """

def key_interface():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player_1.move_right(1)
    if keys[pygame.K_a]:
        player_1.move_left(1)
    if keys[pygame.K_w]:
        player_1.move_up(1)
    if keys[pygame.K_s]:
        player_1.move_down(1)

"""Name: Armageddon
    Parameters: None
    Returns: None
    Purpose: This get rid of everything so when the next floor spawns there will be a blank canvas
    """

def Armageddon():
    global Enemy_ID
    Enemy_ID = 1
    for i in StairCase_Group:
        i.remove_self(StairCase_Group)
    for i in Walls:
        i.remove_self(Walls)
    for i in Shops_Group:
        i.remove_self(Shops_Group)
    for i in enemies:
        i.remove_self(enemies)
    for i in Dropped_Golds:
        i.remove_self(Dropped_Golds)
    for i in Dropped_Hearts:
        i.remove_self(Dropped_Hearts)
    for i in enemy_shots:
        i.remove_self(enemy_shots)
    for i in player_shots:
        i.remove_self(player_shots)
    for i in setting_hitbox_group:
        if i.option != "Resume":
            i.remove_self(setting_hitbox_group)
    for i in Boss_Group:
        i.remove(Boss_Group)
    for i in Boss_health_bar_Group:
        i.remove(Boss_health_bar_Group)

"""Name: enemy_AI 
    Parameters: None
    Returns: None
    Purpose: This holds makes the ai do the necessary actions like moving and shooting.
    """

def enemy_AI():

    """ Name: the_pathfinding_for_the_ai
        Parameters: i = enemy
        Returns: None
        Purpose: this makes redopathfinding false so the enemy cant pathfind again while it is doing it as permforming
        it will then call the a star algorithm to perform it doing it to each player before seeing if one is longer
        than the other. The shortest path then gets converted to the master path which will be used by the enemy
        """

    def the_pathfinding_for_the_ai(i):
        i.redopathfinding = False
        i.xadjustment = i.yadjustment = 0
        path1 = i.AStarAlgorithm(player_1,0,0)
        i.test_master_path = path1
        path2 = i.AStarAlgorithm(player_2,0,0)
        if path2 != []:
            i.test_master_path = path2
        if i.test_master_path == []:
            i.start_timer_for_pathfinding = False
        i.master_path = i.test_master_path

    """Name: threading_for_pathfinding
        Parameters: none
        Returns: none
        Purpose: This function gets threaded so the player can play while the enemies find a path towards the player
        as well it decides whos client gets to work out the path depending on the Enemy_ID
        """

    def threading_for_pathfinding():
        for i in enemies:
            if i.redopathfinding:
                if i.start_timer_for_pathfinding:
                    if i.Enemy_ID % 2 == 0 and player_1.PlayerNumber == "player1":
                        the_pathfinding_for_the_ai(i)
                    elif i.Enemy_ID % 2 == 1 and player_1.PlayerNumber == "player2":
                        the_pathfinding_for_the_ai(i)
                else:
                    i.the_timer_for_the_pathfinding()

    threading.Thread(target=threading_for_pathfinding).start()

    for e in enemies:
        if e.master_path != []:
            enemy_magnifier = e.get_magnifier()
            if e.rect.x == (e.master_path[0][0] * enemy_magnifier) + e.xadjustment \
                    and e.rect.y == (e.master_path[0][1] * enemy_magnifier) + e.yadjustment:
                e.master_path.pop(0)
            else:
                if e.rect.x > (e.master_path[0][0] * enemy_magnifier) + e.xadjustment:
                    e.rect.x -= 1
                    e.direction = "L"
                    player_1.tell_server("enemy_move",-1,0,"L",e.Enemy_ID)
                elif e.rect.x < (e.master_path[0][0] * enemy_magnifier) + e.xadjustment:
                    e.rect.x += 1
                    e.direction = "R"
                    player_1.tell_server("enemy_move",1,0,"R",e.Enemy_ID)
                if e.master_path != []:
                    if e.rect.y > (e.master_path[0][1] * enemy_magnifier) + e.yadjustment:
                        e.rect.y -= 1
                        e.direction = "U"
                        player_1.tell_server("enemy_move",0,-1,"U",e.Enemy_ID)
                    elif e.rect.y < (e.master_path[0][1] * enemy_magnifier) + e.yadjustment:
                        e.rect.y += 1
                        e.direction = "D"
                        player_1.tell_server("enemy_move",0,1,"D",e.Enemy_ID)
        else:
            e.redopathfinding = True
    for i in enemies:
        i.enemy_shoot()
        i.current_time_a_star_algorithm = time.time()
        i.time_elapsed_a_star_algorithm = i.current_time_a_star_algorithm - i.last_time_the_a_star_pathfinding_was_used
        i.last_time_the_a_star_pathfinding_was_used = i.current_time_a_star_algorithm
        if not i.redopathfinding:
            i.countdown_for_refresh_of_a_star_algorithm += i.time_elapsed_a_star_algorithm
        if i.countdown_for_refresh_of_a_star_algorithm >= i.how_long_until_it_refreshes_the_a_star_algorithm:
            i.redopathfinding = True
            i.countdown_for_refresh_of_a_star_algorithm = 0

"""Name: the_length_of_the_wall_list
    Parameters: temp = integer,list_for_walls = dictionary
    Returns: None
    Purpose: This separates the wall into sections of 5 with each section going to left, right,up or down this means that
    the when the enemy uses the astar algorithm they can use the dictionarys to see where the walls are
    """

def the_length_of_the_wall_list(temp,list_for_walls):
    global dictionary_for_walls
    dictionary_for_walls = {"1": {"Left": {}, "Right": {}, "Up": {}, "Down": {}},
                            "2": {"Left": {}, "Right": {}, "Up": {}, "Down": {}},
                            "5": {"Left": {}, "Right": {}, "Up": {}, "Down": {}},
                            "10": {"Left": {}, "Right": {}, "Up": {}, "Down": {}}}
    for w in Walls:
        length = w.x2 - w.x1
        height = w.y2 - w.y1
        length_divided_by_magnifier = math.floor(length / temp)
        height_divided_by_magnifier = math.floor(height / temp)
        for i in range(length_divided_by_magnifier):
            for t in range(height_divided_by_magnifier):
                if i == 0 or i == length_divided_by_magnifier - 1 or t == 0 or t == height_divided_by_magnifier - 1:
                    if i == length_divided_by_magnifier - 1:
                        if not dictionary_for_walls[str(temp)]["Left"]:
                            dictionary_for_walls[str(temp)]["Left"][math.floor(w.x1 / temp) + i] = [math.floor(w.y1/temp) + t]
                        else:
                            true = True
                            for key in dictionary_for_walls[str(temp)]["Left"]:
                                if key == math.floor(w.x1 /temp) + i:
                                    dictionary_for_walls[str(temp)]["Left"][key].append(math.floor(w.y1 /temp) + t)
                                    true = False
                                    break
                            if true == True:
                                dictionary_for_walls[str(temp)]["Left"][math.floor(w.x1 /temp) + i] = [math.floor(w.y1/temp) + t]
                    if i == 0:
                        if not dictionary_for_walls[str(temp)]["Right"]:
                            dictionary_for_walls[str(temp)]["Right"][math.floor(w.x1 / temp) + i] = [math.floor(w.y1/temp) + t]
                        else:
                            true = True
                            for key in dictionary_for_walls[str(temp)]["Right"]:
                                if key == math.floor(w.x1 /temp) + i:
                                    dictionary_for_walls[str(temp)]["Right"][key].append(math.floor(w.y1 /temp) + t)
                                    true = False
                                    break
                            if true == True:
                                dictionary_for_walls[str(temp)]["Right"][math.floor(w.x1 /temp) + i] = [math.floor(w.y1/temp) + t]
                    if t == 0:
                        if not dictionary_for_walls[str(temp)]["Down"]:
                            dictionary_for_walls[str(temp)]["Down"][math.floor(w.y1 / temp) + t] = [math.floor(w.x1/temp) + i]
                        else:
                            true = True
                            for key in dictionary_for_walls[str(temp)]["Down"]:
                                if key == math.floor(w.y1 /temp) + t:
                                    dictionary_for_walls[str(temp)]["Down"][key].append(math.floor(w.x1 /temp) + i)
                                    true = False
                                    break
                            if true == True:
                                dictionary_for_walls[str(temp)]["Down"][math.floor(w.y1 /temp) + t] = [math.floor(w.x1/temp) + i]
                    if t == height_divided_by_magnifier - 1:
                        if not dictionary_for_walls[str(temp)]["Up"]:
                            dictionary_for_walls[str(temp)]["Up"][math.floor(w.y1 / temp) + t] = [math.floor(w.x1/temp) + i]
                        else:
                            true = True
                            for key in dictionary_for_walls[str(temp)]["Up"]:
                                if key == math.floor(w.y1 /temp) + t:
                                    dictionary_for_walls[str(temp)]["Up"][key].append(math.floor(w.x1 /temp) + i)
                                    true = False
                                    break
                            if true == True:
                                dictionary_for_walls[str(temp)]["Up"][math.floor(w.y1 /temp) + t] = [math.floor(w.x1/temp) + i]
                    list_for_walls.append((math.floor(w.x1 / temp) + i, math.floor(w.y1 / temp) + t))

"""Name: translate_the_array_into_real_walls
    Parameters: id_for_procedural_generation = integer
    Returns: None
    Purpose: This calls the procedural_generation and then sends the information every 0.05 seconds to not overwhelm the 
    server and then it will convert the array into walls
    """

def translate_the_array_into_real_walls(id_for_procedural_generation):
    walls_to_be_sent_for_conversion, stuff_inside_room= spawn_spawning_room()
    id_for_procedural_generation += 1
    if id_for_procedural_generation % 2 == 1:
        if player_1.PlayerNumber == "player1":
            for key in walls_to_be_sent_for_conversion:
                player_1.tell_server("make_rooms", 0, 0, 0,key)
                Spare_Walls_Group.add(wall(key[0] + xadjustment, (key[1] + yadjustment), (key[2], key[3])))
                time.sleep(0.03)
            for key in stuff_inside_room["Enemies"]:
                random_number = random.randint(1,3)
                weapon_for_enemy = sniper()
                if random_number == 1:
                    weapon_for_enemy = minigun()
                elif random_number == 2:
                    weapon_for_enemy = sword()
                player_1.tell_server("create_enemies",key[0],key[1],None,[2,weapon_for_enemy.type])
                Spare_Enemies_Group.add(Melee_Enemy(key[0]+xadjustment,key[1]+yadjustment,(0, 0, 255),25,weapon_for_enemy))
            for key in stuff_inside_room["Shop"]:
                player_1.tell_server("create_inside",key[0],key[1],None,["shop"])
                Spare_Shop_Group.add(Shop_Keeper(50,key[0]+xadjustment,key[1]+yadjustment))
            for key in stuff_inside_room["Staircase"]:
                player_1.tell_server("create_inside",key[0],key[1],None,["staircase"])
                Spare_StairCase_Group.add(StairCase(key[0]+xadjustment,key[1]+yadjustment))

"""Name: player_bar
    Purpose: This is used to show the health of the player and the xp of the player"""
class player_bar(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,colour = tuple,x = integer,y = integer,size = tuple,type = string,base_height = integer,
        base_length = integer
        Return: None
        Purpose: This sets up the player_bar object with the necessary information"""
    def __init__(self,colour,x,y,size,type,base_height,base_length):
        super(player_bar, self).__init__()
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        pygame.draw.rect(self.image,colour,[0,0,200,50])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__base_length = base_length
        self.__base_height = base_height
        self.type = type

    """Name: change_size
        Parameters: self,colour = tuple, base_stat = integer, new_stat = integer
        Returns: None
        Purpose: It changes the size of the bar to make it representative of the of the players stats including health 
        and xp
        """

    def change_size(self,colour,base_stat,new_stat):
        for i in characters:
            if i.connection != None:
                self.image = pygame.transform.scale(self.image,[self.__base_length * (new_stat / base_stat),self.__base_height])
                pygame.draw.rect(self.image,colour,[0,0,200,50])

"""Name: border_for_health
    Purpose: It gives the border of the health so it shows the max size of the health"""

class border_for_health(pygame.sprite.Sprite):
    """Name: __init__
        Parameter: self,width = integer,height = integer,x = integer,y = integer
        Return: None
        Purpose: This sets up the border_for_health object with the necessary information"""
    def __init__(self,width,height,x,y):
        super(border_for_health, self).__init__()
        self.image = pygame.Surface((width,height))
        pygame.draw.rect(self.image,(0,0,0),[0,0,0,0],2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "black"

"""Name: permanent_text_on_screen
        Parameters: None
        Returns: None
        Purpose: This displaces text that will forever appear on the screen this includes the amount of health the player
        has and the level the player is.
        """

def permanent_text_on_screen():
    text = str(player_1.hp) + " / " +str(player_1.base_hp)
    myFont = pygame.font.SysFont("Arial", 35)
    f = myFont.render(text, True, (0, 255, 0))
    screen.blit(f, (80,712))
    player_1.draw_level()
    if shop_open:
        myFont = pygame.font.SysFont("Arial", 35)
        f = myFont.render("Gold: "+str(player_1.wallet), True, (204, 204, 0))
        screen.blit(f, (500, 550))
        level_points = player_1.get_level_points()
        f = myFont.render("Xp Money: " + str(level_points), True, (0, 0, 139))
        screen.blit(f, (500, 600))
    if setting_open:
        f = myFont.render("Move: W A S D", True, (126,126,126))
        screen.blit(f, (80, 100))
        f = myFont.render("Shoot/Buy: Left Click", True, (126,126,126))
        screen.blit(f, (80, 150))
        f = myFont.render("Special Ability/Buy: Right Click", True, (126,126,126))
        screen.blit(f, (80, 200))
        f = myFont.render("Open Shop: E", True, (126,126,126))
        screen.blit(f, (80, 250))

"""Name:create_pre_running_hitboxes
    Parameters: None
    Returns: None
    Purpose: This makes the hitboxes around Start and Quit so the player can actually interact with them"""

def create_pre_running_hitboxes():
    pre_game_hitbox_Sprite = other_hitboxes(300, 360, "Start", (160, 110))
    pre_game_hitbox_Group.add(pre_game_hitbox_Sprite)
    pre_game_hitbox_Sprite = other_hitboxes(300, 490, "Quit", (160, 75))
    pre_game_hitbox_Group.add(pre_game_hitbox_Sprite)

"""Name: pre_game_collide_check
    Parameters: pre_running = boolean, Quit_Game = boolean
    Returns: pre_running = boolean,Quit_Game = boolean
    Purpose: This sees if the right click of the mouse interacts with the hitboxes of Start or quit and then does
    the necessary actions"""

def pre_game_collide_check(pre_running,Quit_Game):
    hits = pygame.sprite.groupcollide(mouse_hitbox_group, pre_game_hitbox_Group, True, False)
    if hits != {}:
        for i in mouse_hitbox_group:
            i.remove_self(mouse_hitbox_group)
        for t, Pre_game_hitbox_check in hits.items():
            for Pre_game_hitbox_check_2 in Pre_game_hitbox_check:
                if Pre_game_hitbox_check_2.option == "Start":
                    pre_running = False
                elif Pre_game_hitbox_check_2.option == "Quit":
                    pre_running = False
                    Quit_Game = True
    return pre_running,Quit_Game

"""Name: spawn_next_rooms
    Parameter: Room_Generated = boolean, x_adjustment_for_walls = integer, y_adjustment_for_walls = integer, 
    procedural_generation_generated = boolean
    Return: Room_Generated = boolean, x_adjustment_for_walls = integer, y_adjustment_for_walls = integer,
    procedural_generation_generated = boolean
    Purpose: This spawns the next room and if it is procedurally generated it will allow the creation of another 
    procedurally generated floor. It also checks to see if the player died and if they did it will then return to the
    spawn room so the player can redo the dungeon."""

def spawn_next_rooms(Room_Generated,x_adjustment_for_walls,y_adjustment_for_walls,procedural_generation_generated):
    global xadjust
    if room == 0 and Room_Generated == False:
        Room_Generated = True
        if You_Died:
            if player_1.PlayerNumber == "player1":
                player_2.rect.x = player_1.rect.x + 200
                player_2.rect.y = player_1.rect.y
                player_1.weapon = sniper()
                player_2.weapon = sword()
            else:
                player_2.rect.x = player_1.rect.x - 200
                player_2.rect.y = player_1.rect.y
                player_1.weapon = sword()
                player_2.weapon = sniper()
            player_1.hp = player_1.base_hp
            for i in players_bar_group:
                if i.type == "red":
                    i.change_size((255,0,0),player_1.base_hp,player_1.hp)
            player_2.hp = player_2.base_hp
        Armageddon()
        player_1.wallet = 0
        Create_Starting_Area(xadjustment,yadjustment,Walls,wall,StairCase_Group,StairCase,Shops_Group,Shop_Keeper,Melee_Enemy,enemies)
        x_adjustment_for_walls = 0
        y_adjustment_for_walls = 0
        #Playground(xadjustment,yadjustment,Walls,wall,StairCase_Group,StairCase,Shops_Group,Shop_Keeper,Melee_Enemy,enemies,player_1,player_2)
    if not procedural_generation_generated:
        procedural_generation_generated = True
        threading.Thread(target=translate_the_array_into_real_walls, args=[id_for_procedural_generation]).start()
    if not Room_Generated:
        Room_Generated = True
        Armageddon()
        list_for_walls = []
        if room == 1:
            Create_First_Floor(xadjustment,yadjustment,Walls,wall,player_1,player_2,enemies,Melee_Enemy,StairCase_Group,StairCase)
        else:
            """elif room % 2 == 0:
            xadjust = Create_Boss_Room(xadjustment,yadjustment,Walls,wall,StairCase_Group,StairCase,Shops_Group,Shop_Keeper,Melee_Enemy,enemies,player_1,player_2)
            Boss_Group.add(ghost_boss_spawn(xadjust,yadjustment,room))
            counter = 0
            for i in Boss_Group:
                if i.type == "ghost":
                    counter += 1
                    ID = i.Enemy_ID
                if i.type == "slime":
                    counter += 1
                    ID = i.Enemy_ID
            if counter >= 1:
                spawn_boss_health_bar(Boss_health_bar_Group,ID)
        elif room >= 2:"""
            if player_1.PlayerNumber == "player1":
                player_2.rect.x = player_1.rect.x + 100
                player_2.rect.y = player_1.rect.y
            else:
                player_2.rect.x = player_1.rect.x - 100
                player_2.rect.y = player_1.rect.y
            for i in Spare_Walls_Group:
                Walls.add(i)
                i.remove_self(Spare_Walls_Group)
            for i in Spare_Enemies_Group:
                enemies.add(i)
                i.remove_self(Spare_Enemies_Group)
                if player_1.difficulty == "Easy":
                    i.add_amplifiers_to_dictionary("Damage", "Dungeon1", 1.15 * room/4)
                    i.add_amplifiers("Damage")
                if player_1.difficulty == "Medium":
                    i.add_amplifiers_to_dictionary("Damage", "Dungeon1", 1.3 * room/4)
                    i.add_amplifiers("Damage")
                if player_1.difficulty == "Hard":
                    i.add_amplifiers_to_dictionary("Damage", "Dungeon1", 1.5*room/4)
                    i.add_amplifiers("Damage")
            for i in Spare_Shop_Group:
                Shops_Group.add(i)
                i.remove_self(Spare_Shop_Group)
            for i in Spare_StairCase_Group:
                StairCase_Group.add(i)
                i.remove_self(Spare_StairCase_Group)
            procedural_generation_generated = False
        the_length_of_the_wall_list(5, list_for_walls)
        x_adjustment_for_walls = 0
        y_adjustment_for_walls = 0
    return Room_Generated, x_adjustment_for_walls, y_adjustment_for_walls, procedural_generation_generated

"""Name: draw_things_on_screen
    Parameter: None
    Return: None
    Purpose: This draws everything onto the screen"""

def draw_things_on_screen():
    preview_attack_Group.draw(screen)
    Boss_attack_Group.draw(screen)
    StairCase_Group.draw(screen)
    characters.draw(screen)
    enemies.draw(screen)
    enemy_shots.draw(screen)
    Boss_Group.draw(screen)
    Walls.draw(screen)
    Dropped_Golds.draw(screen)
    Dropped_Hearts.draw(screen)
    Shops_Group.draw(screen)
    player_shots.update(player_shots)
    enemy_shots.update(enemy_shots)
    player_shots.draw(screen)
    players_bar_group.draw(screen)
    permanent_text_on_screen()
    Boss_health_bar_Group.draw(screen)

Quit_Game = False
pre_running = True
while pre_running:
    screen.fill((255,255,255))
    myFont = pygame.font.SysFont("Arial", 100)
    f = myFont.render("Play", True, (0, 0, 0))
    screen.blit(f, (300, 350))
    myFont = pygame.font.SysFont("Arial", 80)
    f = myFont.render("Quit", True, (255, 0, 0))
    screen.blit(f, (312, 475))
    myFont = pygame.font.SysFont("Arial", 300)
    f = myFont.render("?", True, (0, 0, 0))
    screen.blit(f, (300, 50))
    create_pre_running_hitboxes()
    pre_running_check_event()
    pre_running,Quit_Game = pre_game_collide_check(pre_running,Quit_Game)
    pygame.display.flip()
    clock.tick(60)

if not Quit_Game:
    connect_to_server()
    running = True
else:
    running = False
id_for_procedural_generation = 0
backup_dictionary_for_procedural_generation = {}
while running:
    screen.fill((255,255,255))
    running = event_check()
    Room_Generated, x_adjustment_for_walls, y_adjustment_for_walls,procedural_generation_generated = spawn_next_rooms(Room_Generated,x_adjustment_for_walls,y_adjustment_for_walls,procedural_generation_generated)
    key_interface()
    collide_check()
    draw_things_on_screen()
    if shop_open:
        shop_open_ui()
        shop_distance_away_from_player()

    if setting_open:
        setting_open_ui(room)

    enemy_AI()

    pygame.display.flip()
    clock.tick(60)

    current_time = time.time()
    time_elapsed = current_time - last_time
    last_time = current_time

    if not available_shoot:
        time_since_last_shot += time_elapsed
    if time_since_last_shot >= player_1.weapon.time:
        available_shoot = True
        time_since_last_shot = 0

    current_time2 = time.time()
    time_elapsed2 = current_time2 - last_time2
    last_time2 = current_time2

    if not available_shoot2:
        time_since_last_special += time_elapsed2
    if time_since_last_special >= player_1.Special_Ability.time:
        available_shoot2 = True
        time_since_last_special = 0

    player_1.time_for_the_regen_take_place()
    boss_group_actions(Boss_Group,player_1,player_2)
print("Bye Bye")