from database.dbConfig import conn, cursor
import base64

## 생성
# 데이터베이스 생성 함수
def create_database(db_name: str) -> None:
    query = "CREATE DATABASE IF NOT EXISTS " + db_name + ";"
    cursor.execute(query)
    conn.commit()

# 테이블 생성 함수
def create_table(table_name: str, columns: str) -> None:
    query = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + columns + ");"
    cursor.execute(query)
    conn.commit()

## 삭제    
# 데이터베이스 삭제 함수
def drop_database(db_name: str) -> None:
    query = "DROP DATABASE IF EXISTS " + db_name + ";"
    cursor.execute(query)
    conn.commit()
    
# 테이블 삭제 함수
def drop_table(table_name: str) -> None:
    query = "DROP TABLE IF EXISTS " + table_name + ";"
    cursor.execute(query)
    conn.commit()
    
## 테이블 조작    
# 레코드 삽입 함수
def insert_record(table_name: str, values: dict) -> None:
    """
    values는 {애트리뷰트: 값} 형태로 입력, dict임
    """
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))  # 플레이스홀더 생성 (%s를 값의 개수만큼 반복)
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

    # 쿼리 문자열 출력 (디버깅용)
    print(query)

    # 숫자 데이터를 포함한 튜플 생성
    value_tuple = tuple(values.values())

    # 쿼리 실행
    cursor.execute(query, value_tuple)
    conn.commit()


# 레코드 조회 함수
def select_records(table_name: str, conditions: str = None) -> list:
    if conditions:
        query = "SELECT * FROM " + table_name + " WHERE " + conditions + ";"
    else:
        query = "SELECT * FROM " + table_name + ";"
    cursor.execute(query)
    return cursor.fetchall()
    
# 특정 레코드의 특정 애트리뷰트 조회 함수
def select_attrs(table_name: str, attr_name: str, conditions: str = None) -> list:
    try:
        if conditions:
            query = f"SELECT {attr_name} FROM {table_name} WHERE {conditions};"
        else:
            query = f"SELECT {attr_name} FROM {table_name};"

        print(query)  # 쿼리 확인 (디버깅용)

        cursor.execute(query)
        print("done")  # 쿼리 실행 완료 시 출력 (디버깅용)

        return cursor.fetchall()
    except Exception as e:
        print(f"Error occurred during query execution: {e}")
        return []  # 빈 리스트 반환 또는 예외 처리에 따라 적절한 처리 수행

# 조건 만족하는 부분 변경
def update_record(table_name: str, values: dict, conditions: str) -> None:
    set_values = ', '.join([column + "=%s" for column in values.keys()])

    query = f"UPDATE {table_name} SET {set_values} WHERE {conditions};"
    cursor.execute(query, tuple(values.values()))
    conn.commit()

<<<<<<< HEAD
# 조건 만족하는 특정 애트리뷰트 변경
def update_attrs(table_name: str, attr_name: str, value: str, conditions: str) -> None:
    query = "UPDATE " + table_name + " SET " + attr_name + '= "' + value + '" WHERE ' + conditions + ';'
    cursor.execute(query)
    conn.commit()

# 레코드 삭제 함수
def delete_record(table_name: str, conditions: str) -> None:
    query = "DELETE FROM " + table_name + " WHERE " + conditions + ";"
    print("쿼리", query)
=======
# 레코드 삭제 함수
def delete_record(table_name: str, conditions: str) -> None:
    query = "DELETE FROM " + table_name + " WHERE " + conditions + ";"
>>>>>>> 705fa18a19adbe70f19f8ddbab56445413e7287a
    cursor.execute(query)
    conn.commit()
    
## 테이블의 정보(내부 데이터X) 가져오기
# 테이블 총 행 수 체크
def get_table_length(table_name: str) -> int:
    query = "SELECT COUNT(*) FROM " + table_name + ";"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
