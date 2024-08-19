import os
import torch
from fastapi import FastAPI, File, UploadFile
from mtcnn.mtcnn import MTCNN
from torchvision.transforms import Resize, ToTensor
from pydantic import BaseModel
from typing import List
import numpy as np
from io import BytesIO
from PIL import Image
from src.base_model.inception_resnet_v1 import InceptionResnetV1

app = FastAPI()

# Load the pre-trained face embedding model
model = InceptionResnetV1(pretrained='vggface2')
checkpoint = torch.load(
    'src/trained_model/20180402-114759-vggface2.pt')
model.load_state_dict(checkpoint)
model.eval()
print("Finish loading model")

# Initialize the MTCNN face detector
detector = MTCNN()


class ImageResponse(BaseModel):
    boxes: List[List[float]]
    embeddings: List[List[float]]


@app.post("/process_image", response_model=ImageResponse)
async def process_image(image: UploadFile = File(...)):
    # Get the input image from the request
    image_data = await image.read()

    # Convert image data to numpy array
    pil_image = Image.open(BytesIO(image_data)).convert('RGB')
    image_array = np.array(pil_image)

    # Use MTCNN to detect faces in the image
    faces = detector.detect_faces(image_array)
    boxes = []
    embeddings = []

    for face in faces:
        x1, y1, width, height = face['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        boxes.append([x1, x2, y1, y2])

        face_img = pil_image.crop((x1, y1, x2, y2))

        face_tensor = ToTensor()(Resize((160, 160))(face_img)).unsqueeze(0)

        with torch.no_grad():
            face_embedding = model(face_tensor).numpy()

        embeddings.append(face_embedding.tolist()[0])

    # Return the bounding boxes and embeddings as a JSON response
    return ImageResponse(
        boxes=boxes,
        embeddings=embeddings
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001)
