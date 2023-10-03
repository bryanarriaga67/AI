import sys
import time

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

def breadth_first_search(starting_node, goal_coordinate, map_representation, dimension, cuttoff_time):
    #Keep track of visited states
    explored = []
    #Queue that will store successor nodes
    queue = [starting_node]
    max_num_nodes = list()
    start_time = time.time()
    while len(queue) != 0:
        #Store num nodes in memory
        max_num_nodes.append(len(queue))
        current_node = queue.pop(0)
        #Add current node to explored list
        explored.append(current_node.coordinate)

        # Check if the elapsed time exceeds the cutoff
        current_time = time.time()
        elapsed_time_ms = (current_time - start_time) * 1000
        if elapsed_time_ms > float(cuttoff_time*1000):
            print("Goal Node not found")
            return None  # You can choose how to handle the termination
        

        for successor_node in generate_successor_nodes(current_node, map_representation, dimension):
            #Check for repeated states
            if successor_node.coordinate not in explored:
                if successor_node.coordinate == goal_coordinate:
                    #Store coordinate of goal node
                    path = [successor_node.coordinate]
                    #store cost to get to goal node from current node
                    path_cost = successor_node.cost
                    #move to goal node
                    current_node = successor_node
                    #backtrack to starting node and break once there
                    while current_node.parent_node is not None:
                        #go back to parent node from goal node
                        current_node = current_node.parent_node
                        #add current coordinate to path list
                        path.append(current_node.coordinate)
                        #add up cost to get to goal node
                        path_cost += current_node.cost
                    #reverse list of path cooridnates
                    path = path[::-1]
                    end_time = time.time()  # Record the end time
                    runtime_ms = (end_time - start_time) * 1000 
                    print("1) Cost of path:", path_cost)
                    print("2) Number of nodes expanded:", len(explored))
                    print("3) Maximum number of nodes in memory: ", max(max_num_nodes))
                    print("4) Runtime of algorithm:", runtime_ms, "milliseconds")
                    print("5) Path:", path)
                    return
                #push successor nodes into queue
                queue.append(successor_node)

if len(sys.argv) != 4:
    print("Usage: python3 PA1.py <filename> <search algorithm> <cutoff time in seconds")
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
    print('hi')
    breadth_first_search(starting_node, goal_coordinate, map_representation, dimension,cutoff_time)
        

        
    

