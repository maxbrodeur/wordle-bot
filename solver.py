from random import randint

def pick_random():
	with open("fiveletterwords.txt", 'r') as f:
		lines = f.readlines()
		length = len(lines)
		index =	randint(0,length)
		return lines[index]

#HERE
def new_guess(correct, absent, present):
	with open("fiveletterwords.txt", 'r') as f:

		lines = f.readlines()
		lines = [word for word in lines if all([letter not in absent for letter in word])]
		lines = [word for word in lines if all([word[index]==letter for letter, index in correct])]
		lines = [word for word in lines if all(letter in word for letter in present)]

		length = len(lines)
		index =	randint(0,length-1)
		return lines[index]