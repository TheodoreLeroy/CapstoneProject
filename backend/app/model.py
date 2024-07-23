from .database import db
import numpy as np

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    embedding = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, name, embedding):
        self.name = name
        self.embedding = embedding

    @staticmethod
    def create(name, embedding):
        embedding_blob = embedding.tobytes()
        new_student = Student(name=name, embedding=embedding_blob)
        db.session.add(new_student)
        db.session.commit()
        return new_student

    @staticmethod
    def get_by_id(student_id):
        return Student.query.get(student_id)

    @staticmethod
    def get_all():
        return Student.query.all()

    @staticmethod
    def update(student_id, name=None, embedding=None):
        student = Student.get_by_id(student_id)
        if student:
            if name:
                student.name = name
            if embedding is not None:
                student.embedding = embedding.tobytes()
            db.session.commit()
        return student

    @staticmethod
    def delete(student_id):
        student = Student.get_by_id(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
        return student

    @staticmethod
    def embedding_to_array(embedding_blob):
        return np.frombuffer(embedding_blob, dtype=np.float32)

    @staticmethod
    def array_to_embedding(embedding_array):
        return embedding_array.tobytes()
