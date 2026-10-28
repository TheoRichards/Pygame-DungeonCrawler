import random

"""Name: add_things_to_inside_procedural_generation
    Parameter: dictionary_for_inside_room = dictionary
    Return: stuff_inside_the_rooms = dictionary
    Purpose: This adds the shop,enemies and staircase into the procedural generation this uses the inside dictionary
     it adds the added things to a dictionary which is then returned."""
def add_things_to_inside_procedural_generation(dictionary_for_inside_room):
    how_many_enemies_to_spawn = random.randint(5,7)
    stuff_inside_the_rooms = {"Enemies":[],
                              "Staircase":[],
                              "Shop":[]}
    for i in range(how_many_enemies_to_spawn):
        list_of_xs = list(dictionary_for_inside_room)
        random_x = random.randint(0,len(list_of_xs)-1)
        actual_x = list_of_xs[random_x]
        random_y = random.randint(0,len(dictionary_for_inside_room[actual_x])-1)
        actual_y = dictionary_for_inside_room[actual_x][random_y]
        stuff_inside_the_rooms["Enemies"].append([actual_x*75,actual_y*75])
        dictionary_for_inside_room[actual_x].remove(actual_y)
    how_many_shops_to_spawn = random.randint(0,2)
    for i in range(how_many_shops_to_spawn):
        list_of_xs = list(dictionary_for_inside_room)
        random_x = random.randint(0, len(list_of_xs) - 1)
        actual_x = list_of_xs[random_x]
        random_y = random.randint(0, len(dictionary_for_inside_room[actual_x]) - 1)
        actual_y = dictionary_for_inside_room[actual_x][random_y]
        stuff_inside_the_rooms["Shop"].append([actual_x*75, actual_y*75])
        dictionary_for_inside_room[actual_x].remove(actual_y)
    has_staircase_spawned = True
    while has_staircase_spawned:
        list_of_xs = list(dictionary_for_inside_room)
        random_x = random.randint(0, len(list_of_xs) - 1)
        actual_x = list_of_xs[random_x]
        random_y = random.randint(0, len(dictionary_for_inside_room[actual_x]) - 1)
        actual_y = dictionary_for_inside_room[actual_x][random_y]
        array_for_binary = list_of_xs
        array_for_binary.sort()
        found = binary_search_procedural_generation(array_for_binary,actual_x+1)
        if found:
            array_for_binary = dictionary_for_inside_room[actual_x+1]
            array_for_binary.sort()
            found = binary_search_procedural_generation(array_for_binary,actual_y+1)
            if found:
                has_staircase_spawned = False
                stuff_inside_the_rooms["Staircase"].append([actual_x*75,actual_y*75])
    return stuff_inside_the_rooms

"""Name: combine_walls
    Parameters: dictionary_for_walls_procedural = dictionary
    Returns: walls_sent_for_conversion = dictionary
    Purpose:This combines walls next to each other into one larger walls so when it gets sent to the main server to be
    converted into another dictionary there is a lot less making it more efficient 
    """

def combine_walls(dictionary_for_walls_procedural):
    total = 0
    for i in dictionary_for_walls_procedural:
        for t in dictionary_for_walls_procedural[i]:
            total += 1
    walls_to_be_sent_for_conversion = []
    list_of_keys_in_order = list(dictionary_for_walls_procedural)
    list_of_keys_in_order.sort()
    """magnifier_procedural_generation = 75"""
    magnifier_procedural_generation = 5
    while dictionary_for_walls_procedural:
        horizontal_to_remove = []
        vertical_to_remove = []
        width_horizontal = 1
        height_vertical = 1
        first_position = list_of_keys_in_order[0]
        x_h = x_v = current_x_h = current_x_v = first_position
        y_h = y_v = current_y_h = current_y_v = dictionary_for_walls_procedural[first_position][0]
        horizontal_to_remove.append([x_h,y_h])
        vertical_to_remove.append([x_h,y_h])
        forwards_horizontal_check = True
        while forwards_horizontal_check:
            array_sorted_for_binary = dictionary_for_walls_procedural[first_position]
            array_sorted_for_binary.sort()
            found = binary_search_procedural_generation(array_sorted_for_binary,current_y_h+1)
            if found:
                current_y_h += 1
                width_horizontal += 1
                horizontal_to_remove.append([current_x_h,current_y_h])
            else:
                forwards_horizontal_check = False
        backwards_horizontal_check = True
        while backwards_horizontal_check:
            array_sorted_for_binary = dictionary_for_walls_procedural[first_position]
            array_sorted_for_binary.sort()
            found = binary_search_procedural_generation(array_sorted_for_binary, y_h - 1)
            if found:
                y_h -= 1
                width_horizontal += 1
                horizontal_to_remove.append([x_h,y_h])
            else:
                backwards_horizontal_check = False
        forwards_vertical_check = True
        while forwards_vertical_check:
            found = binary_search_procedural_generation(list_of_keys_in_order,current_x_v+1)
            if found:
                array_sorted_for_binary = dictionary_for_walls_procedural[current_x_v+1]
                array_sorted_for_binary.sort()
                found = binary_search_procedural_generation(array_sorted_for_binary,current_y_v)
                if found:
                    current_x_v += 1
                    height_vertical += 1
                    vertical_to_remove.append([current_x_v,current_y_v])
                else:
                    forwards_vertical_check = False
            else:
                forwards_vertical_check = False
        backwards_vertical_check = True
        while backwards_vertical_check:
            found = binary_search_procedural_generation(list_of_keys_in_order,x_v-1)
            if found:
                array_sorted_for_binary = dictionary_for_walls_procedural[x_v-1]
                array_sorted_for_binary.sort()
                found = binary_search_procedural_generation(array_sorted_for_binary,y_v)
                if found:
                    x_v -= 1
                    height_vertical += 1
                    vertical_to_remove.append([x_v,y_v])
                else:
                    backwards_vertical_check = False
            else:
                backwards_vertical_check = False
        if len(vertical_to_remove) > len(horizontal_to_remove):
            walls_to_be_sent_for_conversion.append([x_v*magnifier_procedural_generation,y_v*magnifier_procedural_generation,height_vertical*magnifier_procedural_generation,magnifier_procedural_generation])
            for keys in vertical_to_remove:
                dictionary_for_walls_procedural[keys[0]].remove(keys[1])
                if not dictionary_for_walls_procedural[keys[0]]:
                    del dictionary_for_walls_procedural[keys[0]]
                    found = binary_search_procedural_generation(list_of_keys_in_order,keys[0])
                    if found:
                        list_of_keys_in_order.remove(keys[0])
        else:
            walls_to_be_sent_for_conversion.append([x_h*magnifier_procedural_generation,y_h*magnifier_procedural_generation,magnifier_procedural_generation,width_horizontal*magnifier_procedural_generation])
            for keys in horizontal_to_remove:
                dictionary_for_walls_procedural[keys[0]].remove(keys[1])
            if not dictionary_for_walls_procedural[first_position]:
                del dictionary_for_walls_procedural[first_position]
                list_of_keys_in_order.remove(first_position)
    return walls_to_be_sent_for_conversion

