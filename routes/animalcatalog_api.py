<<<<<<< HEAD
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
=======
from fastapi import APIRouter, Response
>>>>>>> 705fa18a19adbe70f19f8ddbab56445413e7287a

import sys
sys.path.append('../')
import database.queries as q
<<<<<<< HEAD
from models.animalcatalog_models import AnimalPost
=======
>>>>>>> 705fa18a19adbe70f19f8ddbab56445413e7287a

# 라우터 객체
router = APIRouter(prefix="/animalcatalog")

<<<<<<< HEAD
@router.get("")
async def animalcatalog_get(req: Request):
    cookies = req.cookies 
    try:
        cookie_id = cookies["id"]
        cookie_user_name = cookies["user_name"]
        print(cookies)
    except:
        return JSONResponse(status_code=200, content={
                "type":"string",
                "value": "unauthenticated user"
            })
    
    condition = 'id = "' + str(cookie_id)+'" and user_name = "'+str(cookie_user_name)+'"'
    data = q.select_records('userdata', condition)[0]
    print({
                "type":"object",
                "properties":{
                    "id": data[0],
                    "user_name": data[1],
                    "user_id": data[2],
                    "user_pw": data[3],
                    "mileleage": data[4],
                    "catalog": data[5]
                }
            })
    return JSONResponse(status_code=200, content={
                "type":"object",
                "properties":{
                    "id": data[0],
                    "user_name": data[1],
                    "user_id": data[2],
                    "user_pw": data[3],
                    "mileleage": data[4],
                    "catalog": data[5]
                }
            })
    
@router.post('')
async def animalcatalog_post(req:Request, data:AnimalPost):
    cookies = req.cookies 
    try:
        cookie_id = cookies["id"]
        cookie_user_name = cookies["user_name"]
    except:
        return JSONResponse(status_code=200, content={
                "type":"string",
                "value": "unauthenticated user"
            })    
    catalog_data = data.value
    condition = 'id = "' + str(cookie_id)+'" and user_name = "'+str(cookie_user_name)+'"'
    q.update_attrs('userdata', 'catalog', catalog_data ,condition)
    data = q.select_records('userdata', condition)[0]

    return JSONResponse(status_code=200, content={
                "type":"object",
                "properties":{
                    "id": data[0],
                    "user_name": data[1],
                    "user_id": data[2],
                    "user_pw": data[3],
                    "mileleage": data[4],
                    "catalog": data[5]
                }
            })
=======



>>>>>>> 705fa18a19adbe70f19f8ddbab56445413e7287a

