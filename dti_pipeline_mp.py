#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  dti_pipeline_mp.py (multiprocess verison)
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
import subprocess

arguments_names = ["config", "COMPFILE", "PARMFILE", "SubjectFolder", "SubjectList", "Flags"]
flag_names = ["dwi_to_dti","autoseg","fdt_masks","fdt_bedpost","fdt_probtrackx2","connectome"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names ) - 1
FLAG_PARAMETERS = len( flag_names )
NUM_REGIONS = 83

slash = "/"
arguments = {}
flag_arguments = {}

debug=False


# ----------------------------------------------
# Function definitions
# ----------------------------------------------

# this function is going to try to find a file that contains 'DWI' on its name
def findDWI(files):
  for f in files:
    if (f.find("DWI") != -1 and f.find("b0") == -1 and f.find("AD") == -1 and f.find("stripped") == -1 and f.find("RD") == -1 and f.find("FA") == -1 and f.find("DTI") == -1 and f.find("RA") == -1 and f.find("MD") == -1 ):
      return f
    
  return None

# this function is going to try to find a file that contains 'brainmask' on its name 
def findBrainMask(files):
  for f in files:
    if (f.find("brainmask") != -1):
      return f
    
  return None

# this function is going to try to find a file that contains 'RD' on its name 
def findRD(files):
  for f in files:
    if (f.find("RD") != -1):
      return f
    
  return None

# this function is going to try to find a file that contains 'FA' on its name 
def findFA(files):
  for f in files:
    if (f.find("FA") != -1):
      return f
    
  return None

# this function is going to try to find a file that contains 'AD' on its name 
def findAD(files):
  for f in files:
    if (f.find("AD") != -1):
      return f

  return None

# this function is going to try to find a file that contains 'b0' on its name 
def findB0(files):
  for f in files:
    if (f.find("b0") != -1):
      return f

  return None

# This function creates a configuration file by giving the name of the file, and its parameters
# paramaters -> a dictionary containing all the keys (parameters names) and values (locations) 
def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()

# Checking if he user entered the correct parameters in order to run the script
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


# ----------------------------------------------
# Display help option (--help) to user
# ----------------------------------------------

if len(sys.argv) > 1 and sys.argv[1] == "--help":
  print ""
  print "------DTI Pipeline multiprocess (mp) version ------"
  print "Syntax to run this script: python dti_pipeline_mp.py -config config_dti_pipeline.txt "
  print ""
  print "The config file requires the following format:"
  print "COMPFILE: AutoSeg computation file"
  print "PARMFIle: AutoSeg parameters file"
  print "SubjectFolder: SubjectFolder_Directory"
  print "SubjectList: SubjectList file location"
  print "Flags: pipeline component flag file"
  print ""
  exit(0)


# ----------------------------------------------
# Basic command line parsing
# ----------------------------------------------
		
if debug:
  print "Num of arguments passed:",len(sys.argv) -1

# Error message if wrong numbers of parameters
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

if debug:
  print arguments
  print "working directory:",os.getcwd()

# ----------------------------------------------
# Parse configuration (config) file
# ----------------------------------------------

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

checkParameters(arguments, arguments_names)

# ----------------------------------------------
#  Parse flag file
# ----------------------------------------------

flag_file = open(arguments["Flags"])

f_lines = flag_file.readlines()
if len(f_lines) != FLAG_PARAMETERS:
  print "ERROR: the flag file must contain only ",FLAG_PARAMETERS," parameters"
  print "Type --help for more information"
  exit(-1)

for g in range(0, FLAG_PARAMETERS):
	if f_lines[g].find(":") == -1:
		print "ERROR: The line",g+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "ACCEPTABLE VALUES: YES or NO"
		print "For more information use --help"
		exit(-1)
	tokens_2 = f_lines[g].rstrip().split(":")
	
	if tokens_2[1] != "yes" and tokens_2[1] != "no":
	  exit(-1)
	  print "Flag could not find the correct values."
		
	flag_arguments[tokens_2[0]] = tokens_2[1]
	
checkParameters(flag_arguments,flag_names)	

# ----------------------------------------------
# Define subject folder (and associated files)
# ----------------------------------------------

subject_folder = arguments["SubjectFolder"]

# checking if the slash exists
if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

f = open(arguments["SubjectList"])


# ----------------------------------------------
# Execute the pipeline for the subjects defined
# in the subject list (see arguments["SubjectList"])
# ----------------------------------------------

