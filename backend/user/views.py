from flask import Blueprint, request, jsonify

from backend import db
from backend.user.model import User

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=["POST"])
def user_register():
    request_json = request.get_json()
    user = User(
        username=request_json.get("username"),
        password=request_json.get("password"),
        mobile=request_json.get("mobile")
    )
    db.session.add(user)
    db.session.commit()
    data = {
        "code": 200,
        "msg": "success",
        "data": {
            "token": "xxx",
            "username": request_json.get("username"),
            "id": user.id
        }
    }
    return jsonify(data)


@user_bp.route('/usernames/<string:username>/count/', methods=["GET"])
def count(username):
    count = User.query.filter_by(username=username).count()
    data = {
        "code": 200,
        "msg": "success",
        "data": count
    }
    return jsonify(data)


@user_bp.route('/auths/', methods=['POST'])
def auths():
    request_json = request.get_json()
    user_obj = User.query.filter_by(username=request_json.get("username")).first()
    if user_obj:
        if request_json.get("password") == user_obj.password:
            data = {
                "token": 200,
                "msg": "success",
                "username": request_json.get("username")
            }
        else:
            data = {
                "err_msg": "password is False"
            }
    else:
        user_mobile_obj = User.query.filter_by(mobile=request_json.get("mobile")).first()
        if user_mobile_obj:
            if request_json.get("password") == user_obj.password:
                data = {
                    "token": 200,
                    "msg": "success",
                    "username": request_json.get("username")
                }
            else:
                data = {
                    "err_msg": "password is False"
                }
        else:
            data = {
                "err_msg": "username or password is False"
            }
    return jsonify(data)





