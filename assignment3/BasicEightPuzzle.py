"""Ken Lo
UWNetID: thlo
HW 3 Part II - 2"""

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['K. Lo']
PROBLEM_CREATION_DATE = "18-OCT-2017"
PROBLEM_DESC=\
'''This formulation of the Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

# <COMMON_CODE>
class State:
    def __init__(self, l):
        self.l = l

    def __eq__(self, s2):
        return self.l == s2.l

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        return str(self.l)

    def __hash__(self):
        return (self.__str__()).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State(self.l[:])
        return news

    def can_move(self, num):
        '''Tests whether it's legal to move the number'''
        try:
            num_index = self.l.index(num)
            if num_index != 0 and self.l[num_index - 1] == 0: # if 0 is to the left
                return True
            if num_index != len(self.l) - 1 and self.l[num_index + 1] == 0: # if 0 is to the right
                return True
            if num_index < 6 and self.l[num_index + 3] == 0: # if 0 is below
                return True
            if num_index > 2 and self.l[num_index - 3] == 0: # if 0 is above
                return True
            return False
        except (Exception) as e:
            print(e)

    def move(self, num):
        """Assuming moving is legal, swap the position of zero and the number"""
        news = self.__copy__()
        num_idx, zero_idx = news.l.index(num), news.l.index(0)
        news.l[zero_idx], news.l[num_idx] = news.l[num_idx], news.l[zero_idx]
        return news  # return new state


# goal:
CREATE_GOAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])

def goal_test(s):
    '''s is in goal state if it equals to the defined CREATE_GOAL_STATE'''
    return s.l == list(range(0, 9))


def goal_message(s):
    return "The Puzzle Transport is Triumphant!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# </COMMON_CODE>

#<OPERATORS>
OPERATORS = [Operator("Move " + str(n),
                      lambda s, n1=n: s.can_move(n1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, n1=n: s.move(n1) )
             for n in list(range(1, 9))]
#</OPERATORS>

#<INITIAL_STATE>
# puzzle0:
#CREATE_INITIAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])
# puzzle1a:
#CREATE_INITIAL_STATE = lambda: State([1, 0, 2, 3, 4, 5, 6, 7, 8])
# puzzle2a:
#CREATE_INITIAL_STATE = lambda: State([3, 1, 2, 4, 0, 5, 6, 7, 8])
# puzzle4a:
CREATE_INITIAL_STATE = lambda: State([1, 4, 2, 3, 7, 0, 6, 8, 5])
#</INITIAL_STATE>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
