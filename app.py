import os
import re
import db
import json
from flask import Flask, session, redirect, url_for, request, render_template, flash, session, jsonify
from flask_session import Session
from datetime import timedelta, datetime
from bson.json_util import dumps
import connect
import insertdata
import copy
import schedule
import publishschedule
import time
import threading

app = Flask(__name__)
app.secret_key = b'123456789'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

user_right = False
timer = False
auto_mode = True
stop_threads = False

# Create schedule thread
# def run_schedule():
#     while True:
#         schedule.run_pending()
#         print("Running schedule thread, schedule list:", schedule.jobs)
#         time.sleep(5)
#         global stop_threads 
#         if stop_threads: 
#             print("Stoped old schedule")
#             break
# sched_thread = threading.Thread(target = run_schedule)
# sched_thread.start()

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard', username=session['username']))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard', username=session['username']))
    error = ''
    if request.method == 'POST':
        username = request.form["username"]
        pwd = request.form["pwd"]
        user = db.db.User.find_one({'name': username, 'pwd': pwd})
        if user != None:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("dashboard", username=username))
        else:
            error = "*Invalid credential, please try again."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    global user_right, auto_mode
    user_right = False
    auto_mode = True
    session.clear()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    succ = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        pwd = request.form["pwd"]
        check_username = db.db.User.find_one({'name': username})
        if check_username != None:
            return render_template("signup.html", err="User name has already existed.")
        else:
            db.db.User.insert_one(
                {'name': username, 'pwd': pwd, 'email': email, 'access': 0})
            succ = "Successful registered."
    return render_template("signup.html", succ=succ)


def check_login(username):
    if "logged_in" in session:
        if username == session['username']:
            return True
    return False


@app.route("/dashboard/<username>")
def dashboard(username):
    if check_login(username):
        data = db.db.Sensor.find_one(
            {'date': datetime.now().strftime('%Y-%m-%d')})
        if data != None:
            return render_template("dashboard.html", username=session['username'], data='{"data":' + str(json.dumps(data['data'])) + '}', loop_time=connect.loop_time)
        return render_template("dashboard.html", username=session['username'], data='{"data":[]}', loop_time=connect.loop_time)
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/recv_data")
def get_data(username):
    if check_login(username):
        data = db.db.Sensor.find_one(
            {'date': datetime.now().strftime('%Y-%m-%d')})
        if data != None:
            return '{"data":' + str(json.dumps(data['data'])) + '}'
        return json.dumps('{"data":[]}')
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/sent_data", methods=['GET', 'POST'])
def set_data(username):
    if check_login(username):
        global user_right, auto_mode
        store_data = request.json
        # print(store_data)
        send_data = copy.deepcopy(request.json)
        send_data.pop('schedule')
        print(store_data)
        # print(send_data)
        send_data = "["+str(send_data).replace("\'", "\"")+"]"
        print(send_data)
        store_data['time'] = datetime.now().strftime('%H:%M:%S')
        connect.client.on_publish = connect.on_publish
        ret = connect.client.publish("Topic/LightD", send_data)
        print("ret is", ret)
        # print(store_data)
        if store_data['schedule'] != 0:
            if user_right == False:
                auto_mode = True
            schedule.clear()
            global stop_threads
            stop_threads = True
            # sched_thread.join()
            sched_thread = threading.Thread(target = publishschedule.make_schedule, args = (store_data,))
            sched_thread.start()
        else:
            user_right = True
            auto_mode = False
        a, b = ret
        if a == 0:
            insertdata.store_request(store_data)
            return 'OK'
        return 'Error'        
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/auto_mode", methods=['POST'])
def change_uright(username):
    if check_login(username):
        auto = request.json
        print(auto)
        global auto_mode, user_right
        auto_mode = auto['auto']
        user_right = True if auto_mode == False else False
        print(auto_mode, user_right)
        return 'OK'
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/report", methods=['GET', 'POST'])
def get_report(username):
    if check_login(username):
        report = request.json
        print(report)
        if report['type'] == 'sensor':
            check_data = db.db.Sensor.find_one({'date': report['date']})
        else:
            check_data = db.db.Board.find_one({'date': report['date']})
        if check_data != None:
            return '{"data":' + str(json.dumps(check_data['data'])) + '}'
        return '{"data":[]}'
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/status", methods=['GET', 'POST'])
def get_status(username):
    if check_login(username):
        return '{"umode":"' + str(user_right) + '","amode":"' + str(auto_mode) + '","schedule":"' + str(schedule.next_run()) + '"}'
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(port=5000)
