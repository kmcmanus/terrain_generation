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

"""
for y in xrange(10):
	seed = random.randint(0, 10000)
	grid = render.init(50, 30, 16, current_map_generator, current_height_generator,"Map" + str(y), g.BORDER_OCEAN, g.BORDER_OCEAN)
	print "Hi!"
	current_output(grid, current_color_generator)	
	for x in xrange(2):
		grid = current_detailer(grid, current_weight_generator)
		print "Done Detailing"
		current_output(grid, current_color_generator)
	print "Done Outputting"	
"""
y = 0

grid = render.init(50, 30, 16, current_map_generator, current_height_generator,"Map" + str(y), g.BORDER_OCEAN, g.BORDER_OCEAN)
for i in range(3):
	grid = current_detailer(grid, current_weight_generator)
render.draw(grid, current_color_generator)

#Loop until the user clicks the close button.
done=False
while done==False:
 
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
	keys = pygame.key.get_pressed()
	mouse = pygame.mouse.get_pressed()
	
	if keys[pygame.K_SPACE] == 1:
		print "Detailing"
		grid = current_detailer(grid, current_weight_generator)
		print "Done Detailing"
		current_output(grid, current_color_generator)
		print "Done Drawing"
	
	
	if keys[pygame.K_BACKSPACE] == 1:
		y += 1
		grid = render.init(50, 30, 16, current_map_generator, current_height_generator,"Map" + str(y), g.BORDER_OCEAN, g.BORDER_OCEAN)
		for i in range(3):
			grid = current_detailer(grid, current_weight_generator)
		render.draw(grid, current_color_generator)
		
	if keys[pygame.K_d] == 1:
                print 'render'
		render.render_bmp(grid, current_color_generator)
                print 'doine render'
		
	if keys[pygame.K_c] == 1:
		if current_color_generator == color.terrain:
			current_color_generator = color.greyscale
		else:
			current_color_generator = color.terrain
		current_output(grid, current_color_generator)
	
	if mouse[0] == True:
		(x, y) = pygame.mouse.get_pos()
		x = int(math.floor(x/grid.square_size))
		y = int(math.floor(y/grid.square_size))
		g.drop_river(x, y, 1000, grid, current_output, current_color_generator)
		current_output(grid, current_color_generator)
		
	

pygame.quit()
