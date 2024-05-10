import os
import glob
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from MLfunction import *

import re

def extract_integer_from_filename(file_path):
    # 파일 경로에서 파일 이름 추출
    file_name = file_path.split('\\')[-1]  # 파일 경로에서 마지막 부분을 파일 이름으로 추출 (Windows 환경)

    # 파일 이름에서 ','와 '.' 사이에 있는 정수 값을 추출하여 반환
    match = re.search(r',(\d+)\.', file_name)  # ','와 '.' 사이에 있는 숫자 패턴 검색
    if match:
        integer_value = int(match.group(1))  # 검색된 정수 값 추출
        return integer_value
    else:
        return None  # 정수 값을 찾지 못한 경우 None 반환

# 주어진 파일 경로 리스트에서 정수 값을 추출하여 리스트로 반환
def extract_integers_from_file_paths(file_paths):
    extracted_values = []
    for file_path in file_paths:
        integer_value = extract_integer_from_filename(file_path)
        if integer_value is not None:
            extracted_values.append(integer_value)
    return extracted_values



# 디렉토리 내의 모든 JPEG 파일 찾기
def find_jpeg_files(directory):
    search_pattern = os.path.join(directory, '*.jpg')  # 디렉토리 내의 모든 .jpeg 파일 검색
    jpeg_files = glob.glob(search_pattern)
    return jpeg_files



# 데이터 생성기 함수 (이미지 파일 경로와 정답 리스트를 입력으로 받아서 배치 데이터를 생성)
def data_generator(image_files, labels, batch_size, img_height, img_width):
    num_samples = len(image_files)
    if num_samples < batch_size:
            raise ValueError("Dataset size is smaller than batch size. Consider resizing dataset or reducing batch size.")

    while True:
        indices = np.random.choice(num_samples, batch_size, replace=False)  # 무작위 인덱스 선택
        batch_images = []
        batch_labels = []
        for idx in indices:
            image = read_image(image_files[idx], img_height, img_width)
            label = labels[idx]
            batch_images.append(image)
            batch_labels.append(label)
        yield np.array(batch_images), np.array(batch_labels)

# 모델 정의
def create_model(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='linear')  # Regression을 위한 출력층 (내용물의 양)
    ])
    return model


def preprocess_image(image_path, img_height, img_width):
    # 이미지 로드 및 전처리
    image = cv2.imread(image_path)  # 이미지 로드
    image = cv2.resize(image, (img_width, img_height))  # 이미지 크기 조정
    image = image.astype(np.float32) / 255.0  # 이미지 정규화
    return image

# 메인 함수
def main():
    masterPath = './functions/imagePrediction/'

    # 데이터셋 디렉토리 경로
    dataset_dir = masterPath + 'dataset'
    testset_dir = masterPath + 'test'

    # JPEG 파일 경로 리스트 가져오기
    jpeg_files_list = find_jpeg_files(dataset_dir)
    test_image_files = find_jpeg_files(testset_dir)
    #print(jpeg_files_list)
    # 학습 및 테스트 데이터 설정
    train_image_files = jpeg_files_list
    train_labels = extract_integers_from_file_paths(jpeg_files_list)
    test_labels = extract_integers_from_file_paths(test_image_files)
    print(train_labels)

    print(len(train_labels))
    # 모델 입력 이미지 크기
    IMG_HEIGHT = 128
    IMG_WIDTH = 128
    input_shape = (IMG_HEIGHT, IMG_WIDTH, 3)  # RGB 이미지

    # 모델 생성
    model = create_model(input_shape)
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # 데이터 생성기 생성
    batch_size = 20
    train_data_generator = data_generator(train_image_files, train_labels, batch_size, IMG_HEIGHT, IMG_WIDTH)

    # 모델 학습
    #steps_per_epoch = len(train_image_files) // batch_size
    #model.fit(train_data_generator, epochs=150, steps_per_epoch=steps_per_epoch)

    # 모델 저장
    #model.save('imagePrediction.h5')


# 학습된 모델 로드
    # Recreate the exact same model, including its weights and the optimizer
    model = tf.keras.models.load_model('imagePrediction.h5')
    # Show the model architecture
    model.summary()

# 특정 이미지에 대한 결과 예측
    image_path = './test/test2.jpg'
    img_height = 128
    img_width = 128
    result1 = predict_content_amount(model, masterPath+'test.jpg', img_height, img_width)
    result2 = predict_content_amount(model, masterPath+'test2.jpg', img_height, img_width)

    print("Predicted Content1 Amount:", result1)
    print("Predicted Content2 Amount:", result2)

    # 테스트 데이터에 대한 예측
    #test_image_files = jpeg_files_list  # 테스트용 데이터는 학습 데이터와 동일하게 사용
    test_data_generator = data_generator(test_image_files, test_labels, batch_size, IMG_HEIGHT, IMG_WIDTH)
    test_loss, test_mae = model.evaluate(test_data_generator, steps=len(test_image_files) // batch_size)

    print("Test MAE:", test_mae)

if __name__ == "__main__":
    main()