for subject in f.readlines():

  # ----------------------------------------------
  # Step 0: Retrieving subject information
  # ----------------------------------------------

  print "======================================================"
  print "Running subject [ ", subject.rstrip() + " ] "
  
  current_subject_folder = subject_folder + subject.rstrip()
  
  if current_subject_folder[len(current_subject_folder)-1] != '/':
    current_subject_folder=current_subject_folder + "/"

  current_subject_files  = os.listdir( current_subject_folder ) 

  output_config_folder = current_subject_folder+"config"

  if not os.path.isdir( output_config_folder ):
    os.makedirs( output_config_folder )

  # ----------------------------------------------
  # Step 1: DWI to DTI pipeline component
  # ----------------------------------------------
  
  if flag_arguments["dwi_to_dti"] == "yes":

    config_file = current_subject_folder+"config/config_dwi_to_dti.txt"
    
    createConfigFile( config_file, {"Mask":findBrainMask(current_subject_files), 
      "DWIVolume":findDWI(current_subject_files), "SubjectFolder":current_subject_folder})

    print "Executing DWI to DTI pipeline component:"
  
    if os.system("python dwi_to_dti.py -config " + config_file ) != 0:
      print "DWI to DTI pipeline component failed ... exiting pipeline!"
      exit(-1)

  else:
     print "DWI to DTI pipeline component not executed!"


  current_subject_files  = os.listdir( current_subject_folder ) 

  # ----------------------------------------------
  # Step 2: AutoSeg pipeline component
  # ----------------------------------------------
  
  if flag_arguments["autoseg"] == "yes":

    config_file = current_subject_folder+"config/config_autoseg.txt"
    
    createConfigFile( config_file, {"COMPFILE":arguments["COMPFILE"], 
      "PARMFILE":arguments["PARMFILE"], "SubjectFolder":current_subject_folder})

    print "Executing AutoSeg pipeline component:"
  
    if os.system("python autoseg.py -config " + config_file ) != 0:
      print "AutoSeg pipeline component failed ... exiting pipeline!"
      exit(-1)

  else:
     print "AutoSeg pipeline component not executed!"

  # ----------------------------------------------
  # Step 3: FDT Masks pipeline component
  # ----------------------------------------------

  if flag_arguments["fdt_masks"] == "yes":

    config_file = current_subject_folder+"config/config_fdt_masks.txt"
    
    createConfigFile( config_file, {"BrainMask":current_subject_folder+findBrainMask(current_subject_files), 
      "DWI_AD":current_subject_folder+findAD(current_subject_files), 
      "DWI_B0":current_subject_folder+findB0(current_subject_files), 
      "SubjectFolder":current_subject_folder})

    print "Executing FDT masks pipeline component:"
  
    if os.system("python fdt_masks.py -config " + config_file ) != 0:
      print "FDT masks pipeline component failed ... exiting pipeline!"
      exit(-1)

  else:
     print "FDT masks pipeline component not executed!"
  

  # ----------------------------------------------
  # Step 4: FDT Bedpost pipeline component
  # ----------------------------------------------
  
  if flag_arguments["fdt_bedpost"] == "yes":

    mask_folder = current_subject_folder + "mask/"
    config_file = current_subject_folder + "config/config_bedpost.txt"

    createConfigFile( config_file, {"INPUT_VOL":current_subject_folder+findDWI(current_subject_files), 
      "INPUT_MASK":mask_folder+"brain.nii.gz", "SubjectFolder":current_subject_folder})

    print "Executing FDT Bedpost pipeline component:"

    if os.system("python fdt_bedpost.py -config " + config_file ) != 0:
      print "FDT Bedpost pipeline component failed ... exiting pipeline!"
      exit(-1)

  else:
    print "FDT Bedpost pipeline component not executed!"

  # ----------------------------------------------
  # Step 5: FDT probtrack pipeline component
  # ----------------------------------------------

  waypoint_file = current_subject_folder + "mask/waypoint.nii.gz"
  exclusion_file = current_subject_folder + "mask/exclusion.nii.gz"
  final_gm_atlas_warp = current_subject_folder+"atlas/final_gm_warp.nii.gz"

  for i in range(1,NUM_REGIONS+1):

    region_folder = current_subject_folder + "mask/region" + str(i) + "/"
    seed_file = region_folder + "region" + str(i) + ".nii.gz"
    termination_file = region_folder + "termination.nii.gz"
    
    if flag_arguments["fdt_probtrackx2"] == "yes":

      print "Running Probtrack script on region " + str(i)

      probtrack_config_file = current_subject_folder+"config/config_probtrack"+str(i)+".txt"

      createConfigFile( probtrack_config_file, 
        {"OUTPUTFOLDER":str(i), 
        "SEEDFILE":seed_file, 
        "WAYPOINTS":waypoint_file, 
        "TERMINATIONMASK":termination_file, 
        "EXCLUSIONMASK":exclusion_file, 
        "SubjectFolder":current_subject_folder, 
        "ATLAS":final_gm_atlas_warp })

      cmd = ["python", "fdt_probtrackx2.py", "-config", probtrack_config_file ]
      subprocess.Popen( cmd )
    
    else:
      print "FDT probtrack pipeline component not executed for region " + str(i) + "!"

  # ----------------------------------------------
  # Step 6: Create subject connectome
  #
  # Not executed in multi-process (mp) version
  #
  # Only config file generated!
  #
  # To run connectome pipeline component simply 
  # type at in a shell:
  #
  # > python connectome.py -config <subject_folder/config/config_connectome.txt
  #
  # where <subject_folder> must be replaced with the 
  # fully qualified path of the subject's folder
  #
  # ----------------------------------------------

  if flag_arguments["connectome"] == "yes":

    config_file = current_subject_folder + "config/config_connectome.txt"

    createConfigFile( config_file, {"SubjectFolder":current_subject_folder} )

    print "Configuratin file for connectome pipeline component created [ " + config_file + " ] "

  else:
    print "FDT connectome component not executed!"
