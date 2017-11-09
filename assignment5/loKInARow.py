"""Ken Lo
CSE 415 HW 5
K In A Row agent"""

INITIAL_STATE = None
K = None
MY_SIDE = None
OPP_NICKNAME = None

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global INITIAL_STATE
    INITIAL_STATE = initial_state
    global K
    K = k
    global MY_SIDE
    MY_SIDE = what_side_I_play
    global OPP_NICKNAME
    OPP_NICKNAME = opponent_nickname

    return "OK"

def introduce():
    return """Hi, my name is Riqroq The Frog, my creator is Ken Lo, his UWID is thlo. I am friendly, \
    when I'm winning, but when I'm not, you better beware!"""

def nickname():
    return 'riqroq'

def makeMove(currentState, currentRemark, timeLimit=10000):
    pass

def staticEval(state):
    pass