"""Name: repeat_for_create_corridor_walls
    Parameters:dictionary_for_binary = dictionary,keys = integer,key = integer,can_wall_block_be_placed = boolean
    Returns:True = boolean,False = boolean
    Purpose:This is to help reduce the number of lines there is by having the code be the same but changing the 
    parameters.It checks the position of the coordinates with the dictionary to see if it is there and it is it will
    return true but if it isnt it will return false which gets assigned to can_wall_block_be_placed which gets used 
    in place_the_wall
    """

def repeat_for_create_corridor_walls(dictionary_for_binary,keys,key,can_wall_block_be_placed):
    if can_wall_block_be_placed:
        array_sorted = list(dictionary_for_binary)
        array_sorted.sort()
        found = binary_search_procedural_generation(array_sorted,keys)
        if found:
            array_sorted_2 = dictionary_for_binary[keys]
            array_sorted_2.sort()
            found = binary_search_procedural_generation(array_sorted_2,key)
            if found:
                return False
    else:
        return False
    return True

""" Name:place_the_wall
    Parameters:dictionary_for_walls_procedural = dictionary,keys = integer,key = integer,
    can_wall_block_be_placed = boolean 
    Returns: None
    Purpose: This sees if can_wall_block_be_placed is true and if there is already a key with the value (x-coordinate)
    and if there is it will append the y coordinate to it but if there isnt a key with it will make the new key and 
    then append the y coordinate
    """

def place_the_wall(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed):
    if can_wall_block_be_placed:
        array_sorted = list(dictionary_for_walls_procedural)
        array_sorted.sort()
        found = binary_search_procedural_generation(array_sorted, keys)
        if found:
            dictionary_for_walls_procedural[keys].append(key)
        else:
            dictionary_for_walls_procedural[keys] = [key]

""" Name: more_precise_corridor_walls
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary,
    dictionary_for_walls_procedural = dictionary,keys = integer,key = integer
    Returns: None
    Purpose: To shorten the amount of lines of code. This uses the function of repeat_for_create_corridor_walls but 
    changes the dictionary that needs to be checked this is because i need it to be compared to everything to make sure
    nothing is in the way before placing the wall.
    """

def more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key):
    can_wall_block_be_placed = True
    can_wall_block_be_placed = repeat_for_create_corridor_walls(permanent_dictionary_for_corridor,keys,key,can_wall_block_be_placed)
    can_wall_block_be_placed = repeat_for_create_corridor_walls(dictionary_for_doorway,keys,key,can_wall_block_be_placed)
    can_wall_block_be_placed = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed)
    place_the_wall(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed)

""" Name: create_corridor_walls
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary,
    dictionary_for_walls_procedural = dictionary
    Returns:None
    Purpose: This loops through all the coordinates and then checks the surrounding coordinates to see if there is
    anything already there. 
    """
def create_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural):
    for keys in permanent_dictionary_for_corridor:
        for key in permanent_dictionary_for_corridor[keys]:
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key+1)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key-1)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key+1)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key-1)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key+1)
            more_precise_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key-1)

""" Name: place_the_doorway_wall
    Parameters: can_wall_block_be_placed = boolean,walls_destroyed_from_doorway = dictionary,
    keys = integer,key = integer,dictionary_for_walls_procedural = dictionary
    Returns:None
    Purpose: It uses binary search to see if there is something already at that coordinate the thing being checked
    changes with the parameter dictionary_for_walls_procedural if there is something there is will not place the wall
    but if there is something it will not do anything
    """

def place_the_doorway_wall(can_wall_block_be_placed,walls_destroyed_from_doorway,keys,key,dictionary_for_walls_procedural):
    if can_wall_block_be_placed:
        array_sorted = list(walls_destroyed_from_doorway)
        array_sorted.sort()
        found = binary_search_procedural_generation(array_sorted,keys)
        if not found:
            place_the_wall(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed)
        else:
            array_sorted = walls_destroyed_from_doorway[keys]
            array_sorted.sort()
            found = binary_search_procedural_generation(array_sorted,key)
            if not found:
                place_the_wall(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed)

""" Name: more_precise_doorway_walls
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary,
    dictionary_for_walls = dictionary,keys = integer,key = integer,
    walls_destroyed_from_doorway
    Returns: None
    Purpose: It sets up the can_wall_block_be_placed to be true. It then goes through other functions which can return
    true or false to change the variable can_wall_block_be_placed it then passes that variable to another function
    called place_the_doorway_walls 
    """

def more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key,walls_destroyed_from_doorway):
    can_wall_block_be_placed = True
    can_wall_block_be_placed = repeat_for_create_corridor_walls(permanent_dictionary_for_corridor,keys,key,can_wall_block_be_placed)
    can_wall_block_be_placed = repeat_for_create_corridor_walls(dictionary_for_doorway,keys,key,can_wall_block_be_placed)
    can_wall_block_be_placed = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys,key,can_wall_block_be_placed)
    place_the_doorway_wall(can_wall_block_be_placed,walls_destroyed_from_doorway,keys,key,dictionary_for_walls_procedural)

""" Name: create_doorway_walls
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary,
    dictionary_for_walls_procedural = dictionary
    Returns: None
    Purpose: it loops through the coordinates of all the doorways then goes to a function to check all surrounding 
    coordinates 
    """

def create_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,walls_destroyed_from_doorway):
    for keys in dictionary_for_doorway:
        for key in dictionary_for_doorway[keys]:
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key+1,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys,key-1,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key+1,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys+1,key-1,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key+1,walls_destroyed_from_doorway)
            more_precise_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,keys-1,key-1,walls_destroyed_from_doorway)

""" Name: adding_to_dictionary
    Parameters: dictionary_that_needs_the_adding = dictionary,keys = integer,key = integer
    Returns: None
    Purpose: It checks to if the key is already in the dictionary and if it is it will just add the second value to the
    key but if it isnt there it will create the key and the add the second value
    """

def adding_to_dictionary(dictionary_that_needs_the_adding,keys,key):
    array_sorted = list(dictionary_that_needs_the_adding)
    array_sorted.sort()
    found = binary_search_procedural_generation(array_sorted,keys)
    if found:
        dictionary_that_needs_the_adding[keys].append(key)
    else:
        dictionary_that_needs_the_adding[keys] = [key]

