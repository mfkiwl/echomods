#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
#
# Library for tagging image
# Used in `20180310a`
# Definitely not optimized
#
# -------------------------

'''Description: Autotagging images for the `20180310a` experiment.'''

__author__      = "kelu124"
__copyright__   = "Copyright 2018, Kelu124"
__license__ 	= "cc-by-sa/4.0/" 


import sys
import pyexiv2
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

Imgs = []
for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if ( f.endswith(".jpg") or f.endswith(".png") )]:
        Imgs.append( os.path.join(dirpath, filename) )

print Imgs

for FileName in Imgs:
	edit = 0

	metadata = pyexiv2.ImageMetadata(FileName)
	try:
		metadata.read()
	except IOError:
		print "Not an image"
	else:
		# Modules
		metadata['Exif.Image.Software'] = "matty"
		# Experiment
		metadata['Exif.Image.Make'] = "20180403a"


		metadata['Exif.Photo.MakerNote'] = "graph"
		# Description
		metadata['Exif.Image.ImageDescription'] = "Testing the 75V pulser"

		# Saving the image

		metadata.write()
		print "Image "+FileName+" saved"

