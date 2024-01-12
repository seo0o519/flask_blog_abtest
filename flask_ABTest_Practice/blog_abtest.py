from flask import Flask, jsonify, request, render_template, make_response, session
# flask 서버, 데이터 jsonify 형식으로, request에서 값 받아옴, html페이지 리턴, status code 리턴 
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
# 세션 등록, 로그인된 유저 정보 참조, 로그인이 된 사용자만 access가능, 로그인시 객체에 넘겨줌->세션 가능, 로그아웃시 객체에 넘겨줌 
from flask_cors import CORS
# 다른 서버에 요청 가능하게 해줌(헤더 추가해주는 라이브러리)
from blog_view import blog
from blog_control.user_mgmt import User
import os
# http / https

#https 만을 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # 환경설정

app = Flask(__name__, static_url_path = '/static') # static 폴더에서 기타 파일들 가져옴
CORS(app)
app.secret_key = 'seo_server' # flask 로그인

app.register_blueprint(blog.blog_abtest, url_prefix='/blog') # blueprint 등록
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong' # 세션 복잡 => 보안 강화


@login_manager.user_loader # flask_login이 http request에서 id 추출 => 그 아이디를 user_id param에 넣어줌 
def load_user(user_id):
    return User.get(user_id) # 해당 user_id를 가지고 mysql에서 정보를 뽑아와서 객체를 만들고 해당 객체를 리턴 


@login_manager.unauthorized_handler
def unauthorized(): # 로그인 안 한 사용자가 로그인시에만 접근 가능한 api를 request 했을 때 호출
    return make_response(jsonify(success=False), 401)

@app.before_request
def app_before_request():
    if 'client_id' not in session: # HTTP 요청에 대한 정보가 flask의 session 객체에 담김, 
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #  session에 client_id라는 정보를 추가함 / IP 주소 저장 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)

