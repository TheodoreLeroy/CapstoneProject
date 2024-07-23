import cv2

class HaarCascade:
    def __init__(self, haar_cascade_path):
        # Initialize Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(haar_cascade_path)

    def detect_faces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        return faces
