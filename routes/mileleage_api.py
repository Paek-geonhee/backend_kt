from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import tensorflow as tf
import cv2
import numpy as np
import sys
sys.path.append('../')
import database.queries as q
from models.mileleage_models import FloggingStart
from ML.mileleage import product, predict_content_amount, predict_content_amount_np


import json
# 라우터 객체
router = APIRouter(prefix="/mileleage")


min_gap = 1


def update_mileleage(mlg, user_id, user_name):
    condition = f"user_id = '{user_id}' and user_name = '{user_name}'"

    # 현재 마일리지 조회
    mileleage_value = q.select_attrs('userdata', 'mileleage', condition)
    if mileleage_value:
        current_mileage = int(mileleage_value[0][0]) + mlg

        # 업데이트할 값 딕셔너리 생성
        update_values = {'mileleage': current_mileage}


        try:
            # 레코드 업데이트
            q.update_record('userdata', update_values, condition)
        except Exception as e:
            print(f"레코드 업데이트 오류 발생: {e}")
    else:
        print("조건에 해당하는 데이터가 없습니다.")

    
logging.basicConfig(
    filename='server.log',  # 로그 파일 경로
    level=logging.INFO,     # 로그 레벨 (INFO 수준 이상의 로그만 기록)
    format='%(asctime)s %(levelname)s: %(message)s'  # 로그 포맷
)

    q.update_record('userdata','mileleage = {cur_mile}', condition)



# /mileleage/flogging
@router.post("/flogging")
async def mileleage_flogging(request: Request, image: UploadFile = File(...)):
    cookies = request.cookies
    try:
        cid = cookies["user_id"]
        cpw = cookies["user_pw"]
        cname = cookies["user_name"]
        condition = 'user_id = "' + str(cid)+'" and user_pw = "'+str(cpw)+'"'
        data = q.select_records('userdata', condition)
    except:
        return {
            "error":"none",
            "type":"string",
            "value": "unauthenticated user"
        }
    if(cookies == {}):
         return {
             "error":"null",
            "type":"string",
            "value": "unauthenticated user"
        }
    condition = 'user_id = "' + str(cid)+'" and user_name = "'+str(cname)+'"'
    data = q.select_records('flogging', condition)


    image_data = await image.read()
    file_path = image_data.decode('utf-8')

    #nparr = np.frombuffer(image_data, np.uint8)
    #cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR 형식으로 이미지를 읽음

            # OpenCV 이미지를 RGB 형식으로 변환 (선택적)
    #cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    if(not data):
        print("no data")
        # 만약 유저 이미지 데이터가 없다면 빈 봉투를 처음 등록하는 경우임.
        try:
            
        # JSON 데이터를 파일에 쓰기
            

            model = tf.keras.models.load_model('./routes/prediction_model.h5')
            #value = predict_content_amount_np(model, cv_image_rgb, 128, 128)
            value = predict_content_amount(model, file_path, 128, 128)

            values = {
                "user_id": str(cid),
                "user_name": str(cname),
                "start_score": int(value)
            }
            q.insert_record('flogging', values)
                
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "type":"string",
                "value" : str(e) + "occured"
            })
    else:
        try:

            # 유저 정보 확인 후 기존에 등록된 이미지 데이터 로드
            condition = 'user_id="'+str(cid)+'" and user_name="'+str(cname)+'"'
            start_data = q.select_records('flogging', condition)
            
            # 빈 봉투 이미지와 내용물이 든 봉투 이미지를 불러오고 시간 정보 체크
            start_value = start_data[0][2]
            start_time = str(start_data[0][3])
            model = tf.keras.models.load_model('./routes/prediction_model.h5')
            #end_value = predict_content_amount_np(model, cv_image_rgb, 128, 128)
            end_value = predict_content_amount(model, file_path, 128, 128)
            #image_data
            end_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


            # 마일리지 생성 및 갱신 여부 확인
            mileleage = abs(start_value - end_value)

            dt1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            time_difference = dt2 - dt1
            minutes_difference = time_difference.total_seconds() / 60

            # 시간 차이 설정
            dt3 = minutes_difference # float


            # 시간 간격이 30분 이상일 경우 마일리지를 갱신하고 이미지 정보를 제거
            # 만약 시간 간격이 30분 미만일 경우 마일리지 갱신을 수행하지 않고 result에 1을 담아 클라이언트에게 전송
            result = 1
            if dt3 >= min_gap:
                update_mileleage(mileleage, cookies["user_id"], cookies["user_name"])
                q.delete_record('flogging', condition)
                result = 0
                
                
            # 통신 상태가 정상적이라면 결과 코드로 result를 전송
            return JSONResponse(status_code=200, content={
                                "type":"int",
                                "result" : result}
                                )
            
        except Exception as e:  
            return JSONResponse(status_code=500, content={
                "type":"string",
                "value" : str(e) + "occured"
            })
        
    
    
        

    # start_image와 end_image 업로드 시간 차이 30분 이상
    # 현재 타입 str이니까 적당히 변경
    # AI 모델 삽입해서
    
    
    
        




