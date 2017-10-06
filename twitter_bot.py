#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import datetime
import urllib
import re
from PIL import Image
import numpy as np

import ImageConverter

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

    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)

        # リプライが来た場合
        if str(status.in_reply_to_screen_name) == bot_user_name:

            # テキストメッセージ
            tweet_text = "@" + str(status.user.screen_name) + " "
            tweet_text += "Hello！\n" + str(datetime.datetime.today())

            # タイムラインを取得
            time_line = api.mentions_timeline()

            # タイムラインの先頭のメッセージ内容
            print("リプライが届きました...\n[@"+status.user.screen_name+"]\n"+time_line[0].text+"\n")

            # ファイル名の先頭
            date_name = re.split(' ', str(datetime.datetime.today()))[0] + '_'

            # リプライ画像の保存
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
            # 例外処理
            except:
                if j == 0:
                    print('Error:画像がありません')
                else:
                    print('Error:画像の保存に失敗しました')

            print(reply_images)

            # 画像の変換をし、変換後のファイル名をリストで渡す
            converter = ImageConverter.ImageConverter(reply_images)
            convert_images = converter.invert_color()

            # 添付する画像を指定
            print(convert_images)
            media_ids = [api.media_upload(i).media_id_string for i in convert_images]
            print(tweet_text)
            api.update_status(status=tweet_text, in_reply_to_status_id=status.id, media_ids=media_ids)
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
