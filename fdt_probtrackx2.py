#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  fdt_probtrackx2.py
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
#  (1) probtrackx2
#  (2) ImageStat

import sys
import os
import os.path
import csv

arguments_names = ["config", "SEEDFILE", "WAYPOINTS","TERMINATIONMASK","EXCLUSIONMASK","SubjectFolder","OUTFOLDER", "ATLAS"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names )	- 1
slash = "/"
arguments = {}

debug = False

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

def create_file(filename, content):
	f = open(filename, "wt")
	for c in content:
		f.write(c + "\n")
	f.close()

def gen_connectome( folder, seed_label ):
	
	f=open( folder + 'waytotal','r')
	total = float(f.readline())
	f.close()

	#print "Total ", total

	row_vec = []

	f=open( folder + 'fdt_probtrackx_intensitySummary.csv','r')

	for line in f:
		tokens = line.split(",")
  		print "length = ", len(tokens )
  		if tokens[1] == 'MAX':
  			row_vec=tokens[2:]
	f.close()

	row_vec[-1]=row_vec[-1].strip()
	row_vec = map(float,row_vec)
	row_vec_norm = [ x/total for x in row_vec ]
	row_vec_norm[seed_label-1]=0.0

	#print "row vec = ", row_vec_norm

	f=open( folder + 'connectome.csv', 'w')
	csvwriter = csv.writer( f )
	csvwriter.writerow( row_vec_norm )
	f.close()

# ----------------------------------------------
# Display help option (--help) to user
# ----------------------------------------------

if len(sys.argv) > 1 and sys.argv[1] == "--help":
  print "   "
  print "--------- This is the FTD Probtrackx2 script ---------------"
  print "  "
  print "Sintax to run the script: ftd_probtrackx2.py -config 'config_file_name.txt'"
  print "Example: ftd_probtrackx2.py -config config_probtrackx2.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- These key/value pairs must be defined in the config file -------- "
  print "   "
  print "WAYPOINTS:'point to the input volume file '"
  print "SEEDFILE:'point to the mask file'"
  print "TERMINATIONMASK:point to the termination mask file"
  print "EXCLUSIONMASK:point to the exclusion mask file"
  print "OUTFOLDER:'point directory where the files will be placed'"
  print "SubjectFolder:'subject directory'"
  print "ATLAS: 'deformed gm atlas' "
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

# ----------------------------------------------
# Define subject folder (and associated files)
# ----------------------------------------------

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"


# ----------------------------------------------
# folder variables
# ----------------------------------------------

output = subject_folder + "probtrack/"
seed_folder = arguments["SEEDFILE"][:arguments["SEEDFILE"].find('.')]
probtrackx_folder = output + arguments["OUTPUTFOLDER"] + "/"

# ----------------------------------------------
# file variables
# ----------------------------------------------

waypoints_file = output+"waypoints.txt"

# ----------------------------------------------
# make some folders
# ----------------------------------------------
  
if not os.path.isdir( output ):
	os.makedirs( output )


# ----------------------------------------------
# Create the probtrack waypoint file
# ----------------------------------------------

create_file(waypoints_file, [arguments["WAYPOINTS"]])

# ----------------------------------------------
# Execute probtrack 
# ----------------------------------------------
	
cmd = "probtrackx2 -V 2 -x " + arguments["SEEDFILE"] + " -l --onewaycondition -c 0.2 -S 2000 --steplength=0.5 -P 5000 --fibthresh=0.01 --distthresh=0.0 --sampvox=0.0 "

cmd = cmd + "--omatrix1 --avoid="+arguments["EXCLUSIONMASK"] + " "

cmd = cmd + "--stop="+arguments["TERMINATIONMASK"] + " "

cmd = cmd + "--forcedir --opd -s "+subject_folder + "dtiprep.bedpostX/merged "

cmd = cmd + "-m "+subject_folder + "dtiprep.bedpostX/nodif_brain_mask "

cmd = cmd + "--dir="+subject_folder + "probtrack/" + arguments["OUTPUTFOLDER"] + " "

cmd = cmd + "--waypoints="+waypoints_file+" --waycond=AND"

os.system(cmd)

# ----------------------------------------------
# Generate connectome data 
# ----------------------------------------------

cmd = "ImageStat " + probtrackx_folder + "fdt_paths.nii.gz -label " + arguments["ATLAS"] + " -intensitySummary -outbase " + probtrackx_folder + "fdt_probtrackx"

print "cmd ", cmd
os.system( cmd )

gen_connectome( probtrackx_folder, int( arguments["OUTPUTFOLDER"] ) )