""" Name: destroy_room_doors_entrance
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary,
    dictionary_for_walls_procedural = dictionary
    Returns: walls_destroyed_from_doorway = dictionary
    Purpose: This checks to see if there is a wall in the north,south,east,west of the doorway coordinate and if there 
    is a wall it will get rid of that wall block and then add the coordinate to another dictionary called
    walls_destroyed_from_doorway to make sure a wall is not placed back into that hole.
    """

def destroy_room_doors_entrance(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural):
    walls_destroyed_from_doorway = {}
    for keys in dictionary_for_doorway:
        for key in dictionary_for_doorway[keys]:
            destroy_wall = True
            destroy_wall = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys,key+1,destroy_wall)
            if not destroy_wall:
                dictionary_for_walls_procedural[keys].remove(key+1)
                if not walls_destroyed_from_doorway:
                    walls_destroyed_from_doorway[keys] = [key+1]
                else:
                    adding_to_dictionary(walls_destroyed_from_doorway,keys,key+1)
            destroy_wall = True
            destroy_wall = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys,key-1,destroy_wall)
            if not destroy_wall:
                dictionary_for_walls_procedural[keys].remove(key-1)
                adding_to_dictionary(walls_destroyed_from_doorway,keys,key-1)
            destroy_wall = True
            destroy_wall = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys+1,key,destroy_wall)
            if not destroy_wall:
                dictionary_for_walls_procedural[keys+1].remove(key)
                adding_to_dictionary(walls_destroyed_from_doorway,keys+1,key)
            destroy_wall = True
            destroy_wall = repeat_for_create_corridor_walls(dictionary_for_walls_procedural,keys-1,key,destroy_wall)
            if not destroy_wall:
                dictionary_for_walls_procedural[keys-1].remove(key)
                adding_to_dictionary(walls_destroyed_from_doorway,keys-1,key)
    return walls_destroyed_from_doorway

""" Name: get_rid_of_extra_corridor
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary
    Returns: None
    Purpose: This checks the surrounding coordinates of the corridor coordinates and sees if it connects to another
    corridor piece or doorway if it only connects to one it will get rid of the corridor. It will keep repeating until
    there is no other corridor pieces to get rid off where it will finish.
    """

def get_rid_of_extra_corridor(permanent_dictionary_for_corridor,dictionary_for_doorway):
    true = True
    while true:
        true = False
        print(permanent_dictionary_for_corridor)
        for key in permanent_dictionary_for_corridor:
            if permanent_dictionary_for_corridor[key]:
                for keys in permanent_dictionary_for_corridor[key]:
                    i = 0
                    if key - 1 >= list(permanent_dictionary_for_corridor)[0]:
                        if permanent_dictionary_for_corridor[key-1]:
                            found = binary_search_procedural_generation(permanent_dictionary_for_corridor[key-1],keys)
                            if found:
                                i += 1
                    if key + 1 <= list(permanent_dictionary_for_corridor)[len(list(permanent_dictionary_for_corridor))-1]:
                        if permanent_dictionary_for_corridor[key+1]:
                            found = binary_search_procedural_generation(permanent_dictionary_for_corridor[key+1],keys)
                            if found:
                                i += 1
                    if permanent_dictionary_for_corridor[key]:
                        found = binary_search_procedural_generation(permanent_dictionary_for_corridor[key],keys-1)
                        if found:
                            i += 1
                    if permanent_dictionary_for_corridor[key]:
                        found = binary_search_procedural_generation(permanent_dictionary_for_corridor[key],keys+1)
                        if found:
                            i += 1
                    for doorway_key in dictionary_for_doorway:
                        for second_doorway_key in dictionary_for_doorway[doorway_key]:
                            if (doorway_key == key -1 and second_doorway_key == keys) or (doorway_key == key + 1 and second_doorway_key == keys):
                                i += 1
                            if doorway_key == key and (second_doorway_key == keys+1 or second_doorway_key == keys - 1):
                                i += 1
                    if i < 2:
                        permanent_dictionary_for_corridor[key].remove(keys)
                        true = True

""" Name: repeat_of_rid_extra_doorway
    Parameters: i = integer,permanent_dictionary_for_corridor = dictionary,keys = integer,key = integer
    Returns: i = integer
    Purpose: This checks the surrounding coordinates using binary search if it is found it will then add one to i and
    return that value
    """

def repeat_of_rid_extra_doorway(i,permanent_dictionary_for_corridor,keys,key):
    array_sorted = list(permanent_dictionary_for_corridor)
    array_sorted.sort()
    found = binary_search_procedural_generation(array_sorted, keys)
    if found:
        array_sorted = permanent_dictionary_for_corridor[keys]
        array_sorted.sort()
        found = binary_search_procedural_generation(array_sorted,key)
        if found:
            i += 1
    return i

""" Name: get_rid_of_extra_doorway
    Parameters: permanent_dictionary_for_corridor = dictionary,dictionary_for_doorway = dictionary
    Returns: None
    Purpose: It sets up the array called doorways_to_pop and loops through all the doorway coordinates it then goes to
    the function of repeat_of_rid_extra_doorway to see if i will change. If i is less than one it will get rid of that 
    y coordinate and if there is nothing else to the x value it will then get rid of the key.It will then run through
    all doorways to pop and get rid of them in the doorway dictionary
    """

def get_rid_of_extra_doorway(permanent_dictionary_for_corridor,dictionary_for_doorway):
    doorways_to_pop = []
    for keys in dictionary_for_doorway:
        for key in dictionary_for_doorway[keys]:
            i = 0
            i = repeat_of_rid_extra_doorway(i,permanent_dictionary_for_corridor,keys,key+1)
            if i != 1:
                i = repeat_of_rid_extra_doorway(i,permanent_dictionary_for_corridor,keys,key-1)
            if i != 1:
                i = repeat_of_rid_extra_doorway(i,permanent_dictionary_for_corridor,keys+1,key)
            if i != 1:
                i = repeat_of_rid_extra_doorway(i,permanent_dictionary_for_corridor,keys-1,key)
            if i < 1:
                dictionary_for_doorway[keys].remove(key)
            if not dictionary_for_doorway[keys]:
                doorways_to_pop.append(keys)
    if doorways_to_pop:
        for keys in doorways_to_pop:
            del dictionary_for_doorway[keys]

""" Name: more_precise_creation_doorways
    Parameters:side_y = integer,side_x = integer,x_number = integer ,y_number = integer,
    permanent_dictionary_for_corridor = dictionary,permanent_dictionary_for_corridor_with_id = dictionary,
    corridor_id_checked = boolean
    Return: None
    Purpose: It checks if there is a corridor coordinate next to a wall coordinates piece in the 4 directions and if 
    there is it will add it to a possible doorway which will be randomly selected in create_doorways
    """

