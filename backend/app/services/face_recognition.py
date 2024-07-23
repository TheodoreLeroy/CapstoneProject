import numpy as np
from ..models import Student

def recognize_faces(embeddings):
    students = Student.query.all()
    student_embeddings = {student.id: Student.embedding_to_array(student.embedding) for student in students}
    
    recognized_faces = []
    for embedding in embeddings:
        for student_id, student_embedding in student_embeddings.items():
            if np.linalg.norm(embedding - student_embedding) < 0.5:  # Threshold for recognition
                recognized_faces.append(student_id)
                break
            
    return recognized_faces
