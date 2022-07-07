
## stuff to add 

    # print a line of space between the lines of the output
    # add image to the finale (or add one in each step)
    # add the counter



diogo = {                   # changed the dictionaries to suit the new game
    "name": "diogo",
    "type": "person",
}

hallway = {
    "name": "hallway",
    "type": "door",
}

key_hallway = {
    "name": "key for hallway",
    "type": "key",
    "target": hallway,
}

dish_washer = {
    "name": "dish washer",
    "type": "furniture",
}

common_room = {
    "name": "common room",
    "type": "room",
}

outside = {
  "name": "outside"
}


## Bedroom 1

ux_room = {
    "name": "ux room",
    "type": "room",
}

students = {
    "name": "students",
    "type": "person",
}

data_door = {
    "name": "data door",
    "type": "door",
}

go_to_balcony = {
    "name": "go to balcony",
    "type": "door",
}

key_data = {
    "name": "key for data door",
    "type": "key",
    "target": data_door,
}



## Bedroom 2

data_room = {
    "name": "data room",
    "type": "room",
}


gladys = {
    "name": "gladys",
    "type": "person",
}

jose = {
    "name": "jose",
    "type": "person",
}


key_balcony = {
    "name": "key for balcony",
    "type": "key",
    "target": go_to_balcony,
}


# Living Room

balcony = {
    "name": "balcony",
    "type": "room",
}


chairs = {
    "name": "chairs",
    "type": "door",
}  


key_chair = {
    "name": "key for chairs",
    "type": "key",
    "target": chairs,
}





all_rooms = [common_room, ux_room, data_room, balcony] ## changed the lists

all_doors = [hallway, data_door, go_to_balcony, chairs]

# define which items/rooms are related

object_relations = {                                    ## changed the object relations
    "common room": [diogo, dish_washer, hallway],
    "dish washer": [key_hallway],
    "outside": [chairs], 
    "hallway": [common_room, ux_room],
    "ux room": [students, data_door],
    "students": [key_data],
    "data door": [ux_room, data_room],
    "data room":[gladys, jose,  go_to_balcony],
    "jose":[key_chair],  ## check for situation where you don't complete the project and try to go to the balcony
    "gladys":[key_balcony],
    "balcony":[chairs],
    "go to balcony": [data_room, balcony],
    "chairs": [balcony, outside]
    
    
   
}


# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": common_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")
    

def start_game(): ## CHANGE THE TEXT TO FIT THE IRONHACK GAME"
    """
    Start the game
    """
    linebreak()
    print("You wake up at Ironhack common room in the morning and are already late for your classes. You must get to the class before you get at full day absence, but see the Program Manager looking at you with angry face. How will you escape?")
    linebreak()
    play_room(game_state["current_room"])


counter=3


def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    

    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You've made it through another day at Ironhack! Enjoy the view :)")
    else:

        print("You are now in " + room["name"])
        intended_action = input("""    What would you like to do? Type 'look around' or 'interact'?    """).strip()
        if intended_action == "look around":
            explore_room(room)
            play_room(room)
        elif intended_action == "interact":
            examine_item(input("Who or what would you like to interact with?").strip())
    
        else:

            global counter
            counter=counter-1
            if counter==0:
                print("GAME OVER, START AGAIN")
                game_state["current_room"] = common_room
                game_state["keys_collected"]=[]
                counter = 3

                start_game()
            else:
                print('you have ' + str(counter) + 'tries')
                play_room(room)

            print("Not sure what you mean. Type 'look around' or 'interact'")
            play_room(room)

        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You look around. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You interact with " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    if (item["name"] == 'hallway'): 
                        output += "You go into the hallway and move towards the UX/UI classroom"
                    elif (item["name"] == 'data door'): 
                        output += "You exit the room towards the Data Analytics classrom" ## not appearing in the code

                    next_room = get_next_room_of_door(item, current_room)
                else:
                    if(item["name"] == 'go to balcony'):
                        output += "You haven't completed all the assignments. Get back to work!"
                    else:
                        output += "It is locked but you don't have the key." ## do
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found) ## here we coded the keys into tasks
                    if (item["name"] == 'dish washer'):
                        output += "You wash the dishes and are allowed to leave." 
                    elif (item["name"] == 'students'):
                        output += "The students interview you and let you go."
                    elif (item["name"] == 'gladys'):
                        output += "Gladys debugs your labs."
                    elif (item["name"] == 'jose'):
                        output += "Jose tells you to work harder. You finish your project"
                    
                        
                else:
                    if (item["name"] == 'diogo'):
                        output += "Diogo says you must wash the dishes!"    
                    else:
                        output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()