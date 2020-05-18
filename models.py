from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=True)
    pwd = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

