import tensorflow as tf
from tensorflow.keras.layers import Input, Dropout, Dense, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2

class InceptionResNetV2Model:
    def __init__(self, input_shape=(200, 200, 3), embedding_dim=128, dropout_rate=0.5):
        self.input_shape = input_shape
        self.embedding_dim = embedding_dim
        self.dropout_rate = dropout_rate
        self.base_model = self._load_base_model()
        self.embedding_model = self._build_embedding_model()

    def _load_base_model(self):
        base_model = InceptionResNetV2(weights='imagenet', include_top=False, pooling='avg')
        for layer in base_model.layers:
            layer.trainable = False
        return base_model

    def _build_embedding_model(self):
        input_layer = Input(shape=self.input_shape)
        x = self.base_model(input_layer)
        x = Dropout(self.dropout_rate, name='Dropout')(x)
        x = Dense(self.embedding_dim, use_bias=False, name='Bottleneck')(x)
        x = BatchNormalization(momentum=0.995, epsilon=0.001, scale=False, name='Bottleneck_BatchNorm')(x)
        embedding_model = Model(inputs=input_layer, outputs=x)
        return embedding_model

    def get_model(self):
        return self.embedding_model


if __name__ == '__main__':
    model_builder = InceptionResNetV2Model()
    embedding_model = model_builder.get_model()
    embedding_model.summary()
