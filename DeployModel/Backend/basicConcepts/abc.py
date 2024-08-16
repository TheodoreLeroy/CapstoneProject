from sklearn.metrics.pairwise import cosine_similarity
import cv2
import torch
# from .forms import ClassForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
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


image_path = "hien1.jpg"


def post():
    # Get the image from the request
    # image = request.FILES.get('image')

    # if not image:
    #     return JsonResponse({'error': 'No image provided'}, status=400)

    with open(image_path, "rb") as image_file:
        print(type(image_file))
        files = {"image": ("test_image.jpg", image_file, "image/jpeg")}

        # Send the request to the external API
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)

    if response.status_code == 200:
        print("API request successful")
        data = response.json()
        # print("Received boxes:", data['boxes'])
        # print("Received embeddings shape:", [
        #       len(emb) for emb in data['embeddings']])

        # file_name = "quynh.txt"
        # with open(file_name, 'w') as file:
        #     for vector in data['embeddings']:
        #         # print(vector)
        #         # break
        #         vector_str = ' '.join(map(str, vector))
        #         file.write(f'{vector_str}\n')
        # print("ok")

        # Open the original image for drawing
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        i = 0
        # Draw bounding boxes
        for box in data['boxes']:
            # print(box)
            x1, x2, y1, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            i+1

        # Display the image with bounding boxes
        plt.figure(figsize=(12, 8))
        plt.imshow(np.array(image))
        plt.axis('off')
        plt.title("Detected Faces")
        plt.show()
        # return JsonResponse(data)
        return data
    # else:
    #     return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)
# -0.003185610519722104


data = post()
boxs = data.get('boxes', [])
print(data['boxes'])
embedding = data.get('embeddings')
# print(embedding)
# for item in embedding:
#     print(item)


def identify(face_embedding):
    file_name = 'hien.txt'  # the weekend
    with open(file_name, 'r') as file:
        target_embed = [list(map(float, line.split())) for line in file]
    # print(target_embed)
    target_embed = torch.tensor(target_embed).clone().detach()
    i = 0
    ident = -1
    max_similarity = 0
    for face in face_embedding:

        face = torch.tensor(face).clone().detach()

        similarity = cosine_similarity(
            face.cpu().numpy().reshape(1, -1),
            target_embed.unsqueeze(0).cpu().numpy().reshape(1, -1)
        )
        if similarity > max_similarity:
            max_similarity = similarity
            ident = i
        print("Cosine Similarity:", similarity)
        i += 1
    if max_similarity > 0.5:
        print(ident)
        drawing(boxs[ident], True)
    else:
        drawing(data, False)
        # if similarity > 0.6:
        #     print("giong")
        #     drawing(boxs[i], True)
        # else:
        #     print("khong giong")
        #     drawing(boxs[i], False)


def drawing(boxi, iden):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    align = 'center'
    font = ImageFont.truetype("arial.ttf", 20)
    # boxing = data['boxes']
    if iden is True:
        # for box in boxi:
        x1, x2, y1, y2 = boxi
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        # Position text slightly below the rectangle
        text_position = (x1, y2 + 5)
        # Vi tri        Text    Mau``
        draw.text(text_position, "em bao boi",
                  align='center', fill="red", font=font)
        # Display the image with bounding boxes
        plt.figure(figsize=(12, 8))
        plt.imshow(np.array(image))
        plt.axis('off')
        plt.title("Detected Faces")
        plt.show()
    else:
        for box in data['boxes']:
            x1, x2, y1, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            # Position text slightly below the rectangle
            text_position = (x1, y2 + 5)
            # Vi tri        Text    Mau``
            draw.text(text_position, "deo giong",
                      align=align, font=font, fill="red")
        # Display the image with bounding boxes
        plt.figure(figsize=(12, 8))
        plt.imshow(np.array(image))
        plt.axis('off')
        plt.title("Detected Faces")
        plt.show()


identify(embedding)


# print("hehe")
# file_name = 'test.txt'
# with open(file_name, 'r') as file:
#     target_embed = [list(map(float, line.split())) for line in file]
# print(target_embed)


def draw_embeddings_on_image(image_path, boxes, embeddings):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Draw bounding boxes and embeddings
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        # Display first 5 values for brevity
        embedding_text = f"Embedding {i+1}: {embeddings[i][:6]}..."
        draw.text((x1, y1 - 10), embedding_text, fill="red", font=font)

    # Display the image with bounding boxes and embeddings
    plt.figure(figsize=(12, 8))
    plt.imshow(np.array(image))
    plt.axis('off')
    plt.title("Detected Faces with Embeddings")
    plt.show()


# image_path = "drake.jpg"
# boxs = [[50, 50, 150, 150], [200, 200, 300, 300]]  # Example bounding boxes
# embeddings = [
#     [0.1, 0.2, 0.3, 0.4, 0.5],  # Example embeddings
#     [0.6, 0.7, 0.8, 0.9, 1.0]
# ]
# draw_embeddings_on_image(image_path, boxes=boxs, embeddings=embedding)
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

# from .models import *

# # test()
# # test_and_draw()
# class Helper:
#     # i want to
#     # get all student object in database
#     # get student id to find path to that student
#     def get_queryset(self):
#         return Student.objects.all()

#     # student = Student.objects.get(student_id=47)
#     # print(student)
#     # print("yolo")

#     def get_student_image_paths(self):
#         students = self.get_queryset()
#         for student in students:
#             print(
#                 f"Student ID: {student.id}, Image Path: {student.image_path}")

#     def identify(snapshot_embedd, studentId):
#         return

# class CameraHandle(generics.ListCreateAPIView):
#     # student = Student.objects.get(student_id=47)
#     # print(student)

#     serializer_class = CameraInfor

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 0 is the default camera
#         self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
#         self.running = True
#         self.snapshot_thread = threading.Thread(target=self.take_snapshots)
#         self.snapshot_thread.start()

#     def take_snapshots(self):
#         next_snapshot_time = datetime.now() + timedelta(seconds=30)
#         while self.running:
#             ret, frame = self.cap.read()
#             if ret:
#                 cv2.imshow('Frame', frame)
#                 if datetime.now() >= next_snapshot_time:
#                     timestamp = int(time.time())
#                     directory = 'Data/classes/AI168/slot'
#                     if not os.path.exists(directory):
#                         os.makedirs(directory)
#                     filename = os.path.join(
#                         directory, f'snapshot_{timestamp}.jpg')
#                     cv2.imwrite(filename, frame)
#                     print(f"Snapshot saved as {filename}")
#                     next_snapshot_time = datetime.now() + timedelta(seconds=30)
#                     self.send_image_to_api(filename)
#             if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
#                 self.running = False
#                 break
#         self.cap.release()
#         cv2.destroyAllWindows()

#     def send_image_to_api(self, image_path):
#         with open(image_path, 'rb') as image:
#             files = {'image': (os.path.basename(
#                 image_path), image, 'image/jpeg')}
#             response = requests.post(
#                 'http://127.0.0.1:5001/process_image', files=files)
#             print(f"API response: {response.status_code}, {response.text}")

#     def post(self, request, *args, **kwargs):
#         return JsonResponse({'status': 'Camera is running and taking snapshots every 10 minutes'})

#     def destroy(self, request, *args, **kwargs):
#         self.running = False
#         self.snapshot_thread.join()
#         self.cap.release()
#         cv2.destroyAllWindows()
#         return JsonResponse({'status': 'Camera stopped'})

#     def __del__(self):
#         self.running = False
#         self.snapshot_thread.join()
#         self.cap.release()
#         cv2.destroyAllWindows()
