"""Ken Lo
CSE 415 HW 5
K In A Row agent"""

INITIAL_STATE = None
K = 3
MY_SIDE = 'X'
OPP_SIDE = 'O'
OPP_NICKNAME = None

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

    return "OK"

def introduce():
    return """Hi, my name is Riqroq The Frog, my creator is Ken Lo, his UWID is thlo. I am friendly, \
    when I'm winning, but when I'm not, you better beware!"""

def nickname():
    return 'riqroq'

def makeMove(currentState, currentRemark, timeLimit=10000):
    #TODO implement
    pass

def staticEval(state):
    board = state[0]
    m = len(board) # num of rows
    n = len(board[0]) # num of cols
    my_score = 0
    opp_score = 0

    #check horizontal
    for hor in board:
        my_needed_to_win = testCanWin(hor, MY_SIDE)
        opp_needed_to_win = testCanWin(hor, OPP_SIDE)
        if my_needed_to_win > 0:
            my_score += 10 ** (K - my_needed_to_win)
        if opp_needed_to_win > 0:
            opp_score += 10 ** (K - opp_needed_to_win)


        #TODO check if working
    for i in range(0, n):
        temp = []
        for j in range(0, m):
            temp.append(board[j][i])
        my_needed_to_win = testCanWin(temp, MY_SIDE)
        opp_needed_to_win = testCanWin(temp, OPP_SIDE)
        if my_needed_to_win > 0:
            my_score += 10 ** (K - my_needed_to_win)
        if opp_needed_to_win > 0:
            opp_score += 10 ** (K - opp_needed_to_win)


    #TODO check \
    temp = []
    for i in range(0, n):
        try:
            temp.append(board[i][i])
        except:
            pass
    my_needed_to_win = testCanWin(temp, MY_SIDE)
    opp_needed_to_win = testCanWin(temp, OPP_SIDE)
    if my_needed_to_win > 0:
        my_score += 10 ** (K - my_needed_to_win)
    if opp_needed_to_win > 0:
        opp_score += 10 ** (K - opp_needed_to_win)

    #TODO check /
    




    return my_score - opp_score



def testCanWin(row, side):
    """return the minimum number of moves needed for the player of "side" to win the row,
                                    return -1 if the player cannot win the row"""


    try:
        row = row.remove('-')
    except ValueError:
        pass

    win_steps_list = []
    for i, cell in enumerate(row):
        needed_to_win = 0
        current_consecutive = 0

        if cell == side or cell == ' ':
            current_consecutive += 1
            if cell == ' ':
                needed_to_win += 1
            if current_consecutive >= K:
                win_steps_list.append(needed_to_win)
            else:

                for j in row[i + 1:]:
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

#0,0; 1,1; 2,2
#1,0; 2,1; 3,2
#0,1; 1,2; 2,3
#2,0

INITIAL_STATE = \
              [[[' ',' ',' '],
                [' ',' ',' '],
                [' ',' ',' ']], "X"]

print(staticEval(INITIAL_STATE))

#print(testCanWin([' ', ' ', 'X'], 'O'))
