"""Ken Lo
CSE 415 HW 5
K In A Row agent"""

import random
import time

INITIAL_STATE = None
K = None
MY_SIDE = None
OPP_SIDE = None
OPP_NICKNAME = None
ZOBRISTNUM = []
ZHASH_DICT = {}
MOVE = 0


def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global INITIAL_STATE
    INITIAL_STATE = initial_state

    global K
    K = k

    global MY_SIDE
    MY_SIDE = what_side_I_play

    global OPP_SIDE
    if what_side_I_play == 'X':
        OPP_SIDE = 'O'
    else:
        OPP_SIDE = 'X'

    global OPP_NICKNAME
    OPP_NICKNAME = opponent_nickname

    global ZOBRISTNUM
    m = len(initial_state[0])  # num of rows
    n = len(initial_state[0][0])
    ZOBRISTNUM = [[0] * 2 for i in range(m * n)]
    for i in range(m):
        for j in range(2):
            ZOBRISTNUM[i][j] = random.randint(0, 4294967296)

    return "OK"


def zhash(board):
    """hash function for the board"""
    val = 0
    flattened = [x for y in board for x in y]
    for i in range(0, len(flattened)):
        mark = None
        if flattened[i] == 'O': mark = 0
        if flattened[i] == 'X': mark = 1
        if mark != None:
            val ^= ZOBRISTNUM[i][mark]
    return val


def introduce():
    return """Hi, my name is Riqroq The Frog, my creator is Ken Lo, his UWID is thlo. I am friendly, \
    when I'm winning, but when I'm not, you better beware!"""


def nickname():
    return 'riqroq'


import math

UTTERANCES = ["You should go easy on me, I'm just a frog.", \
              "Hmm, this should be good.", \
              "Have you ever met a friendly frog like I am? I'm still going to win though!", \
              "Have you ever been to China? I heard they eat frogs :S", \
              "Croak. Croak. Croak.", \
              "The dream of every frog is to become a prince."]


def makeMove(currentState, currentRemark, timeLimit=10000):
    startTime = time.time()
    global MOVE
    MOVE += 1
    if MOVE == 1:
        newRemark = "Hello " + OPP_NICKNAME + ". Croak. Let's play a good game, show some good sportsFROGship."
    else:
        newRemark = random.choice(UTTERANCES)
    v, newState, move = doSearch(currentState, timeLimit, startTime)
    return [[move, newState], newRemark]


def timeCheck(startTime, timeLimit):
    """check if time limit is approaching"""
    return timeLimit - time.time() + startTime < 0.01


def doSearch(state, timeLimit, startTime):
    """start alpha beta search, return the best move, its state and its value"""
    depth = 1
    children = getNextMoves(state, MY_SIDE)
    beststate, bestmove = children[0]
    bestV = getMin(beststate, depth, -math.inf, math.inf, startTime, timeLimit)
    for childstate, childmove in children[1:]:
        if timeCheck(startTime, timeLimit):
            break
        childV = getMin(childstate, depth, -math.inf, math.inf, startTime, timeLimit)
        if childV > bestV:
            beststate = childstate
            bestmove = childmove
            bestV = childV
    return bestV, beststate, bestmove


def getMax(state, depth, alpha, beta, startTime, timeLimit):
    """get maximum value, with alpha beta pruning"""
    h = staticEval(state)
    if depth == 0 or is_terminal_state(state, h) or timeCheck(startTime, timeLimit):
        return h
    v = -math.inf
    for s, move in getNextMoves(state, MY_SIDE):
        v = max(v, getMin(s, depth - 1, alpha, beta, startTime, timeLimit))
        alpha = max(alpha, v)
        if alpha >= beta:
            return alpha
    return v


def getMin(state, depth, alpha, beta, startTime, timeLimit):
    """get min value, with alpha beta pruning"""
    h = staticEval(state)
    if depth == 0 or is_terminal_state(state, h) or timeCheck(startTime, timeLimit):
        return h
    v = math.inf
    for s, move in getNextMoves(state, OPP_SIDE):
        v = min(v, getMax(s, depth - 1, alpha, beta, startTime, timeLimit))
        beta = min(beta, v)
        if alpha >= beta:
            return beta
    return v


