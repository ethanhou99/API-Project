# api_proj

## Abstract

This project aims to download images from a specific user on Twitter. Once the images are downloaded the ffmepg api will
convert these photos into a mp4 vedio and the Google api will recognize what stuff are on the images.


## Instruction

The main code is called 'api_project.py' in the master branch. You need to type in your authentication keys on the top and
you can also type in the username of your target. To use the Google API, please make sure the authentication-json-file's path
is typed in the function 'google_recognizer()'. You also need to enter the images' relative path in the google_recognizer().


## Branches

* This API contains three branches: master, ffmepg and googleapi. 
* The final code is in the master branch and the rest branches are for the development.

### Database Branch
* On 11/24/2018 the Mysql database function is added to this API.
* On 11/25/2018 the MongoDB database function is added to this API.

## Result

There are some result example under the folder of 'api_proj/photo-vedio/', like:
![image](https://github.com/ethanhou99/api_proj/blob/master/photo-vedio/img8.jpg)

![image](https://github.com/ethanhou99/api_proj/blob/master/photo-vedio/img9.jpg)

If you have any questions please feel free to contact me.
