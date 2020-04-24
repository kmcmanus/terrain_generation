import pygame
import grid
import BMPWriter
import time
import color

def init(width, height, square_size, map_generator, height_generator, name, h_border, v_border):
	global window
	#create the screen
	window = pygame.display.set_mode((width * square_size, height * square_size)) 
	pygame.init()
	return grid.grid(width, height, square_size, map_generator, height_generator, name, h_border, v_border)

def draw(g, color_generator):	
	for x in xrange(g.horizontal_squares):
		for y in xrange(g.vertical_squares):
			pygame.draw.rect(window, color_generator(g.map[x%g.horizontal_squares][y%g.vertical_squares]), pygame.Rect(x*g.square_size, y*g.square_size, g.square_size, g.square_size))
			
	for river in g.rivers:
		for point in river:
			x = point[0]
			y = point[1]
			pygame.draw.rect(window, color.blue, pygame.Rect(x * g.square_size, y * g.square_size, g.square_size, g.square_size))
	#draw it to the screen
	pygame.display.flip() 	
	render_bmp(g, color_generator)
	
def render_bmp(gr, color_generator):
	pixels = ""
	header = BMPWriter.default_bmp_header
	header["width"] = gr.horizontal_squares * gr.square_size
	header["height"] = gr.vertical_squares * gr.square_size
	for y in xrange(gr.vertical_squares - 1, -1,  -1):
		line = ""
		for x in xrange(gr.horizontal_squares):
			(r, g, b) = color_generator(gr.map[x][y])
			line += BMPWriter.pack_color(r, g, b) * gr.square_size
		line += BMPWriter.row_padding(header['width'], header['colordepth'])
		pixels += line * gr.square_size
	BMPWriter.bmp_write(header, pixels, "/home/kevin/Pictures/" + gr.name + "." + str(gr.horizontal_squares) + ".bmp")
	
def write_terrain(g, color_generator):
	file = open("/" + g.name + "." + str(g.horizontal_squares) + ".txt", "w")
	#for y in xrange(len(g.map)):
	#	for x in xrange(len(g.map[y])):
	for y in xrange(g.vertical_squares):
		for x in xrange(g.horizontal_squares):
			file.write(color.terrain_char(g.map[x][y]))
		file.write("\n")
	
def print_terrain(g, color_generator):
	for y in xrange(g.vertical_squares):
		for x in xrange(g.horizontal_squares):
			print color.terrain_char(g.map[x][y]),
		print ""
		
	print "--------------I'M ALL DONE-----------------"
	
def write_out(g, color_generator):
	file = open("/" + g.name + "." + str(g.horizontal_squares) + ".txt", "w")
	for y in xrange(len(g.map)):
		for x in xrange(len(g.map[y])):
			file.write(str(g.map[x][y]) + ", ")
		file.write("\n")
	
def print_out(g, color_generator):
	for y in xrange(len(g.map)):
		for x in xrange(len(g.map[y])):
			print str(g.map[x][y]) + ", ",
		print ""
		
	print "--------------I'M ALL DONE-----------------"
