import random as rand

def random():
	return rand.randrange(0, 1000)  / 1000.0
	
def constant(c):
	return lambda: c
	
if __name__ == '__main__':
	for x in xrange(100):
		print random()