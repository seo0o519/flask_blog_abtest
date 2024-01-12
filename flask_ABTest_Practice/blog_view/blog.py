from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime


blog_abtest = Blueprint('blog', __name__)

@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET': 
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('blog.blog_fullstack1')) 
        #return redirect('/blog/test_blog') 둘 중에 더 선호하는 방식 사용하면 됨 
        # redirect : return을 다른 routing 경로로 변경해줌
        # blog : blueprint 이름 // test_blog : 함수 이름 
    elif request.method == 'POST': 
        #content type이 application/json인 경우에는 아래 방식으로 데이터 가져옴
        #print('set_email', request.get_json())

        #데이터를 form으로 전달받는 경우에는 아래 방식으로 데이터 가져옴
        print('set_email', request.form)

        user = User.create(request.form['user_email'], request.form['blog_id'])
        login_user(user, remember=True, duration=datetime.timedelta(days=365)) # 세션 정보 만들어줌, 로그인 유지 및 기간 설정
        return redirect(url_for('blog.blog_fullstack1')) 


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.blog_fullstack1'))
    

@blog_abtest.route('/blog_fullstack1')
def blog_fullstack1():
    if current_user.is_authenticated: # 등록된 사용자인지 판별 & 로그인 되어있는 사용자인지 판별
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email) #user_email 값은 html에 전달, jinja 조건문에서 사용
    else: # 로그인 안 된 경우
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'anonymous', webpage_name) # mongo db에 session ip, user email, webpage_name 저장 
        return render_template(webpage_name)
    