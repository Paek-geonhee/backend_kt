import re

def extract_integer_between_characters(filename):
    res = []
    for f in filename:
    # 정규 표현식을 사용하여 ','와 '.' 사이의 정수값 추출
        match = re.search(r',(\d+)\.', f)
        if match:
            # 추출된 정수값 반환
            integer_value = int(match.group(1))
            res.append(integer_value)
        else:
            # 매치되는 패턴이 없을 경우 None 반환
            return None
    return res