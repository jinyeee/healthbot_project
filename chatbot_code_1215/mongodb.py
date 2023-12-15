# # $python -m pip install pymongo
# # $python -m pip install "pymongo[srv]"==3.11
# # $pip install dnspython

# from pymongo import MongoClient
# from datetime import datetime

# # MongoDB 연결
# client = MongoClient('mongodb+srv://HealthCube:HealthCube@healthcube.urxe61y.mongodb.net/')
# db = client["HealthCube"]  # 데이터베이스 선택

# def insert_user_chat(user_id, message, db_name=None, collection_name=None):
#     # 데이터베이스가 존재하지 않으면 생성
#     db = client[db_name]

#     # 컬렉션이 존재하지 않는 경우, 생성
#     if collection_name not in db.list_collection_names():
#         db.create_collection(collection_name)
#         print(f"Collection '{collection_name}' created.")

#     # 사용자별로 문서를 생성하여 데이터 삽입
#     data = {
#         "user_id": user_id,
#         "message": message,
#         #"timestamp": datetime.utcnow()  # 예시로 timestamp 추가 -> 없을예정
#     }
#     result = db[collection_name].insert_one(data).inserted_id
#     return result


# # 확인
# # atlas gui > Database > Collections : 확인 가능

# ====================================
# gpt가 작성해준것은
from pymongo import MongoClient

chat_data = {
    'role': "a",
    'dialogue': "sdf"
}


# MongoDB 연결 함수
def connect_to_mongo():
    # MongoDB 연결 정보
    # host = "localhost"
    # port = "27017"
    # MongoDB 클라이언트 연결
    client2 = MongoClient(client = MongoClient('mongodb+srv://HealthCube:HealthCube@healthcube.urxe61y.mongodb.net/'))
    return client2

# 사용자 채팅 데이터 삽입 함수
def insert_user_chat(chat_data, db_name="HealthCube", collection_name="user_chat_logs"):
    try:
        # MongoDB 연결
        client2 = connect_to_mongo()
        # 데이터베이스가 존재하지 않으면 생성
        db = client2[db_name]

        # 컬렉션이 존재하지 않는 경우, 생성
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")

        # 대화 데이터 삽입
        result = db[collection_name].insert_one(chat_data)
        inserted_id = result.inserted_id
        print(f"Data inserted with ID: {inserted_id}")

    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

    finally:
        # 연결 닫기
        client2.close()
insert_user_chat(chat_data)