"""
Aman Arya(aarya22), Ken Lo(thlo)
CSE 415
Assignment 4
Wicked Problem: Dyadic Relationship"""
import random

PROBLEM_NAME = 'Dyadic Relationship'


class State:
    # d keys: I, S
    def __init__(self, d):
        self.d = d
        self.a = 0

    def __eq__(self, s2):
        if self.d['interest'] != s2.d['interest']: return False
        if self.d['satisfaction'] != s2.d['satisfaction']: return False
        if self.d['frequency'] != s2.d['frequency']: return False
        return True

    def copy(self):
        """returns a copy of the current state"""
        newd = {}
        for k in self.d.keys():
            newd[k] = self.d[k]
        new = State(newd)
        new.a = self.a
        return new

    def __hash__(self):
        return (self.__str__()).__hash__()

    def __str__(self):
        """returns a string representation of the current state"""
        return str(self.d)

    def move(self, which):
        """"perform operation of 'which' kind"""
        a = self.a
        print(a)
        news = self.copy()
        if which == 'pos':
            news.d['frequency'] += 1
            a += 0.2
            news.d['satisfaction'] = round(news.d['satisfaction'] + 0.2, 1)
            news.d['interest'] = round(news.d['interest'] + calcV(self.d, a), 5)
        elif which == 'neg':
            news.d['frequency'] -= 1
            a -= 0.2
            news.d['satisfaction'] = round(news.d['satisfaction'] - 0.2, 1)
            news.d['interest'] = round(news.d['interest'] + calcV(self.d, a), 5)
        else:
            print('undefined move')
        return news

    def can_move(self, which):
        """test whether it's legal to do an operation of 'which' kind"""
        try:
            a = get_a()
            self.a = a
            if which == 'pos':
                if a + 0.2 > 1: return False
                if self.d['satisfaction'] + 0.2 > 5: return False
                if self.d['frequency'] + 1 > 7: return False
                if self.d['interest'] + calcV(self.d, a + 0.2) > 0.99: return False
                if self.d['interest'] + calcV(self.d, a + 0.2) < 0.01: return False
            elif which == 'neg':
                if a - 0.2 < 0.01: return False
                if self.d['satisfaction'] - 0.2 < 1: return False
                if self.d['frequency'] - 1 < 0: return False
                if self.d['interest'] + calcV(self.d, a - 0.2) > 0.99: return False
                if self.d['interest'] + calcV(self.d, a - 0.2) < 0.01: return False
            return True
        except Exception as e:
            print(e)


# example goal state
CREATE_GOAL_STATE = lambda: State({'interest': 0.99, 'satisfaction': 1, 'frequency': 7})

CREATE_INITIAL_STATE = lambda: State({'interest': 0.5, 'satisfaction': 3, 'frequency': 2})


def goal_test(s):
    """test if s is in goal state, i.e., having same I and S"""
    goal = CREATE_GOAL_STATE()
    tol = 0.05
    return abs(s.d['interest'] - goal.d['interest']) <= tol and abs(s.d['satisfaction'] - goal.d['satisfaction']) <= tol


GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)


def goal_message():
    """print goal_message"""
    return 'Now you are BFFs!'


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


NAMES = {'pos': 'Positive action', 'neg': 'Negative action'}
OPERATORS = [Operator(NAMES[which],
                      lambda s, which1=which: s.can_move(which1),
                      lambda s, which1=which: s.move(which1)
                      ) for which in NAMES.keys()]


def h(state):
    """maps the state to a non-negative real number"""
    g = CREATE_GOAL_STATE()
    return abs((g.d['interest'] - state.d['interest'])) + abs((g.d['satisfaction'] - state.d['satisfaction']))


def calcV(d, a):
    N = d['frequency']
    S = d['satisfaction']
    I = d['interest']
    return N / (10 * S) * I * (2 * a - 1) - 0.01


def get_a():
    """get a random number from a normal distribution that is between 0.01 and 1"""
    a = 999
    while a > 1 or a < 0.01:
        a = random.gauss(0.5, 0.5 / 3)
    return a


"""
To get new state from previous state,
first we have a random variable a from 0.01 to 1,
when doing 'pos' operator, a = a + 0.2,
and when doing 'neg' operator, a = a - 0.2.
For either operator,
new interest = old interest + V,
where V = freq. / (10 * satis.) * interest * (2 * a - 1) - 0.01



Example 1: 
goal: {'interest': 0.7, 'satisfaction': 3, 'frequency': 5}

init: {'interest': 0.5, 'satisfaction': 4, 'frequency': 2}
h(init): 1.2
assuming a = 0.21

after 'pos' operator,
V = 2 / (10 * 4) * 0.5 * (2 * (0.21+0.2) - 1) - 0.01 = -0.0245
pos: {'interest': 0.4755, 'satisfaction': 5, 'frequency': 3}
h(pos): (0.7 - 0.4755) + (5 - 3) 2 = 2.224

after 'neg' operator,
V = 2 / (10 * 4) * 0.5 * (2 * (0.21-0.2) - 1) - 0.01 = -0.0345
neg: {'interest': 0.4655, 'satisfaction': 3, 'frequency': 1}
h(neg): (0.7 - 0.465) + (3 - 3) = 0.234

Example 2:
goal: {'interest': 0.3, 'satisfaction': 2, 'frequency': 3}

init: {'interest': 0.6, 'satisfaction': 2, 'frequency': 5}
h(init): (0.6 - 0.3) + (2 - 2) = 0.3
assuming a = 0.34

after 'pos' operator,
V = 5 / (10 * 2) * 0.6 * (2 * (0.34+0.2) - 1) - 0.01 = 0.002
pos: {'interest': 0.6002, 'satisfaction': 3, 'frequency': 6}
h(pos): (0.6002 - 0.3) + (3 - 2) = 1.3002

after 'neg' operator,
V = 5 / (10 * 2) * 0.6 * (2 * (0.34-0.2) - 1) - 0.01 = -0.118
neg: {'interest': 0.482, 'satisfaction': 1, 'frequency': 4}
h(neg): (0.482 - 0.3) + (2 - 1) = 1.182
"""
