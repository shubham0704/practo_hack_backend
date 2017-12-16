"""
Get data from an image
Name, exp
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
import cloudvisreq
import unicodedata
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
import re
from PIL import Image


def preprocess(fname):
	# TODO resize image
    gray = cv2.imread(fname, 0)
    thnew = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 217, 0)
    equ = cv2.equalizeHist(thnew)
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(equ,kernel,iterations = 2)
    kernel = np.ones((2,2),np.uint8)
    erode = cv2.erode(dilate,kernel,iterations = 2)
    f, ext = fname.split('.')
    new_name = f + '_preprocess.' + ext
    cv2.imwrite(new_name, erode)
    return new_name


def sanitize_data(fname, prepro=False, vertical=False):
	img = Image.open(fname)
	if img.size[0] < img.size[1]:
		vertical = True
	if prepro == True:
		data = cloudvisreq.get_lines(image_filenames=[preprocess(fname)])
	else:
		data = cloudvisreq.get_lines(image_filenames=[fname])
	
	data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
	lines = data.split('\n')
	dates = []
	#print data, '\n\n\n'
	if vertical == False:
		for line in lines:
			items = line.split()
			if len(items) > 1:
				for item in items:
					print  items, item
					try:
						if re.match('([0-9].+)/([0-9].+)', item) or re.match('([a-zA-Z].+).[0-9].+', item):
							now = parse(item)
							dates.append(now)
					except Exception as e:
						print e
						continue
			else:
				try:
					if re.match('([0-9].+)/([0-9].+)', line) or re.match('([a-zA-Z].+).[0-9].+', line):	
						now = parse(lines)
						dates.append(now)
				except:
					pass
	else:
		for line in lines:
			items = line.split()
			for i, item in enumerate(items):
				if re.match("EXP", item):
					date = "".join((x for x in items[i+1:]))
					#print date
					date = parse(date)
					dates.append(date)
	try:
		print max(dates)
	except Exception as e:
		print e

	return 

#sanitize_data('sbnew.png', prepro=False)
