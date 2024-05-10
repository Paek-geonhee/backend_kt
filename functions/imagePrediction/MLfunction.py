import os
import glob
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 이미지를 읽고 정규화하여 반환하는 함수
def read_image(file_path, img_height, img_width):
    image = cv2.imread(file_path)  # 이미지 읽기
    image = cv2.resize(image, (img_width, img_height))  # 이미지 크기 조정
    image = image.astype(np.float32) / 255.0  # 이미지 정규화
    return image

def predict_content_amount(model, image_path, img_height, img_width):
    # 이미지 전처리
    input_image = read_image(image_path, img_height, img_width)
    input_image = np.expand_dims(input_image, axis=0)  # 배치 차원 추가 (1, height, width, channels)

    # 모델 예측
    prediction = model.predict(input_image)

    # 예측 결과 반환 (0에서 100 사이 값으로 클리핑)
    content_amount = np.clip(prediction[0][0], 0, 100)
    return content_amount