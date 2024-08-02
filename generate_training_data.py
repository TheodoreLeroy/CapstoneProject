import os
import random
import numpy as np
from pyprojroot.here import here

def generate_triplets(path, num_triplets_each_person=100):
    """
    Generate triplets for training a triplet-based model using anchor, positive, and negative images.

    Parameters:
        path (str): Path to the directory containing the images, structured with one subdirectory per class.
        num_triplets_each_person (int, optional): Number of triplets to generate for each person (default is 100).

    Returns:
        tuple: A tuple containing three lists - anchors, positives, and negatives.
               Each list contains file paths to the anchor, positive, and negative images, respectively.
    """
    anchors, positives, negatives = [], [], []

    class_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for folder in class_folders:
        folder_path = os.path.join(path, folder)
        image_files = os.listdir(folder_path)

        for _ in range(num_triplets_each_person):
            anchor = random.choice(image_files)
            positive = random.choice(image_files)
            other_folder = random.choice([f for f in class_folders if f != folder])
            other_folder_path = os.path.join(path, other_folder)
            negative = random.choice(os.listdir(other_folder_path))
            
            anchors.append(os.path.join(folder_path, anchor))
            positives.append(os.path.join(folder_path, positive))
            negatives.append(os.path.join(other_folder_path, negative))

    return anchors, positives, negatives

if __name__ == '__main__':
    anchors, positives, negatives = generate_triplets(here("mtcnn-faces"), num_triplets_each_person=100)
    print(anchors[0], positives[0], negatives[0])
