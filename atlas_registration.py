#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  atlas_registration.py
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
#  In order to run this script, the following software applications 
#  required:
#  ----------------------------------------------------------------
#  (1) ANTS
#  (2) WarpImageMultiTransform

import sys
import os
import os.path
import csv
from shutil import copyfile

arguments_names = ["config", "SubjectFolder", "DWI_B0", "DWI_AD", "T1", "T2"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names )	- 1
slash = "/"
arguments = {}

debug=False


# ----------------------------------------------
# Function definitions
# ----------------------------------------------

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

# ----------------------------------------------
# Display help option (--help) to user
# ----------------------------------------------

if len(sys.argv) > 1 and sys.argv[1] == "--help":
  print "   "
  print "--------- This is the atlas_registration script ---------------"
  print "  "
  print "Syntax to run the script: atlas_registration.py -config 'config_file_name.txt'"
  print "Example: atlas_registration.py -config config_atlas_registration.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- These key/value pairs must be defined in the config file -------- "
  print "   "
  print "SubjectFolder:'Subject Directory'"
  print "DWI_B0:'DWI B0 image'"
  print "DWI_AD:'DWI AD image'"
  print "T1:'T1 image'"
  print "T2:'T2 image'"
  print "  "
 
  exit(0)

# ----------------------------------------------
# Basic command line parsing
# ----------------------------------------------
		
if debug:
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

if debug:
	print arguments
	print "working directory:",os.getcwd()

checkParameters(arguments, arguments_names)

# ----------------------------------------------
# Parse configuration file
# ----------------------------------------------

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

# ----------------------------------------------
# Define subject folder (and associated files)
# ----------------------------------------------

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

# ----------------------------------------------
# make some folder variables
# ----------------------------------------------

registration_folder = subject_folder + "registration/"
atlas_folder = subject_folder + "atlas/"

# ----------------------------------------------
# make some folders
# ----------------------------------------------

if not os.path.isdir( registration_folder ):
	os.makedirs( registration_folder )

# ----------------------------------------------
# make some file variables
# ----------------------------------------------

outFileName = registration_folder + "t1t2_"
warp = outFileName + "Warp.nii.gz"
affine = outFileName + "Affine.txt"

# ----------------------------------------------
# execute non-rigid registration
# ----------------------------------------------

print "Performing joint T1,T2,b0,AD atlas registration"
cmd="ANTS 3 -m CC\[" + arguments["DWI_B0"] + "," + arguments["T1"] + ",1,4\] -m MI\[" + arguments["DWI_AD"] + "," + arguments["T2"] + ",1,4\] -r Guass\[3,0\] -i 100x50x25 -t SyN\[0.25\] -o " + outFileName
os.system( cmd )

# ----------------------------------------------
# execute subject specific atlas warps
# ----------------------------------------------

target = atlas_folder + "wm.nii.gz"
target_out = atlas_folder + "wm_warp.nii.gz"

cmd = "WarpImageMultiTransform 3 " + target + " " + target_out + " -R " + arguments["DWI_B0"] + " --use-NN " + warp + " " + affine
print cmd
os.system( cmd )

target = atlas_folder + "final_gm.nii.gz"
target_out = atlas_folder + "final_gm_warp.nii.gz"

cmd = "WarpImageMultiTransform 3 " + target + " " + target_out + " -R " + arguments["DWI_B0"] + " --use-NN " + warp + " " + affine
print cmd
os.system( cmd )

target = atlas_folder + "csf.nii.gz"
target_out = atlas_folder + "csf_warp.nii.gz"

cmd = "WarpImageMultiTransform 3 " + target + " " + target_out + " -R " + arguments["DWI_B0"] + " --use-NN " + warp + " " + affine
print cmd
os.system( cmd )

