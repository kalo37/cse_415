"""Ken Lo UWNetID: thlo
HW 3 Part II - 3"""
# Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.4a, October 14, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# A small change was made on Oct. 14, so that backtrace
# uses None as the BACKLINK value for the initial state,
# just as in ItrDFS.py, rather than using -1 as it did
# in an earlier version.

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from priorityq import PriorityQ

# DO NOT CHANGE THIS SECTION
if sys.argv==[''] or len(sys.argv)<2:
    import EightPuzzleWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_custom'](s)

else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
def AStar(initial_state):
    global COUNT, BACKLINKS
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQ()
    CLOSED = []
    BACKLINKS[initial_state] = None
    g = {initial_state: 0}

    OPEN.insert(initial_state, heuristics(initial_state))

    while not len(OPEN) == 0:
        S, f = OPEN.deletemin()
        while S in CLOSED:
            S, f = OPEN.deletemin()
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION: begining
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        COUNT += 1
        print(COUNT)

        L = []
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED):
                    L.append(new_state)
                    BACKLINKS[new_state] = S
                    if new_state not in g.keys():
                        g[new_state] = g[S] + 1

        for s2 in L:
            if s2 in OPEN:
                OPEN.remove(s2)

        for elt in L:
            OPEN.insert(elt, heuristics(elt) + g[elt])


def occurs_in(s1, lst):
    for s2 in lst:
        if s1 == s2: return True
    return False

# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while S:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path

def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))

if __name__=='__main__':
    path, name = runAStar()
