# src/student_import.py

import os
from PIL import Image
import torch
import pickle
from face_recognition import FaceRecognition
from database import import_student
from config import Config

class StudentImporter:
    def __init__(self):
        self.face_recognition = FaceRecognition(device='cpu')

    def process_student(self, student_id, name, image_path):
        """
        Process the student image to create embeddings and store in the database.
        """
        image = Image.open(image_path)
        
        # Generate embedding using FaceRecognition class
        embedding = self.face_recognition.model(self.face_recognition.mtcnn(image).unsqueeze(0)).detach().cpu().numpy()
        
        # Store student data and embedding in the database
        import_student(student_id, name, embedding)

        print(f"Finishing import student({student_id},{name})")


    def import_students_from_folder(self, folder_path):
        """
        Import all students from a folder. Each student should have a corresponding image file.
        Args:
            folder_path (str): The folder containing student images.
        """
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(('jpg', 'jpeg', 'png')):
                continue
            
            # Extract student_id and name from the filename
            student_id, name = self._extract_student_info(filename)
            if not student_id or not name:
                print(f"Skipping file {filename}: invalid filename format")
                continue

            image_path = os.path.join(folder_path, filename)
            self.process_student(student_id, name, image_path)
    
    def _extract_student_info(self, filename):
        """
        Extract student information from the filename.
        Assumes the format '{student_id}={name}.ext'
        Args:
            filename (str): The filename to extract info from.
        Returns:
            tuple: A tuple containing (student_id, name)
        """
        try:
            name_part, _ = os.path.splitext(filename)
            student_id, name = name_part.split('=', 1)
            return student_id, name
        except ValueError:
            return None, None