#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  run_bedpost.py
#  
#  Copyright 2015 Andy <Andy@ANDY-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

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

arguments_names = ["DTIPREP_DIR", "config", "INPUT_VOL", "INPUT_MASK", "PERL_SCRIPT"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	exit(-1)
	
for i in range(0, NUM_PARAMETERS):
	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE" 
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

#checking
checkParameters(arguments, arguments_names)
print arguments
	
#all arguments were checked
if not (arguments["DTIPREP_DIR"][len(arguments["DTIPREP_DIR"]) - 1] == slash):
    arguments["DTIPREP_DIR"] += slash
outputVolName = arguments["DTIPREP_DIR"] + "data.nii.gz"
outputBVec = arguments["DTIPREP_DIR"] + "bvecs"
outputBVal = arguments["DTIPREP_DIR"] + "bvals"
outputMask = arguments["DTIPREP_DIR"] + "nodif_brain_mask.nii.gz"

os.system("mkdir " + arguments["DTIPREP_DIR"])
print("Running DWIConvert")
os.system("DWIConvert --inputVolume "+arguments["INPUT_VOL"]+" --outputVolume "+outputVolName+" --conversionMode NrrdToFSL --outputBVectors "+outputBVec+" --outputBValues "+outputBVal)
print("Running sed")
os.system("sed -i ':a;N;$!ba;s/\\n/ /g' "+outputBVal)		#replacing '/n' for ' '
print("Running ITKFromats")
os.system("convertITKformats "+arguments["INPUT_MASK"]+" "+outputMask)
print("Running BEDPOST")
os.system("bedpostx "+arguments["DTIPREP_DIR"]+" -n 2 -model 2")