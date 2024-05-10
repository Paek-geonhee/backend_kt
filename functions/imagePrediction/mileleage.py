import os
import glob
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from functions.imagePrediction.MLfunction import *

masterPath = './functions/imagePrediction/'

def product(start_image, end_image):
    model = tf.keras.models.load_model(masterPath +'imagePrediction.h5')

    img_height = 128
    img_width = 128

    start_value = predict_content_amount(model, start_image, img_height, img_width)
    end_value = predict_content_amount(model, end_image, img_height, img_width)

    return end_value - start_value

# def product():
#     model = tf.keras.models.load_model(masterPath +'imagePrediction.h5')

    

#     image_path = masterPath + 'test/test2.jpg'
#     img_height = 128
#     img_width = 128
#     result1 = predict_content_amount(model, masterPath+'test.jpg', img_height, img_width)
#     result2 = predict_content_amount(model, masterPath+'test2.jpg', img_height, img_width)

#     print("Predicted Content1 Amount:", result1)
#     print("Predicted Content2 Amount:", result2)

# product()