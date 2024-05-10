from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse

from datetime import datetime

import sys
sys.path.append('../')
import database.queries as q
from models.mileleage_models import FloggingStart
from functions.imagePrediction.mileleage import product

# 라우터 객체
router = APIRouter(prefix="/mileleage")





# /mileleage/flogging
@router.post("/flogging")
async def mileleage_flogging(image: FloggingStart, request: Request):
    cookies = request.cookies
    try:
        cookie_id = cookies["id"]
        cookie_user_name = cookies["user_name"]
        condition = 'id = "' + str(cookie_id)+'" and user_name = "'+str(cookie_user_name)+'"'
        data = q.select_records('floggingimage', condition)
    except:
        return {
            "type":"string",
            "value": "unauthenticated user"
        }
    if(cookies == {}):
         return {
            "type":"string",
            "value": "unauthenticated user"
        }
    
    if(not data):
        try:
            image_data = image.value
            
            values = {
                "id": cookie_id,
                "user_name": cookie_user_name,
                "start_image": image_data
            }
            
            q.insert_record('floggingimage', values)
                
            return JSONResponse(status_code=200, content={
                "type":"string",
                "value": "file uploaded successfully"
            })
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "type":"string",
                "value" : str(e) + "occured"
            })
    else:
        try:
            condition = 'id="'+str(cookie_id)+'" and user_name="'+str(cookie_user_name)+'"'
            start_data = q.select_records('floggingimage', condition)
            #start_image = str(start_data[0][2])
            start_image = start_data[0][2]
            start_time = str(start_data[0][3])
            
            #end_image = str(image.value)
            end_image = image.value
            end_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            mileleage = product(start_image, end_image)

            q.delete_record('floggingimage', condition)
            
            dt1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            dt3 = str(dt2- dt1)
            
            return JSONResponse(status_code=200, content={
                'type':"object",
                "properties": {
                    "time": dt3,
                    "image" : start_image
                }
            })
            
        except Exception as e:  
            return JSONResponse(status_code=500, content={
                "type":"string",
                "value" : str(e) + "occured"
            })
        
    
    
        
    # start_image와 end_image 업로드 시간 차이 30분 이상
    # 현재 타입 str이니까 적당히 변경
    # AI 모델 삽입해서
    
    
    
        




