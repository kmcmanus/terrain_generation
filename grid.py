import random
import color
BORDER_WRAP = 0
BORDER_MIRROR = 1
BORDER_MOUNTAINS = 2
BORDER_OCEAN = 3
BORDER_RANDOM = 4

SHIFT_UP = -1
SHIFT_DOWN = 1
SHIFT_LEFT = -1
SHIFT_RIGHT = 1
SHIFT_IN = 10
SHIFT_OUT = -10
SHIFT_RANDOM = 0
around = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def drop_river(x, y, size, grid, draw, colorer):
	grid.rivers.append([])
	#print "Begin"
	def r(x, y, size, grid):
		#print "Recurse"
		if grid.map[x][y] <= color.water_level:
			#at the ocean, end
			#print (x, y)
			#print grid.map[x][y]
			#print color.water_level
			#print "At Ocean"
			return
			
		if grid.rivers[-1].count((x, y)) > 0:
			#print "Already in"
			return
		
		grid.rivers[-1].append((x, y))
		lowest_points = []
		lowest_level = 1000
		for point in around:
			t_x = x + point[0]
			t_y = y + point[1]
			if t_x < 0 or t_y < 0 or t_x >= grid.horizontal_squares or t_y >= grid.vertical_squares:
				continue
			t_level = grid.map[t_x][t_y]
			if t_level <= lowest_level and grid.rivers[-1].count((t_x, t_y)) > 0:
				continue
			if t_level == lowest_level:
				lowest_points.append((t_x, t_y))
			if t_level < lowest_level:
				lowest_points = [(t_x, t_y)]
				lowest_level = t_level
		if lowest_points == []:
			return
		#pick a random lowest point and go with it
		point = lowest_points[random.randint(0, len(lowest_points) - 1)]
		r(point[0], point[1], size - 1, grid)
		
	r(x, y, size, grid)
	#print "End"

def random_map(grid, height_generator):
	for x in xrange(grid.horizontal_squares):
			grid.map.append([])
			for y in xrange(grid.vertical_squares):
				color = height_generator()
				grid.map[-1].append(color)
				
def continent_map(other_height_generator):
	def func(grid, height_generator):
		for x in xrange(grid.horizontal_squares):
			grid.map.append([])
			for y in xrange(grid.vertical_squares):
				grid.map[-1].append(0)
		for current_continent in xrange(random.randint(7, 14)):
			print "Continent " + str(current_continent)
			grid.continent.append([])
			drop = random.randint(2, 10)
			def drop_continent(x, y, prob):
				if x < 0 or y < 0 or x >= grid.horizontal_squares or y >= grid.vertical_squares or grid.map[x][y] > 0:
					return
				p = random.randint(1, 100)
				"""
				if p > (100 - (100 - prob) / 2.0):
					grid.continent[-1].append((x, y))
					grid.map[x][y] = -1
				"""
				if prob <= p:
					grid.map[x][y] = -1
					grid.continent[-1].append((x, y))
					return
				#if grid.continent[-1].count((x, y)) == 0:
				if grid.map[x][y] == 0:
					grid.map[x][y] = height_generator()					
					grid.continent[-1].append((x, y))
					drop_continent(x, y + 1, prob - drop)
					drop_continent(x, y - 1, prob - drop)
					drop_continent(x + 1, y, prob - drop)
					drop_continent(x - 1, y, prob - drop)					
				else:
					return
			tries = 0
			for tries in xrange(1000):				
				x = random.randrange(grid.horizontal_squares * 0.2, grid.horizontal_squares * 0.8)
				y = random.randrange(grid.vertical_squares * 0.2, grid.vertical_squares * 0.8)
				if grid.map[x][y] == 0 and grid.map[grid.horizontal_squares - 1 - x][grid.vertical_squares - 1 - y] == 0:
					break
					
			if tries == 999:
				break
			print "Tries: " + str(tries)
			drop_continent(x, y, 100)
		for x in xrange(grid.horizontal_squares):
			for y in xrange(grid.vertical_squares):
				if grid.map[x][y] == -1:	
					grid.map[x][y] = other_height_generator()
					for continent in grid.continent:
						if continent.count((x, y)) > 0:
							def all_points_in_continent(continent, points):
								if len(points) == 0:
									return True
								return continent.count(points[0]) > 0 and all_points_in_continent(continent, points[1:])
					
							if all_points_in_continent(continent, [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]):
								grid.map[x][y] = height_generator()			
				if grid.map[x][y] == 0:	
					grid.map[x][y] = other_height_generator()
		for x in xrange(grid.horizontal_squares):
			for y in xrange(grid.vertical_squares):
				if grid.map[x][y] >= color.mountain_level:
						if random.randint(1, 5) == 5:
							drop_river(x, y, random.randint(500, 1000), grid, None, None)
	return func
	
