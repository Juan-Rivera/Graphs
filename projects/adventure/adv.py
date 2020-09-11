from room import Room
from player import Player
from world import World
from util import Stack 

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# use this Stack as a way to backtrack
master_path = []

#store available moves here
moves = {}

# reverse directions for when going backwards
reverse_direction = { 
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# # add current room to visited
# visited_rooms.add(player.current_room.id)
# # get exits to start traversal
moves[player.current_room.id] = player.current_room.get_exits()

# traverse if length of visited < length of rooms in world
while len(moves) < len(world.rooms) - 1:

    # check if current room id is in visited
    if player.current_room.id not in moves:
        room = player.current_room.id
        # add the room to visited
        
        #grab previous direction
        moves[room] = player.current_room.get_exits()
        back = master_path[-1]
        #remove previous direction to avoid that direction
        moves[player.current_room.id].remove(back)
    # change traversal
    while len(moves[player.current_room.id]) == 0:
        #remove previous exits set
        back = master_path.pop()
        # add last set of exits
        traversal_path.append(back)
        # use travel function to move to previous room
        player.travel(back)

    # check current_room's exits and find last room on list, go to that room.
    # append to path as this is the right directions
    next_move = moves[player.current_room.id].pop(0)
    # append it to record of going there
    traversal_path.append(next_move)
    master_path.append(reverse_direction[next_move])
    # use the directions dictionary to go backwards through rooms
    player.travel(next_move)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)



for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
