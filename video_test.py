import cv2

cap = cv2.VideoCapture(0)
while 1:
    ret, frame = cap.read()
    # face_tool = Face_Tool()
    # image = face_tool.read_face_img(frame)
    # face_info_dict, img_result = face_tool.face_rec(image)

    cv2.imshow("src", frame)
    cv2.waitKey(10)