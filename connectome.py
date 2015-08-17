#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  connectome.py
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

import sys
import os
import csv
import numpy as np

arguments_names = ["config", "SubjectFolder"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names ) - 1
NUM_REGIONS=83	
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
  print "-------- Subject specific connectome creation script -------------------"
  print "   "
  print "Sintax to run the script: connectome.py -config 'config_file_name.txt'"
  print "Example: connectome.py -config connectome.txt"
  print "   "
  print "------------------------------------------------------------"
  print "------- These key/value pairs must be defined in the config file -------- "
  print "   "
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
	exit(-1)
	
for i in range(0, NUM_PARAMETERS):
	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "Please type --help to get more information"
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

checkParameters(arguments, arguments_names)

if debug:
	print arguments

# ----------------------------------------------
# Define subject folder (and associated files)
# ----------------------------------------------
	
subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

# ----------------------------------------------
# Create some variables
# ----------------------------------------------

connectome_file = subject_folder+"connectome.csv"

# ----------------------------------------------
# Create an connectome filled with zeros
# ----------------------------------------------

C=np.zeros(shape=(NUM_REGIONS,NUM_REGIONS))

# ----------------------------------------------
# Create seed matrix used to hold the connectivity
# data of each seed
# ----------------------------------------------

seed_matrix=[]

# ----------------------------------------------
# Loop through each seed and add connectivity 
# data to seed_matrix (i.e. row 0 in seed matrix => seed region 1)
# ----------------------------------------------

for i in range(0,NUM_REGIONS):

	c_file=subject_folder+"probtrack/"+str(i+1)+"/connectome.csv"

	f=open(c_file,"r")

	for row in csv.reader(f):

		seed_matrix.append( map( float, row ) )

	f.close()

print seed_matrix

# ----------------------------------------------
# Create the connectome using connectivity data
# in seed_matrix
# ----------------------------------------------

for i in range(0,NUM_REGIONS):

	if debug:
		print seed_matrix[i][0:NUM_REGIONS]

	for j in range(i,NUM_REGIONS):

		C[i][j] = seed_matrix[i][j] + seed_matrix[j][i]
		C[j][i] = C[i][j]

	if debug:
		print C

# ----------------------------------------------
# Save connectome to subject folder
# ----------------------------------------------

f=open(connectome_file, 'w')

csvwriter = csv.writer( f )

csvwriter.writerows( C )

f.close()

