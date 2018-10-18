#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import tweepy
import wget
import subprocess
import os, io
from google.cloud import vision
from google.cloud.vision import types

#Twitter authentication
consumer_key = "Your consumer key"
consumer_secret = "Your consumer secret"
access_token = "Your access token"
access_token_secret = "Your access token secret"

#Google authentication
jsonpath = "Your Google authentication json file's path" #Example: "/Users/user/Desktop/api_proj/92200.json"
imgpath = 'Your img path' #Example: '/Users/user/Desktop/api_proj/*.jpg'
    
def download_img(userid, pagenum):
    # If the page number is too large the api will show warning msg and shut down
    if (pagenum > 50):
        print("Warning, the pagenum is too large!")
        os._exit(0)       
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)#This section is for the authentication
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #If the Twitter isn't responding, the api will show warning msg and shut down
    try:
        tweets = api.user_timeline(id = userid, page = pagenum)
        image_link = []
    except:
        print("Twitter is not responding, please check your network!")
        os._exit(0)

    #Twitter's media entities are in the extended entities, this loop is to find the img url
    for tweet in tweets:
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            image_link.append(media[0]['media_url'])

    i = 1
    for image in image_link:#Download images from twitter
        print("Downloading image %s" %i)
        wget.download(image)
        print('\n')
        i += 1
        
#Since ffmepg api can only deal with images with the name of natural#, the img name needs to be changed
def rename_img(imgpath):
    img_list = os.listdir(imgpath)
    i = 0
    
    for img in img_list:
        if img.endswith('.jpg'):
            src = os.path.join(os.path.abspath(imgpath), img)
            dst = os.path.join(os.path.abspath(imgpath), format('img' + str(i), '0>3s') + '.jpg')
            os.rename(src, dst)
            i = i + 1

# Usually this part will find images in the current path directly
# If images search failed, please add correct path to the argument
def vedio_conv(path):
    os.system('ffmpeg -framerate 1/6 -i '+path+'/img%1d.jpg test.mp4')

def google_recognizer(jsonpath, imgpath):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= jsonpath#"/Users/yicunhou/Desktop/922004261583.json"
    client = vision.ImageAnnotatorClient()
    
    img_list = os.listdir(os.getcwd())
    for img in img_list:
        if img.endswith('.jpg'):
            ylb = 50
            img_path = os.path.join(os.path.abspath(os.getcwd()), img)
            file_name = os.path.join(
                os.path.dirname(__file__),img_path)
                #'imgpath')

            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            image = types.Image(content=content)
            
            try:
                response = client.label_detection(image=image)
                labels = response.label_annotations
            except:
                print("Google is not responding, please check your network!")
                os._exit(0)

            print(img + "'s Labels:")

            for label in labels:
                image = Image.open(img)
                # initialise the drawing context with
                # the image object as background
                draw = ImageDraw.Draw(image)
                # create font object with the font file and specify
                # desired size
                font = ImageFont.truetype('GillSans.ttc', size=45)
                # starting position of the message
                (x, y) = (50, ylb)
                message = label.description
                color = 'rgb(250, 250, 250)' # white color
                # draw the message on the background
                draw.text((x, y), message, fill=color, font=font)
                ylb = ylb + 50
                image.save(img)
                print(label.description)     
            print('\n')
    
def main():
    #You can change the page# to decide how many images to download
    #You can also change the username
    download_img('IKEAUSA', 10)
    path = os.getcwd()
    rename_img(path)
    vedio_conv(path)
    google_recognizer(jsonpath, imgpath)
    
if __name__ == '__main__':
    main()
