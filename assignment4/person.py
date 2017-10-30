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
					  lambda s, which1 = which: s.can_move(which1),
					  lambda s, which1 = which: s.move(which1)
					  ) for which in NAMES.keys()]


def h(state):
	"""maps the state to a non-negative real number"""
	g = CREATE_GOAL_STATE()
	return abs((g.d['interest'] - state.d['interest'])) + abs((g.d['satisfaction'] - state.d['satisfaction']))

def calcV(d, a):
	N = d['frequency']
	S = d['satisfaction']
	I = d['interest']
	return N / S * I * (2 * a - 1) - 0.01

def get_a():
	"""get a random number from a normal distribution that is between 0.01 and 1"""
	a = 999
	while a > 1 or a < 0.01:
		a = random.gauss(0.5, 0.5 / 3)
	return a


"""
Examples:
Suppose our GOAL_STATE is {I: 0.9, S: 2},
and initial_state {I: 0.7, S: 1}, with hidden variables
N = 2, a = 0.4 and V = -0.289, 
we have h(initial_state) = 1.2
if we apply 'pos' operator to initial_state,
we have new_state  {I: 0.411, S: 2}
which yields h(new_state) = 0.489

Suppose our another GOAL_STATE2 is {I: 0.3, S: 5},
and initial_state {I: 0.9, S:3}, with hidden variables
N = 6, a = 0.3 and V = -0.154
we have h(initial_state) = 2.6
if we apply 'neg' operator to initial_state,
we have new_state2 {I: 0.746, S: 2},
which yields h(new_state2) = 3.446
"""
