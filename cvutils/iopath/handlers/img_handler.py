import cv2

import numpy as np

from PIL import Image, ImageFile

from .base import BaseFileHandler

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImgHandler(BaseFileHandler):

    str_like = False
    for_img = True

    def load_from_fileobj(self, file, **kwargs):
        content = file
        img_np = np.frombuffer(content, np.uint8)
        
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        return img

    def dump_to_fileobj(self, obj, **kwargs):
        return cv2.imencode('.png', obj)[1].tostring()
    
    def dump_to_str(self, obj, **kwargs):
        return cv2.imencode('png', obj)[1].tostring()
