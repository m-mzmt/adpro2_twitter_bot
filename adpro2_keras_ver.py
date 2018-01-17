#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import datetime
import numpy as np
from PIL import Image


from Twitter.twitter_util import image_save, reply, tweet_result
from cat_classifier_keras import classifier

from crop import crop_face

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

    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)
        # リプライが来た場合
        if str(status.in_reply_to_screen_name) == bot_user_name:
            # テキストメッセージ
            # タイムラインを取得
            time_line = api.mentions_timeline()
            # タイムラインの先頭のメッセージ内容
            print("リプライが届きました...\n[@"+status.user.screen_name+"]\n"+time_line[0].text+"\n")


            # 1.リプライ画像の保存 -> 2.顔を切り取りcat.jpgで保存 -> 3.chainerに通して判定

            # 1.リプライ画像の保存

            reply_images = image_save(time_line[0])
            if len(reply_images) == 0:
                reply(api=api, tweet_text='Error:画像がありませんฅ(´・ω・｀)ฅにゃーん', status=status)
                return True

            # 2.顔を切り取りcat.jpgで保存
            # TODO: 複数枚の画像に対応、複数匹写ってた場合の処理

            # 1枚ずつ処理してく
            for i, image in enumerate(reply_images):
                result = crop_face(image)
                print(str(i+1) + "枚目: " + str(result) + "匹検出")
                if result > 0:
                    # 学習処理
                    for j in range(result):
                        img = Image.open('/tmp/cat_face_64x64_' + str(j) + '.jpg')
                        img = img.convert("RGB")
                        cats_name = classifier(np.array(np.asarray(img)))

                        # 複数匹処理
                        # TODO: リプライに添付するクロップ画像のファイルパス修正
                        tweet_result(name=cats_name.argmax(), api=api, status=status)
                else:
                    reply(api=api, tweet_text="Error:猫の顔が検出できませんでした...ฅ(´・ω・｀)ฅにゃーん", status=status)
                    return True

            return True

    def on_error(self, status_code):
        if status_code == 420:
            print('API limit exceeded')
            return False
        else:
            print('Got an error with status code: ' + str(status_code))
            return False

    def on_timeout(self):
        print('Timeout...')
        return False


if __name__ == '__main__':
    print("\n -=-=- OK -=-=- \n")
    main()
