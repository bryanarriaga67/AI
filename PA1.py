import sys

class Node:
    def __init__(self, coordinate, cost = 0, parent_node = None):
        self.coordinate = coordinate
        self.cost = cost
        self.parent_node = parent_node
    
    def __str__(self):
        parent_node_coordinate = None
        if self.parent_node is not None:
            parent_node_coordinate = self.parent_node.coordinate
        return f"Node(coordinate={self.coordinate}, cost={self.cost}, parent node coordinate={parent_node_coordinate})"

def generate_successor_nodes(current_node, map_representation, dimension):
    current_node_coordinate = current_node.coordinate
    potential_node_coordinate = []
    successor_nodes = []

    #Checking bounds
    if current_node_coordinate[0]+1 < dimension[0]:
        potential_node_coordinate.append([current_node_coordinate[0]+1, current_node_coordinate[1]])
    if current_node_coordinate[0]-1 >= 0:
        potential_node_coordinate.append([current_node_coordinate[0]-1, current_node_coordinate[1]])
    if current_node_coordinate[1]+1 < dimension[1]:
        potential_node_coordinate.append([current_node_coordinate[0], current_node_coordinate[1]+1])
    if current_node_coordinate[1]-1 >= 0:
        potential_node_coordinate.append([current_node_coordinate[0], current_node_coordinate[1]-1])

    #Checking for passable terrain and generating nodes
    for coordinate in potential_node_coordinate:
        cost = map_representation[coordinate[0]][coordinate[1]]
        if cost != 0:
            successor_nodes.append(Node(coordinate, cost, current_node))

    return successor_nodes

def breadth_first_search(starting_node, goal_coordinate, map_representation, dimension):
    explored = []
    queue = [starting_node]
    while len(queue) != 0:
        current_node = queue.pop(0)
        explored.append(current_node.coordinate)
        for successor_node in generate_successor_nodes(current_node, map_representation, dimension):
            if successor_node.coordinate not in explored:
                if successor_node.coordinate == goal_coordinate:
                    print("1) Cost of path:")
                    print("2) Number of nodes expanded:")
                    print("3) Macimum number of nodes in memory:")
                    print("4) Runtime of algorithm:")
                    print("5) Path:")
                    return
                queue.append(successor_node)

if len(sys.argv) != 3:
    print("Usage: python3 PA1.py <filename> <search algorithm>")
    sys.exit(1)

filename = sys.argv[1]
search_algorithm = sys.argv[2]
dimension = None
starting_node = None
goal_coordinate = None
map_representation = []

with open(filename, 'r') as file:
    for input_row, line in enumerate(file):
        line = [int(element) for element in line.split()]
        if input_row == 0:
            dimension = line
        elif input_row == 1:
            starting_node = Node(line)
        elif input_row == 2:
            goal_coordinate = line
        else: 
            map_representation.append(line)

if search_algorithm == 'BFS':
    breadth_first_search(starting_node, goal_coordinate, map_representation, dimension)
        

        
    