def more_precise_creation_doorways(side_y,side_x,x_number,y_number,permanent_dictionary_for_corridor,
                                              permanent_dictionary_for_corridor_with_id,corridor_id_checked):
        if permanent_dictionary_for_corridor[side_x + x_number]:
            found = binary_search_procedural_generation(permanent_dictionary_for_corridor[side_x + x_number],side_y + y_number)
            if found:
                corridor_id_2 = permanent_dictionary_for_corridor_with_id[side_x + x_number][side_y+y_number]
                if not corridor_id_checked:
                    corridor_id_checked[corridor_id_2] = [[side_x + int(x_number/2), side_y+int(y_number/2)]]
                else:
                    true = True
                    for corridor_id_loop in corridor_id_checked:
                        if corridor_id_loop == corridor_id_2:
                            corridor_id_checked[corridor_id_loop].append([side_x + int(x_number/2), side_y+int(y_number/2)])
                            true = False
                    if true:
                        corridor_id_checked[corridor_id_2] = [[side_x + int(x_number/2), side_y+int(y_number/2)]]

""" Name: create_doorways
    Parameters: permanent_dictionary_for_corridor = dictionary,permanent_dictionary_for_corridor_with_id = dictionary,
    dictionary_for_procedural_generation_with_id = dictionary,dictionary_for_walls_procedural = dictionary
    Returns:None
    Purpose: It creates all the variables to allow to see if a wall piece is 2 blocks away from a corridor piece this 
    then gets added to an array which gets randomly selected at the this means that one room will be put to every
    different corridor.
    """

def create_doorways(permanent_dictionary_for_corridor,permanent_dictionary_for_corridor_with_id,dictionary_for_procedural_generation_with_id,dictionary_for_walls_procedural):
    dictionary_for_doorway = {}
    for key in dictionary_for_procedural_generation_with_id:
        corridor_id_checked = {}
        top_array_of_ys = []
        bottom_array_of_ys = []
        top_side_x = dictionary_for_procedural_generation_with_id[key][list(dictionary_for_procedural_generation_with_id[key])[0]][0]
        length = len(dictionary_for_procedural_generation_with_id[key][list(dictionary_for_procedural_generation_with_id[key])[0]])-1
        bottom_side_x = dictionary_for_procedural_generation_with_id[key][list(dictionary_for_procedural_generation_with_id[key])[0]][length]
        left_side_array_of_xs = dictionary_for_procedural_generation_with_id[key][list(dictionary_for_procedural_generation_with_id[key])[0]].copy()
        left_side_y = list(dictionary_for_procedural_generation_with_id[key])[0]
        right_side_array_of_xs = left_side_array_of_xs.copy()
        right_side_y = list(dictionary_for_procedural_generation_with_id[key])[len(dictionary_for_procedural_generation_with_id[key])-1]
        for keys in dictionary_for_procedural_generation_with_id[key]:
            bottom_array_of_ys.append(keys)
            top_array_of_ys.append(keys)
        bottom_array_of_ys.pop(0)
        bottom_array_of_ys.pop(len(bottom_array_of_ys)-1)
        top_array_of_ys.pop(0)
        top_array_of_ys.pop(len(top_array_of_ys)-1)
        left_side_array_of_xs.pop(0)
        left_side_array_of_xs.pop(len(left_side_array_of_xs)-1)
        right_side_array_of_xs.pop(0)
        right_side_array_of_xs.pop(len(right_side_array_of_xs)-1)
        while len(left_side_array_of_xs) != 0:
            random_number = random.randint(0, len(left_side_array_of_xs) - 1)
            random_x_from_array = left_side_array_of_xs[random_number]
            left_side_array_of_xs.pop(random_number)
            if left_side_y - 2 >= list(permanent_dictionary_for_corridor)[0]:
                more_precise_creation_doorways(random_x_from_array,left_side_y,-2,0,permanent_dictionary_for_corridor,
                                               permanent_dictionary_for_corridor_with_id,corridor_id_checked)
        while len(right_side_array_of_xs) != 0:
            random_number = random.randint(0, len(right_side_array_of_xs) - 1)
            random_x_from_array = right_side_array_of_xs[random_number]
            right_side_array_of_xs.pop(random_number)
            if right_side_y + 2 <= list(permanent_dictionary_for_corridor)[len(list(permanent_dictionary_for_corridor)) - 1]:
                more_precise_creation_doorways(random_x_from_array,right_side_y,2,0,permanent_dictionary_for_corridor,
                                               permanent_dictionary_for_corridor_with_id,corridor_id_checked)
        while len(top_array_of_ys) != 0:
            random_number = random.randint(0, len(top_array_of_ys) - 1)
            random_x_from_array = top_array_of_ys[random_number]
            top_array_of_ys.pop(random_number)
            if random_x_from_array - 2 >= list(permanent_dictionary_for_corridor)[0]:
                more_precise_creation_doorways(top_side_x,random_x_from_array,0,-2,permanent_dictionary_for_corridor,
                                               permanent_dictionary_for_corridor_with_id,corridor_id_checked)
        while len(bottom_array_of_ys) != 0:
            random_number = random.randint(0,len(bottom_array_of_ys)-1)
            random_x_from_array = bottom_array_of_ys[random_number]
            bottom_array_of_ys.pop(random_number)
            if random_x_from_array + 2 <= list(permanent_dictionary_for_corridor)[len(list(permanent_dictionary_for_corridor))-1]:
                more_precise_creation_doorways(bottom_side_x,random_x_from_array,0,2,permanent_dictionary_for_corridor,
                                               permanent_dictionary_for_corridor_with_id,corridor_id_checked)
        for key in corridor_id_checked:
            random_number = random.randint(0,len(corridor_id_checked[key])-1)
            if not dictionary_for_doorway:
                dictionary_for_doorway[corridor_id_checked[key][random_number][0]] = [corridor_id_checked[key][random_number][1]]
            else:
                true = True
                for keys in dictionary_for_doorway:
                    if keys == corridor_id_checked[key][random_number][0]:
                        dictionary_for_doorway[corridor_id_checked[key][random_number][0]].append(corridor_id_checked[key][random_number][1])
                        true = False
                if true:
                    dictionary_for_doorway[corridor_id_checked[key][random_number][0]] = [corridor_id_checked[key][random_number][1]]
    get_rid_of_extra_corridor(permanent_dictionary_for_corridor,dictionary_for_doorway)
    get_rid_of_extra_doorway(permanent_dictionary_for_corridor,dictionary_for_doorway)
    walls_destroyed_from_doorway = destroy_room_doors_entrance(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural)
    create_doorway_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural,walls_destroyed_from_doorway)
    create_corridor_walls(permanent_dictionary_for_corridor,dictionary_for_doorway,dictionary_for_walls_procedural)

