#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import tweepy
import wget
import subprocess
import io, os, sys
from google.cloud import vision
from google.cloud.vision import types
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import pymysql
from pymongo import MongoClient

#Twitter authentication
consumer_key = "Your consumer key"
consumer_secret = "Your consumer secret"
access_token = "Your access token"
access_token_secret = "Your access token secret"

#Google authentication
jsonpath = "Your Google authentication json file's path" #Example: "/Users/user/Desktop/api_proj/92200.json"
imgpath = 'Your img path' #Example: '/Users/user/Desktop/api_proj/*.jpg'
objects = ""

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
                objects = objects+label.description+"\n"
                print(label.description)
            print('\n')

def mysql(name, twid, pagenum, imgpath, objects):
    con = pymysql.connect(host='localhost', user='root',
                      passwd='12345678', database='userinfo', charset='utf8')
    print('Connected to database')
    cur = con.cursor()
    sql = "INSERT INTO information (USERNAME, TWITTER_ID, PAGE_NUMBER, IMG_PATH, DESCRIPTOR) VALUES (%s, %s, %s, %s, %s)"
    val = (name, twid, pagenum, imgpath, objects)
    cur.execute(sql, val)
    con.commit()
    cur.close()
    print('Backup finished')
    con.close()

def mogodb(name, twid, pagenum, imgpath, objects):
    conn = MongoClient('localhost',27017)
    db = conn.USERINFO
    db.users.insert({"USERNAME":name, 'TWITTER_ID':twid, 'PAGE_NUM':pagenum, 'IMG_PATH': imgpath, 'OBJECTS': objects})

def checkmog():
    y = "1"
    while y == "1":
        print("- Manage my MongoDB\n* Press 1 for specific search\n* Presss 2 for collective results\n* Press any key else to exit")
        op = input()
        if op == "1":
            print("* Please input column(ex. USERNAME)")
            cl = input()
            print("* Please input content(ex. Lucy)")
            ct = input()
            conn = MongoClient('localhost',27017)
            db = conn.USERINFO
            collection = db.users
            results = collection.find({cl: ct})
            for result in results:
                print(result)
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()

        elif op == "2":
            conn = MongoClient('localhost',27017)
            db = conn.USERINFO
            collection = db.users
            results = collection.find({'PAGE_NUM':{'$gt':0}})
            i = 0
            for result in results:
                pn = result['PAGE_NUM']
                pn = pn + pn
                i = i + 1
            print("- Number of images per feed: ", pn/i)
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()
        else:
            break
            
def main():

    #You can change the page# to decide how many images to download
    #You can also change the username
    print("Please input your username:")
    name = input()
    print("Please input the Twitter ID you want to check:")
    twid = input()
    print("Please input the number of twitters you want to check:")
    num = int(input())
    download_img(twid, num)
    path = os.getcwd()
    rename_img(path)
    google_recognizer(jsonpath, imgpath)
    vedio_conv(path)
    database(name, twid, num, imgpath, objects)
    print("Api demo finished, thanks!")
    
if __name__ == '__main__':
    main()
