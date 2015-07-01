#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  test2.py
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
#  # In order to run this script, the following software are required:
#  * dtiestim
#  * dtiprocess

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
			print "For more information use --help"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			print "For more information use --help"
			exit(-1)

if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print "------ This script converts the DWI volume to the DTI space ------"
	print "Syntax to run this script: dwi_to_rd.py -config config_filename"
	print ""
	print "The config file requires the following format:"
	print "DWIVolume:DWIVolume_DIRECTORY"
	print "outputRD:outputRD_DIRECTORY"
	print "Mask:Mask_DIRECTORY"
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

arguments_names = ["DWIVolume", "config", "SubjectFolder", "Mask"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	print "For more information use --help"
	exit(-1)
	
for i in range(0, NUM_PARAMETERS):
	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "For more information use --help"
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

#checking paramters
checkParameters(arguments, arguments_names)
print arguments

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"
  
for k in arguments.keys():
  arguments[k] = subject_folder + arguments[k]


#running dtiestim
outputDTIName = arguments["DWIVolume"]
  
outputDTIName = outputDTIName.split(".")[0] + "_DTI" + ".nii.gz"

os.system("dtiestim -M "+arguments["Mask"]+" -m wls --correctionType nearest --inputDWIVolume "+arguments["DWIVolume"]+" --outputDTIVolume "+outputDTIName)	


#running dtiprocess
outputFAName = outputDTIName.replace("DTI", "FA")
outputRDName = outputDTIName.replace("DTI", "RD")
os.system("dtiprocess --dti_image "+outputDTIName+" --RD_output "+outputRDName+" --fa_output "+outputFAName+" --saveScalarsAsFloat")

