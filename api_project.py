#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import tweepy
import wget
import subprocess
import os, io
from google.cloud import vision
from google.cloud.vision import types

consumer_key = "Your consumer key"
consumer_secret = "Your consumer secret"
access_token = "Your access token"
access_token_secret = "Your access token secret"

def download_img():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)#This section is for the authentication
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = api.user_timeline(id = "IKEAUSA", page = 10)#You can change the page# to decide how many images to download
    image_link = []

    for tweet in tweets:#Twitter's media entities are in the extended entities, this loop is to find the img url
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            image_link.append(media[0]['media_url'])

    i = 1
    for image in image_link:#Download images from twitter
        print("Downloading image %s" %i)
        wget.download(image)
        print('\n')
        i += 1

def rename_img(imgpath): #Since ffmepg api can only deal with images with the name of natural#, the img name needs to be changed
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
