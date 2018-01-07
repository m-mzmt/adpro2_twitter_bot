import glob
import cv2, sys, re


class Inflate_Image:
    """
    class: Inflate_Image
    画像データの水増し
    """
    def __init__(self, path):
        if path is None:
            print("select an image\n")
            return False
        self.path = path

    def Flip_horizontal(self):
        try:
            img = cv2.imread(self.path)
            flip_img = cv2.flip(img,1)
            output_file = str(self.path).replace("crop.jpg","crop-flip.jpg")
            cv2.imwrite(output_file, flip_img)
            print(output_file)
        except:
            return


if __name__ == '__main__':
    file_paths = glob.glob("./*crop.jpg")
    for path in file_paths:
        print(path)
        Inflate_Image(path).Flip_horizontal()
