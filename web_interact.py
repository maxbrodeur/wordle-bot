from selenium import webdriver
import time

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

def start(fullscreen=False):
	global driver
	driver = webdriver.Safari()
	# driver = webdriver.Chrome()
	driver.get('https://www.nytimes.com/games/wordle/index.html')
	if fullscreen:
		driver.maximize_window()

	body = driver.find_element_by_tag_name("body")
	body.send_keys(webdriver.common.keys.Keys.ESCAPE)

	if fullscreen:
		#scroll down because of add
		body.send_keys(webdriver.common.keys.Keys.SPACE)

	# MAKE KEYBOARD

	host1 = driver.find_element_by_xpath('//div[@id="wordle-app-game"]')
	key_root = host1.find_element_by_xpath('//div[@aria-label="Keyboard"]')
	

	global keyb
	keyb = {}
	rows = key_root.find_elements_by_class_name("Keyboard-module_row__YWe5w")
	for row in rows:
		btns = row.find_elements_by_tag_name("button")
		for btn in btns:
			attr = btn.get_attribute("data-key")
			keyb[attr] = btn
	# MAKE BOARD
	global board
	board = host1.find_elements_by_class_name("Row-module_row__dEHfN")



#Gets the keyboard in dictionary form {"a": button, "b": button, etc...}
def get_keyboard():
	return keyb

def input_word(word):
	time.sleep(0.5)
	for i in range(5):
		letter = word[i]
		if letter in keyb.keys():
			btn = keyb[letter]
			click(btn)
	click(keyb["↵"])



def get_evaluations(row):
	row = board[row]
	# root = getShadowRoot(row)
	# tiles = root.find_elements_by_tag_name("game-tile")
	tiles = row.find_elements_by_class_name("Tile-module_tile__3ayIZ")

	present = []
	correct = []
	absent = []
	for i in range(len(tiles)):
		tile = tiles[i]
		# evaluation = tile.get_attribute("evaluation")
		evaluation = tile.get_attribute("data-state")
		while(evaluation=="tbd"):
			evaluation = tile.get_attribute("data-state")
			animation = tile.get_attribute("data-animation")
			if(animation=="idle"):
				return -1,-1,-1

		# letter = tile.get_attribute("letter")
		label = tile.get_attribute("aria-label")
		letter = label[0]
		
		if evaluation == "correct":
			pair = (letter, i)
			correct.append(pair)
		elif evaluation == "present":
			pair = (letter, i)
			present.append(pair)
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

# CODE FOR OLD WEBSITE
# driver.get('https://www.powerlanguage.co.uk/wordle/')
# host1 = driver.find_element_by_tag_name("wordle-app-game")
# root1 = getShadowRoot(host1)
# Get second shadow host and access its shadow root
# host2 = root1.find_element_by_tag_name("game-theme-manager")
# host3 = host2.find_element_by_tag_name("game-keyboard")
# host2 = host1.find_element_by_tag_name("game-theme-manager")
# key_root = getShadowRoot(host3)
# host3 = host2.find_elements_by_class_name("Keyboard-module_keyboard__1HSnn")[0]
# board = host2.find_elements_by_tag_name("game-row")
# body.click() #hides instructions