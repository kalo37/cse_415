"""
Aman Arya(aarya22)
1535134
CSE 415
Assignment 5

KInARow Bot
"""
import math
import copy
import random
import time

height = 0
width = 0
moves = []
side = ''
opponent = ''
k1 = 0
movecount = 0


def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    """
    Preparation function for the game. Reads the board and calculates possible moves.
    Also sets global variables.

    :param initial_state: state provided intially
    :param k: amount needed to win
    :param what_side_I_play: side played by program
    :param opponent_nickname: nickname of the opponent
    :return: "OK" if everything works fine
    """
    global height, width, moves, side, opponent, rows, cols, lslant, rslant, k1, movecount

    k1 = k
    side = what_side_I_play
    opponent = opponent_nickname
    board = initial_state[0]
    forbidden = []
    movesmade = []
    height = len(board)
    width = len(board[0])
    for i in range(height):
        for j in range(width):
            if board[i][j] == "-":
                forbidden.append((i, j))
            elif board[i][j] == "X" or board[i][j] == "O":
                movesmade.append((i, j))
                movecount += 1
    moves = [(x, y) for x in range(0, height)
             for y in range(0, width)]
    moves = [move for move in moves if move not in forbidden]
    moves = [move for move in moves if move not in movesmade]
    
    return "OK"


def get_opponent(side):
    """
    Given a side find the opponents element
    :param side: side of program
    :return: opponents side
    """
    if side == 'X':
        return 'O'
    else:
        return 'X'


def introduce():
    return "I\'m Dennis the 37 year old repressed Peasant, that\'s my name. ' \
           '\nNot like you would bother to find out, you automatically treat me ' \
           '\nas an inferior. I live in an anarcho-syndacalist commune, and the ' \
           '\nexecutive officer for the week is Aman Arya (aarya22).\n"


def nickname():
    return "Dennis"


def opening_salvo():
    openings = ['The opening moves have been played! I will play your capitalist game!',
                'Surely the workers will win this game. We probably built it!']
    return random.choice(openings)


def midgame():
    q = ['Interesting...But let\'s see you deal with this capitalist dog.',
         'Oh, so I do get a turn eh? Fine! There you go.',
         'Go ahead, Dare me. The proles will rise up.']
    return random.choice(q)


def closetowin():
    c = ['The revolution is at hand! Be careful.',
         'Anarchy is near! Careful you capitalist!',
         'Enjoy your greed while it lasts...']
    return random.choice(c)


def win():
    w = ['Revolution has been completed. Enjoy your new place in society.',
         'No longer do the proles have to be oppressed! Capitalism has been defeated!']
    return random.choice(w)


def loss():
    l = ['The revolution is simply delayed... I will come back.',
         'Of course you won. You\'ve played played zero-sum games all your life!',
         'Surely you have tricked me somehow with your capitalist tricks. I demand a rematch']
    return random.choice(l)


def random_move(currentState):
    """
    Randomly chooses a move
    :param currentState: state of current board
    :return: (move, newState) move randomly chosen and state applied with that move
    """
    move = random.choice(moves)
    newState = apply_move(move, currentState)
    return (move, newState)


def readState(state):
    """
    Reads the board and removes any moves on the board currently
    :param state: state of current board
    """
    global height, width, moves

    board = state[0]
    movesmade = []
    for i in range(height):
        for j in range(width):
            if board[i][j] == "X" or board[i][j] == "O":
                movesmade.append((i, j))
    moves = [move for move in moves if move not in movesmade]


def makeMove(currentState, currentRemark, timeLimit=10):
    """
    Makes a move. If in the beginning few rounds, choose a random move. Otherwise
    use alpha-beta pruned minimax w/ IDFS. New remark is found by the score of the current board.
    :param currentState: state of current board
    :param currentRemark: remark made
    :param timeLimit: timeLimit to make the move
    :return: ([move, newState], newRemark)
    move: move made
    newState: state with newMove applied
    newRemark: remark made that is calculated by how well the move is
    """
    global movecount, k1

    readState(currentState)
    if movecount < 1:
        move = random_move(currentState)
        newRemark = opening_salvo()
    else:
        move, score = alphabeta_search(currentState, timeLimit)
        winscore = math.pow(10, k1-1)
        closescore = winscore - (2*math.pow(10, k1-2))
        if score >= winscore:
            newRemark = win()
        elif score >= closescore:
            newRemark = closetowin()
        elif score < (-1 * winscore):
            newRemark = loss()
        elif score < closescore:
            newRemark = midgame()

    moves.remove(move[0])
    movecount += 1

    return [[move[0], move[1]], newRemark]


def alphabeta_search(state, timelimit, d=5):
    """
    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Also uses an IDFS to get a move even if time runs out.
    :param state: state of current board
    :param timelimit: time limit to make a move
    :param d: ply of alpha-beta pruning
    :return: action, score
    action: best possible action
    score: score from the action being implemented
    """

    successors = get_successors(state)
    timestart = time.time()
    action, score = argmax(successors,
                           star(lambda a, s: min_value(s, -math.inf, math.inf, 0, d, timelimit, timestart)))

    return action, score


def star(f):
    "Helper function for tuples"
    return lambda args: f(*args)


def argmax(seq, fn):
    """
    Gets the best seq for the highest fn(seq) value.
    :param seq: list of possible board successors
    :param fn: function to evaluate the board
    :return: best possible action, score for best possible action
    """
    best = seq[0]
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best = x
            best_score = x_score
    return best, best_score


