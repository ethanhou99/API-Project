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
import operator
from collections import Counter

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
    if (pagenum > 50):
        print("Warning, the pagenum is too large!")
        os._exit(0)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        tweets = api.user_timeline(id = userid, page = pagenum)
        image_link = []
    except:
        print("Twitter is not responding, please check your network!")
        os._exit(0)

    for tweet in tweets:
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            image_link.append(media[0]['media_url'])
    
    if (image_link == []):
        print("No image found in the first " + str(pagenum) +" pages")
        os._exit(0)
    
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
    print(path)
    os.system('ffmpeg -framerate 1/6 -i '+path+'/img%1d.jpg test.mp4')

def google_recognizer(jsonpath, imgpath):
    global objects
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
                objects = objects+label.description+" "
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

def sqlsearch(cont):
    db= pymysql.connect(host='localhost', user='root',
                    passwd='12345678', database='userinfo', charset='utf8')
    cur = db.cursor()  
    sql = "select * from information WHERE DESCRIPTOR LIKE " + "'" + cont +"%'"
    try:  
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            uid = row[0]
            utime = row[1]
            uname = row[2]
            utid = row[3]
            upgnum = row[4]
            upath = row[5]
            uob = row[6]
            print(uname,uob)
    except Exception as e:
        print("Exception occured, please check your input.")
        raise e  
    finally:  
        db.close()

def sqlave():
    db= pymysql.connect(host='localhost', user='root',
                    passwd='12345678', database='userinfo', charset='utf8')
    cur = db.cursor()  
    sql = "select PAGE_NUMBER from information"
    i = 0
    upgnum = 0
    try:  
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            upgnum = upgnum + row[0]
            i = i + 1
        print("Number of images per feed: ", upgnum//i)

    except Exception as e:
        print("Exception occured, please check your input.")
        raise e  
    finally:  
        db.close()

def mongopop():
    conn = MongoClient('localhost',27017)
    mydb = conn["USERINFO"]
    mycol = mydb["users"]
    obls = []
    for x in mycol.find({},{ "_id": 0, "OBJECTS": 1 }):
        cont = x["OBJECTS"].split(" ")
        obls = obls + cont
        obdic = sorted(Counter(obls).items(), key=operator.itemgetter(1))
    print("- The most popular descriptor is: ", obdic[-1][0])
    print("- It shows "+ str(obdic[-1][1])+" times")

def sqlpop():
    db= pymysql.connect(host='localhost', user='root',
                    passwd='12345678', database='userinfo', charset='utf8')
    cur = db.cursor()  
    sql = "select DESCRIPTOR from information"
    obls = ""
    try:  
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            obls = obls + row[0]
        obls = sorted(Counter(obls.split(" ")).items(), key=operator.itemgetter(1))
        print("- The most popular descriptor is: ", obls[-1][0])
        print("- It shows "+ str(obls[-1][1])+" times")
    except Exception as e:
        print("Exception occured, please check your input.")
        raise e  
    finally:  
        db.close()

def checkmysql():
    y = "1"
    while y == "1":
        print("- Manage MySQL\n* Press 1 for specific search\n* Presss 2 for collective results\n* Press 3 to check the most popular descriptor\n* Press any key else to exit")
        op = input()
        if op == "1":
            print("* Please input content(ex. clothes)")
            content = input()
            sqlsearch(content)
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()
        elif op == "2":
            sqlave()
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()
        elif op == "3":
            sqlpop()
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()
        else:
            break

def checkmog():
    y = "1"
    while y == "1":
        print("- Manage my MongoDB\n* Press 1 for specific search\n* Presss 2 for collective results\n* Press 3 to check the most popular descriptor\n* Press any key else to exit")
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
        elif op == "3":
            mongopop()
            print("* Press 1 to restart\n* Press any key else to exit")
            y = input()
        else:
            break

def main():

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
    #vedio_conv(path)
    mysql(name, twid, num, imgpath, objects)
    mogodb(name, twid, num, imgpath, objects)
    print("- Record uploaded to database successfully.\n* Press 1 to check MySQL\n* Press 2 to check MongoDB\n* Press any key else to exit")
    op = input()
    if op == "1":
        checkmysql()
    elif op == "2":
        checkmog()
    else:
        pass

    print("Api demo finished, thanks!")
    
if __name__ == '__main__':
    main()
