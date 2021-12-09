from collections import deque

class State(object):
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
    
    # finding all the possible nodes in each level
    def nextstate(self):
        if self.boat == 1:
            sign = -1
            direction = "from left to right"
        else:
            sign = 1
            direction = "from right to left"
        for m in range(3):
            for c in range(3):
                newState = State(self.missionaries+sign*m, self.cannibals+sign*c, self.boat+sign*1)
                if m+c >= 1 and m+c <= 2 and newState.validity():
                    action = "Move %d missionaries and %d cannibals %s. %r" % ( m, c, direction, newState)
                    yield action, newState
    
    def __repr__(self):
        return "Current State (%d, %d, %d)" % (self.missionaries, self.cannibals, self.boat)
    
    # conditions like missionaries not to be outnumbered by cannibals are checked
    def validity(self):
        if self.missionaries<0 or self.cannibals<0 or self.missionaries>3 or self.cannibals>3 or (self.boat!=0 and self.boat!=1):
            return False
        if self.missionaries>self.cannibals and self.missionaries<3:
            return False
        if self.missionaries<self.cannibals and self.missionaries>0:
            return False
        return True
    
    # goal_state is (0,0,0)
    def goal_state(self):
        if self.missionaries==0 and self.cannibals==0 and self.boat==0:
            return True
        
class Node(object):
    def __init__(self, parent_node, action, depth, state):
        self.parent_node = parent_node
        self.action = action
        self.depth = depth
        self.state = state
    def next_node(self):
        for (action,next_state) in self.state.nextstate():
            nextnode = Node(parent_node= self, action= action, depth= self.depth+1, state= next_state)
            yield nextnode
    
    def final_solution(self):
        solution = []
        node_final = self
        while node_final.parent_node is not None:
            solution.append(node_final.action)
            node_final = node_final.parent_node
        solution.reverse()
        return solution

# Breadth First Search algorithm
def bfs(initial_state):
    initial_node = Node(parent_node=None, action= None, depth= 0, state= initial_state)
    q = deque([initial_node])
    max_depth = -1
    while True:
        if not q:
            return None
        n = q.popleft()
        if n.depth > max_depth:
            max_depth = n.depth
        if n.state.goal_state():
            solution = n.final_solution()
            return solution
        q.extend(n.next_node())
def main():
    print('Left side -> Original river bank')
    print('Right side -> Destination river bank')
#State(no. of missionaries, no. of cannibals, boat)- on the original river bank
    initial_state = State(3,3,1)
    solution = bfs(initial_state)
    if solution is None:
        print("No solution")
    else:
        print("Solution obtained in {} steps".format(len(solution)))
        for s in solution:
            print("{}".format(s))
if __name__ == "__main__":
    main()