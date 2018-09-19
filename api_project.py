#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import tweepy
import wget
import subprocess
import os

consumer_key = "3NaLT71Ac76C9JH6tf5YYKXJr"
consumer_secret = "iHQeyLQMQBdROGTzWDtmPZAcIGbdAKCG44TnaJgFVwW8HXlZLr"
access_token = "3895743257-Ai6TaeldDTIu22YA4w6m9lFne54aejVwoIdBqDh"
access_token_secret = "5GOWjN7i2bOVKP1k56pC5NdBYnNkQcdlG231fOWcNzrNA"

def download_img():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = api.user_timeline(id = "IKEAUSA", page = 10)
    image_link = []

    for tweet in tweets:
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            image_link.append(media[0]['media_url'])

    i = 1
    for image in image_link:
        print("Downloading image %s" %i)
        wget.download(image)
        print('\n')
        i += 1

def rename_img(imgpath):
    img_list = os.listdir(imgpath)
    i = 0
    
    for img in img_list:
        if img.endswith('.jpg'):
            src = os.path.join(os.path.abspath(imgpath), img)
            dst = os.path.join(os.path.abspath(imgpath), format('img' + str(i), '0>3s') + '.jpg')
            os.rename(src, dst)
            i = i + 1

def vedio_conv(path):
    os.system('ffmpeg -framerate 1/6 -i '+path+'/img%1d.jpg test.mp4')
    
def main():
    download_img()
    path = os.getcwd()
    rename_img(path)
    vedio_conv(path)

if __name__ == '__main__':
    main()
