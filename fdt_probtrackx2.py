#!/usr/bin/env python
# _AUTHOR_ _ARTHUR MEDEIROS_

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 7		
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
	print "ERROR: You must pass only",NUM_ARGUMENTS*2,"arguments!"
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

arguments_names = ["BEDPOST", "config", "SEEDFILE", "WAYPOINTS","TERMINATIONMASK","EXCLUSIONMASK","OUTPUTPROBTRACK","MASKFILE"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	exit(-1)
	
#getting the location 
for i in range(0,len(lines)):
  	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE" 
		exit(-1)
	tokens = lines[i].rstrip().split(':')
	arguments[tokens[0]] = tokens[1]
	
	
#print("probtrackx -s "+arguments["BEDPOST"]+" -m "+arguments["MASKFILE"]+" -x "+arguments["SEEDFILE"]+" --waypoints "+arguments["WAYPOINTS"]+" --avoid "+arguments["EXCLUSIONMASK"]+" --stop "+arguments["TERMINATIONMASK"]+" -o "+arguments["OUTPUTPROBTRACK"])		
#os.system("probtrackx -s "+arguments["BEDPOST"]+" -m "+arguments["MASKFILE"]+" -x "+arguments["SEEDFILE"]+" --waypoints="+arguments["WAYPOINTS"]+" --avoid="+arguments["EXCLUSIONMASK"]+" --stop="+arguments["TERMINATIONMASK"]+" -o "+arguments["OUTPUTPROBTRACK"])
	
os.system("probtrackx2 -x "+arguments["SEEDFILE"]+" -V 1 -l --onewaycondition -c 0.2 -S 2000 --steplength=0.5 -P 5000 --fibthresh=0.01 --distthresh=0.0 --sampvox=0.0 --avoid="+arguments["EXCLUSIONMASK"]+" --stop="+arguments["TERMINATIONMASK"]+" --forcedir --opd -s "+arguments["BEDPOST"]+" -m "+arguments["MASKFILE"]+" --dir="+os.getcwd()+"/probtrack_test"+" --waypoints="+arguments["WAYPOINTS"]+" --waycond=AND")	