def getNextMoves(state, side):
    """get all successors of "side" of the current state"""
    if side == 'X':
        nextside = 'O'
    else:
        nextside='X'
    s = state[0][:]
    board = [x[:] for x in s]
    moves = []
    new_states = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == ' ':
                moves.append((i, j))
                temp = [x[:] for x in board]
                temp[i][j] = side
                new_states.append([temp, nextside])
    return list(zip(new_states, moves))


def is_terminal_state(state, h):
    """return true if state is a terminal state, false otherwise"""
    if h > (10 ** K) or h < -(10 ** K):
        return True
    for r in state[0]:
        if r.count(' ') != 0:
            return False
    return True


def staticEval(state):
    board = state[0]
    zhash_value = zhash(board)
    if zhash_value in ZHASH_DICT.keys():
        return ZHASH_DICT[zhash_value]
    else:
        m = len(board)  # num of rows
        my_score = 0
        opp_score = 0

        horizontals = [x for x in board]

        for hor in horizontals:
            my_needed_to_win = testCanWin(hor, MY_SIDE)
            opp_needed_to_win = testCanWin(hor, OPP_SIDE)
            if my_needed_to_win >= 0:
                my_score += (10 ** (K - my_needed_to_win))
            if opp_needed_to_win >= 0:
                opp_score += (10 ** (K - opp_needed_to_win))

        verticals = [list(x) for x in zip(*board)]

        for ver in verticals:
            my_needed_to_win = testCanWin(ver, MY_SIDE)
            opp_needed_to_win = testCanWin(ver, OPP_SIDE)
            if my_needed_to_win >= 0:
                my_score += (10 ** (K - my_needed_to_win))
            if opp_needed_to_win >= 0:
                opp_score += (10 ** (K - opp_needed_to_win))

        def get_forward_diag():
            """get all forward diagonals, and return them if their lengths are larger than K"""
            b = [None] * (m - 1)
            shifted = [b[i:] + r + b[:i] for i, r in enumerate(horizontals)]
            shifted_cols = [list(x) for x in zip(*shifted)]
            all_diags = [[c for c in r if not c == None] for r in shifted_cols]
            return [x for x in all_diags if len(x) >= K]

        forward_diags = get_forward_diag()
        for d in forward_diags:
            my_needed_to_win = testCanWin(d, MY_SIDE)
            opp_needed_to_win = testCanWin(d, OPP_SIDE)
            if my_needed_to_win >= 0:
                my_score += (10 ** (K - my_needed_to_win))
            if opp_needed_to_win >= 0:
                opp_score += (10 ** (K - opp_needed_to_win))

        def get_backward_diag():
            """get all backward diagonals, and return them if their lengths are larger than K"""
            b = [None] * (m - 1)
            shifted = [b[:i] + r + b[i:] for i, r in enumerate(horizontals)]
            shifted_cols = [list(x) for x in zip(*shifted)]
            all_diags = [[c for c in r if not c == None] for r in shifted_cols]
            return [x for x in all_diags if len(x) >= K]

        backward_diags = get_backward_diag()
        for d in backward_diags:
            my_needed_to_win = testCanWin(d, MY_SIDE)
            opp_needed_to_win = testCanWin(d, OPP_SIDE)
            if my_needed_to_win >= 0:
                my_score += (10 ** (K - my_needed_to_win))
            if opp_needed_to_win >= 0:
                opp_score += (10 ** (K - opp_needed_to_win))

        total_score = my_score - opp_score
        ZHASH_DICT[zhash(board)] = total_score
        return total_score


def testCanWin(row, side):
    """return the minimum number of moves needed for the player of "side" to win the row,
                                    return -1 if the player cannot win the row"""

    clean_row = row[:]
    clean_row = list(filter(lambda x: x != '-', clean_row))

    win_steps_list = []
    for i, cell in enumerate(clean_row):
        needed_to_win = 0
        current_consecutive = 0

        if cell == side or cell == ' ':
            current_consecutive += 1
            if cell == ' ':
                needed_to_win += 1
            if current_consecutive >= K:
                win_steps_list.append(needed_to_win)
            else:
                for j in clean_row[i + 1:]:
                    if j == side or j == ' ':
                        current_consecutive += 1
                        if j == ' ':
                            needed_to_win += 1
                        if current_consecutive >= K:
                            win_steps_list.append(needed_to_win)
                    elif j != side:
                        current_consecutive = 0
                        needed_to_win = 0

    if win_steps_list != []:
        return min(win_steps_list)
    else:
        return -1
