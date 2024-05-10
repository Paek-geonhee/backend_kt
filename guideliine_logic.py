from konlpy.tag import Okt

import os
import sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import database.queries as q


async def search_in_db(search_word) -> dict:
    if(type(search_word) == int):
        condition = 'id='+ str(search_word)
        record = q.select_records('guide', condition)[0]
        record_dict = {
            "id": record[0],
            "theme": record[1],
            "category": record[2],
            "title": record[3],
            "content": record[4],
            "has_image": record[5]
        }
        return record_dict
    else:
        condition = 'theme like "%'+search_word +'%" or '+'category like "%'+search_word +'%" or ' +'title like "%'+search_word +'%" or ' +'content like "%'+search_word+'%";'
        record = q.select_records('guide', condition)
        return record

async def extract_nouns(sentence):
    okt = Okt()
    nouns = okt.nouns(sentence)
    return nouns








