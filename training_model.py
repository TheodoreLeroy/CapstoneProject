import os
from pyprojroot.here import here
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from generate_training_data import generate_triplets
from for_training_model import for_training_model
import matplotlib.pyplot as plt
import argparse
from FaceNetModel import FaceNetModel

def preprocess_image(filename):
    image_string = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image


def visualize(anchor, positive, negative):
    """Visualize a few triplets from 1 instance of the dataset."""
    fig, axs = plt.subplots(1, 3, figsize=(10, 10))
    axs[0].imshow(anchor)
    axs[0].set_title("Anchor")
    axs[1].imshow(positive)
    axs[1].set_title("Positive")
    axs[2].imshow(negative)
    axs[2].set_title("Negative")
    for ax in axs:
        ax.axis('off')
    plt.show()


def preprocess_triplets(anchor, positive, negative):
    """
    Given the filenames corresponding to the three images, load and
    preprocess them.
    """
    return (
        preprocess_image(anchor),
        preprocess_image(positive),
        preprocess_image(negative),
    )


def prepare_data(train_size=1000):
    """
    Prepare data for training as a tf.data.Dataset instance.
    """
    anchor, positive, negative = generate_triplets(here("mtcnn-faces"), train_size)
    dataset_anchor = tf.data.Dataset.from_tensor_slices(anchor)
    dataset_positive = tf.data.Dataset.from_tensor_slices(positive)
    dataset_negative = tf.data.Dataset.from_tensor_slices(negative)
    dataset = tf.data.Dataset.zip((dataset_anchor, dataset_positive, dataset_negative))
    dataset = dataset.shuffle(buffer_size=1024)
    dataset = dataset.map(preprocess_triplets)
    return dataset


def training_process(epochs, batch_size, learning_rate=0.0001, margin=0.5, train_size=1000, cache=True):
    """
    Fine-tune pre-trained model.
    epochs: number of epochs
    batch_size: batch size
    learning_rate: learning rate
    margin: margin for triplet loss
    train_size: number of training images each person
    cache: cache the dataset
    """
    dataset = prepare_data(train_size)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    if cache:
        dataset = dataset.cache()
    
    model_triple_loss, embedding_model = for_training_model()
    model_triple_loss = FaceNetModel(model_triple_loss, margin)
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model_triple_loss.compile(optimizer=optimizer)
    model_triple_loss.fit(dataset, epochs=epochs)

    fine_tune_model_dir = here("fine_tune_model")
    if not os.path.exists(fine_tune_model_dir):
        os.mkdir(fine_tune_model_dir)

    embedding_model.save(os.path.join(fine_tune_model_dir, "embedding_model.h5"))


def arg_parse():
    parser = argparse.ArgumentParser(description="Training model arguments")
    parser.add_argument("--epochs", type=int, default=1, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=1e-5, help="Learning rate")
    parser.add_argument("--margin", type=float, default=0.5, help="Margin for triplet loss")
    parser.add_argument("--train_size", type=int, default=1000, help="Number of training images")
    parser.add_argument("--cache", type=bool, default=True, help="Cache the dataset")
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    training_process(args.epochs, args.batch_size, args.learning_rate, args.margin, args.train_size, args.cache)
