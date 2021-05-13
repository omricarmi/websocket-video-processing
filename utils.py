import numpy as np
from cv2 import cv2
import base64


def base64_url_data_to_cv2_image(data):
    data = base64.b64decode(data.split(',')[1])
    data = np.fromstring(data,np.uint8)
    img = cv2.imdecode(data,cv2.IMREAD_COLOR)
    return img


def cv2_image_to_base64_url_data(img,ext='jpeg'):
    _, data = cv2.imencode(f'.{ext}',img)
    data = base64.b64encode(data)
    return f"data:image/{ext};base64,{data.decode('utf-8')}"