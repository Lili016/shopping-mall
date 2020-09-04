from datetime import datetime

from backend import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME, default=datetime.now)


if __name__ == '__main__':
    db.create_all()
