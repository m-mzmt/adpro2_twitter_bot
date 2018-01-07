#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import datetime
import urllib
import cv2
import re

from chainer import datasets
from chainer import serializers

import chainer_MyModel as Model

# ファイル APIKey(text形式) よりIDと各キーを読み込む
api_key = open('APIKey', 'r').read()

# Twitterオブジェクトの生成
bot_user_name = api_key.split('\n')[0]
auth = tweepy.OAuthHandler(api_key.split('\n')[1], api_key.split('\n')[2])
auth.set_access_token(api_key.split('\n')[3], api_key.split('\n')[4])
api = tweepy.API(auth)


def main():
    listener = Listener()
    stream = tweepy.Stream(auth, listener)
    stream.userstream()


class Listener(tweepy.StreamListener):

    def __init__(self):
        super(Listener, self).__init__()
        self.model = Model.MyModel()
        serializers.load_npz('model_epoch', self.model)

    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)

        # リプライが来た場合
        if str(status.in_reply_to_screen_name) == bot_user_name:

            # テキストメッセージ
            tweet_text = "@" + str(status.user.screen_name) + " "

            # タイムラインを取得
            time_line = api.mentions_timeline()

            # タイムラインの先頭のメッセージ内容
            print("リプライが届きました...\n[@"+status.user.screen_name+"]\n"+time_line[0].text+"\n")

            # ファイル名の先頭
            date_name = re.split(' ', str(datetime.datetime.today()))[0] + '_'

            # 1.リプライ画像の保存 -> 2.顔を切り取りcat.jpgで保存 -> 3.chainerに通して判定

            # 1.リプライ画像の保存
            try:
                j = 0
                reply_images = []
                for img in time_line[0].extended_entities['media']:
                    # print(img['media_url'])
                    reply_image = urllib.request.urlopen(img['media_url'])
                    # ファイル名を確定後、リストに格納
                    image_name = date_name + str(time_line[0].id) + '-' + str(j) + '.jpg'
                    reply_images.append(image_name)
                    # 画像を読み込んで保存
                    image_file = open(image_name, 'wb')
                    image_file.write(reply_image.read())
                    image_file.close()
                    reply_image.close()
                    print('画像 ' + image_name + ' を保存しました')
                    j = j + 1
            except:
                # 例外処理
                if j == 0:
                    tweet_text += "Error:画像がありませんฅ(´・ω・｀)ฅにゃーん"
                else:
                    tweet_text += "Error:画像の保存に失敗しましたฅ(´・ω・｀)ฅにゃーん"
                api.update_status(status=tweet_text, in_reply_to_status_id=status.id)
                print(tweet_text)
                return True

            # 2.顔を切り取りcat.jpgで保存
            try:
                image = cv2.imread(reply_images[0])
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cascade = cv2.CascadeClassifier("cat_cascade.xml")
                face_images = cascade.detectMultiScale(image_gray, scaleFactor=1.1,
                                                       minNeighbors=1, minSize=(1, 1))
                face_image_len = 0
                if len(face_images) > 0:
                    for (x, y, w, h) in face_images:
                        face_image = image[y:y + h, x:x + w]
                        if face_image_len < w:
                            face_image_len = w
                            cv2.imwrite("cat_face.jpg", face_image)
                            face_image = cv2.resize(face_image, (64, 64))
                            cv2.imwrite("cat_face_min.jpg", face_image)
                else:
                    tweet_text += "Error:猫の顔が検出できませんでした...ฅ(´・ω・｀)ฅにゃーん"
                    api.update_status(status=tweet_text, in_reply_to_status_id=status.id)
                    print(tweet_text)
                    return True
            except:
                tweet_text += "Error:猫の顔の検出に失敗しました...ฅ(´・ω・｀)ฅにゃーん"
                api.update_status(status=tweet_text, in_reply_to_status_id=status.id)
                print(tweet_text)
                return True

            # 3.chainerに通して判定
            try:
                data = [('cat_face_min.jpg', 3), ('cat_face_min.jpg', 3)]
                d = datasets.LabeledImageDataset(data)

                def transform(data):
                    img, lable = data
                    img = img / 255.
                    return img, lable

                d = datasets.TransformDataset(d, transform)

                train, test = datasets.split_dataset(d, 1)
                x, t = test[0]
                x = x[None, ...]
                y = self.model(x)
                y = y.data

                cats = ["スフィンクス", "アビシニアン", "ベンガル", "バーマン",
                        "ボンベイ", "ブリティッシュショートヘア", "エジプシャンマウ",
                        "メインクーン", "ペルシャ", "ラグドール", "ロシアンブルー", "シャム"]
                cats_images = ["Sphynx.jpg", "Abyssinian.jpg", "Bengal.jpg", "Birman.jpg", "Bombay.jpg",
                              "British_Shorthair.jpg", "Egyptian_Mau.jpg", "Maine_Coon.jpg",
                              "Persian.jpg", "Ragdoll.jpg", "Russian_Blue.jpg", "Siamese.jpg"]

                tweet_text += "この猫は... " + cats[y.argmax(axis=1)[0]] + " ですฅ(´・ω・｀)ฅにゃーん"

                media_images = ["cat_face.jpg", "./cat_images/"+cats_images[y.argmax(axis=1)[0]]]
                media_ids = [api.media_upload(i).media_id_string for i in media_images]
                api.update_status(status=tweet_text, in_reply_to_status_id=status.id, media_ids=media_ids)
                print(tweet_text)
                return True

            except:
                tweet_text += "Error:猫の顔の判定に失敗しました...ฅ(´・ω・｀)ฅにゃーん"
                api.update_status(status=tweet_text, in_reply_to_status_id=status.id)
                print(tweet_text)
                return True

        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


if __name__ == '__main__':
    print("\n -=-=- OK -=-=- \n")
    main()
