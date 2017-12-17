from controllers.modules import *


__PERM__UPLOADS__ = "uploads/permanent/"
__TEMP__UPLOADS__ = "uploads/temp/"


def find_maxVal(gray, template_path):
	visualize = True
	found = None
	maxVal = 0
	maxLoc = None
	print abspath(template_path)
	template = cv2.imread(abspath(template_path))
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	#template = cv2.imread(template_path, 0)
	(tH, tW) = template.shape[:2]
	template = cv2.Canny(template, 50, 200)
	

	# loop over the scales of the image
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break

		edged = cv2.Canny(resized, 200, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		# check to see if the iteration should be visualized
		if visualize == False:
			# draw a bounding box around the detected region
			clone = np.dstack([edged, edged, edged])
			cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
				(maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
			cv2.imshow("Visualize", clone)
			cv2.waitKey(0)

		# if we have found a new maximum correlation value, then ipdate
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
	if not maxVal:
		maxVal = 0.0
		r = (0,0)
		tH, tW = (0,0)
		found = (maxVal, maxLoc, r)
	return found,(tH, tW)


def crop_text(fname):
	found = None
	image = cv2.imread(abspath(fname))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#gray = cv2.imread(image, 0)

	found_hor = find_maxVal(gray, './controllers/data/template_horizontal.jpg')
	found_ver = find_maxVal(gray, './controllers/data/template_vertical.jpg')
	print 'found horizontal: ', found_hor, type(found_hor)
	print 'found vertical:', found_ver, type(found_ver)
	verti = False
	try:
		if found_ver[0][0] >= found_hor[0][0]:
			found = found_ver[0]
			(tH, tW) = found_ver[1]
			verti = True
		else:
			found = found_hor[0]
			(tH, tW) = found_hor[1]
			print 'horizontal'
	except Exception as e:
		print "Exception occured is :",e 
	# unpack the bookkeeping varaible and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	# draw a bounding box around the detected result and display the image
	#cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	#cv2.imshow("Image", image)
	if verti == True:
		imCrop = image[int(startY):int(startY+endY), int(startX):int(startX+endX)]
	else:
		#imCrop = image[int(startY):int(startY+endY), int(startX):int(startX+endX)]
		imCrop = image[int(startX):int(endX), int(startY):int(endY)]
	f, ext = fname.split('.')
	new_name = f + '_cropped.' + ext
	cv2.imwrite(new_name, imCrop)
	return new_name
