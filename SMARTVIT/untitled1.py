# from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
# from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

import paho.mqtt.publish as publicare 
import random
import datetime
import glob
import json
# import cv2
import io
from time import sleep

### The MQTT Broker login details must be filled in instead of *********
MQTT_TOPIC = '**********'
MQTT_PATH = "**********"
MQTT_HOST = '**********'


# Load the model
model = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)



image_list = []

def image_to_mqtt():
    f=open("./asaved_leaf/leaf.jpg", "rb") #3.7kiB in same folder
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    
    publicare.single(MQTT_PATH, byteArr, hostname=MQTT_HOST)

def message():
    for filename in glob.glob('./static/uploads/*.jpg'):
         
        im=Image.open(filename)
        image_list.append(im)
        # im.show()
        
        size = (224, 224)
        image = ImageOps.fit(im, size, Image.ANTIALIAS)
        
        
        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array
        
        # run the inference
        prediction = model.predict(data)
        # print(prediction)
        
        downy = float(prediction[0][0])
        powdery = float(prediction[0][1])
        grot = float(prediction[0][2])
        healthy = float(prediction[0][3])
        
        d = datetime.datetime.now()
        date = d.strftime("%x")
        
        phase = 0
        m = int(d.strftime("%m"))
        if(m == 3): phase = 0
        elif(m == 4): phase = 1
        elif(m == 5): phase = 2
        elif(m == 6): phase = 4
        # print(phase)
        
        disease = ""
        
        x = max(downy, powdery, grot, healthy)
        if(x == downy): 
            disease = "Downy Mildew"
        elif(x == powdery): 
            disease = "Powdery Mildew"
        elif(x == grot): 
            disease = "Grey Rot"
        else: 
            disease = "Healthy"
            
        # print(disease)
        
        
        if(disease != "Healthy"):
            im.save('./asaved_leaf/leaf.jpg')
            image_to_mqtt()
                 
        
        payload_dict = {"Date": date,
                        "Disease": disease
            }
        
        print(payload_dict)
        
        # print(payload_dict)
        try: 
            publicare.single(MQTT_TOPIC,qos = 1,hostname = MQTT_HOST,payload = json.dumps(payload_dict)) 
        except: 
            pass
    
# message()