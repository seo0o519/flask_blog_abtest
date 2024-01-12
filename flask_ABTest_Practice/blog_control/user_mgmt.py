from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

class User(UserMixin): # UserMixin class 상속받음
    def __init__(self, user_id, user_email, blog_id):
        self.id = user_id # id는 flask_login 코드 안에서도 access하기 때문에 이름 바꾸면 안됨
        self.user_email = user_email
        self.blog_id = blog_id

    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id): # 특정 user_id에 해당하는 user 객체를 반환하는 함수 
        mysql_db = conn_mysqldb() # connection된 mysql 가져옴
        db_cursor = mysql_db.cursor() # cursor 가져옴
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'" # user_info : 테이블 이름
        db_cursor.execute(sql)
        user = db_cursor.fetchone() # user_id에 매칭되는 record는 하나 뿐, record는 db에 입력된 순서대로 들어옴 
        if not user:
            return None
        
        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user
    
    @staticmethod
    def find(user_email): # 특정 email에 해당하는 user 객체를 반환하는 함수 
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL = '" + str(user_email) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user
    
    @staticmethod
    def create(user_email, blog_id): # 새로운 데이터를 db에 추가하는 함수
        user = User.find(user_email)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_EMAIL, BLOG_ID) VALUES ('%s', '%s')" % (str(user_email), str(blog_id))
            db_cursor.execute(sql)
            mysql_db.commit() # data 처리 시 commit
            return User.find(user_email)
        else:
            return user
    
    @staticmethod
    def delete(user_id): # 사용자를 db에서 삭제하는 함수
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
            deleted = db_cursor.execute(sql)
            mysql_db.commit() # data 처리 시 commit
            return deleted # 딱히 쓰이지는 않지만 그냥 일다 이렇게 리턴 