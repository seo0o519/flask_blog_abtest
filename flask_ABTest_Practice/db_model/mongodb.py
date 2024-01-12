import pymongo

MONGO_HOST = 'localhost'
MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST)) # MongoDB에 연결

def conn_mongodb():
    try:
        MONGO_CONN.admin.command('ismaster') # MongoDB 연결 상태 확인 
        blog_ab = MONGO_CONN.blog_session_db.blog_ab # blog_session_db 데이터베이스의 blog_ab 컬렉션에 액세스
    except:
        MONGO_CONN = pymongo.MongoClient('mongodb://%s' % (MONGO_HOST)) # MongoDB 연결 끊긴 경우 재연결
        blog_ab = MONGO_CONN.blog_session_db.blog_ab
    return blog_ab