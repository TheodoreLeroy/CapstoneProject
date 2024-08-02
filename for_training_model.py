import tensorflow as tf

from tensorflow.keras.layers import Input, Layer
from tensorflow.keras.models import Model

from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input

from FaceNetModel import FaceNetModel
from InceptionResnetV2 import InceptionResNetV2Model

class DistanceLayer(Layer):
    """
    This layer computes the distance between the anchor embedding and the positive embedding,
    and the anchor embedding and the negative embedding.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, anchor, positive, negative):
        ap_distance = tf.reduce_sum(tf.square(anchor - positive), axis=-1)
        an_distance = tf.reduce_sum(tf.square(anchor - negative), axis=-1)
        return ap_distance, an_distance


def for_training_model(target_shape=(200, 200)):
    anchor_input = Input(name="anchor", shape=target_shape + (3,))
    positive_input = Input(name="positive", shape=target_shape + (3,))
    negative_input = Input(name="negative", shape=target_shape + (3,))

    embedding_model = InceptionResNetV2Model().get_model()
    
    distances = DistanceLayer()(
        embedding_model(preprocess_input(anchor_input)),
        embedding_model(preprocess_input(positive_input)),
        embedding_model(preprocess_input(negative_input))
    )

    model = Model(inputs=[anchor_input, positive_input, negative_input], outputs=distances)
    return model, embedding_model

if __name__ == '__main__':
    train_model, embedding_model = for_training_model()
    face_net = FaceNetModel(train_model)

    dummy_data = [
        tf.zeros((1, 160, 160, 3)),
        tf.zeros((1, 160, 160, 3)),
        tf.zeros((1, 160, 160, 3))
    ]

    face_net(dummy_data)
    embedding_model.summary()
    face_net.summary()
