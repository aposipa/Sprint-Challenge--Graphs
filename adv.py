from room import Room
from player import Player
from world import World

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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
backwards_path = []
backwards_path_compass = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

# current player location
room_location = player.current_room.id
# index of room start point
visited[room_location] = player.current_room.get_exits()

# loop through unvisited rooms
while len(visited) < len(room_graph):
    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        last_path = backwards_path[-1]
        visited[player.current_room.id].remove(last_path)

    # if all rooms have been visited, stop loop and find unvisited nodes
    if len(visited[player.current_room.id]) == 0:
        last_path = backwards_path[-1]
        backwards_path.pop()
        traversal_path.append(last_path)
        player.travel(last_path)

    # didn't take the exit
    else:
        cardinal_direction = visited[player.current_room.id][-1]
        visited[player.current_room.id].pop()
        traversal_path.append(cardinal_direction)
        backwards_path.append(backwards_path_compass[cardinal_direction])
        player.travel(cardinal_direction)



# TRAVERSAL TEST - DO NOT MODIFY
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
