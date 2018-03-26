import operator
import difflib

from controllers.modules import *
# from modules import *
from controllers import cloudvisreq
# import cloudvisreq

MON = ["JAN", "FEB", "MAR", "MAY", "JUN", "JUNE", "JULY", "JUL", "AUG", "SEPT", "SEP", "OCT", "NOV", "DEC"]


def preprocess(fname):
    image = cv2.imread(fname, 0)
    thnew = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 7)
    equ = cv2.equalizeHist(thnew)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(equ, kernel, iterations=2)
    kernel = np.ones((2, 2), np.uint8)
    erode = cv2.erode(dilate, kernel, iterations=2)
    f, ext = fname.split('.')
    new_name = f + '_preprocess.' + ext
    cv2.imwrite(new_name, erode)
    return new_name


def resize(fname, width=700):
    image = cv2.imread(fname, 0)
    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    f, ext = fname.split('.')
    new_name = f + '_preprocess.' + ext
    cv2.imwrite(new_name, image)
    return new_name


def sanitize_data(fname, prepro=False, vertical=False):
    fname = resize(fname)
    if prepro == True:
        data = cloudvisreq.get_lines(image_filenames=[preprocess(fname)])
    else:
        data = cloudvisreq.get_lines(image_filenames=[fname])

    # data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')

    # patt = EXP. Mon.YY
    patt = re.compile(r"EXP\.( *[a-zA-Z]+)\.?([\d]+)")
    obj = re.search(patt, data)
    if obj:
        month, year = obj.group(1, 2)
        month = difflib.get_close_matches(month, MON, n=1, cutoff=0.1)[0]

        return "{} {}".format(month.strip(), year.strip())

    # patt = MM/YYYY
    patt = re.compile(r"\d{2}/\d{4}")
    dates = re.findall(patt, data)
    if dates:
        dates = [parse(date) for date in dates]
        dates.sort(reverse=True)

        return "{:%b %Y}".format(dates[0])

    # patt = Mon YYYY
    patt = re.compile(r"(%s)\.?\s*(\d{4})" % "|".join(MON))
    dates = re.findall(patt, data)
    if dates:
        dates = [
            (difflib.get_close_matches(date[0], MON, n=1, cutoff=0.1)[0], date[1])
            for date in dates
        ]

        dates = [parse(" ".join(date)) for date in dates]
        dates.sort(reverse=True)

        return "{:%b %Y}".format(dates[0])

    return "Not Found"


def get_name(fname):
    # img = Image.open(abspath(fname))
    data = cloudvisreq.get_lines(image_filenames=[resize(fname)])
    # data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')

    freq = {}
    data = data.replace("\n", " ")
    data = [word.title().strip("-.,") for word in data.split() if word not in set(stopwords.words('english'))]

    for word in data:
        if len(word) < 4:
            continue
        if word in freq.keys():
            freq[word] += 1
        else:
            freq[word] = 1

    names = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

    names = [x[0] for x in names if x[1] == names[0][1]]
    return " or ".join(names) or "Not Found"


if __name__ == '__main__':
    # print(get_name('/home/ujjwal/Github/practo_hack_backend/uploads/temp/bc228d1a-8dd0-4447-ba61-95fc05a287e7.jpg'))
    for file in os.listdir('/home/ujjwal/Github/practo_hack_backend/uploads/temp'):
        if isfile(os.path.join('/home/ujjwal/Github/practo_hack_backend/uploads/temp', file)) \
                and not splitext(file)[0].endswith("preprocess"):
            print(file)
            print(get_name(os.path.join('/home/ujjwal/Github/practo_hack_backend/uploads/temp', file)))
            print(sanitize_data(os.path.join('/home/ujjwal/Github/practo_hack_backend/uploads/temp', file)))

    # print(
        # sanitize_data('/home/ujjwal/Github/practo_hack_backend/uploads/temp/2e76d016-6d1b-437c-b76b-5deec8a8041a.jpg'))

    # print(sanitize_data('/home/ujjwal/Github/practo_hack_backend/uploads/temp/IMG_20171217_131015.jpg'))
    # print(get_name('/home/ujjwal/Github/practo_hack_backend/uploads/temp/IMG_20171217_131015.jpg'))

    # print(sanitize_data('/home/ujjwal/Github/practo_hack_backend/uploads/temp/bdd07912-feba-4036-9312-64953d71dd1b.jpg'))
    # print(get_name('/home/ujjwal/Github/practo_hack_backend/uploads/temp/bdd07912-feba-4036-9312-64953d71dd1b.jpg'))
