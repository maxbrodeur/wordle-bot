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
		lines = [word for word in lines if all(letter in word for letter, _ in present)]
		lines = [word for word in lines if all(word[index]!=letter for letter, index in present)]

		length = len(lines)
		if length == 0:
			print("IMPOSSIBLE")
			print("Correct: "+str(correct))
			print("Absent: "+str(absent))
			print("Present: "+str(present))
			print(lines)
			exit(-1)
		else:
			index = randint(0,length-1)
		return lines[index]