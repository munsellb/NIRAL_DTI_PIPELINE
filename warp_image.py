#!/usr/bin/env python
# _AUTHOR_ _ARTHUR MEDEIROS_

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 4		
slash = "/"
import sys
import os
arguments = {}

if len(sys.argv) > 1 and sys.argv[1] == "-- help":
  print ""
  print "--------This is the warp_image script--------"
  print "The sintax to run the script: warp_image.py -conf 'config_file_name.txt'"
  print "Example: warp_image.py -conf 'config.txt' "
  print "------------------------------------------------------------"
  print "------- This is how the config file must look like: -------- "
  print "   "
  print "REF:'It is the register'"
  print "MOV:'It is the Atlas'"
  print "OUT_ANTS_PREFIX:'point directory where the files will be placed'"
  print "OUT_WARP: 'point directory where the files will be placed'"
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
	print "ERROR: You must pass only",NUM_ARGUMENTS*2,"arguments!"
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

arguments_names = ["REF", "config","MOV","OUT_ANTS_PREFIX","SubjectFolder"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
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
	
	#ID_ARGS.append(split_str[0])
	#NAME_ARGS.append(split_str[1])


#checking

checkParameters(arguments, arguments_names)
print arguments_names


subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"
  
arguments["REF"] = subject_folder + arguments["REF"]  

os.system("mkdir registration")

arguments["OUT_ANTS_PREFIX"]=subject_folder + "registration/" + arguments["OUT_ANTS_PREFIX"]
output = subject_folder + "registration/" + arguments["MOV"][arguments["MOV"].rfind("/")+1:]
output = output[:output.find(".")] + "_warp.nii.gz"
print "output name: ", output
#running WARP
os.system("WarpImageMultiTransform 3 "+arguments["MOV"]+" "+output+" -R "+arguments["REF"]+" --use-NN "+arguments["OUT_ANTS_PREFIX"]+"Warp.nii.gz"+" "+arguments["OUT_ANTS_PREFIX"]+"Affine.txt")