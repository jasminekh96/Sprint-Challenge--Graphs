# ## Hints

# There are a few smaller graphs in the file which you can test your traversal method on before committing to the large graph. You may find these easier to debug.

# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.
# # do i need an opposite directions thing going on?

# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a `'?'` for an exit. If you use the `bfs` code from the homework, you will need to make a few modifications.

# 1. Instead of searching for a target vertex, you are searching for an exit with a `'?'` as the value. If an exit has been explored, you can put it in your BFS queue like normal.

# 2. BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.


from room import Room
from player import Player
from world import World
from util import Queue, Stack
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


# the opposite directions of each direction
opposite_directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
# empty base pathway of what you start with which is no rooms
pathway = []
# the rooms that have been visited put into an empty object
been_there = {}

# get exits from the room we're in and add it as a value to the current_room.id in been_there object, expecting been_there to be 0 because have not been there
been_there[player.current_room.id] = player.current_room.get_exits() 

# while the len of the been_there rooms is less than the len of room_graph minus 1, iteration
while len(been_there) < len(room_graph) - 1: 
    # base case, if the current room has not been visited
    if player.current_room.id not in been_there:
        # get exits from the room we're in and add it as a value to the current_room.id in been_there object
        been_there[player.current_room.id] = player.current_room.get_exits() 
        # been to the room so now removing it from the pathway, like dequeque
        last_room = pathway[-1]
        been_there[player.current_room.id].remove(last_room)
    # while it is 0 pop/return last value then append what you popped
    while len(been_there[player.current_room.id]) < 1:
        last_room = pathway.pop()
        traversal_path.append(last_room)
        player.travel(last_room)
    # if been there then pop it and append move (add to end of obj) what you popped then move the opposite_directions??
    move = been_there[player.current_room.id].pop()
    traversal_path.append(move)
    pathway.append(opposite_directions[move])
    player.travel(move)


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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
