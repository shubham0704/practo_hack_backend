from controllers.modules import *
#from modules import *
try:
    makedirs(RESULTS_DIR)
except:
    pass

def make_image_data_list(image_filenames):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    img_requests = []
    for imgname in image_filenames:
        with open(imgname, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            img_requests.append({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'DOCUMENT_TEXT_DETECTION',
                        'maxResults': 1
                    }]
                    
            })
    return img_requests

def make_image_data(image_filenames):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filenames)
    return json.dumps({"requests": imgdict }).encode()


def request_ocr(api_key, image_filenames):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filenames),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


def get_lines(image_filenames=["ocr1.png"]):
    #image_filenames = ["ocr1.png"]
    #api_key = env.api_key
    api_key = os.environ["api_key"]
    if not api_key or not image_filenames:
        print("""
            Please supply an api key, then one or more image filenames
            $ python cloudvisreq.py api_key image1.jpg image2.png""")
    else:
        response = request_ocr(api_key, image_filenames)
        if response.status_code != 200 or response.json().get('error'):
            #print(response.text)
            pass
        else:
            for idx, resp in enumerate(response.json()['responses']):
                # save to JSON file
                imgname = image_filenames[idx]
                jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                with open(jpath, 'w') as f:
                    datatxt = json.dumps(resp, indent=2)
                    #print("Wrote", len(datatxt), "bytes to", jpath)
                    #f.write(datatxt)

                # print the plaintext to screen for convenience
                #print("---------------------------------------------")
                #print 'response:\n', resp, "\n\n\n"

                try:
                    t = resp['textAnnotations'][0]
                except:
                    return
                #print("    Bounding Polygon:")
                #print(t['boundingPoly'])
                #print("    Text:")
                #print(t['description'])
                return t['description']
