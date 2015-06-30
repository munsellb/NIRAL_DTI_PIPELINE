#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  niral_dti_system.py
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

# this function is going to try to find a file that contains 'DWI' on its name
def findDWI(files):
  for f in files:
    if (f.find("DWI") != -1 and f.find("stripped") == -1):
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

# Displaying the help option to the user
if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print ""
	print "------This is the main script of the pipeline------"
	print "Syntax to run this script: python niral_dti_system.py -config config_global_system.txt "
	print ""
	print "The config file requires the following format:"
	print "ATLAS:location of the ATLAS file"
	print "T1:location of the T1 file"
	print "T2:location of the T2 file"
	print "SubjectFolder:SubjectFolder_Directory"
	print "SubjectList:SubjectList file location"
	print ""
	exit(0)

		
print "Num of arguments passed:",len(sys.argv) -1

# Error message in case of using wrong numbers of parameters
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


# This is the dictionary. These names, except for 'config', must be in the config file
arguments_names = ["T1", "config", "T2", "ATLAS", "SubjectFolder", "SubjectList"]

checkParameters(arguments, arguments_names)

subject_folder = arguments["SubjectFolder"]

# checking if the slash exists
if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

f = open(arguments["SubjectList"])


# This loop runs according to the number of Subjects the user wants to process
for subject in f.readlines():
  print "Running the following subject: ", subject.rstrip()
  
  current_subject_folder = subject_folder + subject.rstrip()
  
  if current_subject_folder[len(current_subject_folder)-1] != '/':
    current_subject_folder=current_subject_folder + "/"
  current_subject_files  = os.listdir( current_subject_folder ) 
  
  output_config_folder = current_subject_folder+"config"
  os.system("mkdir "+output_config_folder)
  
  # Calling the script that transforms the DWI in the DTI space
  createConfigFile(current_subject_folder+"config/config_dwi_to_dti.txt", {"Mask":findBrainMask(current_subject_files), "DWIVolume":findDWI(current_subject_files), "SubjectFolder":current_subject_folder})
  print "Running DWI to DTI script:"
  os.system("python dwi_to_dti.py -config "+current_subject_folder+"config/config_dwi_to_dti.txt")
  
  # Calling the script that does the registration to the Atlas
  OUT_ANTS_PREFIX = "warp_t1w_t2w_"
  createConfigFile(current_subject_folder+"config/config_nonrigid_registration.txt", {"ATLAS":arguments["ATLAS"], "OUT_ANTS_PREFIX":OUT_ANTS_PREFIX, "RD":findRD(current_subject_files), "T1":arguments["T1"], "T2":arguments["T2"], "SubjectFolder":current_subject_folder})
  print "Running Non Rigid Registration script:"
  os.system("python nonrigid_registration.py -config "+current_subject_folder+"config/config_nonrigid_registration.txt")
  
  # Applying the registration to the Subject 
  createConfigFile(current_subject_folder+"config/config_warp_image.txt", {"REF":findRD(current_subject_files),"MOV":arguments["ATLAS"],"OUT_ANTS_PREFIX":OUT_ANTS_PREFIX,"SubjectFolder":current_subject_folder})
  print "Running Warp Image script:"
  os.system("python warp_image.py -config "+current_subject_folder+"config/config_warp_image.txt")
  
  # Running the bedpost script
  createConfigFile(current_subject_folder+"config/config_bedpost.txt", {"INPUT_VOL":findDWI(current_subject_files), "INPUT_MASK":findBrainMask(current_subject_files), "SubjectFolder":current_subject_folder})
  print "Running Bedpost script:"
  os.system("python fdt_bedpost.py -config "+current_subject_folder+"config/config_bedpost.txt")
  
  warped_atlas = arguments["ATLAS"][:arguments["ATLAS"].find(".")] + "_deform.nii.gz"
  warped_atlas = warped_atlas[warped_atlas.rfind("/"):]
  
  
  # loop that runs 90 times to extract all the brain regions
  for i in range(1,2):   
    
    # extracting a brain region
    print "Extracting region " + str(i)
    createConfigFile(current_subject_folder+"config/config_extract_regions.txt", {"INPUT_IMAGE":warped_atlas, "EXTRACT_LABEL":str(i), "SubjectFolder":current_subject_folder})
    os.system("python extract_brain_region.py -config "+current_subject_folder+"config/config_extract_regions.txt")
    
    # creating the masks necessary to run the probtrack
    print "Running FDT Masks script on region " + str(i)
    createConfigFile(current_subject_folder+"config/config_create_fdt_masks.txt", {"SubjectFolder":current_subject_folder, "FAVolume":findFA(current_subject_files), "RDVolume":findRD(current_subject_files), "BrainMask":findBrainMask(current_subject_files), "region_label":str(i) })
    os.system("python create_fdt_masks.py -config "+current_subject_folder+"config/config_create_fdt_masks.txt")
    
    # calling the probtrack script 
    print "Running Probtrack script on region " + str(i)
    createConfigFile(current_subject_folder+"config/config_probtrack.txt", {"SEEDFILE":"regions/"+"brain"+str(i)+".nii.gz", "WAYPOINTS":"masks/waypoint.nii.gz", "TERMINATIONMASK":"masks/termination.nii.gz", "EXCLUSIONMASK":"masks/exclusion.nii.gz", "SubjectFolder":current_subject_folder })
    os.system("python fdt_probtrackx2.py -config "+current_subject_folder+"config/config_probtrack.txt")
    
