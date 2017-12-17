from controllers.modules import *
#from modules import *
from controllers import cloudvisreq
#import cloudvisreq


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
	img = Image.open(abspath(fname))
	if img.size[0] < img.size[1]:
		vertical = True
	if prepro == True:
		data = cloudvisreq.get_lines(image_filenames=[preprocess(fname)])
	else:
		data = cloudvisreq.get_lines(image_filenames=[fname])
	
	#data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
	lines = data.split('\n')
	dates = []
	
	for line in lines:
		items = line.split()
		if len(items) > 1:
			for item in items:
				try:
					if re.match('([0-9].+)/([0-9].+)', item) or re.match('([a-zA-Z].+).[0-9].+', item):
						now = parse(item)
						dates.append(now)
				except Exception as e:
					
					continue
		else:
			try:
				if re.match('([0-9].+)/([0-9].+)', line) or re.match('([a-zA-Z].+).[0-9].+', line):	
					now = parse(lines)
					dates.append(now)
			except:
				pass
	
	for line in lines:
		items = line.split()
		
		for i, item in enumerate(items):
			if "EX" in item:
				date = "".join((x for x in items[i+1:]))
				try:
					date = parse(date)
					dates.append(date)
				except:
					pass
	try:
		#print vertical
		return max(dates)

	except Exception as e:
		return None

	return 

def get_name(fname):
	

	#img = Image.open(abspath(fname))
	data = cloudvisreq.get_lines(image_filenames=[fname])
	#data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
	lines = data.split('\n')
	#print get_lines
	freq = {}
	for line in lines:
		items = line.split()
		for item in items:
			if item not in freq and len(item) > 4 :
				for ele in freq:
					if item in ele:
						freq[ele] += 1
				freq[item] = 0
				if len(items) < 2:
					freq[item] +=2
			elif item in freq:
				freq[item] += 4
	maxVal = 0
	k = None
	candidates = []
	for x, y in freq.items():

		if maxVal < y:
			candidates[:] = []
			k = x
			maxVal = y
		elif maxVal == y:
			candidates.append(k)
	if len(candidates) > 1:
		k = " ".join((item for item in candidates))
		return k 
	return k


# if __name__ == '__main__':

# 	#print get_name('/home/master/Desktop/GIT/practo_hack_backend/uploads/temp/bc228d1a-8dd0-4447-ba61-95fc05a287e7.jpg')
# 	print sanitize_data('/home/master/Desktop/GIT/practo_hack_backend/uploads/temp/bc228d1a-8dd0-4447-ba61-95fc05a287e7.jpg')