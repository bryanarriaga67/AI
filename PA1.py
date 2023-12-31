'''
CS 4320 - PA1 PT1
Aaron Cardiel
Bryan Arriaga
'''

import sys
import time
import heapq
from collections import deque

#Node class
class Node:
    def __init__(self, coordinate, cost = 0, parent_node = None, depth = 0, g_cost = 0, f_cost = 0):
        self.coordinate = coordinate
        self.cost = cost
        self.parent_node = parent_node
        self.depth = depth
        self.g_cost = g_cost
        self.f_cost = f_cost
    def __lt__(self, other):
        # Define custom comparison for the priority queue
        return self.f_cost < other.f_cost
    #prints info of 
    def __str__(self):
        parent_node_coordinate = None
        if self.parent_node is not None:
            parent_node_coordinate = self.parent_node.coordinate
        return f"Node(coordinate={self.coordinate}, cost={self.cost}, parent node coordinate={parent_node_coordinate}, depth={self.depth})"

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

def depth_limited_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time, depth_limit):
    # Keep track of visited states
    explored = set()
    # Keep track of states coordinates in stack for faster look up
    stack_coordinate_set = set()
    # Stack that will store successor nodes (Depth-Limited Search uses a stack)
    stack = [starting_node]
    # List to keep track of max number of nodes
    max_num_nodes = []
    start_time = time.time()
    
    while stack:
        # Store the number of nodes in memory
        max_num_nodes.append(len(stack))
        # Popping current node from stack
        current_node = stack.pop()
        stack_coordinate_set.discard(tuple(current_node.coordinate))  # Dequeue coordinate of current node
        current_depth = current_node.depth

        # Check if the elapsed time exceeds the cutoff
        current_time = time.time()
        elapsed_time_ms = (current_time - start_time) * 1000
        if elapsed_time_ms > float(cutoff_time) * 1000:
            print("Goal Node not found within the cutoff time.")
            return -1, len(explored), max(max_num_nodes), None   # Terminate the search if the cutoff time is exceeded
        
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
            return path_cost, len(explored), max(max_num_nodes), path
        
        for successor_node in generate_successor_nodes(current_node, map_representation, dimension):
            # Check for repeated states
            if tuple(successor_node.coordinate) not in explored and tuple(successor_node.coordinate) not in stack_coordinate_set and current_depth + 1 <= depth_limit:
                successor_node.depth = current_depth + 1
                stack.append(successor_node)  # Push successor nodes onto the stack
                stack_coordinate_set.add(tuple(successor_node.coordinate))

    return -1, len(explored), max(max_num_nodes), None

def iterative_deepening_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time):
    depth_limit = 0
    solved = False
    num_explored = 0
    max_num_nodes = 0
    # Check if the elapsed time exceeds the cutoff
    start_time = time.time()
    while not solved and ((time.time() - start_time) * 1000) < (float(cutoff_time) * 1000):
        path_cost, num_explored, max_num_nodes, path = depth_limited_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time, depth_limit)
        depth_limit += 1
        if path:
            print("1) Cost of path:", path_cost)
            print("2) Number of nodes expanded:", num_explored)
            print("3) Maximum number of nodes in memory:", max_num_nodes)
            print("4) Runtime of algorithm:", (time.time() - start_time) * 1000, "milliseconds")
            print("5) Path:", path)
            return
        
    print("Goal Node not found")
    print("Cost of Path: -1")
    print("Number of nodes expanded:", num_explored)
    print("Maximum number of nodes in memory:", max_num_nodes) 
    print("Runtime of algorithm:", (time.time() - start_time) * 1000, "Milliseconds")
    print("Path: NULL")


def manhattan_distance(coordinate1, coordinate2):
    # Calculate the Manhattan distance between two coordinates
    return abs(coordinate1[0] - coordinate2[0]) + abs(coordinate1[1] - coordinate2[1])

def A_star_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time):
    # Keep track of visited states
    explored = set()
    # Keep track of the nodes in the open_list for faster look up and no repeated states
    open_list_coordinate_set = set()
    # Priority queue (min heap) to store nodes
    open_list = [starting_node]
    heapq.heapify(open_list)
    # List to keep track of max number of nodes
    max_num_nodes = []
    start_time = time.time()

    while open_list:
        # Store the number of nodes in memory
        max_num_nodes.append(len(open_list))
        # Popping the node with the lowest f value from the priority queue
        current_node = heapq.heappop(open_list)
        open_list_coordinate_set.discard(tuple(current_node.coordinate))

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
            if tuple(successor_node.coordinate) not in explored and tuple(successor_node.coordinate) not in open_list_coordinate_set:
                # Calculate the Manhattan distance heuristic from the successor to the goal
                heuristic_cost = manhattan_distance(successor_node.coordinate, goal_coordinate)
                # Update the cost of the successor node with the heuristic cost
                successor_node.f_cost = successor_node.cost + current_node.g_cost + heuristic_cost
                successor_node.g_cost = successor_node.cost + current_node.g_cost
                heapq.heappush(open_list, successor_node)  # Push successor nodes onto the priority queue

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
    iterative_deepening_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time)
        
if search_algorithm == 'AS':
    A_star_search(starting_node, goal_coordinate, map_representation, dimension, cutoff_time)   

