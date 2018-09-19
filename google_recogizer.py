import io
import os

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "json file's path"
client = vision.ImageAnnotatorClient()

img_list = os.listdir(os.getcwd())
for img in img_list:
    if img.endswith('.jpg'):
        img_path = os.path.join(os.path.abspath(os.getcwd()), img)
        file_name = os.path.join(
            os.path.dirname(__file__),img_path)
            #'img's path')
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print(img + "'s Labels:")
        for label in labels:
            print(label.description)
        print('\n')