import os
import glob
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

from extractInt import extract_integer_between_characters


# 디렉토리 내의 모든 JPEG 파일 찾기
def find_jpeg_files(directory):
    search_pattern = os.path.join(directory, '*.jpg')  # 디렉토리 내의 모든 .jpg 파일 검색
    jpeg_files = glob.glob(search_pattern)
    return jpeg_files

# 이미지를 읽고 정규화하여 반환하는 함수
def read_image(file_path, img_height, img_width):
    image = cv2.imread(file_path)  # 이미지 읽기
    image = cv2.resize(image, (img_width, img_height))  # 이미지 크기 조정
    image = image.astype(np.float32) / 255.0  # 이미지 정규화
    return image

# 데이터 생성기 함수 / batch용
def data_generator(image_files, labels, batch_size, img_height, img_width):
    num_samples = len(image_files)
    while True:
        indices = np.random.choice(num_samples, batch_size, replace=False)
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
        Dense(1, activation='linear')
    ])
    return model


def main():
    # 데이터셋 디렉토리 경로
    dataset_dir = './dataset'
    testset_dir = './test'

    # JPEG 파일 경로 리스트 가져오기
    jpeg_files_list = find_jpeg_files(dataset_dir)

    # 학습 및 테스트 데이터 설정
    train_image_files = jpeg_files_list
    train_labels = extract_integer_between_characters(jpeg_files_list)  # 학습용 정답(내용물 양)을 지정할 빈 리스트
      # 랜덤 정수 생성 (0 이상 100 이하)

    

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
    steps_per_epoch = len(train_image_files) // batch_size
    model.fit(train_data_generator, epochs=150, steps_per_epoch=steps_per_epoch)

    # 모델 저장
    #model.save("prediction_model.h5")
    model = tf.keras.models.load_model('./ML/prediction_model.h5')

    # 테스트 데이터에 대한 예측
    test_image_files = find_jpeg_files(testset_dir)  # 테스트용 데이터는 학습 데이터와 동일하게 사용
    test_labels = extract_integer_between_characters(test_image_files)
    test_data_generator = data_generator(test_image_files, test_labels, batch_size, IMG_HEIGHT, IMG_WIDTH)
    test_loss, test_mae = model.evaluate(test_data_generator, steps=len(test_image_files) // batch_size)

    print("Test MAE:", test_mae)

if __name__ == "__main__":
    main()
