#!/usr/bin/env python
#__author__ = 'JESSEROCHA'

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 3
slash = "/"
import sys
import os
arguments = {}

def checkParameters(parameters, valid_ones):
	for k in parameters.keys():
		if not (k in valid_ones):
			print "ERROR:", k, "is not a valid paramater!"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			exit(-1)

print "Num of arguments passed:",len(sys.argv) -1

if len(sys.argv)-1 != NUM_ARGUMENTS*2:
	print "ERROR: You must pass",NUM_ARGUMENTS*2,"arguments!"
	exit(-1)

i = 1
while i < len(sys.argv):
	print "!"
	if sys.argv[i].find("-") != -1:
		arguments[sys.argv[i][1:]] = sys.argv[i+1]
		i = i + 1
	i = i + 1
print arguments
print "working directory:",os.getcwd()

arguments_names = ["config", "INPUT_IMAGE", "OUTPUT_IMAGE","EXTRACT_LABEL"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should contain",NUM_PARAMETERS,"parameters"
	exit(-1)

#getting the location
for i in range(0,len(lines)):
  	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		exit(-1)
	tokens = lines[i].rstrip().split(':')
	arguments[tokens[0]] = tokens[1]

#checking

checkParameters(arguments, arguments_names)
print arguments

#running ImageMath
os.system("ImageMath " + arguments["INPUT_IMAGE"] + " -extractLabel " + arguments["EXTRACT_LABEL"] + " -outfile " + arguments["OUTPUT_IMAGE"] )

print "done!!!!!!!!"

f.close()
