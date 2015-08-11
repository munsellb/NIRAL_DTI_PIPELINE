#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  autoseg.py
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
#  (1) AutoSeg
#
#

import sys
import os
import os.path
import csv
from shutil import copyfile

arguments_names = ["config", "PARMFILE", "COMPFILE", "SubjectFolder"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names )	- 1

slash = "/"
arguments = {}

debug=False


# ----------------------------------------------
# Function definitions
# ----------------------------------------------

def findLabel1(files):
	for f in files:
		if (f.find("T1_SkullStripped_corrected_label_1.nrrd") != -1):
			return f
    
  	return None

def findLabel2(files):
	for f in files:
		if (f.find("Imperial_Parc_SubCort_Extended-WarpReg_label_2.nrrd") != -1):
			return f
    
  	return None
 
def findLabel3(files):
	for f in files:
		if (f.find("T1_SkullStripped_corrected_label_3.nrrd") != -1):
			return f
    
  	return None

def findLabel4(files):
	for f in files:
		if (f.find("Imperial_Parc_SubCort_Extended-WarpReg_label_4.nrrd") != -1):
			return f
    
  	return None

# this function is going to try to find a file that contains 'T1' on its name 
def findT1(files):
	for f in files:
		if (f.find("T1") != -1):
			return f
    
  	return None

# this function is going to try to find a file that contains 'T2' on its name 
def findT2(files):
	for f in files:
		if (f.find("T2") != -1):
			return f
    
  	return None

def create_autoseg_comp_file( infile, outfile, parameters):
	copyfile( infile, outfile )
	f = open(outfile, "a")
	for k in parameters.keys():
		f.write(k+": "+parameters[k]+"\n")
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
  print "--------- This is the AutoSeg script ---------------"
  print "  "
  print "Syntax to run the script: autoseg.py -config 'config_file_name.txt'"
  print "Example: autoseg.py -config config_autoseg.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- This is how the config file must look like: -------- "
  print "   "
  print "COMPFILE:'Computation File '"
  print "PARMFILE:'Parameter File'"
  print "SubjectFolder:'Subject Directory'"
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

struct_folder = subject_folder + "struct/"
atlas_folder = subject_folder + "atlas/"
parcellation_folder = subject_folder + "struct/AutoSeg_Process/WarpROI/"
ems_folder = subject_folder + "struct/AutoSeg_Process/ems/"
t1t2_folder = subject_folder + "T1T2/"

# ----------------------------------------------
# make some atlas variables
# ----------------------------------------------

gray_matter_atlas = atlas_folder + "gm.nii.gz"
white_matter_atlas = atlas_folder + "wm.nii.gz"
csf_atlas = atlas_folder + "csf.nii.gz"
final_gm_atlas = atlas_folder + "final_gm.nii.gz"

# ----------------------------------------------
# make some folders
# ----------------------------------------------

if not os.path.isdir( atlas_folder ):
	os.makedirs( atlas_folder )

if not os.path.isdir( t1t2_folder ):
	os.makedirs( t1t2_folder )

# ----------------------------------------------
# make some file variables
# ----------------------------------------------

autoseg_parm_file = struct_folder + "AutoSeg_Parameters.txt"
autoseg_comp_file = struct_folder + "AutoSeg_Computation.txt"

T1_file = struct_folder + findT1( os.listdir( struct_folder ) ) 
T2_file = struct_folder + findT2( os.listdir( struct_folder ) )

# ----------------------------------------------
# create subject specific AutoSeg parameter and computation files
# ----------------------------------------------

copyfile( arguments["PARMFILE"], autoseg_parm_file )
create_autoseg_comp_file( arguments["COMPFILE"], autoseg_comp_file, {"Process Data Directory":struct_folder, 
      "Data Directory":struct_folder, "Data":T1_file + " " + T2_file, "Data AutoSeg Directory":"AutoSeg_Process" } )

# ----------------------------------------------
# execute AutoSeg
# ----------------------------------------------

cmd = "AutoSeg -computationFile " + struct_folder + "AutoSeg_Computation.txt" + " -parameterFile " + struct_folder + "AutoSeg_Parameters.txt"
os.system( cmd )

# ----------------------------------------------
# create label file variables 
# ----------------------------------------------

white_matter_labels = ems_folder + findLabel1( os.listdir( ems_folder ) ) 
gray_matter_labels = parcellation_folder + findLabel2( os.listdir( parcellation_folder ) )
deep_gray_matter_labels = parcellation_folder + findLabel4( os.listdir( parcellation_folder ) ) 
csf_labels = ems_folder + findLabel3( os.listdir( ems_folder ) )

# ----------------------------------------------
# Create subject specific atlas files (nifty format)
# ----------------------------------------------

print "Creating gray matter atlas using Imperial parcellation generated from AutoSeg"
cmd="ImageMath " + gray_matter_labels + " -add " + deep_gray_matter_labels + " -outfile " + gray_matter_atlas
os.system( cmd )

print "Creating white matter atlas using Imperial parcellation generated from AutoSeg"
cmd="convertITKformats " + white_matter_labels + " " + white_matter_atlas
os.system( cmd )

print "Creating csf atlas using Imperial parcellation generated from AutoSeg"
cmd="convertITKformats " + csf_labels + " " + csf_atlas
os.system( cmd )

# ----------------------------------------------
# Copy T1 and T2 files into T1T2 folder (in nifty format)
# ----------------------------------------------

print "Getting T1 image"
cmd="convertITKformats " + T1_file + " " + t1t2_folder + "t1.nii.gz"
os.system( cmd )

print "Getting T2 image"
cmd="convertITKformats " + T2_file + " " + t1t2_folder + "t2.nii.gz"
os.system( cmd )

# ----------------------------------------------
# Create an empty final gm atlas file (in nifty format)
# ----------------------------------------------

print "Creating final (empty) gm atlas"
cmd="ImageMath " + gray_matter_labels + " -constOper 2/0 -outfile " + final_gm_atlas
os.system( cmd )
  

