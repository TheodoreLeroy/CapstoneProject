# src/face_recognition.py

from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
import torch
from PIL import Image
from database import get_students_by_id
import numpy as np

class FaceRecognition:
    def __init__(self, ids, device='cpu'):
        """
        Initialize the FaceRecognition class with MTCNN for face detection
        and InceptionResnetV1 for face embedding.
        """
        self.device = torch.device(device)
        self.mtcnn = MTCNN(image_size=160, margin=20).to(self.device)
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        self.student_embeddings = self._load_student_embedding(ids)

    def _load_student_embeddings(self, ids):
        """
        Load student embeddings from the database.
        Args: 
            ids: A list of students' id attending a specific class
        Returns:
            dict: A dictionary mapping student IDs to embedding tuples
        """
        student_data = get_students_by_id(ids)
        student_embeddings = {
            student_id: torch.tensor(embedding).to(self.device)
            for student_id, embedding in student_data.items()
        }
        return student_embeddings

    def recognize_faces(self, image):
        """ 
        Recognize faces in a given image.
        Args:
            image (PIL.Image): The image containing faces to recognize.
        Returns:
            list: A list of identified students' ids or 'Unknown'.
        """
        aligned_faces = self.mtcnn(image)
        if aligned_faces is None:
            return ["No face detected"]



        embeddings = self.model(aligned_faces)
        identified_students = [self._identify_student(embedding) for embedding in embeddings]

        # returnData = {
        #     "identified_students": identified_students,
        #     "embeddings": embeddings
        # }

        return identified_students
    

    def _identify_student(self, face_embedding, threshold=0.7):
        """
        Identify a student based on the face embedding.
        Args:
            face_embedding (torch.Tensor): The embedding of the detected face.
        Returns:
            str: The identified student's id or 'Unknown'.
        """
        max_similarity = 0
        identified_student = "Unknown"
        for student_id, db_embedding in self.student_embeddings.items():
            similarity = cosine_similarity(
                face_embedding.detach().cpu().numpy().reshape(1, -1),
                db_embedding.unsqueeze(0).detach().cpu().numpy().reshape(1, -1)
            )
            if similarity > max_similarity:
                max_similarity = similarity
                identified_student = student_id
        return identified_student if max_similarity > threshold else "Unknown"