import pygame
import sys
import color
import generator
import render
import detailer
import weight
import grid as g
import random
import math

current_color_generator = color.terrain
current_height_generator = generator.land
current_detailer = detailer.shift
current_output = render.draw
current_weight_generator = weight.random
current_map_generator = g.continent_map(generator.ocean) #g.ocean_map(generator.ocean)
if len(sys.argv) > 1:
	random.seed(sys.argv[1])
else:
	seed = random.randint(0, 10000)
	print "Seed is " + str(seed)
	random.seed(seed)

for y in xrange(20):

	seed = random.randint(0, 10000)
	grid = render.init(50, 30, 16, current_map_generator, current_height_generator,"Map" + str(seed), g.BORDER_OCEAN, g.BORDER_OCEAN)
	print "Hi!"
	render.draw(grid, current_color_generator)	
	current_output(grid, current_color_generator)
	for x in xrange(4):
		grid = current_detailer(grid, current_weight_generator)
		print "Done Detailing"
		current_output(grid, current_color_generator)
		render.render_bmp(grid, current_color_generator)	
	print "Done Outputting"	

pygame.quit()