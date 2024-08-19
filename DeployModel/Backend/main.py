from backend.src.face_recognition import FaceRecognition

#Cái này chỉ là hướng dẫn sử dụng :D
#ông tạo cái database Student(id) rồi điền cái config của mysql vô cái file bash này ha

"""
Tạo db nè
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    embedding BYTEA
);
"""

if __name__ == '__main__':
    """
        Vào lớp -> query ra ids của học sinh trong lớp đó -> list_of_students_id
    """
    list_of_students_id = []

    fr = FaceRecognition(list_of_students_id) # Khởi tạo FaceRecognition

    while True: #for each 5 minutes:
        image = None # Chụp ảnh: format = PIL.Image
        list_of_attending_students = fr.recognize_faces(image) 
        note = """
            giờ ông có list of attended students id rồi thì ông cho vào cái database gì để log lại
            xem là thằng học sinh này trong giờ này có đi học không
            nếu đủ 7/10 thì oke cho là present, không là cho absent
        """
    

    """
    Về phần import student thì ông có hai cách để import 
    - 1 là import theo files, có dạng là {studentid}={name}.jpg, dùng hàm import_students_from_folder
    - 2 là import theo từng học sinh dùng hàm process_student
    cụ thể thế naofp xem trong student_import.py
    """