""" Name: corridor_check_availability
    Parameters: x = integer,y = integer,permanent_dictionary_for_corridor_with_id = dictionary,corridor_id = integer
    Returns: None
    Purpose: It sees if there is an x value already in the dictionary and if so it will just assign the y and corridor 
    id to it but if there is no x value already it will add the x value as a key and assign another dictionary to it
    which then the y will add as a second key and corridor id to the value
    """

def corridor_check_availability(x,y,permanent_dictionary_for_corridor_with_id,corridor_id):
    array_sorted = list(permanent_dictionary_for_corridor_with_id)
    array_sorted.sort()
    found = binary_search_procedural_generation(array_sorted,x)
    if found:
        permanent_dictionary_for_corridor_with_id[x][y] = corridor_id
    else:
        permanent_dictionary_for_corridor_with_id[x] = {}
        permanent_dictionary_for_corridor_with_id[x][y] = corridor_id

""" Name: more_precise_creation_corridor
    Parameters: dictionary_for_open_spaces = dictionary,x = integer,y = integer,x_number = integer,
    y_number = integer,permanent_dictionary_for_corridor = dictionary
    Returns: check_availability = boolean
    Purpose: This function serves to shorten the line count by having the necessary variables set as parameters. It 
    checks to see if the corridor block next to the current one and if there it will then set the check_availability to
    False and then returns this variable.
    """

def more_precise_creation_corridor(dictionary_for_open_spaces,x,y,x_number,y_number,permanent_dictionary_for_corridor):
    if dictionary_for_open_spaces[x + x_number]:
        found = binary_search_procedural_generation(dictionary_for_open_spaces[x + x_number], y)
        if found:
            check_availability = True
            if permanent_dictionary_for_corridor[x + x_number]:
                permanent_dictionary_for_corridor[x + x_number].sort()
                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x + x_number], y - 1)
                if found:
                    check_availability = False
                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x + x_number], y + 1)
                if found:
                    check_availability = False
            return check_availability

""" Name: loops_allowed
    Parameters: x = integer, y = integer, x_number = integer, y_number = integer, permanent_dictionary_for_corridor = dictionary
    check_availability = boolean, chance_of_loops_allowed = integer
    Return: check_availability = boolean
    Purpose: This allows for loops if the person with the code changes the random_number_for_loop with the the greater
    the number the more likely there is a loop to generate. This is done by checking 2 blocks that the side is trying
    to generate to and if there is it will then set check availability to False and then return the new boolean value"""

def loops_allowed(x,y,x_number,y_number,permanent_dictionary_for_corridor,check_availability,chance_of_loops_allowed):
    random_number_for_loop = random.randint(1,chance_of_loops_allowed)
    if random_number_for_loop == 1:
        array_ordered = permanent_dictionary_for_corridor[x + x_number]
        array_ordered.sort()
        found = binary_search_procedural_generation(array_ordered, y+y_number)
        if found:
            check_availability = False
        return check_availability

"""Name: create_corridors
    Parameters: dictionary_for_open_spaces = dictionary, permanent_dictionary_for_corridor = dictionary,
    array_corridor_creation = array, permanent_dictionary_for_corridor_with_id = dictionary, corridor_id = integer
    Return: None
    Purpose: this creates the corridors by using a depth first search with restrictions which include not allowing 2 
    corridor blocks next to each other, not going out of the area, that it cant go back where it came from for example
    if the previous went left the new one cant go to the right, and it will check 2 to the direction it is going to make
    sure that there isnt a loop. This puts all the corridor blocks coordinates inside a corridor dictionary
    """

