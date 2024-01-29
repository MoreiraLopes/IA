#STUDENT NAME: Gonçalo Rafael Correia Moreira Lopes
#STUDENT NUMBER: 107572

#DISCUSSED TPI-1 WITH: (names and numbers):
#Hugo Correia, 108215

import math
from tree_search import *



class OrderDelivery(SearchDomain):
    def __init__(self, connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates
        self.mapa = {}
        

    def actions(self, state):
        city = state[0]
        actlist = []
        for (C1, C2, D) in self.connections:
            if (C1 == city):
                actlist += [(C1, C2)]
            elif (C2 == city):
                actlist += [(C2, C1)]
        return actlist

    def result(self, state, action):
    
        current_city, targets, start_city = state
        next_city = action[1]

        new_targets = tuple(city for city in targets if city != next_city)

        return (next_city, new_targets, start_city)


    def satisfies(self, state, goal):
    
        return state[0] == state[2] and len(state[1]) == 0


    def cost(self, state, action):
        source_city, destination_city = action
        for (a, b, c) in self.connections:
            if a not in self.mapa:
                self.mapa[a] = {}
            if b not in self.mapa:
                self.mapa[b] = {}
            self.mapa[a][b] = c
            self.mapa[b][a] = c

        return self.mapa[source_city][destination_city]

    def heuristic(self, state, goal):
        current_city, targets, _ = state
        if not targets:  
            return 0

        total_distance = 0
        for target_city in targets:
            x1, y1 = self.coordinates[current_city]
            x2, y2 = self.coordinates[target_city]
            total_distance += abs(x2 - x1) + abs(y2 - y1)  

        return total_distance / len(targets)





 

class MyNode(SearchNode):
    def __init__(self, state, parent, depth, cost, heuristic):
        super().__init__(state, parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = cost + heuristic
        self.flag_for_removal = False 
        self.children = []  


   
class MyTree(SearchTree):
    def __init__(self, problem, strategy='breadth', maxsize=None):
        super().__init__(problem, strategy)
        self.maxsize = maxsize
        fisrt_node = MyNode(problem.initial, None, 0, 0, self.problem.domain.heuristic(problem.initial, self.problem.goal))
        self.open_nodes = [fisrt_node]
        self.non_terminals = 0
        self.terminals = 0

    
    
    def astar_add_to_open(self, lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda node: (node.eval, node.state[0]))

    
    
    def search2(self):
        while self.open_nodes:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)

            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate, node, node.depth + 1, node.cost + self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate, self.problem.goal))
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)

            soma = (len(self.open_nodes) + self.terminals + self.non_terminals)
            if self.strategy == 'A*' and self.maxsize is not None and soma > self.maxsize:
                self.manage_memory()
                
        return None  
    
    def manage_memory(self):
        while len(self.open_nodes) > self.maxsize:
            self.open_nodes.sort(key=lambda node: (node.eval, node.state[0]), reverse=True)
            for node in self.open_nodes:
                if not hasattr(node, 'flag_for_removal'):
                    node.flag_for_removal = True
                    parent = node.parent
                    siblings = []
                    if parent:
                        siblings = [n for n in parent.children if n != node]
                    if all(getattr(n, 'flag_for_removal', False) for n in siblings):
                        self.open_nodes.remove(node)
                        if parent:
                            min_eval = min(n.eval for n in siblings)
                            parent.eval = min_eval
                            parent.flag_for_removal = False
                        break


def orderdelivery_search(domain, city, targetcities, strategy='breadth', maxsize=None):
    problem = SearchProblem(domain, initial=(city, tuple(targetcities), city), goal=city)
    tree = MyTree(problem, strategy, maxsize)

    path = tree.search2()
    if path:
        export_path = []
        for node in path:
            export_path.append(node[0])
        return tree, export_path

    else:
        return None, None





