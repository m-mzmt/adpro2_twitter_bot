import cv2, sys, re

class Crop_Face:
    """
    class: Crop_Face
    cropping cat face
    """
    def __init__(self, files):
        self.files = files
        if files is None:
            print("select an image\n")
            return False


    def Crop_Face(self, img):
        if len(img) <= 1:
            print("no input file\n")

        image_file = img
        output_file = re.sub(r'\.jpg|jpeg|JPG|JPEG|png|PNG$', '-crop.jpg', image_file)

        cascade_file = "cat_cascade.xml"
        print("cascade file: " + cascade_file)

        image = cv2.imread(image_file)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cascade = cv2.CascadeClassifier(cascade_file)
        face_images = cascade.detectMultiScale(
            image_gray,
            scaleFactor=1.1,
            minNeighbors=1,
            minSize=(1, 1))

        if len(face_images) > 0:
            for (x, y, w, h) in face_images:
                face_image = image[y:y+h, x:x+w]
            cv2.imwrite(output_file, face_image)
            print(output_file)