def create_corridors(dictionary_for_open_spaces,permanent_dictionary_for_corridor,array_corridor_creation,permanent_dictionary_for_corridor_with_id,corridor_id):
    chance_of_loops_allowed = 1 #
    while len(array_corridor_creation) != 0:
        direction_array = [1,2,3,4]
        while len(direction_array) != 0:
            if len(array_corridor_creation) > 2:
                direction_check = array_corridor_creation[len(array_corridor_creation)-2][2]
                if direction_check == 1:
                    number_to_be_checked = 3
                elif direction_check == 2:
                    number_to_be_checked = 4
                elif direction_check == 3:
                    number_to_be_checked = 1
                else:
                    number_to_be_checked = 2
                for direct in direction_array:
                    if direct == number_to_be_checked:
                        direction_array.remove(number_to_be_checked)
            random_number = random.randint(0,len(direction_array)-1)
            direction = direction_array[random_number]
            x = array_corridor_creation[len(array_corridor_creation)-1][0]
            y = array_corridor_creation[len(array_corridor_creation)-1][1]
            if direction == 1:
                if x-1 >= list(dictionary_for_open_spaces)[0]:
                    check_availability = more_precise_creation_corridor(dictionary_for_open_spaces,x,y,-1,0,
                                                                        permanent_dictionary_for_corridor)
                    if chance_of_loops_allowed != 0:
                        if x - 2 >= list(permanent_dictionary_for_corridor)[0]:
                            check_availability = loops_allowed(x,y,-2,0,permanent_dictionary_for_corridor,
                                                               check_availability,chance_of_loops_allowed)
                    if check_availability:
                        corridor_check_availability(x-1,y,permanent_dictionary_for_corridor_with_id,corridor_id)
                        permanent_dictionary_for_corridor[x-1].append(y)
                        array_corridor_creation.append([x-1,y,1])
                        dictionary_for_open_spaces[x-1].remove(y)
                        direction_array = [1,2,4]
                    else:
                        direction_array.remove(direction)
                else:
                    direction_array.remove(direction)
            elif direction == 3:
                if x+1 <= list(dictionary_for_open_spaces)[len(dictionary_for_open_spaces)-1]:
                    check_availability = more_precise_creation_corridor(dictionary_for_open_spaces,x,y,1,0,
                                                                        permanent_dictionary_for_corridor)
                    if check_availability:
                        if chance_of_loops_allowed != 0:
                            if x + 2 <= list(permanent_dictionary_for_corridor)[len(permanent_dictionary_for_corridor) - 1]:
                                check_availability = loops_allowed(x,y,2,0,permanent_dictionary_for_corridor,
                                                                   check_availability,chance_of_loops_allowed)
                    if check_availability == True:
                        corridor_check_availability(x+1,y,permanent_dictionary_for_corridor_with_id,corridor_id)
                        permanent_dictionary_for_corridor[x+1].append(y)
                        array_corridor_creation.append([x+1,y,3])
                        dictionary_for_open_spaces[x+1].remove(y)
                        direction_array = [2,3,4]
                    else:
                        direction_array.remove(direction)
                else:
                    direction_array.remove(direction)
            if dictionary_for_open_spaces[x]:
                if direction == 2:
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y+1)
                    if found:
                        check_availability = True
                        if x - 1 >= list(permanent_dictionary_for_corridor)[0]:
                            if permanent_dictionary_for_corridor[x-1]:
                                permanent_dictionary_for_corridor[x-1].sort()
                                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x-1],y+1)
                                if found:
                                    check_availability = False
                        if x + 1 <= list(permanent_dictionary_for_corridor)[len(permanent_dictionary_for_corridor) - 1]:
                            if permanent_dictionary_for_corridor[x+1]:
                                permanent_dictionary_for_corridor[x+1].sort()
                                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x+1],y+1)
                                if found:
                                    check_availability = False
                        if check_availability:
                            if chance_of_loops_allowed != 0:
                                check_availability = loops_allowed(x,y,0,2,permanent_dictionary_for_corridor,
                                              check_availability,chance_of_loops_allowed)
                        if check_availability:
                            corridor_check_availability(x,y+1,permanent_dictionary_for_corridor_with_id,corridor_id)
                            permanent_dictionary_for_corridor[x].append(y+1)
                            array_corridor_creation.append([x,y+1,2])
                            dictionary_for_open_spaces[x].remove(y+1)
                            direction_array = [1,2,3]
                        else:
                            direction_array.remove(direction)
                    else:
                        direction_array.remove(direction)
                elif direction == 4:
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y-1)
                    if found:
                        check_availability = True
                        if x - 1 >= list(permanent_dictionary_for_corridor)[0]:
                            if permanent_dictionary_for_corridor[x - 1]:
                                permanent_dictionary_for_corridor[x - 1].sort()
                                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x - 1],y - 1)
                                if found:
                                    check_availability = False
                        if x + 1 <= list(permanent_dictionary_for_corridor)[len(permanent_dictionary_for_corridor) - 1]:
                            if permanent_dictionary_for_corridor[x + 1]:
                                permanent_dictionary_for_corridor[x + 1].sort()
                                found = binary_search_procedural_generation(permanent_dictionary_for_corridor[x + 1],y - 1)
                                if found:
                                    check_availability = False
                        if check_availability:
                            if chance_of_loops_allowed != 0:
                                check_availability = loops_allowed(x,y,0,-2,permanent_dictionary_for_corridor,
                                                                   check_availability,chance_of_loops_allowed)
                        if check_availability:
                            corridor_check_availability(x,y-1,permanent_dictionary_for_corridor_with_id,corridor_id)
                            permanent_dictionary_for_corridor[x].append(y-1)
                            array_corridor_creation.append([x,y-1,4])
                            dictionary_for_open_spaces[x].remove(y-1)
                            direction_array = [1,3,4]
                        else:
                            direction_array.remove(direction)
                    else:
                        direction_array.remove(direction)
            else:
                if direction == 2 or direction == 4:
                    direction_array.remove(direction)
            if len(direction_array) == 0:
                if x-1 >= list(dictionary_for_open_spaces)[0]:
                    if dictionary_for_open_spaces[x-1]:
                        found = binary_search_procedural_generation(dictionary_for_open_spaces[x-1],y)
                        if found:
                            dictionary_for_open_spaces[x-1].remove(y)
                if x+1 <= list(dictionary_for_open_spaces)[len(dictionary_for_open_spaces)-1]:
                    if dictionary_for_open_spaces[x+1]:
                        found = binary_search_procedural_generation(dictionary_for_open_spaces[x+1],y)
                        if found:
                            dictionary_for_open_spaces[x+1].remove(y)
                if dictionary_for_open_spaces[x]:
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y+1)
                    if found:
                        dictionary_for_open_spaces[x].remove(y+1)
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y-1)
                    if found:
                        dictionary_for_open_spaces[x].remove(y-1)
                array_corridor_creation.pop(len(array_corridor_creation)-1)

""" Name: spawn_root_corridor
    Parameters:how_many_left = integer,how_many_right = integer,how_many_up = integer,how_many_down = integer,
    dictionary_for_procedural_generation = dictionary,dictionary_for_procedural_generation_with_id = dictionary,
    dictionary_for_open_spaces = dictionary,dictionary_for_walls_procedural = dictionary
    Returns: None
    Purpose: This randomly generates the first block of the corridor where the rest of the corridor will be continued
    on. This function will be run again when the corridor is finished and then it will check to see if there is 
    available space for another root of the corridor if not it will run the next function.
    """

def spawn_root_corridor(how_many_left,how_many_right,how_many_up,how_many_down,dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,dictionary_for_open_spaces,dictionary_for_walls_procedural):
    permanent_dictionary_for_corridor = {}
    permanent_dictionary_for_corridor_with_id = {}
    list_of_x_values = list(dictionary_for_open_spaces)
    corridor_id = 0
    for x in range(how_many_left,how_many_right+1):
        permanent_dictionary_for_corridor[x] = []
    true = True
    while true:
        list_of_things_to_pop = []
        for key in list_of_x_values:
            if not dictionary_for_open_spaces[key]:
                list_of_things_to_pop.append(key)
        for key in list_of_things_to_pop:
            list_of_x_values.remove(key)
        if list_of_x_values:
            array_corridor_creation = []
            random_x = random.randint(0,len(list_of_x_values)-1)
            x = list_of_x_values[random_x]
            y = random.randint(how_many_up,how_many_down)
            if dictionary_for_open_spaces[x]:
                found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y)
                if found:
                    corridor_id += 1
                    if not permanent_dictionary_for_corridor_with_id:
                        permanent_dictionary_for_corridor_with_id[x] = {}
                        permanent_dictionary_for_corridor_with_id[x][y] = corridor_id
                    else:
                        corridor_check_availability(x,y,permanent_dictionary_for_corridor_with_id,corridor_id)
                    permanent_dictionary_for_corridor[x].append(y)
                    array_corridor_creation.append([x,y,0])
                    dictionary_for_open_spaces[x].remove(y)
                    create_corridors(dictionary_for_open_spaces,permanent_dictionary_for_corridor,array_corridor_creation,permanent_dictionary_for_corridor_with_id,corridor_id)
        else:
            true = False
            for key in permanent_dictionary_for_corridor:
                permanent_dictionary_for_corridor[key].sort()
    create_doorways(permanent_dictionary_for_corridor,permanent_dictionary_for_corridor_with_id,dictionary_for_procedural_generation_with_id,dictionary_for_walls_procedural)

""" Name: binary_search_procedural_generation
    Parameters: array,number_that_needs_to_be_found
    Returns: "found" = string,"not found" = string
    Purpose: This searches an array by going to the middle of the array and seeing if it is the number
    if it is it will return found but if it isnt it will see if the middle number is larger or smaller than one being 
    found. If the middle number is smaller it will get rid of the bottom half of the array but if its larger it will 
    get rid of the top half then itll find the middle number. This carries on repeating until there is no more
    numbers in the array where it will return false or if the number is found 
    """

