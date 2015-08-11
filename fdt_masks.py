#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  fdt_masks.py
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
#  (1) ImageMath
#
#

import sys
import os
import os.path
import csv
from shutil import copyfile

arguments_names = ["config", "SubjectFolder", "BrainMask", "DWI_AD", "DWI_B0"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names )	- 1
NUM_REGIONS = 83

slash = "/"
arguments = {}

debug=False


# ----------------------------------------------
# Function definitions
# ----------------------------------------------

def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()


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
  print "--------- This is the fdt_masks script ---------------"
  print "  "
  print "Syntax to run the script: fdt_masks.py -config 'config_file_name.txt'"
  print "Example: fdt_masks.py -config config_fdt_masks.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- These key/value pairs must be defined in the config file -------- "
  print "   "
  print "SubjectFolder:'Subject Directory'"
  print "BrainMask:'Binary brain mask image'"
  print "DWI_AD:'AD image volume'"
  print "DWI_B0:'b0 image volume'"
  print "T1:'T1 image volume'"	# TODO
  print "T2:'T2 image volume'"	# TODO
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
# Config file parsing
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

mask_folder = subject_folder + "mask/"
atlas_folder = subject_folder + "atlas/"
config_folder = subject_folder + "config/"

# ----------------------------------------------
# make some atlas variables
# ----------------------------------------------

gray_matter_atlas = atlas_folder + "gm.nii.gz"
final_gm_atlas = atlas_folder + "final_gm.nii.gz"

gray_matter_atlas_warp = atlas_folder + "gm_warp.nii.gz"
white_matter_atlas_warp = atlas_folder + "wm_warp.nii.gz"
csf_atlas_warp = atlas_folder + "csf_warp.nii.gz"
final_gm_atlas_warp = atlas_folder + "final_gm_warp.nii.gz"

# ----------------------------------------------
# Create variables for subject specific mask files
# ----------------------------------------------

waypoint_mask =  mask_folder + "waypoint.nii.gz"
exclusion_mask = mask_folder + "exclusion.nii.gz"
region_mask = mask_folder + "region"
brain_mask = mask_folder + "brain.nii.gz"

# ----------------------------------------------
# make some folders
# ----------------------------------------------

if not os.path.isdir( mask_folder ):
	os.makedirs( mask_folder )

if not os.path.isdir( config_folder ):
	os.makedirs( config_folder )

# ----------------------------------------------
# Create an empty final gm atlas file (in nifty format)
# ----------------------------------------------

print "Creating final (empty) gm atlas"
cmd="ImageMath " + gray_matter_atlas + " -constOper 2/0 -outfile " + final_gm_atlas
os.system( cmd )

# ----------------------------------------------
# create final gray matter mask
# ----------------------------------------------

for label in range(1,NUM_REGIONS+1):

	print "Processing Label [ " + str(label) + " ]"

	# ---------------------------------------
	# Step 1: Extract Label
	# ---------------------------------------
	cmd="ImageMath " + gray_matter_atlas + " -extractLabel " + str(label) + " -outfile " + atlas_folder + "L" + str(label) + ".nii.gz"
	os.system( cmd )
	
	# ---------------------------------------
	# Step 2: Erode Extracted Label
	# ---------------------------------------
	cmd="ImageMath " + atlas_folder + "L" + str(label) + ".nii.gz -erode 1,1 -outfile " + atlas_folder + "LE" + str(label) + ".nii.gz"
	os.system( cmd )
	
	# ---------------------------------------
	# Step 3: Invert Eroded Extracted Label (i.e. output of step 2)
	# ---------------------------------------
	
	cmd="ImageMath " + atlas_folder + "LE" + str(label) + ".nii.gz -constOper 1,1 -outfile " + atlas_folder + "LEN" + str(label) + ".nii.gz"
	os.system( cmd )
	
	cmd="ImageMath " + atlas_folder + "LEN" + str(label) + ".nii.gz -constOper 2,-1 -outfile " + atlas_folder + "LEN" + str(label) + ".nii.gz"
	os.system( cmd )
	
	# ---------------------------------------
	# Step 4: Mask inverted label (i.e. output of step 3) with extracted label (i.e. output of step 1)
	# ---------------------------------------
	
	cmd="ImageMath " + atlas_folder + "L" + str(label) + ".nii.gz -mask " + atlas_folder + "LEN" + str(label) + ".nii.gz -outfile " + atlas_folder + "LM" + str(label) + ".nii.gz"
	os.system( cmd )
	
	# ---------------------------------------
	# Step 5: Add label to  mask (i.e. output of step 5)
	# ---------------------------------------
	cmd="ImageMath " + atlas_folder + "LM" + str(label) + ".nii.gz -constOper 2," + str(label) + " -outfile " + atlas_folder + "LM" + str(label) + ".nii.gz"
	os.system( cmd )
	
	# ---------------------------------------
	# Step 6: Add dilated label (i.e. output of step 6) to final gray matter atlas
	# ---------------------------------------
	cmd="ImageMath " + final_gm_atlas + " -add " + atlas_folder + "LM" + str(label) + ".nii.gz -outfile " + final_gm_atlas
	os.system( cmd )
	
	# ---------------------------------------
	# Step 7: Clean up
	# ---------------------------------------
	
	os.system( "rm " + atlas_folder + "L*" )

