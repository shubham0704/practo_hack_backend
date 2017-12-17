"""
module to storing all the routes
"""

from controllers import *

routes = [
    (
        r"/upload",
        upload.UploadHandler
    ),
    (
        r"/predict",
        predict.PredictHandler
    ),
    (
        r"/ocr",
        expiry.OcrHandler
    )
]
