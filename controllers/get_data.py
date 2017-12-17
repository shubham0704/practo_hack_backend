from controllers.modules import *
#from modules import *
from controllers import cloudvisreq
import cloudvisreq
MON = ["JAN", "FEB", "MAR", "MAY", "JUN", "JUNE", "JULY",  "JUL", "AUG", "SEPT","SEP", "OCT", "NOV", "DEC"]

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
	try:
		lines = data.split('\n')
		#print(lines)
		#print(data)
	except:
		return
	dates = []
	print lines
	for line in lines:
		try:
			dt = re.search("EXP.[\s]{0,1}([A-Z]{3,4}[\s]{0,1}.[0-9]{2,4})", line).group(1)
			dates.append(dt)
		except:
			pass
		items = line.split()
		if len(items) > 1:
			for item in items:
				try:
					if re.match('([0-9].+)/([0-9].+)', item) or re.match('([a-zA-Z].+)([.\w])[0-9].+', item):
						now = parse(item)
						dates.append(now)
				except Exception as e:
					
					continue
			try:
				dt = re.search("[A-Z]{3}.[\s]{0,1}[0-9]{2,4}", line).group(0)
				dates.append(dt)
			except:
				pass
		else:
			try:
				if re.match('([0-9].+)/([0-9].+)', line) or re.match('([a-zA-Z].+).[0-9].+', line):	
					now = parse(line)
					dates.append(now)
				else:
					pass
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
		#print line
		try:
			dt = re.search("EXP.[\s]{0,1}([A-Z]{3,4}[\s]{0,1}.[0-9]{2,4})", line).group(1)
			dates.append(dt)
		except:
			pass
	try:
		#print vertical
		print ('dates:', dates)
		#dates = [parse(dt) for dt in dates]
		return max(dates)

	except Exception as e:
		nd = []
		if dates:	
			for dt in dates:
				try:
					x = parse(dt)
					nd.append(x)
				except:
					try:
						#dt = " ".(it for it in dt.split("."))
						its = dt.split(".")
						# if its[0] not in MON:
						# 	for it in MON:
						# 		if its[0][:1] == it[:1]:
						# 			its[0] == it
						# dt = " ".join((it for it in dt.split(".")))
						# x = parse(dt)
						# nd.append(x)
						if its[0] == "SER":
							its[0] = "SEP"
							its[1] = "20" + its[1] 
						dt = ".".join((it for it in its))
						print (dt)
						nd.append(parse(dt))
					except:
						pass

			#dates = [parse(dt) for dt in dates]
			try:
				filt = []	
				for it in nd:
					if type(it) == type("av"):
						continue
					filt.append(it)
				return max(filt)
			except:
				print(nd)
				return None
		else:
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

if __name__ == '__main__':

 #print get_name('/home/master/Desktop/GIT/practo_hack_backend/uploads/temp/bc228d1a-8dd0-4447-ba61-95fc05a287e7.jpg')
 print sanitize_data('/home/master/Desktop/GIT/practo_hack_backend/uploads/temp/IMG_20171217_131015.jpg')