from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import datetime
import sqlite3
from chatbot import answer
import asyncio

# DB 연결
def connection():
    try:
        con = sqlite3.connect("fashion_user.db")
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

# 회원가입
def insert_userinfo_to_db(result:dict):
    id = result['userid']
    password = result['password']
    name = result['username']
    birth = result['birthday']
    gender = result['gender']
    email = result['email']
    phone = result['phone']
    today = datetime.date.today()
    age = today.year - int(birth[:4])
    conn = connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO member (id, password, name, birth, gender, email, phone, age) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, password, name, birth, gender, email, phone, age))
    except sqlite3.Error:
        print("중복된 아이디")

    conn.commit()
    conn.close()

# =====================================
def user_info(id, password):
    conn = connection()
    cur = conn.cursor()
    cur.execute(f"SELECT name, gender, age FROM member WHERE id = '{id}' AND password = '{password}'")
    if cur.fetchall():
        name, gender, age = cur.fetchall()
    conn.commit()
    conn.close()
    return name, gender, age
    
# 로그인 조회   
def login_db(id, password):
    login = False
    conn = connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id, password FROM member WHERE id = '{id}' AND password = '{password}'")
    if cur.fetchall():
        login = True
    conn.close()
    return login

app = Flask(__name__)

# 보안키 설정
app.config["SECRET_KEY"] = "fashion_project"


@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        result = request.form
        if login_db(result["userid"], result["password"]):
            return render_template('pages/chatbot.html')
        else:
            print('잘못된 ID PW입니다')
            
    return render_template('public/login-page.html')


@app.route('/nlp/signup')
def signup():
    return render_template('pages/sign-up.html')

@app.route('/chatbot')
def chatbot():
    return render_template('pages/chatbot.html')

@app.route("/openai/text", methods=["POST"])
def chat_gpt():
    text = request.form['text']
    return asyncio.run(answer(text))


    
@app.route('/model', methods = ['GET', 'POST'])
def model():
    if request.method == 'POST':
        result = request.form
        if result["password"] != result["confirm_password"]:
            pass
        else:
            insert_userinfo_to_db(result)
            
    return render_template('public/login-page.html')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)