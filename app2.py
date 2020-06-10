import os
import re
import db

from flask import Flask, session, redirect, url_for, request, render_template, flash, session
from flask_session import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from datetime import timedelta
from models import *


app = Flask(__name__)
app.secret_key = b'123456789'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db = SQLAlchemy(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=1)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create app
@app.route("/")
def index():
    if "logged_in" in session:
        return redirect(url_for("dashboard", username=session["username"]))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("dashboard", username=session["username"]))
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        pwd = request.form["pwd"]
        user = db.query(User).filter(
            User.name == username, User.pwd == pwd).all()
        if user:
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
        check_username = db.query(User).filter(User.name == username).all()
        if check_username:
            return render_template("signup.html", err="User name has already existed.")
        else:
            id = (db.query(func.max(User.id)).all())[0][0] + 1
            user = User(id=id, name=username, mail=email, pwd=pwd, admin=False)
            db.add(user)
            db.commit()
            succ = "Successful registered."
    return render_template("signup.html", succ=succ)


@app.route("/dashboard/<username>")
def dashboard(username):
    if "logged_in" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for("login"))