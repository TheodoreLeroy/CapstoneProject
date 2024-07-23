import numpy as np
from PIL import Image
import io
import cv2

def convert_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
