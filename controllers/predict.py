from controllers.modules import *

__PERM__UPLOADS__ = "uploads/permanent/"
__TEMP__UPLOADS__ = "uploads/temp/"


class PredictHandler(RequestHandler):

	def set_default_headers(self):
	    print("setting headers!!!")
	    self.set_header("Access-Control-Allow-Origin", "*")
	    self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
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
		"take in uploaded image of the medicine and then return information in json format"
		pass