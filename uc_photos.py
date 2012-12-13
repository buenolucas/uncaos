#!/usr/bin/python
# coding: utf-8

# uc_photos.py
# photos

import re
import PIL.Image, PIL.ExifTags
import os
import shutil
import sys
import time
#--------------
# default vars
#--------------

#alloewd formats as photos
formats = ["jpg","jpeg"]

#min size. needed to don get thumbs or someone trash
minsize = 300000 

#prefix to namimg. Ex: PIC0000001.jpg
prefix = "PIC"


#--------------
# vars
#--------------

#total files
totalFiles = 0

#total matched files
counter = 0

#total folders created
totalFolders = 0

if len(sys.argv) != 3:  # the program name and the two arguments
  # stop the program and print an error message
  sys.exit("Error: Must provide destination and source folders")

destination = sys.argv[2]
source = sys.argv[1]

#check folders

if not os.path.exists(source):
         sys.exit("ERROR: Source folder don't exists")

if not os.path.exists(destination):
         sys.exit("ERROR: Destination folder don't exists")


#--------------
# functions
#--------------
def confirm(default = "no"):
	question = "We will search your photos in:\n"\
		   "'"+source+"'\n"\
		   "And move matched photos to:\n"\
		   "'"+destination+"'\nAre you sure about this?"
	valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
	if default == None:
        	prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)
	
	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
        	if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


#--------------
# init
#--------------
print chr(27) + "[2J"
print "Welcome to Uncaos - a tool for stupids like me"

r = confirm()
if r == False : 
	sys.exit("Hasta La Vista")



print "Seeking your treasure...."

for root, dirs, files in os.walk(source, topdown=False):
    
    for file in files:
	totalFiles+=1		
	extension = os.path.splitext(file)[1][1:].lower()

	#check if file has a allowed extension
	if extension not in formats: 
		continue
	filepath = os.path.join(root, file)

	size = os.path.getsize(filepath)
	if size < minsize :
		continue

	# open file and get metadata
	img = PIL.Image.open(filepath)
	info_raw = img._getexif()
	destinationFolder = ""
	if hasattr(info_raw, 'keys'):

		for tag in info_raw.keys():
			tag_decoded = PIL.ExifTags.TAGS.get(tag, tag)
			if tag_decoded == 'DateTime':
				timestamp = info_raw[tag]
				date, time = timestamp.split(" ")
				destinationFolder = date.replace (":", "-")
				break

	# check if is undated	
	if len(destinationFolder) == 0 :
		destinationFolder = "undated"

	#prepare new filename	
	counter+=1
	newname = prefix+"{0:07d}".format(counter)+"."+extension 

	#set destination path
	destinationPath = os.path.join(destination,destinationFolder)

	#create, if no exist
	if not os.path.exists(destinationPath):
		totalFolders+=1
		os.mkdir(destinationPath)

	#check if file exists and procced move
	if os.path.exists(os.path.join(destinationPath,newname)):
	    print 'WARNING: this file was not copied :' + os.path.join(root,file)
	else :
		shutil.move(os.path.join(root,file), os.path.join(destinationPath,newname))

print "Finished!"# moved "+str(counter)+" photos to new "+str(totalFolders)+" folders."
print str(counter)+ " treasures found"
print str(totalFolders)+ " folders created."
print str(totalFiles)+ " files scanned in "#+str(datetime.timedelta(time.time() - stime))
print "\nNow, get your happiness!"
