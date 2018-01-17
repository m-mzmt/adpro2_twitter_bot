#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import urllib
import re

'''
:param タイムライン
:return 画像のリスト
'''
def image_save(timeline):
    date_name = re.split(' ', str(datetime.datetime.today()))[0] + '_'
    reply_images = []
    image_save_dir = './image/raw/'

    try:
        for i, img in enumerate(timeline.extended_entities['media']):
            reply_image = urllib.request.urlopen(img['media_url'])
            # ファイル名を確定後、リストに格納
            image_name = date_name + \
                str(timeline.id) + '-' + str(i) + '.jpg'
            reply_images.append(image_save_dir + image_name)
            # 画像を読み込んで保存
            image_file = open(image_save_dir + image_name, 'wb')
            image_file.write(reply_image.read())
            image_file.close()
            reply_image.close()
            print('画像 ' + image_name + ' を保存しました')

        return reply_images
    except AttributeError:
        return []

def reply(tweet_text, api, status):
    api.update_status(status=status.user.screen_name + " " + tweet_text, in_reply_to_status_id=status.id)
    print(tweet_text)


def tweet_result(name, api, status):
    cats = ["スフィンクス", "アビシニアン", "ベンガル", "バーマン",
            "ボンベイ", "ブリティッシュショートヘア", "エジプシャンマウ",
            "メインクーン", "ペルシャ", "ラグドール", "ロシアンブルー", "シャム"]
    cats_images = ["Sphynx.jpg", "Abyssinian.jpg", "Bengal.jpg", "Birman.jpg", "Bombay.jpg",
                   "British_Shorthair.jpg", "Egyptian_Mau.jpg", "Maine_Coon.jpg",
                   "Persian.jpg", "Ragdoll.jpg", "Russian_Blue.jpg", "Siamese.jpg"]

    tweet_text = " この猫は... " + cats[name] + " ですฅ(´・ω・｀)ฅにゃーん"

    media_images = ["/tmp/cat_face_64x64_0.jpg", "./cat_images/" + cats_images[name]]
    media_ids = [api.media_upload(i).media_id_string for i in media_images]
    api.update_status(status='@'+status.user.screen_name + tweet_text, in_reply_to_status_id=status.id, media_ids=media_ids)
    print(tweet_text)