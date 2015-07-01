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
# In order to run this script, the following software are required:
# * convertITKFormats (can be found on niral_utilities package)
# * DWI Convert (can be found on Slicer)
# * Bedpost (can be found on FSL)

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 3		
slash = "/"
import sys
import os
arguments = {}

if len(sys.argv) > 1 and sys.argv[1] == "--help":
  print "   "
  print "-------- This is the FDT Bedpost script -------------------"
  print "   "
  print "Sintax to run the script: fdt_bedpost.py -config 'config_file_name.txt'"
  print "Example: fdt_bedpost.py -config config_bedpost.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- This is how the config file must look like: -------- "
  print "   "
  print "DTIPREP_DIR:'point directory where the files will be placed'"
  print "INPUT_VOL:'point to the input volume file '"
  print "INPUT_MASK:'point to the mask file'"
  print "   "
 
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

arguments_names = ["config", "INPUT_VOL", "INPUT_MASK","SubjectFolder"]

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
		print "Please type --help to get more information"
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

#checking
checkParameters(arguments, arguments_names)
print arguments
	
subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"
  
for k in arguments.keys():
  arguments[k] = subject_folder + arguments[k]	
	

#all arguments were checked

dtiprep_folder = subject_folder + "dtiprep/"

#creating a folder called dtiprep inside the folder. This folder will contain the files required to run the bedpost
os.system("mkdir " + dtiprep_folder)

# these are going to be the name of the files
outputVolName = dtiprep_folder + "data.nii.gz"
outputBVec = dtiprep_folder + "bvecs"
outputBVal = dtiprep_folder + "bvals"
outputMask = dtiprep_folder + "nodif_brain_mask.nii.gz"

# Runnin the DWI Convert
print("Running DWIConvert")
os.system("DWIConvert --inputVolume "+arguments["INPUT_VOL"]+" --outputVolume "+outputVolName+" --conversionMode NrrdToFSL --outputBVectors "+outputBVec+" --outputBValues "+outputBVal)
# Parsing bvals file from column format to line format (required by bedpost) 
print("Running sed")
os.system("sed -i ':a;N;$!ba;s/\\n/ /g' "+outputBVal)		#replacing '/n' for ' '
#Running ITK formats
print("Running ITKFromats")
os.system("convertITKformats "+arguments["INPUT_MASK"]+" "+outputMask)
# Runnin Bedpost
print("Running BEDPOST")

cmd = "bedpostx "+dtiprep_folder+" -n 2 -model 2"
print "cmd=", cmd

os.system( cmd )
