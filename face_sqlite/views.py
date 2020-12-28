import time

from django.shortcuts import render
import numpy as np
from django.http import JsonResponse, HttpResponse
import base64
import cv2

from face_sqlite.models import Face
from face_sqlite.face_tools.face_calss import Face_Tool


def echoRuntime(func):
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime)
        print(func.__name__ + " running time is %.2f s" % msecs)
        return result

    return wrapper


def test(request):
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        face_tool = Face_Tool()
        image = face_tool.read_face_img(frame)
        face_info_dict, img_result = face_tool.face_rec(image)

        cv2.imshow("src", img_result)
        cv2.waitKey(10)
    # return HttpResponse("success")
    return JsonResponse(result_dict)


def register(request):
    if (request.method == 'POST'):
        t0 = time.time()
        img_data = request.POST.get('image')  # 本质就是解码字符串
        work_id = request.POST.get('work_id')  # 本质就是解码字符串
        name = request.POST.get('name')  # 本质就是解码字符串
        tt = time.time()
        print("接收一张图片需要{}秒".format(tt - t0))
        # print(test_image)
        img_byte = base64.b64decode(img_data)
        img_np_arr = np.fromstring(img_byte, np.uint8)
        image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
        t1 = time.time()
        print("解码张图片需要{}秒".format(t1 - tt))
        # cv2.imwrite("./register.png", image)
        # t2 = time.time()
        # print("保存一张图片需要{}秒".format(t2 - t1))

        # image = "/home/db/bing/DjangoFaceRec/face_sqlite/face_tools/face.jpg"
        # image = "/home/db/bing/DjangoFaceRec/face_sqlite/face_tools/dubing0.jpg"
        face_tool = Face_Tool()
        image = face_tool.read_face_img(image)
        face_locations, face_encode_list = face_tool.face_encording(image)
        if face_locations != []:
            # face_encode_list[0] 为第一张人脸
            code = face_tool.face_register(name=name, work_id=work_id, face_encode_list=face_encode_list[0])
            # code = face_tool.face_register(name="小明", work_id="234", face_encode_list=face_encode_list[0])
            return HttpResponse("register!" + str(code))
        else:
            return HttpResponse("register!" + str(0))


def login(request):
    if (request.method == 'POST'):
        t0 = time.time()
        img_data = request.POST.get('image')  # 本质就是解码字符串
        tt = time.time()
        print("接收一张图片需要{}秒".format(tt - t0))
        # print(test_image)
        img_byte = base64.b64decode(img_data)
        img_np_arr = np.fromstring(img_byte, np.uint8)
        image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
        t1 = time.time()
        print("解码张图片需要{}秒".format(t1 - tt))
        cv2.imwrite("./login.png", image)
        t2 = time.time()
        print("保存一张图片需要{}秒".format(t2 - t1))

        # image = "/home/db/bing/DjangoFaceRec/face_sqlite/face_tools/face.jpg"
        face_tool = Face_Tool()
        image = face_tool.read_face_img(image)
        # result_dict, image_result = face_tool.face_rec(image=image)
        result_dict = face_tool.face_rec(image=image)
        print(result_dict)

        return JsonResponse(result_dict)
