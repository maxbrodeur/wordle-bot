import solver
import web_interact as web

import time

web.start()

#guess = solver.pick_random()
#guess = "atone"
#guess = "beast"
guess = "arose"
web.input_word(guess)
time.sleep(2) #	wait for redraw

green = []
black = []
yellow = []
for i in range(5):
	correct, absent, present = web.get_evaluations(i)

	#IF GUESS WAS INVALID
	while correct == -1:
		web.clear()
		guess = solver.new_guess(green, black, yellow)
		web.input_word(guess)
		time.sleep(2) #	wait for redraw
		correct, absent, present = web.get_evaluations(i)

	if len(correct) == 5: break
	green = list(set(correct) | set(green))
	black = list(set(absent) | set(black))
	yellow = list(set(present) | set(yellow))
	print(yellow)

	guess = solver.new_guess(green, black, yellow)
	web.input_word(guess)
	time.sleep(2) #	wait for redraw


time.sleep(10)
web.close()