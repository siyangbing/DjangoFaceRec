# -*-coding:utf-8-*-

import os
import time

import requests
import cv2
import base64
from DjangoFaceRec.settings import BASE_DIR

# img = cv2.imread(os.path.join(BASE_DIR, "test_face/face.jpg"))
img = cv2.imread(os.path.join(BASE_DIR, "test_face/db.jpg"))

data = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

url_fangfeizuocang = 'http://192.168.3.174:8000/face_rec/login/'
index = 0

# base64_text = aa
# print(r.content.decode("utf-8"))
name = "eu"
work_id = 111
register_dict = {"name":name,
                 "image":data,
                 'work_id':work_id}

while True:
    r = requests.post(url_fangfeizuocang, data=register_dict)
    # r_tongdianzuocang = requests.post(url_tongdianzuocang, data={'image': data_tongdianzuocang})

    # print(r.content)
    print(r.content.decode("utf-8"))
    # print(r_tongdianzuocang.content.decode("utf-8"))
    # requests.get(url_kaiguandeng,params=data)
    # time.sleep(1)
    index = index + 1
    # requests.post(url_shiziluoding, data=data_642)
    # print(index)

    # break
    # time.sleep(1)
