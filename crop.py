import cv2


'''
:param リプライで受け取った画像
:return 検出した顔の数

顔の画像を保存
'''

def crop_face(img):
    image = cv2.imread(img)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("cat_cascade.xml")
    face_images = cascade.detectMultiScale(image_gray, scaleFactor=1.1,
                                           minNeighbors=1, minSize=(1, 1))
    if len(face_images) > 0:
        for i, (x, y, w, h) in enumerate(face_images):
            face_image = image[y:y + h, x:x + w]
            cv2.imwrite('/tmp/cat_face_orig_' + str(i) + '.jpg', face_image)
            face_image = cv2.resize(face_image, (64, 64))
            cv2.imwrite("/tmp/cat_face_64x64_" + str(i) + ".jpg", face_image)
        return len(face_images)

    else:
        return 0