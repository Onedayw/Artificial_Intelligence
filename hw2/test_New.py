#!/usr/bin/env python
# coding=utf-8

import os

os.system('rm -rf ./Result')
os.system('mkdir ./Result')

for i in xrange(1,97):
	print("--Test Case #{0}--".format(i))
	os.system('cp ./TestCase_New/Test{0}/input.txt ./input.txt'.format(i))
	os.system('time ./a.out')
	print("")
	os.system('diff ./output.txt ./TestCase_New/Test{0}/output.txt'.format(i))
	os.system('cp ./output.txt ./Result/output{0}.txt'.format(i))

os.system('rm input.txt output.txt')