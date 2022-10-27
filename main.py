import solver
import web_interact as web

import time

web.start(fullscreen=True)
# web.start()

#guess = solver.pick_random()
#guess = "atone"
guess = "beast"
# guess = "arose"
time.sleep(2) #	wait for redraw
web.input_word(guess)

green = []
black = []
yellow = []
for i in range(6):
	correct, absent, present = web.get_evaluations(i)

	#IF GUESS WAS INVALID
	while correct == -1:
		web.clear()
		guess = solver.new_guess(green, black, yellow)
		web.input_word(guess)
		correct, absent, present = web.get_evaluations(i)

	if len(correct) == 5: break
	# CASE: letter is labelled absent but is also labelled as correct elsewhere
	for letter in absent:
		indices = list(range(5))
		found = False
		for l, i in green:
			if letter == l:
				found = True
				indices[i] = -1
		if found:
			# label as present in word but not anywhere else as correct position
			for i in indices:
				if i>=0:
					present.append((letter, i))
			absent = [a for a in absent if a!=letter]

		
	green = list(set(correct) | set(green))
	black = list(set(absent) | set(black))
	yellow = list(set(present) | set(yellow))

	guess = solver.new_guess(green, black, yellow)
	web.input_word(guess)


time.sleep(10)
web.close()