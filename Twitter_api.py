#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import tweepy
import wget
import subprocess
import os

consumer_key = "Your consumer_key"
consumer_secret = "Your consumer_secret "
access_token = "Your access_token"
access_token_secret = "Your access_token_secret"

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

def main():
    download_img()

if __name__ == '__main__':
    main()