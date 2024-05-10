from database.dbConfig import *
import base64


# CSV 파일 읽기
with open('./GuideLine_images_bi.csv', 'r') as file:
    lines = file.readlines()

for line in lines:
    # CSV 라인에서 base64 데이터 추출 (예시: 첫 번째 컬럼에 base64 데이터가 있다고 가정)
    columns = line.split(',')
    base64_data = columns[-1].strip()    # base64 데이터가 있는 컬럼 인덱스 지정

    # base64 데이터를 blob으로 디코딩
    blob_data = base64.b64decode(base64_data)

    # MySQL에 새로운 레코드 삽입
    sql = "INSERT INTO images (iid, ord, name, data) VALUES (%s,%s,%s,%s)"
    val = (columns[0], columns[1], columns[2], blob_data)

    cursor.execute(sql, val)

conn.commit()
print("레코드가 성공적으로 삽입되었습니다.")
