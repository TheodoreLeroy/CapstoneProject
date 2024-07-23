from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import cv2
import numpy as np

class VGG16Model:
    def __init__(self, trained_model):
        # Load the pre-trained VGG16 model
        self.model = trained_model

    def get_embeddings(self, img, faces):
        embeddings = []
        for (x, y, w, h) in faces:
            face_img = img[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (224, 224))
            face_array = img_to_array(face_img)
            face_array = np.expand_dims(face_array, axis=0)
            face_array = preprocess_input(face_array)
            embedding = self.model.predict(face_array)
            embeddings.append(embedding)
        return embeddings
