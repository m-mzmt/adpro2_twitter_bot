import glob
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
        output_file = output_file.replace("./","./crop/")
        cascade_file = "cat_cascade.xml"
        print("cascade file: " + cascade_file)

        try:
            image = cv2.imread(image_file)        
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(cascade_file)
            face_images = cascade.detectMultiScale(image_gray,
                                                   scaleFactor=1.1,
                                                   minNeighbors=1,
                                                   minSize=(1, 1))
            print(face_images)
            image_len=0
            if len(face_images) > 0:
                for (x, y, w, h) in face_images:
                    face_image = image[y:y+h, x:x+w]
                    if image_len < w:
                        image_len = w
                        face_image = cv2.resize(face_image,(64,64))
                        print(output_file)
                        cv2.imwrite(output_file, face_image)
        except:
            return


if __name__ == '__main__':
    filepaths = glob.glob("./*.jpg")
    for p in filepaths:
        print(p)
        Crop_Face(p).Crop_Face(p)