def max_value(state, alpha, beta, depth, d, timelimit, timestart):
    "Helper function for the max value"
    if depth > d or terminal(state) or time.time() - timestart >= timelimit * 0.9:
        return staticEval(state)
    v = -math.inf
    for (a, s) in get_successors(state):
        v = max(v, min_value(s, alpha, beta, depth + 1, d, timelimit, timestart))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(state, alpha, beta, depth, d, timelimit, timestart):
    "Helper function for the min value"
    if depth > d or terminal(state) or time.time() - timestart >= timelimit * 0.9:
        return staticEval(state)
    v = math.inf
    for (a, s) in get_successors(state):
        v = min(v, max_value(s, alpha, beta, depth + 1, d, timelimit, timestart))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def get_successors(state):
    """
    For a given state, get all the possible next board states
    :param state: state of current board
    :return: list of next board states
    each element is saved as (move, newState)
    """
    return [(move, apply_move(move, state))
            for move in moves]


def apply_move(move, state):
    """
    Given a state apply a move on it to get state with move applied
    :param move: Move to apply
    :param state: current state
    :return: newState with board applied on it
    """
    global side

    if move not in moves:
        return state
    statecopy = copy.deepcopy(state)
    board = statecopy[0]
    s = statecopy[1]
    x, y = move[0], move[1]
    board[x][y] = side
    statecopy[1] = get_opponent(statecopy[1])
    return statecopy


def terminal(state):
    """
    For a test, check whether it is the final state
    :param state: state of board
    :return: True if board is finished, False if board is not finished
    """
    global k1

    return (abs(staticEval(state)) >= math.pow(10, k1-1)) or len(moves) == 0


def staticEval(state):
    """
    Calculates a score for a given state. This score is calculated as the following.

    For each row, column, diagonals (that fit k), reverse-diagonals (that fit k)

    if there are k of my side consecutively.
        return score of 10^(k-1)
    if there are (k-1) of my side consecutively and one empty spot.
        return score of 10^(k-2)
    if there are (k-2) of my side consecutively and two empty spots.
        return score of 10^(k-3)

    ...

    if there is one of my side and (k-1) empty spots:
        return score of 10^(k-(k-1) = 10^1 = 10
    if there are none of my side and k empty spots:
        return score of 10^0 = 1

    for the opponents return the opposite score

    :param state: state of current board
    :return: score of how good the board is
    """
    global side
    
    board = state[0]
    diag = diagonals(board)
    revdiag = reverse_diagonals(board)
    r = rows(board)
    c = cols(board)
    score = 0

    for d in diag:
        score += get_score(d)

    for rd in revdiag:
        score += get_score(rd)

    for a in r:
        score += get_score(a)

    for b in c:
        score += get_score(b)

    return score


def get_score(l):
    """
    For a row in compressed form (see compress), calculate the score of this row.
    :param l: row in compressed form
    :return: score of row in compressed form
    """
    global k1, side

    opside = get_opponent(side)
    l = compress(l)
    score = 0
    last = l[0]

    for p in l[1:]:
        if (p[0] == ' ' and last[0] == side) or (p[0] == side and last[0] == ' '):
            if viablerow(p, last):
                if p[0] == ' ':
                    score += math.pow(10, last[1] - 1)
                else:
                    score += math.pow(10, p[1] - 1)
        elif (p[0] == ' ' and last[0] == opside) or (p[0] == opside and last[0] == ' '):
            if viablerow(p, last):
                if p[0] == ' ':
                    score -= math.pow(10, last[1] - 1)
                else:
                    score -= math.pow(10, p[1] - 1)
        last = p

    return score


def viablerow(p1, p2):
    "Helper function to check if p1, p2 can form a viable row"
    global k1

    s1 = p1[1]
    s2 = p2[1]

    return (s1+s2) >= k1


def compress(l):
    """
    Compress a row into a form where it is easy to calculate the score.
    Ignores (-).
    :param l: row
    :return: compressed row

    Ex1:
    ['-', ' '. ' ', ' ', ' ', ' ', '-']
    [(' ', 5)]

    Ex2:
    [' ', ' ', ' ', 'O', ' ', 'O', 'X']
    [(' ', 3), ('O', 1), (' ', 1), ('O', 1), ('X', 1)]
    """
    newl = []

    ind = 1
    for i in l:
        if i != '-':
            last = i
            break
        ind += 1

    count = 1
    for i in l[ind:]:
        if i != '-':
            if i == last:
                count += 1
            else:
                newl.append((last, count))
                last = i
                count = 1

    newl.append((last, count))
    return newl


def rows(board):
    "Helper function to get a list of all the rows in the board"
    global k1

    row = []
    for b in board:
        if len(b) >= k1:
            row.append(b)

    return row


def cols(board):
    "Helper function to get a list of all the columns in the board"
    global k1, width

    col = []
    for k in range(width):
        c = []
        for b in board:
            c.append(b[k])

        if len(c) >= k1:
            col.append(c)

    return col


def diagonals(board):
    "Helper function to get a list of all the diagonals that are >= k"
    global k1, height, width

    diags = []
    for p in range(height+width-1):
        d = []
        for q in range(max(p-height+1, 0), min(p+1, width)):
            d.append(board[height - p + q - 1][q])
        if len(d) >= k1:
            diags.append(d)
    return diags


def reverse_diagonals(board):
    "Helper function to get a list of all the reverse-diagonals that are >= k"
    global k1

    h, w = len(board), len(board[0])
    revdiags = []
    for p in range(h + w - 1):
        d = []
        for q in range(max(p - h + 1, 0), min(p + 1, w)):
            d.append(board[p - q][q])
        if len(d) >= k1:
            revdiags.append(d)
    return revdiags
