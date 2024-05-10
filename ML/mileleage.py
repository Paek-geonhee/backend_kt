import tensorflow as tf
import cv2
import numpy as np

IMG_HEIGHT = 128
IMG_WIDTH = 128

def preprocess_image(image_path, img_height, img_width):
    # 이미지 로드 및 전처리
    image = cv2.imread(image_path)  # 이미지 로드
    image = cv2.resize(image, (img_width, img_height))  # 이미지 크기 조정
    image = image.astype(np.float32) / 255.0  # 이미지 정규화
    return image

def predict_content_amount(model, image_path, img_height, img_width):
    # 이미지 전처리
    input_image = preprocess_image(image_path, img_height, img_width)
    input_image = np.expand_dims(input_image, axis=0)  # 배치 차원 추가 (1, height, width, channels)
    # 모델 예측
    prediction = model.predict(input_image)

    # 예측 결과 반환 (0에서 100 사이 값으로 클리핑)
    content_amount = np.clip(prediction[0][0], 0, 100)
    return content_amount

def preprocess_image_np(image_np, img_height, img_width):
    # 이미지 로드 및 전처리
    image = cv2.resize(image_np, (img_width, img_height))  # 이미지 크기 조정
    image = image.astype(np.float32) / 255.0  # 이미지 정규화
    return image


def predict_content_amount_np(model, image_np, img_height, img_width):
    # 이미지 전처리
    input_image = preprocess_image_np(image_np, img_height, img_width)
    input_image = np.expand_dims(input_image, axis=0)  # 배치 차원 추가 (1, height, width, channels)
    # 모델 예측
    prediction = model.predict(input_image)

    # 예측 결과 반환 (0에서 100 사이 값으로 클리핑)
    content_amount = np.clip(prediction[0][0], 0, 100)
    return content_amount

def product_double(start_img, end_img):
    model = tf.keras.models.load_model('./ML/prediction_model.h5')


    start_value = predict_content_amount(model, start_img, IMG_HEIGHT, IMG_WIDTH)
    end_value = predict_content_amount(model, end_img, IMG_HEIGHT, IMG_WIDTH)

    return abs(end_value - start_value)

def product(img):
    model = tf.keras.models.load_model('./ML/prediction_model.h5')
    return predict_content_amount(model, img, IMG_HEIGHT, IMG_WIDTH)

