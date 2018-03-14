# Ken Lo
# CSE 415
# Assignment 1 Part B

import random

cycle = True  # cycle between responses


def introduce():
	"""Returns an introduction of the agent"""
	intro = """My name is Jon Snow, I know nothing.\n 
	I was created by Ken Lo. If you want to teach me something, contact him at thlo@uw.edu.\n 
	Winter is coming, where is my aunt?"""
	return intro


def agentName():
	"""Returns the nickname of the agent"""
	return 'Jon'


# initialize the memory
memory = {'iam': 'the King in the North', 'youare': 'not aware of the Game of Thrones?',
		  'think': 'the world deserves a new ruler'}


def respond(theInput):
	"""Returns a response based on theInput"""
	wordlist = remove_punctuation(theInput).split(' ')
	wordlist[0] = wordlist[0].lower()
	mapped_wordlist = you_me_map(wordlist)
	mapped_wordlist[0] = mapped_wordlist[0].capitalize()
	global cycle
	if wordlist[0] == '':  # if the user input an empty string
		if cycle:
			cycle = not cycle
			return 'Say something, I am a busy man.'
		else:
			cycle = not cycle
			return """The White Walkers are coming, I must defeat the Night King. 
			Stop wasting my time. Are you going to say something?"""
	if is_greeting(wordlist):  # if the user has a greeting word in the input
		if cycle:
			cycle = not cycle
			return 'I am Jon Snow, the bastard son of Lord Eddard Stark'
		else:
			cycle = not cycle
			return 'Hello, I\'m no one.'
	if 'fat' in wordlist:
		return 'Speaking of fat, Robert is really fat.'
	if 'think' in wordlist:
		memory['think'] = mapped_wordlist[wordlist.index('think') + 1:]
		return 'I think ' + ' '.join(memory['think']) + ', too.'
	if 'love' in wordlist:  # if the user has 'love' in the input
		if cycle:
			cycle = not cycle
			return 'I love Ygritte. <3'
		else:
			cycle = not cycle
			return 'I love my aunt, Dany. <3'
	if 'king' in wordlist:  # if the user mentions 'king'
		if cycle:
			cycle = not cycle
			return '''Have you seen the Night King? I have, beyond he wall. 
					I fought him, he deserves a medal for javeline.'''
		else:
			cycle = not cycle
			return "You know nothing."
	if wordlist[0:2] == ['i', 'am']:  # if the user starts with 'i am ...'
		memory['youare'] = mapped_wordlist[2:]
		return 'Really? Good to know that you are' + mapped_wordlist[2:] + '. '
	if wordlist[0] in ['who', 'what', 'when', 'where', 'why', 'how']:
		# if the user asks a question using W5H
		return 'I don\'t have time to answer questions, I need to defeat the Night King. '
	if 'sleep' in wordlist or 'rest' in wordlist:  # if the user mentions sleep or rest
		return 'The Night King does not rest, we must hurry. '
	if 'cold' in wordlist or 'warm' in wordlist:  # if the user mentions cold or warm
		return """You want to stay warm? My friend Tormund says walking's good, fighting's better
		XXXXing's best. ;) """
	if 'men' in wordlist or 'man' in wordlist:
		return 'We need men, lots of men, if we want to win this Game of Thrones'
	if 'women' in wordlist or 'woman' in wordlist:  # if the user mentions woman/women
		if cycle:
			cycle = not cycle
			return """All men and women must be armed to fight. By the way, you should ask me about
		the women I love. ;) """
		else:
			cycle = not cycle
			return """He rode through the streets of the city, 
						Down from his hill on high, 
						O'er the wynds and the steps and the cobbles, 
						He rode to a woman's sigh.
						
						For she was his secret treasure, 
						She was his shame and bliss. 
						And a chain and a keep are nothing, 
						Compared to a woman s kiss
						
						For hands of gold are always cold 
						But a woman's hands are warm 
						For hands of gold are always cold 
						But a woman's hands are warm"""
	if 'no' in wordlist:  # if the user has 'no' in the input
		if cycle:
			cycle = not cycle
			return 'Never say never! ;)'
		else:
			cycle = not cycle
			return 'Huh? Why not?'
	if 'rule' in wordlist or 'government' in wordlist or 'system' in wordlist or 'emperor' in wordlist:
		# if the user mentions rule/government/system
		return """The old dictatorship only plants fear, we must break the wheel. Where's Dany? """
	if wordlist[0:2] == ['you', 'are']:  # if the user starts with 'you are':
		memory['iam'] = (' '.join(mapped_wordlist[2:]))
		return 'I am ' + ' '.join(mapped_wordlist[
								  2:]) + '''? Say whatever you want, I do not care what the world thinks of me.'''
	if 'tv' in wordlist or 'television' in wordlist:  # if the user mentions tv/television
		return 'Have you heard of the tv show called Game of Thrones? I heard it\'s really good. '
	if 'wedding' in wordlist or 'ceremony' in wordlist or 'ceremonies' in wordlist:  # if the user mentions wedding/ceremony
		return """I don't like weddings and ceremonies, people die in weddings and ceremonies. """
	if has_seasons(wordlist):  # if the user talks about seasons
		return """Winter is already here. I am still waiting for GOT season 8. """
	if 'bastards' in wordlist or 'bastard' in wordlist:  # if the user mentions 'bastard(s)'
		return 'Wait...How do you know I am a bastard?'
	return punt()  # punt if the user input does not meet any rule above


def remove_punctuation(words):
	"""remove any punctuation in words and return it"""
	punctuations = [',', '.', '?', '!', ';', ':']
	unpunctuated = ''.join([c for c in words if c not in punctuations])
	return unpunctuated


CASE_MAP = {'i': 'you', 'I': 'you', 'me': 'you', 'you': 'me',
			'my': 'your', 'your': 'my', 'yours': 'mine', 'mine': 'yours', 'am': 'are'}


def you_me(w):
	'Changes a word from 1st to 2nd person or vice-versa.'
	try:
		result = CASE_MAP[w]
	except KeyError:
		result = w
	return result


def you_me_map(wordlist):
	'Applies YOU-ME to a whole sentence or phrase.'
	return [you_me(w) for w in wordlist]


def is_greeting(wordlist):
	"""Returns True if wordlist contains any of the greeting_words, else returns False"""
	greeting_words = ['hello', 'hi', 'greetings', 'yo', 'hey']
	for word in wordlist:
		if word in greeting_words:
			return True
	return False


def has_seasons(wordlist):
	"""Check if wordlist has any season, return True if it does, else False"""
	triggers = ['spring', 'summer', 'autumn', 'winter', 'season', 'seasons']
	for w in wordlist:
		if w.lower() in triggers:
			return True
		else:
			return False


def punt():
	"""returns a punt"""
	punts = ['I live in Winterfell, how about you, ' + ' '.join(memory['youare']) + ' ? ',
			 'So why do you think i am ' + ''.join(memory['iam']) + ' ?',
			 'Can you tell me more about how you are ' + ' '.join(memory['youare']) + ' ? ',
			 'Part of the Wall has been destroyed by the Night King, we need builders and workers' +
			 ' to rebuild it,',
			 'Do you think I know nothing about feeling in love? Ygritte said so.....',
			 'Why do you think' + ' '.join(memory['think']) + ' ? ',
			 'Stop wasting time thinking about ' + ' '.join(memory['think']) + ', we have more important things to do']
	return random.choice(punts)
