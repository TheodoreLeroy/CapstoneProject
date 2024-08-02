import os
from pyprojroot.here import here
import shutil

def clean_lfw_dataset(dataset_path):
    # Iterate through each folder in the dataset directory
    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)
        
        if os.path.isdir(folder_path):
            # Count the number of image files in the folder
            num_images = len([file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))])
            
            # Delete the folder if it contains fewer than 3 images
            if num_images < 3:
                print(f"Deleting folder: {folder_path} (contains {num_images} images)")
                shutil.rmtree(folder_path)

if __name__ == '__main__':
    dataset_path = "data"  # Change this to the actual path of your LFW dataset
    clean_lfw_dataset(dataset_path)
