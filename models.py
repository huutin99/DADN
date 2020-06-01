from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=True)
    pwd = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

class Sensor(db.Model):
    __tablename__ = "Sensor"
    id = db.Column(db.String, nullable=False)
    value = db.Column(db.SmallInteger, nullable=False)
    recv_time = db.Column(db.DateTime, primary_key=True)

class Monitor(db.Model):
    __tablename__ = "Monitor"
    id = db.Column(db.String, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    intensity = db.Column(db.SmallInteger, nullable=False)
    sent_time = db.Column(db.DateTime, primary_key=True)
