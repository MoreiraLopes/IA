
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state, parent, cost=0): 
        self.state = state
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1
        self.cost = cost

    def in_parent(self, newstate):
        if self.parent == None:
            return False
        if self.state == newstate:
            return True
        return self.parent.in_parent(newstate)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, heuristic=problem.domain.heuristic(problem.initial, problem.goal))
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 1
        self.non_terminals = 0
    
    @property
    def length(self):
        return self.solution.depth

    
    @property
    def avg_branching(self):
        terminal = len(self.open_nodes) + 1
        return (terminals +self.non_terminals - 1)/self.non_terminals
    
    @property
    def cost(self):
        return self.solution.cost
        
    @property
    def average_depth(self):
        return self._avg_depth[0]/self._avg_depth[1]

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    @property
    def plan(self):
        n = self.solution
        _plan = [n.action]
        while n.parent != None:
            n = n.parent
            if n.action:
                _plan[:0] = [n.action]
        return _plan



    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes != []:
            self.terminals = len(self.open_nodes)
            node = self.open_nodes.pop(0)
            # cada vez que o no é aberto passa de terminal para nao terminal

            if self.problem.goal_test(node.state):
                self.solution = node
                # a soluçao e nao terminal
                print("terminals: ", len(self.open_nodes))
                print("non_terminals: ", self.non_terminals)
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)

                if not node.in_parent(newstate) and (limit == None or node.depth < limit) :
                    newnode = SearchNode(newstate,
                                         node, 
                                         cost=node.cost+self.problem.domain.cost(node.state, a),
                                         heuristic=self.problem.domain.heuristic(newstate,self.problem.goal))

                    if newnode.cost > self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes = [newnode]
                    elif newnode.cost == self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes.append(newnode)

                    self.avg_depth = tuple(
                        map(add, self._avg_depth, (newnode.depth, 1))
                    )
                    lnewnodes.append(newnode)


            # os nos derivados das acoes comecam como terminais
            
            self.add_to_open(lnewnodes)

        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self, lnewnodes):
            if self.strategy == "breadth":
                self.open_nodes.extend(lnewnodes)
            elif self.strategy == "depth":
                self.open_nodes[:0] = lnewnodes
            elif self.strategy == "uniform":
                self.open_nodes.extend(lnewnodes)
                self.open_nodes.sort(key=lambda x: x.cost)
            elif self.strategy == "greedy":
                self.open_nodes.extend(lnewnodes)
                self.open_nodes.sort(kdy=lambda x: x.heuristic)
            elif self.strategy == "a*":
                self.open_nodes.extend(lnewnodes)
                self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)

