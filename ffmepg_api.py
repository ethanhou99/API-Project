#!/usr/bin/env python3.6.6
# encoding: utf-8
#Author - Yicun Hou

import wget
import subprocess
import io, os

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
    path = os.getcwd()
    rename_img(path)
    vedio_conv(path)

if __name__ == '__main__':
    main()