import math
import number
import random

teal = (0, 128, 128)
navy = (0, 0, 128)
blue = (0, 0, 255)
tan = (210, 180, 140)
green = (0, 255, 0)
darkgreen = (0, 128, 0)
chocolate = (210, 105, 30)
saddlebrown = (150, 75, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
black = (0, 0, 0)

def get_level(level):
	#level = level - random.random()
	return math.floor(((level/11.0) * 255))
	
grass_level = get_level(7)
water_level = get_level(6)
dirt_level = get_level(8)
shallow_level = get_level(2)
change_area = 3
mountain_level = dirt_level + change_area


def interpolate(c1, c2, weight):
	r = math.floor(number.interpolate(c1[0], c2[0], weight))
	g = math.floor(number.interpolate(c1[1], c2[1], weight))
	b = math.floor(number.interpolate(c1[2], c2[2], weight))
	return (r, g, b)
	
def get_ratio(min, max, val):
	return (max - val) / (max - min)
	
def greyscale(level):
	return (level, level, level)
	
def terrain_char(level):
	if level < 0:
		return " "
	if level < water_level - change_area:
		# "water"
		if level < water_level - shallow_level:
			# "deep water"
			return "w"
		else:
			# "shallow water"			
			return "w"
	elif level < water_level + change_area:
		# "water to sand"
		return "~"
	elif level < water_level + (2 * change_area):
		# "sand to grass"
		return "~"
	elif level < grass_level - change_area:
		# "grass"
		return "."
	elif level < grass_level + change_area:
		# "grass to hill"
		return "."
	elif level < dirt_level - change_area:
		# "dirt"
		return "n"
	elif level < dirt_level + change_area:
		# "mountains"
		return "^"
	elif level <= 256:
		return "A"
	else:
		return black	

def terrain(level):
	if level < 0:
		return black
	if level < water_level - change_area:
		# "water"
		if level < water_level - shallow_level:
			# "deep water"
			return navy
		else:
			# "shallow water"			
			return interpolate(navy, teal, get_ratio(water_level - shallow_level, water_level - change_area, level))
	elif level < water_level + change_area:
		# "water to sand"
		return interpolate(teal, tan, get_ratio(water_level - change_area, water_level + change_area, level))
	elif level < water_level + (2 * change_area):
		# "sand to grass"
		return interpolate(tan, green, get_ratio(water_level + change_area, water_level + (2 * change_area), level))
	elif level < grass_level - change_area:
		# "grass"
		return interpolate(green, darkgreen, get_ratio(water_level + (2 * change_area), grass_level - change_area, level))
	elif level < grass_level + change_area:
		# "grass to hill"
		return interpolate(darkgreen, chocolate, get_ratio(grass_level - change_area, grass_level + change_area, level))
	elif level < dirt_level - change_area:
		# "dirt"
		return interpolate(chocolate, saddlebrown, get_ratio(grass_level + change_area, dirt_level - change_area, level))
	elif level < dirt_level + change_area:
		# "mountains"
		return interpolate(saddlebrown, grey, get_ratio(dirt_level - change_area, dirt_level + change_area, level))
	elif level <= 256:
		return interpolate(grey, white, get_ratio(dirt_level + change_area, 256, level))
	else:
		return black