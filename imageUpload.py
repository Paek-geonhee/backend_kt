#from database.dbConfig import conn, cursor
from dbConfig import conn, cursor


def image_to_blob(file_path):
    with open(file_path, "rb") as f:
        blob_data = f.read()
    return blob_data

# 이미지 파일 경로
#image_path = './point_1_1.png'

# 이미지 파일을 BLOB로 변환
blob_image1 = image_to_blob('./database/point_1_1.png')
blob_image2 = image_to_blob('./database/point_1_2.png')
blob_image3 = image_to_blob('./database/point_1_3.png')
blob_image4 = image_to_blob('./database/point_2_1.png')
blob_image5 = image_to_blob('./database/point_2_2.png')
blob_image6 = image_to_blob('./database/point_3_1.png')

query = "INSERT INTO images(iid, ord, name, data) VALUES (%s, %s, %s, %s)"

cursor = conn.cursor()
cursor.execute(query, (19, 1, 'point_19_1_1.png',blob_image1))
cursor.execute(query, (19, 2, 'point_19_1_2.png',blob_image2))
cursor.execute(query, (19, 3, 'point_19_1_3.png',blob_image3))
cursor.execute(query, (19, 4, 'point_19_2_1.png',blob_image4))
cursor.execute(query, (19, 5, 'point_19_2_2.png',blob_image5))
cursor.execute(query, (22, 1, 'point_22_1_1.png',blob_image6))

conn.commit()