def binary_search_procedural_generation(array,number_that_needs_to_be_found):
    top_number = len(array) - 1
    bottom_number = 0
    while bottom_number <= top_number:
        mid_point = (bottom_number + top_number) // 2
        if array[mid_point] < number_that_needs_to_be_found:
            bottom_number = mid_point + 1
        elif array[mid_point] > number_that_needs_to_be_found:
            top_number = mid_point - 1
        else:
            return True
    return False

""" Name: create_room
    Parameters: dictionary_for_procedural_generation = dictionary,
    dictionary_for_procedural_generation_with_id = dictionary,dictionary_for_inside_room = dictionary,
    dictionary_for_open_spaces = dictionary,random_x = integer,random_y = integer,width_of_room = integer,
    height_of_room = integer,block_of_wall_id = integer,inside_block_id = integer,room_id = integer,
    dictionary_for_walls_procedural = dictionary
    Returns: block_of_wall_id = integer,inside_block_id = integer,room_id = integer
    Purpose: This creates the room by adding the walls to dictionary_for_procedural_generation and the one with id then 
    it also adds to the dictionary_for_inside_room this means when we spawn enemies that they is an easy dictionary to
    access. It also does a binary search to see if those values where the room would be +1 and -1 on the width and height
    are still in the dictionary_for_open_spaces and if they are it will then remove them.
    """

def create_room(dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,dictionary_for_inside_room,
                dictionary_for_open_spaces,random_x,random_y,width_of_room,height_of_room,block_of_wall_id,inside_block_id,room_id,dictionary_for_walls_procedural):
    dictionary_for_procedural_generation_with_id[room_id] = {}
    for x in range(random_x,random_x + width_of_room + 1):
        dictionary_for_procedural_generation_with_id[room_id][x] = []
        for y in range(random_y,random_y+height_of_room+1):
            if x == random_x or x == random_x + width_of_room or y == random_y or y == random_y + height_of_room:
                dictionary_for_procedural_generation["wall_block" + str(block_of_wall_id)] = {"x":x,"y":y}
                dictionary_for_procedural_generation_with_id[room_id][x].append(y)
                block_of_wall_id += 1
                array_for_binary = list(dictionary_for_walls_procedural).copy()
                array_for_binary.sort()
                found = binary_search_procedural_generation(array_for_binary,x)
                if found:
                    dictionary_for_walls_procedural[x].append(y)
                else:
                    dictionary_for_walls_procedural[x] = [y]
            else:
                adding_to_dictionary(dictionary_for_inside_room,x,y)
            found = binary_search_procedural_generation(dictionary_for_open_spaces[x],y)
            if found:
                dictionary_for_open_spaces[x].remove(y)
            if dictionary_for_open_spaces[x]:
                if y == random_y:
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],(y-1))
                    if found:
                        dictionary_for_open_spaces[x].remove(y-1)
                elif y == random_y + height_of_room:
                    found = binary_search_procedural_generation(dictionary_for_open_spaces[x],(y+1))
                    if found:
                        dictionary_for_open_spaces[x].remove(y+1)
                if x - 1 >= list(dictionary_for_open_spaces)[0]:
                    if x == random_x and dictionary_for_open_spaces[x-1]:
                        found = binary_search_procedural_generation(dictionary_for_open_spaces[x-1],y)
                        if found:
                            dictionary_for_open_spaces[x-1].remove(y)
                        if y == random_y:
                            found = binary_search_procedural_generation(dictionary_for_open_spaces[x-1],y-1)
                            if found:
                                dictionary_for_open_spaces[x-1].remove(y-1)
                        if y == random_y + height_of_room:
                            found = binary_search_procedural_generation(dictionary_for_open_spaces[x-1],y+1)
                            if found:
                                dictionary_for_open_spaces[x-1].remove(y+1)
                if x + 1 <= list(dictionary_for_open_spaces)[len(dictionary_for_open_spaces) - 1]:
                    if x == random_x + width_of_room and dictionary_for_open_spaces[x+1]:
                        found = binary_search_procedural_generation(dictionary_for_open_spaces[x+1],y)
                        if found:
                            dictionary_for_open_spaces[x+1].remove(y)
                        if y == random_y:
                            found = binary_search_procedural_generation(dictionary_for_open_spaces[x+1],y-1)
                            if found:
                                dictionary_for_open_spaces[x+1].remove(y-1)
                        if y == random_y + height_of_room:
                            found = binary_search_procedural_generation(dictionary_for_open_spaces[x+1],y+1)
                            if found:
                                dictionary_for_open_spaces[x+1].remove(y+1)
    return block_of_wall_id,inside_block_id,room_id

""" Name: 
    Parameters:
    Returns:
    Purpose:
    """

def binary_search_with_higher_and_lower(array_to_be_found,lower_boundary,higher_boundary):
    top_number = len(array_to_be_found) - 1
    bottom_number = 0
    while bottom_number <= top_number:
        mid_point = (bottom_number + top_number) // 2
        if array_to_be_found[mid_point] < lower_boundary:
            bottom_number = mid_point + 1
        elif array_to_be_found[mid_point] > higher_boundary:
            top_number = mid_point - 1
        else:
            return True
    return False

""" Name: spawn_top_left_corner_of_room
    Parameters: how_many_right = integer,how_many_left = integer,how_many_up = integer,how_many_down = integer,
    dictionary_for_procedural_generation = dictionary,dictionary_for_procedural_generation_with_id = dictionary,
    dictionary_for_inside_room = dictionary,dictionary_for_open_spaces = dictionary,block_of_wall_id = integer
    inside_block_id = integer
    Returns: None
    Purpose: This creates a random coordinate in the area that the room can be produced it then randomly generates
    the width and height and then checks to see if it is is one a way from another room or if there would be a room
    inside a room and if the room would intersect another room if any of these are true it will not allow the room
    to spawn and then add one to the room_not_generated and if that hits 25 or if 10 rooms where generated
     it will then repeat with different height and width
    """

