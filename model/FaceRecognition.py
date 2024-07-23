import faiss
import time
import numpy as np
import cv2

class FaceRecognitionSystem:

    def __init__(self, haar_cascade, vgg_model):
        self.haar_cascade = haar_cascade
        self.vgg_model = vgg_model
        self.index = None

    def load_database_embeddings(self, embeddings_path):
        # Load embeddings from the database
        self.database_embeddings = np.load(embeddings_path)
        d = self.database_embeddings.shape[1]  # Dimension of the embeddings
        self.index = faiss.IndexFlatL2(d)
        self.index.add(self.database_embeddings)

    def recognize_faces(self, embeddings, threshold=0.5):
        embeddings = np.vstack(embeddings)
        distances, indices = self.index.search(embeddings, 1)
        recognized_faces = [idx[0] for dist, idx in zip(distances, indices) if dist[0] < threshold]
        return recognized_faces

    def mark_attendance(self, recognized_faces):
        for student_id in recognized_faces:
            print(f"Student ID {student_id} is present.")

    def process_frame(self, frame, threshold=0.5):
        faces = self.haar_cascade.detect_faces(frame)
        if len(faces) > 0:
            embeddings = self.vgg_model.get_embeddings(frame, faces)
            recognized_faces = self.recognize_faces(embeddings, threshold)
            self.mark_attendance(recognized_faces)
        return frame, faces

    def run(self, capture_interval=300):
        # Camera setup
        camera = cv2.VideoCapture(0)
        while True:
            ret, frame = camera.read()
            if ret:
                processed_frame, faces = self.process_frame(frame)
                for (x, y, w, h) in faces:
                    cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow('Attendance System', processed_frame)
                time.sleep(capture_interval)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        camera.release()
        cv2.destroyAllWindows()
