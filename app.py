import os
import re
import db
import json
from flask import Flask, session, redirect, url_for, request, render_template, flash, session, jsonify
from flask_session import Session
from datetime import timedelta, datetime
from bson.json_util import dumps


app = Flask(__name__)
app.secret_key = b'123456789'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)


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
            return render_template("dashboard.html", username=session['username'], data='{"data":' + str(json.dumps(data['data'])) + '}')
        return render_template("dashboard.html", username=session['username'], data='{"data":[]}')
    return redirect(url_for("login"))


@app.route("/dashboard/<username>/data")
def get_data(username):
    if check_login(username):
        data = db.db.Sensor.find_one(
            {'date': datetime.now().strftime('%Y-%m-%d')})
        if data != None:
            return '{"data":' + str(json.dumps(data['data'])) + '}'
        return json.dumps('{"data":[]}')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(port=5000)
