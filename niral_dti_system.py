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
# 


NUM_ARGUMENTS = 1
NUM_PARAMETERS = 5		
slash = "/"
import sys
import os
arguments = {}

def findDWI(files):
  for f in files:
    if (f.find("DWI") != -1 and f.find("stripped") == -1):
      return f
    
  return None

def findBrainMask(files):
  for f in files:
    if (f.find("brainmask") != -1):
      return f
    
  return None

def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()

def createConfigFiles(subject_folder, arguments):
  
  if subject_folder[len(subject_folder)-1] != '/':
    subject_folder=subject_folder + "/"
  
  output_config_folder = subject_folder+"config"
  os.system("mkdir "+output_config_folder)
  
  subject_files  = os.listdir( subject_folder )
  
  createConfigFile("config_dwi_to_rd.txt", {"Mask":findBrainMask(subject_files), ""})
  

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
	print "This script creates an RD File from a brain volume"
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



arguments_names = ["T1", "config", "T2", "ATLAS", "SubjectFolder", "SubjectList"]

checkParameters(arguments, arguments_names)

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

f = open(subject_folder + arguments["SubjectList"])

for subject in f.readlines():
  print "Running the following subject: ", subject.rstrip()
  current_subject_folder = subject_folder + subject.rstrip()
  


