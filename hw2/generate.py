#!/usr/bin/env python
# coding=utf-8

import os
import random

for i in xrange(1,11):
	os.system('rm -rf ./TestCase/Test{0}'.format(i))
	os.system('mkdir ./TestCase/Test{0}'.format(i))
	fileHandler = file('./TestCase/Test{0}/input.txt'.format(i), 'a')
	mode = ["MINIMAX", "ALPHABETA"]
	youplay = ["X", "O"]
	character = ["X", "O", "."]
	n = random.randint(1,26)
	if n > 13:
		depth = random.randint(1,3)
	else:
		depth = random.randint(1,7)
	fileHandler.write(str(n))
	fileHandler.write("\r\n")
	fileHandler.write(mode[random.randint(0,1)])
	fileHandler.write("\r\n")
	fileHandler.write(youplay[random.randint(0,1)])
	fileHandler.write("\r\n")
	fileHandler.write(str(depth))
	fileHandler.write("\r\n")
	for j in xrange(1,n+1):
		for k in xrange(1,n):
			fileHandler.write(str(random.randint(1,100)))
			fileHandler.write(" ")
		fileHandler.write(str(random.randint(1,100)))
		fileHandler.write("\r\n")
	for j in xrange(1,n+1):
		for k in xrange(1,n+1):
			fileHandler.write(character[random.randint(0,2)])
		if j != n:
			fileHandler.write("\r\n")
	fileHandler.close

		





