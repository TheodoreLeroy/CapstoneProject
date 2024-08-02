import os
import tensorflow as tf
from tensorflow.python.client import device_lib

# Set environment variable to disable oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Function to list available devices
def get_available_devices():
    devices = device_lib.list_local_devices()
    return [x.name for x in devices]

print("Available devices:", get_available_devices())

# Check which GPU TensorFlow is using
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")

# Example using tf.compat.v1.placeholder
with tf.compat.v1.Session() as sess:
    x = tf.compat.v1.placeholder(tf.float32, shape=[None, 10])
    print("Placeholder created:", x)
