#!/usr/bin/env python
# _AUTHOR_ _ARTHUR MEDEIROS_

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 5		
slash = "/"
import sys
import os
arguments = {}

def checkParameters(parameters, valid_ones):
	for k in parameters.keys():
		if not (k in valid_ones):
			print "ERROR:", k, "is not a valid paramater!"
			print "For more information use --help"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			print "For more information use --help"
			exit(-1)

if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print "This script creates Exclusion, Termination and Waypoint Masks"
	print "Syntax to run this script: create_fdt_masks.py -config config_filename"
	print "The config file requires the following format:"
	print "RD:RD_DIRECTORY"
	print "T1:T1_DIRECTORY"
	print "T2:T2_DIRECTORY"
	print "ATLAS:ATLAS_DIRECTORY"
	print "OUT_ANTS_PREFIX:OUT_ANTS_PREFIX -> a prefix name for the output files"
	exit(0)
		
print "Num of arguments passed:",len(sys.argv) -1

if len(sys.argv)-1 != NUM_ARGUMENTS*2:
	print "ERROR: You must pass only",NUM_ARGUMENTS*2,"arguments!"
	print "For more information use --help"
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

arguments_names = ["RD", "config", "T1", "T2","ATLAS","OUT_ANTS_PREFIX"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	print "For more information use --help"
	exit(-1)
	
#getting the location 
for i in range(0,len(lines)):
  	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE" 
		print "For more information use --help"
		exit(-1)
	tokens = lines[i].rstrip().split(':')
	arguments[tokens[0]] = tokens[1]
	
	#ID_ARGS.append(split_str[0])
	#NAME_ARGS.append(split_str[1])


#checking

checkParameters(arguments, arguments_names)
print arguments_names

#running ANTS
os.system("ANTS 3 -m CC\["+arguments["RD"]+","+arguments["T1"]+",1,4\] -m CC\["+arguments["RD"]+","+arguments["T2"]+",1,4\] -r Guass\[3,0\] -i 100x50x25 -t SyN\[0.25\] -o "+arguments["OUT_ANTS_PREFIX"])


