# Generate svg file
import math
import numpy
import random
import scipy.stats

with open('header.txt', 'r') as myfile:
    pre_file = myfile.read()
post_file = '\n\n</svg>'
fo = open("../svg/my_examples/tree.svg", "wb")
fo.write(pre_file);

r = lambda: random.randint(0,66)

def poly_write(f, x00,y00, x10,y10, 
	x01,y01, x11,y11):
	pre_pre_line = '\n<polygon fill="'
	color = '#' + hex(r())[2:] + hex(r())[2:] +hex(r())[2:]
	post_pre_line = '" points="'
	pre_line = pre_pre_line + color + post_pre_line
	post_line = '"/>'

	line = pre_line 
	line = line + str(x00) + ',' + str(y00)
	line = line + ' ' + str(x10) + ',' + str(y10)
	line = line + ' ' + str(x01) + ',' + str(y01)
	line = line + post_line 
	f.write(line)

	line = pre_line
	line = line + str(x10) + ',' + str(y10)
	line = line + ' ' + str(x01) + ',' + str(y01)
	line = line + ' ' + str(x11) + ',' + str(y11)
	line = line + post_line 
	f.write(line)

def recursive_write(f, s, c, x00,y00, x10,y10, 
	x01,y01, x11,y11, x_bx,x_by, y_bx,y_by):
	# first_stop = s + random.expovariate(1.0/100)
	# print s
	mean = s-10
	# print mean
	var = s-15
	p = 1 - (var/mean)
	n = mean/p
	first_stop = s + numpy.random.binomial(n, p)
	# print first_stop
	next_stop = 0
	for i in range(s,int(c)):
		x = float(i)
		poly_write(fo, x00,y00, x10,y10, x01,y01, x11,y11)
		x00 = x01
		y00 = y01
		x10 = x11
		y10 = y11
		d_width = 3000*(math.cos(2*math.pi*x/100)/math.pow(x,1.5))
		d_height = 4000*(math.sin(2*math.pi*x/100)/math.pow(x,1.5))
		x01 = x01 - d_width*x_bx + d_height*y_bx
		y01 = y01 - d_height*y_by + d_width*x_by
		xvect = x01 - x00
		yvect = y01 - y00
		xnorm = yvect
		ynorm = -xvect
		x11 = x01 - xnorm
		y11 = y01 - ynorm
		if (i == round(first_stop)):
			rx00 = x00
			ry00 = y00
			rx01 = x00
			ry01 = y00

			next_stop = i + 5

		if (i == next_stop):
			rx10 = x00
			ry10 = y00
			rx11 = x00
			ry11 = y00
			ry_bx = rx00 - rx10
			ry_by = ry00 - ry10
			ry_mag = math.sqrt(ry_bx*ry_bx + ry_by*ry_by)
			ry_bx = -ry_bx/ry_mag
			ry_by = -ry_by/ry_mag

			yvect = ry10 - ry00
			xvect = rx10 - rx00

			rx_bx = yvect
			rx_by = -xvect
			rx_mag = math.sqrt(rx_bx*rx_bx + rx_by*rx_by)
			rx_bx = -rx_bx/rx_mag
			rx_by = -rx_by/rx_mag

			next_stop = 0
			first_stop = i + numpy.random.binomial(n, p)

			if (scipy.stats.bernoulli.rvs(.5) == 1):
				if (scipy.stats.bernoulli.rvs(.5) == 1):
					recursive_write(f, i+1, c, rx00,ry00, rx10,ry10, \
						rx01,ry01, rx11,ry11, rx_bx,rx_by, ry_bx,ry_by)
				else:
					recursive_write(f, i+1, c, rx00,ry00, rx10,ry10, \
						rx01,ry01, rx11,ry11, -rx_bx,-rx_by, ry_bx,ry_by)
			else:
				if (scipy.stats.bernoulli.rvs(.5) == 1):
					recursive_write(f, i+1, c, rx00,ry00, rx10,ry10, \
						rx01,ry01, rx11,ry11, rx_bx,rx_by, -ry_bx,-ry_by)
				else:
					recursive_write(f, i+1, c, rx00,ry00, rx10,ry10, \
						rx01,ry01, rx11,ry11, -rx_bx,-rx_by, -ry_bx,-ry_by)

x00 = 180.0
y00 = 642.0
x10 = 300.0
y10 = 642.0
start = 20
counter = 400.0

recursive_write(fo, start, counter, x00,y00, \
	x10,y10, x00,y00, x10,y10, 1,0, 0,1)

fo.write(post_file);
fo.close()