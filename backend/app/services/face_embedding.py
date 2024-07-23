from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# Initialize VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = Flatten()(base_model.output)
embedding_model = Model(inputs=base_model.input, outputs=x)

def get_embeddings(img, faces):
    embeddings = []
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (224, 224))
        face_array = img_to_array(face_img)
        face_array = np.expand_dims(face_array, axis=0)
        face_array = preprocess_input(face_array)
        embedding = embedding_model.predict(face_array)
        embeddings.append(embedding)
    return embeddings
