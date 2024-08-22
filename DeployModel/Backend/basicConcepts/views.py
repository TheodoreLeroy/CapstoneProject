from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from datetime import datetime
from PIL import Image
from io import BytesIO
import os
import shutil
import requests
import torch
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image, ImageDraw, ImageFont
from django.utils import timezone
import io
from collections import Counter
from django.db.models import Q
# CLASS
# get list class - url: "class/"
# create new class- url: "addClass/"
# get list class that have id - url: "classes/detail/"
# get 1 class with id of that class - url:


class ClassView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        # Use the appropriate serializer based on the type of request
        if 'classId' in self.kwargs or self.request.path.endswith('detail'):
            return ClassDetailSerializer
        return ClassSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('classId')
        if class_id:
            return Class.objects.filter(id=class_id)
        return Class.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            class_instance = serializer.save()
            # Create directory for the new class instance
            directory_path = 'Data/classes/' + str(class_instance.class_name)
            if(not os.path.exists(directory_path)):
                os.makedirs(directory_path, exist_ok=True)

            os.makedirs(directory_path + '/slot', exist_ok=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        class_id = self.kwargs.get('classId')
        if not class_id:
            return Response({'error': 'Class ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            class_instance = Class.objects.get(id=class_id)
            # Delete directory for the class instance
            directory_path = directory_path = 'Data/classes/' + \
                str(class_instance.class_name)
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            class_instance.delete()
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

# STUDENTS
# get list student - urls: "students/"


class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Student.objects.filter(class_id_id=id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


def handleFilePath(file_path):
    file_path_str = str(file_path)
    path_components = file_path_str.split('/')

    # new_component = 'students'
    # path_components.insert(-1, new_component)

    name, ext = os.path.splitext(path_components[-1])

    new_file_name = name + '.txt'
    path_components[-1] = new_file_name

    new_file_path = '/'.join(path_components)
    return new_file_path

# get list student - urls: "studentsClass<int:classId>/"


class StudentFromClassId(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        class_id = self.kwargs.get('classId')
        return Student.objects.filter(class_id_id=class_id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    # Convert image to embedding type

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                class_instance = Class.objects.get(
                    id=validated_data['class_id'].id)
                student = Student(
                    class_id=validated_data['class_id'],
                    name=validated_data['name'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )
                os.makedirs
                student.save()
                # print(serializer)
                if 'image' in request.FILES:
                    image = Image.open(request.FILES['image'])
                    max_width, max_height = 300, 300  # Desired size
                    # Resize the image while maintaining aspect ratio
                    image.thumbnail((max_width, max_height), Image.LANCZOS)

                    # Convert the image to RGB mode if it has an alpha channel
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    img_io = BytesIO()
                    image.save(img_io, format='JPEG')
                    # print(class_instance.class_name)
                    print("break1")
                    file_path = f'Data/classes/{class_instance.class_name}/students/{student.student_id}_{student.name}'
                    directory = os.path.dirname(
                        file_path + f'/{student.student_id}_{student.name}')
                    if not os.path.exists(directory):
                        os.makedirs(directory, exist_ok=True)
                    image.save(
                        file_path + f'/{student.student_id}_{student.name}.jpg', format='JPEG')

                    # print("break")
                    student.image = file_path + \
                        f'/{student.student_id}_{student.name}.jpg'
                    student.save()
                    # print("first path" + str(student.image))

                    image_path = str(student.image)
                    # print("image path:" + image_path)
                    file_path = handleFilePath(image_path)
                    # print("file path:" + file_path)

                    # Send image to external API
                    data = ProcessImageData(
                        image_path)
                    with open(file_path, 'w') as file:
                        for vector in data['embeddings']:
                            vector_str = ' '.join(map(str, vector))
                            file.write(f'{vector_str}\n')

                # Add id field to data
                respone_data = serializer.data
                respone_data['ID'] = student.student_id
                # print(respone_data)
                return Response(respone_data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error: {e}")
        return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            student_id = self.kwargs.get('pk')
            student = Student.objects.get(pk=student_id)
            student.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found",
                           code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Handle write embedding file


def handlePath(file_path, old_component, new_component):
    file_path_str = str(file_path)
    path_components = file_path_str.split('/')

    # Replace the old component with the new component
    if old_component in path_components:
        index = path_components.index(old_component)
        path_components[index] = new_component

    name, ext = os.path.splitext(path_components[-1])

    for_exist = '/'.join(path_components[:6])
    if not os.path.exists(for_exist):
        os.makedirs(for_exist)

    new_file_name = name + '.txt'
    path_components[-1] = new_file_name

    new_file_path = '/'.join(path_components)
    return new_file_path


def HandleWriteText(data, file_path):
    with open(file_path, 'w') as file:
        for vector in data['embeddings']:
            vector_str = ' '.join(map(str, vector))
            file.write(f'{vector_str}\n')


# API - source model2 - Phuc
# url: http://127.0.0.1:5001/process_image
def ProcessImageData(path):
    with open(path, 'rb') as image_file:
        files = {
            "image": ("test_image.jpg", image_file, "image/jpeg")}
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)
        if response.status_code == 200:
            print("API request success")
            return response.json()
        else:
            return response.Response({'error': 'Failed to process image'}, status=response.status_code)


# SLOT
# get slot-infomation - url: "slot/"
# post create-slot - url: "class=<int:classId>/createSlot"

class SlotInformation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()

    def perform_create(self, serializer):
        # print("perform_create called")
        if serializer.is_valid():
            validate_data = serializer.validated_data
            class_instance = Class.objects.get(id=validate_data['class_id'].id)
            slot_instance = serializer.save()
            slot_name = slot_instance.subject  # Assuming the slot has a 'subject' field
            directory = os.path.join(
                'Data', 'classes', class_instance.class_name, 'slot', slot_name)
            if not os.path.exists(directory):
                os.makedirs(directory + '\images')
                os.makedirs(directory + '\embedding')

        else:
            print(serializer.errors)

    def delete(self, request, *args, **kwargs):
        slot_id = self.kwargs.get('slotId')
        if not slot_id:
            return Response({'error': 'Class ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot_instance = Slot.objects.get(id=slot_id)
            slot_instance.delete()
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Slot.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)


# Get slot-information for 1 class with class_id - url: "class<int:classId>/slot/"
class SlotInformationFromIdClass(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Slot.objects.filter(class_id=id)


# Get 1 slot-information with id - url: "slot<int:slotId>/"


class SlotInformationFromId(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return Slot.objects.filter(id=id)


class GetTimeFrame(generics.ListCreateAPIView):
    serializer_class = TimeFrameSerializer

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return TimeFrame.objects.filter(slot_id=id)

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                print('he1')
                validate_data = serializer.validated_data
                timeframe = TimeFrame(
                    slot_id=validate_data['slot_id']
                )
                slot_instance = Slot.objects.get(
                    id=validate_data['slot_id'].id)
                # slot_id = validate_data['slot_id']
                class_instance = Class.objects.get(
                    id=slot_instance.class_id.id
                )
                print('he2')
                logs = Logs.objects.filter(slot_id=slot_instance.id).first()
                # print(timezone.now())
                # print(type(logs.time))
                if logs is None:
                    self.create_logs_student(slot_instance)
                else:
                    datetime_obj = datetime.fromisoformat(str(logs.time))
                    timezone_obj = datetime.fromisoformat(str(timezone.now()))
                    if not (datetime_obj.year == timezone_obj.year and
                            datetime_obj.month == timezone_obj.month and
                            datetime_obj.day == timezone_obj.day):
                        self.create_logs_student(slot_instance)
                if logs:
                    logs_instance = Logs.objects.filter(
                        Q(time__year=logs.time.year) &
                        Q(time__month=logs.time.month) &
                        Q(time__day=logs.time.day),
                        slot_id=slot_instance
                    )
                print('he3')

                # Pre-save timeframe to get ID
                timeframe.save()
                current_datetime = datetime.now().strftime('%Y%m%d%H%M')
                file_path = os.path.join('Data', 'classes', class_instance.class_name, 'slot', slot_instance.subject, 'embedding',
                                         f'{timeframe.id}_{current_datetime}.txt')

                embedding_file = validate_data['embedding']
                file_data = embedding_file.read()

                files = {"image": ("test_image.jpg", file_data,
                                   embedding_file.content_type)}
                response = requests.post(
                    'http://127.0.0.1:5001/process_image', files=files)
                if response.status_code == 200:
                    print("API request success!")
                    data = response.json()
                else:
                    print("API request failed")
                    print(response.json())

                # file_path is direct to embedding txt
                HandleWriteText(data, file_path)

                # Get student query list
                image_path, AttendList = identify_cosine_similarity.itentify(file_data,
                                                                             class_instance, timeframe.slot_id, data, 0.5)
                timeframe.embedding = image_path
                timeframe.save()
                # facesOneFrame = AttendentStudentsAtOneFrameSerializer

                self.save_attend_student(
                    AttendList, slot_instance.id, timeframe.id)

                self.Caculate_attend_percent(
                    logs_instance, slot_instance.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Error: {e}')
        return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_attend_student(self, AttendList, slot_id, frame_id):
        for id in AttendList:
            facesOneFrame = AttendentStudentsAtOneFrameSerializer(
                data={
                    'slot': slot_id,
                    'student_id': id,
                    'time_frame': frame_id
                }
            )
            # print(" ========= facesOneFrame ========= ")
            # print(facesOneFrame)

            if facesOneFrame.is_valid():
                facesOneFrame.save()
                print("Saved into database")

            else:
                print(facesOneFrame.errors)

    def create_logs_student(self, slot_instance):
        student_list_of_slot = Student.objects.filter(
            class_id_id=slot_instance.class_id
        )
        # print(student_list_of_slot)
        for student in student_list_of_slot:
            logs_data = {
                'student_id': student.student_id,
                'slot_id': slot_instance.id,
                'time': timezone.now().date()
            }
            logs = LogDetail(data=logs_data)
            if logs.is_valid():
                logs.save()
                print(f'Log initialized for student ID {student.student_id}')
            else:
                print(f'Errors: {logs.errors}')

    def Caculate_attend_percent(self, log_instance, slot_id):
        frame_instance = AttendentStudentsAtOneFrame.objects.filter(
            slot=slot_id)
        slot_instance = Slot.objects.get(
            id=slot_id
        )
        student_list_of_slot = Student.objects.filter(
            class_id_id=slot_instance.class_id
        )

        duration = self.getDuration(slot_instance)
        total_frames = 15
        unique_student_ids = frame_instance.values_list(
            'student_id', flat=True)
        id_counts = Counter(unique_student_ids)

        threshold = 0.8 * total_frames
        for student_id, count in id_counts.items():
            # print(student_id)
            if count >= threshold:
                try:
                    stu_attend = log_instance.get(student_id=student_id)
                    stu_attend.attend_status = True
                    stu_attend.save()
                    print(
                        f'ID {student_id} appears in {count} frames, which is {count / total_frames * 100:.2f}% and exceeds 80% of the total frames.')
                except Logs.DoesNotExist:
                    print('not exist')
            else:
                # logs_data = {
                #     'student_id': student_id,
                #     'slot_id': slot_id
                # }
                # logs = LogDetail(data=logs_data)
                # if logs.is_valid():
                #     logs.save()
                #     print('saved')
                # else:
                #     print(logs.errors)
                print(
                    f'ID {student_id} appears in {count} frames, which is {count / total_frames * 100:.2f}% and does not exceed 80% of the total frames.')

    def getDuration(self, slot_instance):
        today = datetime.today().date()
        time_start = datetime.combine(today,
                                      slot_instance.time_start)
        time_end = datetime.combine(today,
                                    slot_instance.time_end)
        duration = time_end - time_start
        duration_minutes = duration.total_seconds() / 60
        return duration_minutes

    def delete(self, request, *args, **kwargs):
        try:
            slot_instance = TimeFrame.objects.all()
            slot_instance.embedding
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Slot.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)


class GetAttendentAtOneFrame(generics.ListAPIView):
    serializer_class = AttendentStudentsAtOneFrameSerializer

    def get_queryset(self):
        id = self.kwargs.get('timeFrameId')
        return AttendentStudentsAtOneFrame.objects.filter(time_frame_id=id)

class GetLog(generics.ListAPIView):
    serializer_class = LogDetail

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return Logs.objects.filter(slot_id=id)

class identify_cosine_similarity:

    @staticmethod
    def getTextPath(file_path):
        file_path_str = str(file_path)
        path_components = file_path_str.split('/')

        name, ext = os.path.splitext(path_components[-1])

        new_file_name = name + '.txt'
        path_components[-1] = new_file_name
        embedd_path = '/'.join(path_components)
        return embedd_path

    @staticmethod
    def CaculatePresent(AttendList, student_id, student_name):
        # AttendList = {'id': [], 'name': []}
        AttendList['id'].append(student_id)
        AttendList['name'].append(student_name)

        return AttendList

    @staticmethod
    def draw_boxes(FaceList, class_id, slot_id, timeframe_id, image_bin):
        image = Image.open(io.BytesIO(image_bin)).convert('RGB')
        draw = ImageDraw.Draw(image)
        align = 'center'
        font = ImageFont.truetype("arial.ttf", 20)
        index = 0
        # FaceList = dict()
        for boxes, id, name in zip(FaceList['boxes'], FaceList['id'], FaceList['name']):
            x1, x2, y1, y2 = boxes
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            # Position text slightly below the rectangle
            text_position = (x1, y2 + 5)
            # Vi tri        Text    Mau``
            if id is not None and name is not None:
                draw.text(text_position, str(id) + '_'
                          + name,
                          align='center', fill="red", font=font)
            index += 1
        # Save the image with bounding boxes
        current_datetime = datetime.now().strftime('%Y%m%d%H%M')
        name = f'{timeframe_id}_{current_datetime}.jpg'
        path = f'Data/classes/{class_id.class_name}/slot/{slot_id.subject}/images/{name}'
        image.save(path)
        return path

    @staticmethod
    def itentify(image_bin, classId, slotId, data, threshold=0.7):
        students = Student.objects.filter(class_id_id=classId)
        timeframes = TimeFrame.objects.filter(slot_id_id=slotId)
        timeframes_id = timeframes.last().id
        student_ids = [student.student_id for student in students]
        student_names = [student.name for student in students]
        student_image_paths = [student.image for student in students]
        attendentStudentsID = []
        boxes = data['boxes']
        embedding_timeframe = data['embeddings']
        ''' For take each face compare to each student database '''
        # count face
        faceIndex = 0
        FaceList = {'boxes': [], 'id': [], 'name': []}
        AttenList = {'id': [], 'name': []}
        # print(timeframeIndex)
        for face in embedding_timeframe:
            # for studentId
            stuIndex = -1
            itemIndex = 0

            face = torch.tensor(face).clone().detach()
            # print(face)
            max_similarity = 0
            for item in student_image_paths:
                # For retrive boxes with reference face
                student_text_embedd = identify_cosine_similarity.getTextPath(
                    item)
                # print(student_text_embedd)
                with open(student_text_embedd, 'r') as file:
                    student_embedd = [list(map(float, line.split()))
                                      for line in file]
                student_embedd = torch.tensor(student_embedd).clone().detach()
                # print(student_embedd)
                similarity = cosine_similarity(
                    face.cpu().numpy().reshape(1, -1),
                    student_embedd.unsqueeze(0).cpu().numpy().reshape(1, -1)
                )
                if similarity > max_similarity:
                    max_similarity = similarity
                    stuIndex = itemIndex

                itemIndex += 1
            if max_similarity > threshold:
                # print('vjp')
                # print(student_ids[stuIndex])
                FaceList['boxes'].append(boxes[faceIndex])
                FaceList['id'].append(student_ids[stuIndex])
                FaceList['name'].append(student_names[stuIndex])
                # print('veryvjp')
                AttenList = identify_cosine_similarity.CaculatePresent(
                    AttenList, student_ids[stuIndex], student_names[stuIndex])
                print(student_ids[stuIndex], student_names[stuIndex])
                print("Cosine Similarity:", max_similarity)
                attendentStudentsID.append(student_ids[stuIndex])
            else:
                FaceList['boxes'].append(boxes[faceIndex])
                FaceList['id'].append('')
                FaceList['name'].append('Unknown')

            faceIndex += 1
        path = identify_cosine_similarity.draw_boxes(FaceList,
                                                     classId,
                                                     slotId,
                                                     timeframes_id,
                                                     image_bin
                                                     )
        # print(" ================== attendentStudentsID ================== ")
        # print(attendentStudentsID)
        # print(" ================== path ================== ")
        # print(path)
        # print(" ================== AttenList ================== ")
        # print(AttenList)
        return path, attendentStudentsID


class LogListCreateView(generics.ListCreateAPIView):
    serializer_class = LogDetail

    def get_queryset(self):
        return Logs.objects.all()

    def get_attend_one_frame_queryset(self):
        key = self.kwargs.get('key')
        print(key)
        oneFrame_serializer = AttendentStudentsAtOneFrameSerializer
        return TimeFrame.objects.all()

    def perfome_create(self, serializer):
        if serializer.is_valid():
            return Response('oke', status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response('j z', status=status.HTTP_400_BAD_REQUEST)


# Connect to camera


class CameraHandle(generics.ListCreateAPIView):
    serializer_class = CameraInfor


# __________________ HA DJANGO ___________________________

# add Class

# def test():
#     # Initialize the camera
#     cap = cv2.VideoCapture(0)  # 0 is the default camera
#     img_counter = 0
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             print("failed to grab frame")
#             break
#         # Display the resulting frame
#         cv2.imshow('frame', frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             print("Quitting")
#             break
#         elif cv2.waitKey(1) & 0xFF == ord(' '):
#             img_name = "myPic_{}.png".format(img_counter)
#             cv2.imwrite(img_name, frame)
#             print("{} written".format(img_name))
#             img_counter += 1

#     # Release the capture and close the window
#     cap.release()
#     cv2.destroyAllWindows()


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
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)


def test_and_draw():
    data = post()
    # Print the received data
    print("Received boxes:", data['boxes'])
    print("Received embeddings shape:", [len(emb)
          for emb in data['embeddings']])

    # image = cv2.imread("myPic_0.png")
    # draw = cv2.imshow("test", image)

    # for box in data['boxes']:
    #     x1, x2, y1, y2 = box
    #     draw.rectangle([x1, y1, x2, y2], outline="red", width=2)


# test()
# test_and_draw()
