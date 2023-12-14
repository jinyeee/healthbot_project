# $python -m pip install pymongo
# $python -m pip install "pymongo[srv]"==3.11
# $pip install dnspython

from pymongo import MongoClient
#from pymongo.cursor import CursorType

host = "localhost"
port = "27017"
client2 = MongoClient('mongodb+srv://HealthCube:HealthCube@healthcube.urxe61y.mongodb.net/')
#'mongodb+srv://<HealthCube>:<HealthCube>@healthcube.urxe61y.mongodb.net/?retryWrites=true&w=majority' ???
#print(mongo)
db = client2["HealthCube"]
doc = {
    'role':'cookie',
    'dialogue':20
}



# 위에서 여기까지 테스트
#=======================
# db_name = "HealthCube"
# collection_name = 'user_chat_logs'
# # 데이터베이스가 존재하지 않으면 생성
# db = mongo[db_name]

# # 컬렉션이 존재하지 않는 경우, 생성
# if collection_name not in db.list_collection_names():
#     db.create_collection(collection_name)
#     print(f"Collection '{collection_name}' created.")

# #나중에 사용자별로 user_id 생성시 적용
def insert_item_one(data, db_name = None, collection_name = None):
    result = db[collection_name].insert_one(data).inserted_id
    return result
# 추가
inserted_id = insert_item_one(doc, db_name= "HealthCube", collection_name='user_chat_logs')
print(f"Data inserted with ID: {inserted_id}")

def insert_item_many(data, db_name = None, collection_name = None):
    # response_queue가 비어있는 경우 처리
    if not data:
        return None
    # 여기서 response_queue를 딕셔너리 형태로 감싸서 처리
    documents = [{"dat": item} for item in data]
    result = db[collection_name].insert_many(documents).inserted_ids
    return result.inserted_ids

# 확인
# atlas gui > Database > Collections : 확인 가능
