from selenium import webdriver

#HELPERS
def getShadowRoot(host):
    shadowRoot = driver.execute_script("return arguments[0].shadowRoot", host)
    return shadowRoot

def click(elem):
	driver.execute_script("return arguments[0].click()",elem)

def update_keyboard():
	# Get first shadow host and access its shadow root
	host1 = driver.find_element_by_tag_name("game-app")
	root1 = getShadowRoot(host1, driver)
	# Get second shadow host and access its shadow root
	host2 = root1.find_element_by_tag_name("game-theme-manager")
	host3 = host2.find_element_by_tag_name("game-keyboard")
	key_root = getShadowRoot(host3, driver)

	keyb = {}
	rows = key_root.find_elements_by_class_name("row")
	for row in rows:
		btns = row.find_elements_by_tag_name("button")
		for btn in btns:
			attr = btn.get_attribute("data-key")
			keyb[attr] = btn

def start():
	global driver
	driver = webdriver.Safari()
	driver.get('https://www.powerlanguage.co.uk/wordle/')
	body = driver.find_element_by_tag_name("body")
	body.click() #hides instructions

	# MAKE KEYBOARD
	host1 = driver.find_element_by_tag_name("game-app")
	root1 = getShadowRoot(host1)
	# Get second shadow host and access its shadow root
	host2 = root1.find_element_by_tag_name("game-theme-manager")
	host3 = host2.find_element_by_tag_name("game-keyboard")
	key_root = getShadowRoot(host3)

	global keyb
	keyb = {}
	rows = key_root.find_elements_by_class_name("row")
	for row in rows:
		btns = row.find_elements_by_tag_name("button")
		for btn in btns:
			attr = btn.get_attribute("data-key")
			keyb[attr] = btn
	
	print(keyb.keys())
	# MAKE BOARD
	global board
	board = host2.find_elements_by_tag_name("game-row")



#Gets the keyboard in dictionary form {"a": button, "b": button, etc...}
def get_keyboard():
	return keyb

def input_word(word):
	for letter in word:
		if letter in keyb.keys():
			btn = keyb[letter]
			click(btn)
	click(keyb["↵"])



def get_evaluations(row):
	row = board[row]
	root = getShadowRoot(row)
	tiles = root.find_elements_by_tag_name("game-tile")

	present = []
	correct = []
	absent = []
	for i in range(len(tiles)):
		tile = tiles[i]
		evaluation = tile.get_attribute("evaluation")
		letter = tile.get_attribute("letter")
		
		if evaluation == "correct":
			pair = (letter, i)
			correct.append(pair)
		elif evaluation == "present":
			present.append(letter)
		elif evaluation == "absent":	
			if letter not in [first for first, _ in correct] and letter not in present:
				absent.append(letter)
		else:
			return -1,-1,-1


	return correct, absent, present


	ans = []
	for key in keyb.keys():
		btn = keyb[key]
		attr = btn.get_attribute("data-state")
		if attr == "absent":
			ans.append(key)
	return ans

def clear():
	for i in range(5):
		click(keyb["←"])

def close():
	driver.close()