def spawn_top_left_corner_of_room(how_many_right,how_many_left,how_many_up,how_many_down,dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,dictionary_for_inside_room,
                                  dictionary_for_open_spaces,block_of_wall_id,inside_block_id,dictionary_for_walls_procedural,room_id):
    completed_room = 0
    room_not_generated = 0
    low_random_number = 8
    high_random_number = 12
    tries = 0
    while tries != 2:
        if tries == 1:
            low_random_number = 4
            high_random_number = 7
            completed_room = 0
            room_not_generated = 0
        while completed_room != 10 and room_not_generated != 25:
            random_x = random.randint(how_many_left,how_many_right)
            random_y = random.randint(how_many_up,how_many_down)
            width_of_room = random.randint(low_random_number,high_random_number)
            height_of_room = random.randint(low_random_number,high_random_number)
            true = True
            if random_x + width_of_room > how_many_right or random_y + height_of_room > how_many_down:
                true = False
            for key in dictionary_for_procedural_generation:
                if true:
                    if (dictionary_for_procedural_generation[key]["x"] == random_x - 1
                        and dictionary_for_procedural_generation[key]["y"] >= random_y
                            and dictionary_for_procedural_generation[key]["y"] <= random_y + height_of_room) \
                            or (dictionary_for_procedural_generation[key]["x"] == random_x + width_of_room + 1
                                and dictionary_for_procedural_generation[key]["y"] >= random_y
                            and dictionary_for_procedural_generation[key]["y"] <= random_y + height_of_room):
                        true = False
                    elif (dictionary_for_procedural_generation[key]["y"] == random_y - 1
                        and dictionary_for_procedural_generation[key]["x"] >= random_x
                        and dictionary_for_procedural_generation[key]["x"] <= random_x + width_of_room) \
                            or (dictionary_for_procedural_generation[key]["y"] == random_y + height_of_room + 1
                                and dictionary_for_procedural_generation[key]["x"] >= random_x
                                and dictionary_for_procedural_generation[key]["x"] <= random_x + width_of_room):
                        true = False
                    elif dictionary_for_procedural_generation[key]["y"] >= random_y and dictionary_for_procedural_generation[key]["y"] <= random_y + height_of_room \
                        and dictionary_for_procedural_generation[key]["x"] >= random_x and dictionary_for_procedural_generation[key]["x"] <= random_x + width_of_room:
                        true = False
                if true:
                    array_for_binary = list(dictionary_for_inside_room)
                    array_for_binary.sort()
                    found = binary_search_procedural_generation(array_for_binary,random_x)
                    if found:
                        array_for_binary = dictionary_for_inside_room[random_x]
                        array_for_binary.sort()
                        found = binary_search_procedural_generation(array_for_binary,random_x)
                        if found:
                            true = False
            if true:
                room_id += 1
                block_of_wall_id, inside_block_id,room_id = create_room(dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,dictionary_for_inside_room,
                                                                dictionary_for_open_spaces,random_x,random_y,width_of_room,height_of_room,block_of_wall_id,inside_block_id,room_id,dictionary_for_walls_procedural)
                completed_room += 1
                room_not_generated = 1
            else:
                room_not_generated += 1
        tries += 1
    spawn_root_corridor(how_many_left,how_many_right,how_many_up,how_many_down,dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,dictionary_for_open_spaces,dictionary_for_walls_procedural)

""" Name: spawn_spawning_room
    Parameters:None
    Returns:walls_to_be_sent_for_conversion = dictionary
    Purpose: This sets up most of the variables that will be used to create the map. It then works out how many across
    and vertical there should be away from the starting room. This is due to the starting room will not move but the 
    rooms will generated will be spawned in different areas. It also gets the outer walls and adds it to a dictionary
    and gets the inside of the room to be added to another dictionary
    """

def spawn_spawning_room():
    dictionary_for_walls_procedural = {}
    dictionary_for_procedural_generation = {}
    dictionary_for_procedural_generation_with_id = {}
    dictionary_for_inside_room = {}
    dictionary_for_open_spaces = {}
    y_array_for_x = []
    """division_for_magnifier = 0.75"""
    division_for_magnifier = 3
    block_of_wall_id = 1
    inside_block_id = 1
    room_id = 1
    random_number = random.randint(int(7/division_for_magnifier),49)
    how_many_right = random_number
    how_many_left = random_number-50
    random_number = random.randint(int(7/division_for_magnifier),49)
    how_many_down = random_number
    how_many_up = random_number - 50
    for y in range(how_many_up,how_many_down+1):
        y_array_for_x.append(y)
    for x in range(how_many_left,how_many_right+1):
        dictionary_for_open_spaces[x] = y_array_for_x.copy()
    dictionary_for_procedural_generation_with_id[room_id] = {}
    for x in range(int(2/division_for_magnifier),int(7/division_for_magnifier)):
        dictionary_for_procedural_generation_with_id[room_id][x] = []
        for y in range(int(2/division_for_magnifier),int(7/division_for_magnifier)):
            if x == int(2/division_for_magnifier) or x == int(7/division_for_magnifier)-1 or y == int(2/division_for_magnifier) or y == int(7/division_for_magnifier)-1:
                dictionary_for_procedural_generation_with_id[room_id][x].append(y)
                if not dictionary_for_walls_procedural:
                    dictionary_for_walls_procedural[x] = [y]
                else:
                    found = binary_search_procedural_generation(list(dictionary_for_walls_procedural),x)
                    if found:
                        dictionary_for_walls_procedural[x].append(y)
                    else:
                        dictionary_for_walls_procedural[x] = [y]
                dictionary_for_procedural_generation["wall_block" + str(block_of_wall_id)] = {"x":x,"y":y}
                block_of_wall_id += 1
            dictionary_for_open_spaces[x].remove(y)
            if x == int(2/division_for_magnifier):
                dictionary_for_open_spaces[x-1].remove(y)
            elif x == int(7/division_for_magnifier)-1:
                dictionary_for_open_spaces[x+1].remove(y)
            if y == int(2/division_for_magnifier):
                dictionary_for_open_spaces[x].remove(y-1)
            elif y == int(7/division_for_magnifier)-1:
                dictionary_for_open_spaces[x].remove(y+1)
            if x == int(2/division_for_magnifier) and y == int(2/division_for_magnifier):
                dictionary_for_open_spaces[x-1].remove(y-1)
            elif x == int(2/division_for_magnifier) and y == int(7/division_for_magnifier)-1:
                dictionary_for_open_spaces[x-1].remove(y+1)
            elif x == int(7/division_for_magnifier)-1 and y == int(2/division_for_magnifier):
                dictionary_for_open_spaces[x+1].remove(y-1)
            elif x == int(7/division_for_magnifier)-1 and y == int(7/division_for_magnifier)-1:
                dictionary_for_open_spaces[x+1].remove(y+1)
    spawn_top_left_corner_of_room(how_many_right,how_many_left,how_many_up,how_many_down,
                                  dictionary_for_procedural_generation,dictionary_for_procedural_generation_with_id,
                                  dictionary_for_inside_room,dictionary_for_open_spaces,
                                  block_of_wall_id,inside_block_id,dictionary_for_walls_procedural,room_id)
    walls_to_be_sent_for_conversion = combine_walls(dictionary_for_walls_procedural)
    stuff_inside_the_rooms = add_things_to_inside_procedural_generation(dictionary_for_inside_room)
    return walls_to_be_sent_for_conversion, stuff_inside_the_rooms

spawn_spawning_room()