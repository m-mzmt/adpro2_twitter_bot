#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import re
from PIL import Image
import numpy as np


class ImageConverter:
    """ 画像変換クラス """
    def __init__(self,files=[]):
        # コンストラクタ
        self.files = files
        if self.files is None:
            print("Error:file is empty")
            return False

    def invert_color(self):
        """ 画像の色を反転して保存 """
        print("\nImageConverter invert_color : 色の反転\n")

        try:
            convert_images = []
            for image_name in self.files:

                reply_image = Image.open(image_name)
                width, height = reply_image.size
                new_image = Image.new('RGB', (width, height))
                img_pixels = np.array([[reply_image.getpixel((x, y)) for x in range(width)] for y in range(height)])

                # 色を反転する
                reverse_color_pixels = 255 - img_pixels
                for y in range(height):
                    for x in range(width):
                        # 反転した色の画像を作成する
                        r, g, b = reverse_color_pixels[y][x]
                        new_image.putpixel((x, y), (r, g, b))

                # 変換後のファイル名を決定し保存
                convert_image_name = image_name.replace(".", "_invert_color.", 1)
                new_image.save(convert_image_name)
                convert_images.append(convert_image_name)
                print('画像 ' + image_name + ' を変換し ' + convert_image_name + ' を保存しました')

        except SyntaxError:
            print('Error:SyntaxError')
        except not SyntaxError:
            print('Error:画像の変換に失敗しました')

        return convert_images