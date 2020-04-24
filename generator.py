import random as rand
import color

def random():
	return rand.randrange(0, 255)
	
def small():
	return rand.randrange(0, 9)
	
def high():
	return 255
	
def earth():
	height = rand.randrange(0, 1000)
	if height <= 5:
		return 255
	if height <= 16:
		return color.get_level(10)
	if height <= 38:
		return color.get_level(9)
	if height <= 83:
		return color.get_level(8)
	if height <= 292:
		return color.get_level(7)
	if height <= 377:
		return color.get_level(6)
	if height <=407:
		return color.get_level(5)
	if height <= 455:
		return color.get_level(4)
	if height <= 594:
		return color.get_level(3)
	if height <= 826:
		return color.get_level(2)
	if height <= 990:
		return color.get_level(1)
	return 0

def land():
	height = rand.randrange(0, 300)
	if height <= 5:
		return 255
	if height <= 16:
		return color.get_level(10)
	if height <= 38:
		return color.get_level(9)
	if height <= 83:
		return color.get_level(8)	
	return color.get_level(7)
	
def ocean():
	height = rand.randrange(600, 999)
	if height <= 594:
		return color.get_level(3)
	if height <= 826:
		return color.get_level(2)
	if height <= 990:
		return color.get_level(1)
	return 1