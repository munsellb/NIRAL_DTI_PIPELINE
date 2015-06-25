#!/usr/bin/env python
#__author__ = 'JESSEROCHA'

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 3
slash = "/"
import sys
import os
arguments = {}

if len(sys.argv) > 1 and sys.argv[1] == "-- help":
  print ""
  print "--------This is the extract_brain_region script--------"
  print "The sintax to run the script: extract_brain_region.py -conf 'config_file_name.txt'"
  print "Example: extract_brain_region.py -conf 'configRegions.txt' "
  print "------------------------------------------------------------"
  print "------- This is how the config file must look like: -------- "
  print "   "
  print "SubjectFolder: 'A directory that contains image data for an unique subject'"
  print "INPUT_IMAGE: 'Warped structural atlas located in SubjectFolder/registration'"
  print "EXTRACT_LABEL:'Label number to extract. The output file is named \"brain<EXTRACT_LABEL>.nii.gz\" and will be located in SubjectFolder/regions'"
  print "  "
  print "  "
 
  exit(0)

 

def checkParameters(parameters, valid_ones):
	for k in parameters.keys():
		if not (k in valid_ones):
			print "ERROR:", k, "is not a valid paramater!"
			print "Please type --help to get more information"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			print "Please type --help to get more information"
			exit(-1)

print "Num of arguments passed:",len(sys.argv) -1

if len(sys.argv)-1 != NUM_ARGUMENTS*2:
	print "ERROR: You must pass",NUM_ARGUMENTS*2,"arguments!"
	print "Please type --help to get more information"
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

arguments_names = ["config", "INPUT_IMAGE","EXTRACT_LABEL","SubjectFolder"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should contain",NUM_PARAMETERS,"parameters"
	print "Please type --help to get more information"
	exit(-1)

#getting the location
for i in range(0,len(lines)):
  	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "Please type --help to get more information"
		exit(-1)
	tokens = lines[i].rstrip().split(':')
	arguments[tokens[0]] = tokens[1]

#checking

checkParameters(arguments, arguments_names)
print arguments

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"
  
arguments["INPUT_IMAGE"] = subject_folder + "registration/" + arguments["INPUT_IMAGE"]

os.system("mkdir "+subject_folder+"regions")
output = subject_folder + "regions/brain" + arguments["EXTRACT_LABEL"] + ".nii.gz"
#running ImageMath
os.system("ImageMath " + arguments["INPUT_IMAGE"] + " -extractLabel " + arguments["EXTRACT_LABEL"] + " -outfile " + output )

f.close()
