import cv2, sys, re

def Crop_Face(img):
    if len(img) <= 1:
        print("no input file\n")

    image_file = img

    cascade_file = "cat_cascade.xml"
    print("cascade file: " + cascade_file)

    image = cv2.imread(image_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    face_images = cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(30, 30)
        )

    print(face_images)
    if len(face_images) > 0:
        for i, (x, y, w, h) in enumerate(face_images):
            face_image = image[y:y+h, x:x+w]
            output_file = re.sub(r'\.jpg|jpeg|JPG|JPEG|png|PNG$', '-'+str(i)+'-crop.jpg', image_file)
            cv2.imwrite(output_file, face_image)
            print(output_file)

    else:
        print("猫は写ってないみたいだにゃー(ΦωΦ)\n")
        return False
