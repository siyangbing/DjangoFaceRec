import os
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from face_sqlite import face_recognition
from face_sqlite.models import Face


def echoRuntime(func):
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime)
        print(func.__name__ + " running time is %.2f s" % msecs)
        return result

    return wrapper


class Face_Tool():
    def __init__(self):
        pass

    def read_face_img(self, image):
        try:
            image = cv2.imread(image)
        except:
            pass
        # Resize frame of video to 1/4 size for faster face recognition processing
        # image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        image = image[:, :, ::-1]
        return image

    def face_detect(self, image):
        pass

    def face_key_point(self, image):
        face_landmarks_list = face_recognition.face_landmarks(image)

    @echoRuntime
    def face_encording(self, image):
        # A list of tuples of found face locations  (top, right, bottom, left) order
        t0 = time.time()
        face_locations = face_recognition.face_locations(image, model="hog")
        print("找到人脸需要时间: {}".format(time.time() - t0))
        if face_locations:
            t0 = time.time()
            face_encodings = face_recognition.face_encodings(image, face_locations)
            print("编码人脸需要: {}".format(time.time() - t0))

            img_w = image.shape[1]
            img_h = image.shape[0]
            # A list of tuples of found face locations  (left，top, right, bottom) order
            face_locations_rate = [(x[3] / img_w, x[0] / img_h, x[1] / img_w, x[2] / img_h) for x in face_locations]

            # p1 = (int(face_locations_rate[0][0]*500),int(face_locations_rate[0][1]*667))
            # p2 = (int(face_locations_rate[0][2]*500), int(face_locations_rate[0][3]*667))
            #
            # image = image[:, :, ::-1]
            # cv2.rectangle(image,p1,p2,(255,255,255),thickness=1)
            # cv2.imshow("asdf",image)
            # cv2.waitKey(0)
        else:
            face_locations_rate = []
            face_encodings = []
        return face_locations_rate, face_encodings

    @echoRuntime
    def face_register(self, name, work_id, face_encode_list):
        face_encode_str = self.to_str(face_encode_list)
        face = Face(name=name, work_id=work_id, face_encode_str=face_encode_str)
        user_info = Face.objects.filter(work_id=work_id)
        if len(user_info) == 0:
            face.save()
            code = 200
            print("成功注册用户！用户名：{} work_id: {}".format(name, work_id))
        else:
            code = 0
            print("用户work_id已经存在，请换一个id ！")
        return code

    def face_delete(self, work_id):
        user_info = Face.objects.filter(work_id=work_id)
        if len(user_info) == 0:
            code = 0
            print("删除失败，用户不存在！")
        else:
            user_info.delete()
            code = 200
            print("删除成功！")
        return code

    @echoRuntime
    def face_rec(self, image):
        face_locations_rate, face_encodings = self.face_encording(image)
        if face_locations_rate:
            # face_encode_str = Face.objects.values( "face_encode_str")
            all_face_data = Face.objects.values("face_encode_str")
            encoding_database_str_list = [x["face_encode_str"] for x in all_face_data]
            encoding_database_list = self.to_list(encoding_database_str_list)

            # matches = face_recognition.compare_faces(encoding_database_list, face_encodings[0])
            face_distances = face_recognition.face_distance(encoding_database_list, face_encodings[0])
            best_match_index = np.argmin(face_distances)
            # image = image[:, :, ::-1]
            if face_distances[best_match_index] < 0.6:
                best_face_encode = encoding_database_str_list[best_match_index]
                face_encode_str = Face.objects.filter(face_encode_str=best_face_encode).values("name", 'work_id')
                name = face_encode_str[0]['name']
                work_id = face_encode_str[0]['work_id']
                location = face_locations_rate[0]
                code = 200
                # img_result = self.draw_box(image, location, name)
            else:
                name = ''
                work_id = ''
                location = ''
                code = 0
                # img_result = image[:, :, ::-1]

            face_info_dict = {"code": code,
                              "name": name,
                              "work_id": work_id,
                              'location': location}

        else:
            face_info_dict = {"code": 0,
                              "name": "",
                              "work_id": "",
                              'location': ""}
            # img_result = image[:, :, ::-1]
        # cv2.imwrite("draw.jpg", img_result)

        return face_info_dict
        # return face_info_dict,img_result

    # 　把浮点列表转换为字符列表
    def to_str(self, list_float):
        str_encoding = ''
        for x in range(128):
            str_encoding += str(list_float[x]) + ','
        return str_encoding

    # 把字符列表转换为浮点列表
    @echoRuntime
    def to_list(self, result):
        list_encode = [x for x in result]
        list_str = [(x.split(',')[:-1]) for x in list_encode]
        str_array = list(map(self.to_float, list_str))
        return str_array

    def to_float(self, list1):
        return list(map(float, list1))

    def draw_box(self, image, boxes, name):

        img_w = image.shape[1]
        img_h = image.shape[0]
        p1 = (int(boxes[0] * img_w), int(boxes[1] * img_h))
        p2 = (int(boxes[2] * img_w), int(boxes[3] * img_h))

        image = image[:, :, ::-1]

        cv2.rectangle(image, p1, p2, (255, 0, 255), 1)
        cv2.putText(image, name, (p1[0], p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        return image


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        face_tool = Face_Tool()
        image = face_tool.read_face_img(image)
        face_info_dict, img_result = face_tool.face_rec(image)
        cv2.imshow("src", img_result)
        cv2.waitKey(1)

        a = 3
