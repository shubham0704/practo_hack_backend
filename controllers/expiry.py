from controllers.modules import *
from controllers.get_data import sanitize_data, get_name
from controllers.template_match import crop_text

__PERM__UPLOADS__ = "uploads/permanent/"
__TEMP__UPLOADS__ = "uploads/temp/"



class OcrHandler(RequestHandler):

	def set_default_headers(self):
		print("setting headers!!!")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
		self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')


	def upload(self, fileinfo):

	    fname = fileinfo['filename']
	    extn = splitext(fname)[1]
	    cname = str(uuid.uuid4()) + extn
	    fh = open(__TEMP__UPLOADS__ + cname, 'wb')
	    fh.write(fileinfo['body'])
	    fh.close()

	    return {"status" : 200, "message" : "File Sucessfully Uploaded", "file_loc" : __TEMP__UPLOADS__ + cname}


	@coroutine
	def post(self):
		response = self.upload(fileinfo=self.request.files['image'][0])
		fname = response['file_loc']
		#crop_image_name = crop_text(abspath(fname))
		#print crop_image_name
		date = sanitize_data(fname)

		name = get_name(fname)
		if date:
			self.write({"status" : 200, "message" : "expiry date detected", "expiry":str(date), "name":name})
		elif name:
			self.write({"status" : 200, "message" : "expiry date not present", "expiry":"NA", "name": name})
		else:
			self.write({"status" : 200, "message" : "expiry date not present", "expiry":"NA", "name": "NA"})
