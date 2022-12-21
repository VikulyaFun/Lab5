import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",user="postgres",password="271104",host="localhost",port="5432")
cursor = conn.cursor()
@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')
@app.route('/registration/', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == ('') or password == ('') or login == (''):
            obida = 'Не оставляй поле пустым, оно расстраивается'
            return render_template('registration.html', full_name=obida)
        else:
            print (login, 'meeeoooowwwww')
            sqlcode='SELECT * FROM service.users WHERE login=\'' + str(login)+'\''
            print (sqlcode)
            cursor.execute(sqlcode)
            records = list(cursor.fetchall())
            if not records:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',(str(name), str(login), str(password)))
                conn.commit()
                return redirect('/login/')
            else:
                return  render_template('registration.html', full_name='Данный login занят другим пользователем')
    return render_template('registration.html')
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == ('') or password == (''):
                obida = 'Не оставляй поле пустым, оно расстраивается'
                return render_template('login.html', full_name=obida)
            else:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                if not records:
                    return render_template('login.html',
                                           full_name='Данные пользователя не найдены. Проверьте правильность данных.')
                else:
                    return render_template('account.html', full_name=records[0][1], username=records[0][2],
                                           password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

