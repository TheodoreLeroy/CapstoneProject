from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("Using GPU")
else:
    print("No GPU available, using CPU")

# Load the LFW dataset
lfw_people = fetch_lfw_people(data_home=None, funneled=True, resize=0.5,
                              min_faces_per_person=70, color=True,
                              slice_=(slice(70, 195), slice(78, 172)),
                              download_if_missing=True, return_X_y=False)


X = lfw_people.images
y = lfw_people.target
target_names = lfw_people.target_names
n_classes = len(target_names)


def resize_image(img):
    return np.array(array_to_img(img, scale=False).resize((224, 224)))


X_resized = np.array([resize_image(img) for img in X])
X_resized = preprocess_input(X_resized)
y_categorical = to_categorical(y, num_classes=n_classes)

X_train, X_test, y_train, y_test = train_test_split(X_resized, y_categorical, test_size=0.25, random_state=42)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = Flatten()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(n_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Save the model
model.save('face_recognition_vgg16.h5')

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test loss: {loss}')
print(f'Test accuracy: {accuracy * 100:.2f}%')