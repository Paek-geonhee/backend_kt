from fastapi import APIRouter, WebSocket

import asyncio
import json
from collections import Counter

import sys
sys.path.append('../')
import database.queries as q
from guideliine_logic import search_in_db, extract_nouns

# 라우터 객체
router = APIRouter(prefix="/guideline")

# 엔드포인트
# /guideline
@router.websocket("")
async def search(websocket:WebSocket):
    await websocket.accept()

    table_length = q.get_table_length('guide')
    
    par_tasks = []
    for i in range(table_length):
        par_tasks.append(search_in_db(i+1))
    
    results_arr = await asyncio.gather(*par_tasks)
    
    # WebSocket을 통해 클라이언트에게 결과를 전달
    par_tasks = []
    for i in range(len(results_arr)):
        result = {
            'type':'object',
            'properties': results_arr[i]
        }
        result = json.dumps(result, ensure_ascii = False)
        print(result)
        par_tasks.append(websocket.send_json(result))
    
    await asyncio.gather(*par_tasks)
    await websocket.close()

#/guideline/{item_id}
@router.get('/{item_id}')
async def get_by_id(item_id: int):
    try:
        condition = "id=" + str(item_id)
        result = q.select_records('guide', condition)[0]
        result_dict = {
            "type":"object",
            "properties":{
                "id": result[0],
                "theme": result[1],
                "category": result[2],
                "title": result[3],
                "content": result[4],
                "has_image": result[5]
                }
            }
        return result_dict
    except:
        return {
            "type":"string",
            "value":"please send right data"
        }
    
@router.websocket("/search")
async def search_ws_search(websocket:WebSocket):
    await websocket.accept()
    
    try:
        search_word = await websocket.receive_json()
        print(search_word)
        search_word = search_word['value']
        
        search_list = search_word.split(" ")
        par_tasks = []
        for i in search_list:
            par_tasks.append(extract_nouns(i))
        par_result = await asyncio.gather(*par_tasks)
        
        extracted_search_list = []
        for i in par_result:
            extracted_search_list.extend(i)
        print(extracted_search_list)
        await websocket.send_json(extracted_search_list)
        
        par_tasks= []
        for i in extracted_search_list:
            par_tasks.append(search_in_db(i))
        
        result = await asyncio.gather(*par_tasks)
        
        spread_result = []
        for i in result:
            spread_result.extend(i)
        
        counts = Counter(spread_result)
        sorted_elem = sorted(counts, key=lambda x: counts[x], reverse=True)
        
        # WebSocket을 통해 클라이언트에게 결과를 전달
        # 순위 보존을 위한 동기적 처리(일부러임)
        if(len(sorted_elem)>10):
            sorted_elem = sorted_elem[0:10]
        
        for i in range(len(sorted_elem)):
            record_dict = {
                "id": sorted_elem[i][0],
                "theme": sorted_elem[i][1],
                "category": sorted_elem[i][2],
                "title": sorted_elem[i][3],
                "content": sorted_elem[i][4],
                "has_image": sorted_elem[i][5]
            }
            result = {
                'type':'object',
                'properties': record_dict
            }
            result = json.dumps(result, ensure_ascii = False)
            
            await websocket.send_json(result)
            print(i, " - ", result)
    except:
        await websocket.send_json({
            "type": "string",
            "value": "Error: Please send right data"
        })
    
    await websocket.close()
    
@router.websocket("/recommend")
async def search_recommend(websocket:WebSocket):
    await websocket.accept()
    
    try:
        search_word = await websocket.receive_json()
        
        search_word = search_word['properties']
        text = search_word['title'] + search_word['content']
        
        nouns = await extract_nouns(text)
        
        if not nouns:
            await websocket.close()

        # 명사 빈도 계산
        counts = Counter(nouns)

        # 빈도가 가장 높은 명사 추출
        top_noun = counts.most_common(3)
        top_noun = [top_noun[0][0], top_noun[1][0], top_noun[2][0]]
        
        par_tasks = []
        for i in top_noun:
            par_tasks.append(search_in_db(i))
        
        result = await asyncio.gather(*par_tasks)
        
        result_list = []
        for i in result:
            result_list.extend(i)
        result_list = list(set(result_list))
        if(len(result_list) > 10):
            result_list = result_list[0:10]
        
        result = []
        for i in range(len(result_list)):
            record_dict = {
                "type":"object",
                "properties": {
                    "id": result_list[i][0],
                    "theme": result_list[i][1],
                    "category": result_list[i][2],
                    "title": result_list[i][3],
                    "content": result_list[i][4],
                    "has_image": result_list[i][5]
                }
            }
            result.append(record_dict)

        
        par_tasks = []
        for i in result:
            par_tasks.append(websocket.send_json(i))
        
        await asyncio.gather(*par_tasks)
        
        await websocket.close()
        
    except:
        await websocket.send_json(
            {
            "type": "string",
            "value": "Error: Please send right data"
            }
        )
        await websocket.close()
        
#/image/{item_id}
@router.get('/{item_id}')
async def get_by_id(item_id: int):
    try:
        condition = "iid=" + str(item_id)
        result = q.select_records('guide', condition)[0]
        result = {
            "type":"object",
                "properties": {
                "iid": result[0],
                "ord": result[1],
                "name": result[2],
                "data": result[3]
            }
        }
        return result
    except:
        {
            "type": "string",
            "value": "Error: Please send right data"
        }
        