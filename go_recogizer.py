import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/yicunhou/Desktop/api_proj/922004261583.json"
# Instantiates a client
client = vision.ImageAnnotatorClient()

img_list = os.listdir(os.getcwd())
for img in img_list:
    if img.endswith('.jpg'):
        img_path = os.path.join(os.path.abspath(os.getcwd()), img)

        # The name of the image file to annotate
        file_name = os.path.join(
            os.path.dirname(__file__),img_path)
            #'/Users/yicunhou/Desktop/api_proj/img11.jpg')

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print(img + "'s Labels:")
        for label in labels:
            print(label.description)
        print('\n')