def ocean_map(other_height_generator):
	def func (grid, height_generator):
		for x in xrange(grid.horizontal_squares):
				grid.map.append([])
				for y in xrange(grid.vertical_squares):
					grid.map[-1].append(0)
					
		for x in xrange(10):
			x = 0
			y = 0
			while grid.map[x][y] != 0:	
				x = random.randrange(0, grid.horizontal_squares)
				y = random.randrange(0, grid.vertical_squares)
			grid.map[x][y] = height_generator()
			rrange = random.randrange(6, 12)
			for i in xrange(rrange):			
				x_change = 0
				y_change = 0
				
				for j in xrange(10):
					if grid.map[x + x_change][y + y_change] != 0:
						x_change = 0
						y_change = 0	
						if random.randint(0, 1) == 0:
							x_change = random.randrange(2) - 1
						else:
							y_change = random.randrange(2) - 1
					else:
						break
				
				x += x_change
				y += y_change
				grid.map[x][y] = height_generator()
		
		for x in xrange(grid.horizontal_squares):
				for y in xrange(grid.vertical_squares):
					if grid.map[x][y] == 0:
						grid.map[x][y] = other_height_generator()
	return func
			
class grid:
	def reset(self, map_generator, height_generator):
		self.square_size = self.starting_square_size		
		self.map = []
		self.continent = []
		self.rivers = []
		map_generator(self, height_generator)
				
		if self.horizontal_border == BORDER_OCEAN:
			if self.horizontal_shift == SHIFT_LEFT:
				#COVER LEFT SIDE WITH OCEAN
				for y in xrange(self.vertical_squares):
					self.map[0][y] = 0
			elif self.horizontal_shift == SHIFT_RIGHT:
				#Cover RIGHT side with ocean
				for y in xrange(self.vertical_squares):
					self.map[-1][y] = 0
				
		if self.horizontal_border == BORDER_MOUNTAINS:
			if self.horizontal_shift == SHIFT_LEFT:
				#COVER LEFT SIDE WITH Mountain
				for y in xrange(self.vertical_squares):
					self.map[0][y] = 255
			elif self.horizontal_shift == SHIFT_RIGHT:
				#Cover right side with mountain
				for y in xrange(self.vertical_squares):
					self.map[-1][y] = 255
		
		if self.vertical_border == BORDER_OCEAN:
			if self.vertical_shift == SHIFT_UP:
				#COVER UP SIDE WITH OCEAN
				for x in xrange(self.horizontal_squares):
					self.map[x][0] = 0
			elif self.vertical_shift == SHIFT_DOWN:
				#Cover down side with ocean
				for x in xrange(self.horizontal_squares):
					self.map[x][-1] = 0
				
		if self.vertical_border == BORDER_MOUNTAINS:
			if self.vertical_shift == SHIFT_UP:
				#COVER UP SIDE WITH Mountain
				for x in xrange(self.horizontal_squares):
					self.map[x][0] = 255
			elif self.vertical_shift == SHIFT_DOWN:
				#Cover down side with mountain
				for x in xrange(self.horizontal_squares):
					self.map[x][-1] = 255

	def __init__(self, width, height, square_size, map_generator, height_generator, name = "map", hor_border = BORDER_WRAP, vert_border = BORDER_WRAP, hor_shift = SHIFT_LEFT, vert_shift = SHIFT_UP):
		self.starting_square_size = square_size
		self.width = width
		self.height = height
		self.name = name
		self.square_size = self.starting_square_size
		self.vertical_squares = height
		self.horizontal_squares = width
		self.horizontal_border = hor_border
		self.vertical_border = vert_border
		self.horizontal_shift = hor_shift
		self.vertical_shift = vert_shift
		self.reset(map_generator, height_generator)