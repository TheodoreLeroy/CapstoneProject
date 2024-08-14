import cv2
# from .forms import ClassForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files.base import ContentFile
import os
import requests
import django
import numpy as np
import matplotlib.pyplot as plt
# Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

# # Initialize Django
# django.setup()


def test():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    img_counter = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("failed to grab frame")
            break
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting")
            break
        elif cv2.waitKey(1) & 0xFF == ord(' '):
            img_name = "myPic_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written".format(img_name))
            img_counter += 1

    # Release the capture and close the window
    cap.release()
    cv2.destroyAllWindows()


def post():
    # Get the image from the request
    # image = request.FILES.get('image')

    # if not image:
    #     return JsonResponse({'error': 'No image provided'}, status=400)
    image_path = "myPic_0.png"

    with open(image_path, "rb") as image_file:
        files = {"image": ("test_image.jpg", image_file, "image/jpeg")}
        # Send the request to the external API
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)

    if response.status_code == 200:
        print("API request successful")
        data = response.json()
        print("Received boxes:", data['boxes'])
        print("Received embeddings shape:", [
              len(emb) for emb in data['embeddings']])
        # Open the original image for drawing
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Draw bounding boxes
        for box in data['boxes']:
            x1, x2, y1, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # Display the image with bounding boxes
        plt.figure(figsize=(12, 8))
        plt.imshow(np.array(image))
        plt.axis('off')
        plt.title("Detected Faces")
        plt.show()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)


post()
# test()
# def test_and_draw():
#     data = post()
#     # Print the received data
#     print("Received boxes:", data['boxes'])
#     print("Received embeddings shape:", [len(emb)
#           for emb in data['embeddings']])

# image = cv2.imread("myPic_0.png")
# draw = cv2.imshow("test", image)

# for box in data['boxes']:
#     x1, x2, y1, y2 = box
#     draw.rectangle([x1, y1, x2, y2], outline="red", width=2)


# test()
# test_and_draw()
