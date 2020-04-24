import number
import grid as g
import random as rand
import math
def smooth(grid, weight_generator):
	new_map = []
	for x in xrange(grid.horizontal_squares):
		new_map.append([])
		for y in xrange(grid.vertical_squares):
			base_color = grid.map[x][y]
			up_color = grid.map[x][y-1]
			down_color = grid.map[x][(y+1)%grid.vertical_squares]
			left_color = grid.map[x-1][y]
			right_color = grid.map[(x+1)%grid.horizontal_squares][y]	
			weight = weight_generator()
			rest = weight/4.0
			color = (weight * base_color) + (rest * up_color) + (rest * down_color)  + (rest * left_color) + (rest * right_color)
			new_map[-1].append(color)
	grid.map = new_map
	return grid
		

def shift(grid, weight_generator):
	new_map = []
	if grid.square_size > 1:
		grid.square_size /= 2
	
	for x in xrange(grid.horizontal_squares):
		new_map.append([])		
		new_map.append([])		
		for y in xrange(grid.vertical_squares):
			new_map[-1].append(0)
			new_map[-1].append(0)
			new_map[-2].append(0)
			new_map[-2].append(0)
			
	print "Resized Map"
	
	for x in xrange(len(grid.map)):
		for y in xrange(len(grid.map[x])):
			color = grid.map[x][y]
			right_color = 0
			down_color = 0
			
			if x + 1 < grid.horizontal_squares:
				right_color = grid.map[x + 1][y]
			elif grid.horizontal_border == g.BORDER_WRAP:
				right_color = grid.map[0][y]
			elif grid.horizontal_border == g.BORDER_MIRROR:
				right_color = grid.map[x][-y]
			elif grid.horizontal_border == g.BORDER_MOUNTAINS:
				right_color = 255
			elif grid.horizontal_border == g.BORDER_OCEAN:
				right_color = 0
			elif grid.horizontal_border == g.BORDER_RANDOM:
				right_color = rand.randrange(0, 255)
			
			if y + 1 < grid.vertical_squares:
				down_color = grid.map[x][y + 1]
			elif grid.vertical_border == g.BORDER_WRAP:
				down_color = grid.map[x][0]
			elif grid.vertical_border == g.BORDER_MIRROR:
				down_color = grid.map[-x][y]
			elif grid.vertical_border == g.BORDER_MOUNTAINS:
				down_color = 255
			elif grid.vertical_border == g.BORDER_OCEAN:
				down_color = 0
			elif grid.vertical_border == g.BORDER_RANDOM:
				down_color = rand.randrange(0, 255)
				
			new_x = x * 2
			new_y = y * 2
			
			#TODO: Have it choose a random quadrant to put the base color
			# or create a shift variable with UP, LEFT, DOWN, RIGHT, IN, OUT, and RANDOM as options
			base_change = 0
			alt_change = 0
			if rand.randrange(0, 99) < 40:
				base_change = rand.randrange(-5, 5)
			new_map[new_x][new_y] = max(0, min(255, color + base_change))
			base_change = 0
			alt_change = 0
			if rand.randrange(0, 99) < 40:
				base_change = rand.randrange(-5, 5)
			if rand.randrange(0, 99) < 40:
				alt_change = rand.randrange(-5, 5)
			new_map[new_x + 1][new_y] = math.floor(number.interpolate(max(0, min(255, color + base_change)), max(0, min(255, right_color + alt_change)), weight_generator()))
			base_change = 0
			alt_change = 0
			if rand.randrange(0, 99) < 40:
				base_change = rand.randrange(-5, 5)
			if rand.randrange(0, 99) < 40:
				alt_change = rand.randrange(-5, 5)
			new_map[new_x][new_y + 1] = math.floor(number.interpolate(max(0, min(255, color + base_change)), max(0, min(255, down_color + alt_change)), weight_generator()))
			new_map[new_x + 1][new_y + 1] = -1
		#print "Line Interpolated - " + str(x) + "/" + str(len(grid.map))
	grid.horizontal_squares *= 2
	grid.vertical_squares *= 2	
	for x in xrange(len(new_map)):
		for y in xrange(len(new_map[x])):
			if new_map[x][y] == -1:
				up_change = 0
				down_change = 0
				left_change = 0
				right_change = 0
				if rand.randrange(0, 99) < 40:
					up_change = rand.randrange(-5, 5)
				if rand.randrange(0, 99) < 40:
					down_change = rand.randrange(-5, 5)
				if rand.randrange(0, 99) < 40:
					right_change = rand.randrange(-5, 5)
				if rand.randrange(0, 99) < 40:
					left_change = rand.randrange(-5, 5)
				vertical_color = number.interpolate(max(0, min(255, new_map[x][(y + 1) % grid.vertical_squares] + up_change)), max(0, min(255, new_map[x][(y - 1) % grid.vertical_squares] + down_change)), weight_generator())
				horizontal_color = number.interpolate(max(0, min(255, new_map[(x + 1) % grid.horizontal_squares][y] + right_change)), max(0, min(255, new_map[(x - 1) % grid.horizontal_squares][y] + left_change)), weight_generator())
				new_map[x][y] = math.floor(number.interpolate(vertical_color, horizontal_color, weight_generator()))
		#print "Line Corner Extrapolated - " + str(x) + "/" + str(len(new_map))
	grid.map = new_map
	
	new_rivers = []
	
	for river in grid.rivers:
		if river != []:
			new_rivers.append(river[0])
		
	grid.rivers = []
	for point in new_rivers:
		new_x = point[0] * 2 + rand.randrange(-1, 1)
		new_y = point[1] * 2 + rand.randrange(-1, 1)
		g.drop_river(new_x, new_y, 100, grid, None, None)
	
	return grid

