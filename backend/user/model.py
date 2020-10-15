from datetime import datetime

from backend import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    email = db.Column(db.String(255))
    email_active = db.Column(db.Boolean, default=False)


class Address(db.Model):
    __tablename__ = "tb_address"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    province_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    district_id = db.Column(db.Integer)
    receiver = db.Column(db.String(255))
    title = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    tel = db.Column(db.String(255))
    place = db.Column(db.TEXT)
    email = db.Column(db.String(255))
    is_deleted = db.Column(db.Boolean, default=False)
    default_address = db.Column(db.Boolean, default=False)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