# ----------------------------------------------
# Run atlas registration and warp atlas
# ----------------------------------------------

reg_config = config_folder + "config_atlas_registration.txt"

createConfigFile( reg_config, 
	{"T1":subject_folder+"T1T2/t1.nii.gz", "T2":subject_folder+"T1T2/t2.nii.gz", 
	"DWI_B0":arguments["DWI_B0"], 
	"DWI_AD":arguments["DWI_AD"], 
	"SubjectFolder":subject_folder})

cmd = "python atlas_registration.py -config " + reg_config
os.system( cmd )

# ----------------------------------------------
# Create FDT waypoint mask
# ----------------------------------------------

print "Creating FDT waypoint mask using white matter atlas"
copyfile( white_matter_atlas_warp, waypoint_mask )

# ----------------------------------------------
# Create FDT exclusion mask (CSF mask + brain mask)
# ----------------------------------------------

print "Creating FDT exclusion mask using csf atlas and brain mask"

cmd="ImageMath " + arguments["BrainMask"] + " -sub " + csf_atlas_warp + " -outfile " + brain_mask
os.system( cmd )

cmd="ImageMath " + brain_mask + " -threshold 1,2 -outfile " + brain_mask
os.system( cmd )

cmd="ImageMath " + brain_mask + " -constOper 1,1 -outfile " + exclusion_mask
os.system( cmd )

cmd="ImageMath " + exclusion_mask + " -constOper 2,-1 -outfile " + exclusion_mask
os.system( cmd )

# ----------------------------------------------
# Creating seed image and termination masks
# ----------------------------------------------

for label in range(1,NUM_REGIONS+1):

	print "Processing Label [ " + str(label) + " ]"

	region_folder = region_mask + str(label) + "/"

	if not os.path.isdir( region_folder ):
		os.makedirs( region_folder )


	seed_mask = region_folder + "region" + str(label) + ".nii.gz"
	seed_mask_not = region_folder + "region_not_" + str(label) + ".nii.gz"
	termination_mask = region_folder + "termination.nii.gz"

	# ----------------------------------------------
	# Create FDT seed mask (seed label extracted from final gray matter atlas )
	# ----------------------------------------------

	print "Creating FDT seed mask using seed label [ " + str(label) + " ]"

	cmd="ImageMath " + final_gm_atlas_warp + " -extractLabel " + str(label) + " -outfile " + seed_mask
	os.system( cmd )

	# ----------------------------------------------
	# Create FDT termination mask (final gm mask w/o seed label )
	# ----------------------------------------------

	print "Creating FDT termination mask using inverted seed mask and final gray matter atlas"

	cmd="ImageMath " + seed_mask + " -constOper 1,1 -outfile " + seed_mask_not
	#print cmd
	os.system( cmd )
	
	cmd="ImageMath " + seed_mask_not + " -constOper 2,-1 -outfile " + seed_mask_not
	#print cmd
	os.system( cmd )
	
	cmd="ImageMath " + final_gm_atlas_warp + " -mask " + seed_mask_not + " -outfile  " + termination_mask
	#print cmd
	os.system( cmd )

