'''
CS 4320 - PA1 PT1
Aaron Cardiel
Bryan Arriaga
'''

import sys
import time
from collections import deque

#Node class
class Node:
    def __init__(self, coordinate, cost = 0, parent_node = None):
        self.coordinate = coordinate
        self.cost = cost
        self.parent_node = parent_node
    #prints info of 
    def __str__(self):
        parent_node_coordinate = None
        if self.parent_node is not None:
            parent_node_coordinate = self.parent_node.coordinate
        return f"Node(coordinate={self.coordinate}, cost={self.cost}, parent node coordinate={parent_node_coordinate})"

def generate_successor_nodes(current_node, map_representation, dimension):
    current_node_coordinate = current_node.coordinate
    #list of potential moves
    potential_node_coordinate = []
    #Nodes that can be reached from current node
    successor_nodes = []

    #Checking bounds

    #Checking if we can move below
    if current_node_coordinate[0]+1 < dimension[0]:
        potential_node_coordinate.append([current_node_coordinate[0]+1, current_node_coordinate[1]])
    #if there is node above
    if current_node_coordinate[0]-1 >= 0:
        potential_node_coordinate.append([current_node_coordinate[0]-1, current_node_coordinate[1]])
    #if there is node to the right
    if current_node_coordinate[1]+1 < dimension[1]:
        potential_node_coordinate.append([current_node_coordinate[0], current_node_coordinate[1]+1])
    #if there is a node to the left
    if current_node_coordinate[1]-1 >= 0:
        potential_node_coordinate.append([current_node_coordinate[0], current_node_coordinate[1]-1])

    #Checking for passable terrain and generating nodes
    for coordinate in potential_node_coordinate:
        cost = map_representation[coordinate[0]][coordinate[1]]
        if cost != 0:
            successor_nodes.append(Node(coordinate, cost, current_node))
    #if we cannot move anywhere and find goal terminate
    if len(successor_nodes) == 0:
        print("Goal Node not Found")
        sys.exit()


    return successor_nodes

def breadth_first_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time):
    # Keep track of visited states
    explored = set()
    # Keep track of states coordinates in queue for faster look up
    queue_coordinate_set = set()
    # Queue that will store successor nodes
    queue = deque([starting_node])
    #list to keep track of max number of nodes
    max_num_nodes = []
    start_time = time.time()
    
    while queue:
        # Store the number of nodes in memory
        max_num_nodes.append(len(queue))
        #Popping current node from queue
        current_node = queue.popleft()
        queue_coordinate_set.discard(tuple(current_node.coordinate)) #Dequeue coordinate of current node
        
        # Check if the elapsed time exceeds the cutoff
        current_time = time.time()
        elapsed_time_ms = (current_time - start_time) * 1000
        if elapsed_time_ms > float(cutoff_time) * 1000:
            print("Goal Node not found within the cutoff time.")
            return None  # Terminate the search if the cutoff time is exceeded
        
        # Add current node to explored set
        explored.add(tuple(current_node.coordinate))
        
        if current_node.coordinate == goal_coordinate:
            # Goal node found, reconstruct the path
            path = [current_node.coordinate]
            path_cost = current_node.cost
            while current_node.parent_node is not None:
                current_node = current_node.parent_node
                path.append(current_node.coordinate)
                path_cost += current_node.cost
            path.reverse()  # Reverse the path to get it in the correct order
            
            end_time = time.time()  # Record the end time
            runtime_ms = (end_time - start_time) * 1000
            print("1) Cost of path:", path_cost)
            print("2) Number of nodes expanded:", len(explored))
            print("3) Maximum number of nodes in memory:", max(max_num_nodes))
            print("4) Runtime of algorithm:", runtime_ms, "milliseconds")
            print("5) Path:", path)
            return path
        
        for successor_node in generate_successor_nodes(current_node, map_representation, dimension):
            # Check for repeated states
            if tuple(successor_node.coordinate) not in explored  and tuple(successor_node.coordinate) not in queue_coordinate_set:
                queue.append(successor_node)  # Enqueue successor nodes
                queue_coordinate_set.add(tuple(successor_node.coordinate))

    # If the loop completes without finding the goal, no path exists
    end_time = time.time()  # Record the end time
    runtime_ms = (end_time - start_time) * 1000
    print("Goal Node not found")
    print("Cost of Path: -1")
    print("Number of nodes expanded:", len(explored))
    print("Maximum number of nodes in memory:", max(max_num_nodes))
    print("Runtime of algorithm:", runtime_ms, "Milliseconds")
    print("Path: NULL")
    return None

def depth_limited_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time):
    pass

if len(sys.argv) != 4:
    print("Usage: python3 PA1.py <filename> <search algorithm> <cutoff time in seconds>")
    sys.exit(1)
#Initialze variables
filename = sys.argv[1]
search_algorithm = sys.argv[2]
cutoff_time = sys.argv[3]
dimension = None
starting_node = None
goal_coordinate = None
map_representation = []

with open(filename, 'r') as file:
    for input_row, line in enumerate(file):
        line = [int(element) for element in line.split()]
        #store dimension
        if input_row == 0:
            dimension = line
        #Create atarting node
        elif input_row == 1:
            starting_node = Node(line)
        #Store goal coordinate
        elif input_row == 2:
            goal_coordinate = line
        #store map as 2d array
        else: 
            map_representation.append(line)

if search_algorithm == 'BFS':
    breadth_first_search(starting_node, goal_coordinate, map_representation, dimension,cutoff_time)
        
if search_algorithm == 'IDS':
    depth_limited_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time)
        
    

