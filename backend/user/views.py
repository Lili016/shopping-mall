from flask import Blueprint, request, jsonify
from flask_restful import Resource
from munch import Munch
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db
from backend.areas.models import Area
from backend.user.model import User, Address
from backend.utils.send_email import send_email
from backend.utils.token import generate_token, check_token
# from backend.utils.wraps import login_wraps
from libs.redis_conn import get_redis_connection


# user_bp = Blueprint('users', __name__)

class RegisterMobileView(Resource):
    def get(self, username):
        count = User.query.filter_by(username=username).count()
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "count": count
            }
        )


class RegisterCreateUserView(Resource):
    def post(self):

        # json_data = request.get_json()
        json_data = request.json
        redis_conn = get_redis_connection(2)
        redis_code = redis_conn.get("sms_%s" % json_data.get("mobile"))

        if redis_code is None:
            raise Exception("验证码失效")
        if redis_code.decode() != json_data.get("sms_code"):
            raise Exception("验证码错误")
        if json_data.get("password") != json_data.get("password2"):
            raise Exception("两次输入密码不相同")

        # 加密密码 导入 from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash(json_data.get("password"))
        user = User(
            username=json_data.get("username"),
            mobile=json_data.get("mobile"),
            password=password_hash
        )
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id, 60 * 60 * 2)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "id": user.id,
                "username": json_data.get("username"),
                "token": token
            }
        )

    def put(self):
        json_data = request.json
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        if not check_password_hash(user_obj.password, json_data.get("oldpassword")):
            raise Exception('旧密码输入错误')
        if not json_data["newpassword1"] == json_data.get("newpassword2"):
            raise Exception("两次密码输入不相同")
        password_hash = generate_password_hash(json_data.get("newpassword1"))
        user_obj.password = password_hash
        db.session.commit()
        return jsonify({"code": 200, "msg": "SUCCESS"})


class UserAuthorizationView(Resource):
    def post(self):
        # json_data = request.get_json()
        json_data = request.json  ### dict
        user_obj = User.query.filter_by(username=json_data.get("username")).first()
        if user_obj is None:
            raise Exception("用户不存在")

        # 确认密码是否正确 check_password_hash(数据库中的正确的密码, 用户输入的密码)
        if not check_password_hash(user_obj.password, json_data.get("password")):
            raise Exception("密码错误")

        token = generate_token(user_obj.id)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "token": token,
                "user_id": user_obj.id,
                "username": json_data.get("username")
            }
        )


class UserCenterInfoView(Resource):

    def get(self):
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "user_id": user_id,
                "username": user_obj.username,
                "mobile": user_obj.mobile,
                "email": user_obj.email,
                "email_active": user_obj.email_active
            }
        )


class UserUpdateEmailView(Resource):
    def put(self):
        email = request.json["email"]
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        user_obj.email = email
        db.session.commit()
        send_email(
            email,
            "Confirm Your Account",
            "http://127.0.0.1:5000/success_verify_email.html",
            token
        )
        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )

    def get(self):
        token = request.args.get("token")
        user_id = check_token(token).get("user_id")
        user_obj = User.query.get(user_id)
        user_obj.email_active = True
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


class AddressViewSet(Resource):
    """
    查询数据
    get  /users/addresses/
    新增数据
    post /users/addresses/
    """

    def get(self):
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address = []
        address_obj = Address.query.filter_by(user_id=user_id, is_deleted=False).all()
        default_address_id = ""
        for one_address_obj in address_obj:
            if one_address_obj.default_address:
                default_address_id = one_address_obj.id
            data = {
                "id": one_address_obj.id,
                "user_id": one_address_obj.user_id,
                "province_id": one_address_obj.province_id,
                "city_id": one_address_obj.city_id,
                "district_id": one_address_obj.district_id,
                "receiver": one_address_obj.receiver,
                "title": one_address_obj.title,
                "mobile": one_address_obj.mobile,
                "tel": one_address_obj.tel,
                "place": one_address_obj.place,
                "email": one_address_obj.email,
            }
            province_obj = Area.query.get(one_address_obj.province_id)
            data["province"] = province_obj.name

            city_obj = Area.query.get(one_address_obj.city_id)
            data["city"] = city_obj.name

            district_obj = Area.query.get(one_address_obj.district_id)
            data["district"] = district_obj.name

            address.append(data)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "addresses": address,
                "limit": 10,
                "default_address_id": default_address_id
            }
        )

    def post(self):
        json_data = request.json
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        count = Address.query.filter_by(user_id=user_id, is_deleted=False).count()
        if count == 0:
            address_obj = Address(
                user_id=user_id,
                receiver=json_data["receiver"],
                province_id=json_data["province_id"],
                city_id=json_data["city_id"],
                title=json_data["title"],
                district_id=json_data["district_id"],
                mobile=json_data["mobile"],
                tel=json_data["tel"],
                place=json_data["place"],
                email=json_data["email"],
                default_address=True
            )
            db.session.add(address_obj)
            db.session.commit()
        else:
            address_obj = Address(
                user_id=user_id,
                receiver=json_data["receiver"],
                province_id=json_data["province_id"],
                city_id=json_data["city_id"],
                title=json_data["title"],
                district_id=json_data["district_id"],
                mobile=json_data["mobile"],
                tel=json_data["tel"],
                place=json_data["place"],
                email=json_data["email"]
            )
            db.session.add(address_obj)
            db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


class AddressViewUpdateSet(Resource):
    def put(self, address_id):
        # Munch 包装成一个对象
        json_data = Munch(request.json)
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address_obj = Address.query.filter_by(user_id=user_id, id=address_id, is_deleted=False).first()
        address_obj.city_id = json_data.city_id
        address_obj.district_id = json_data.district_id
        address_obj.email = json_data.email
        address_obj.mobile = json_data.mobile
        address_obj.place = json_data.place
        address_obj.province = json_data.province
        address_obj.province_id = json_data.province_id
        address_obj.receiver = json_data.receiver
        address_obj.tel = json_data.tel
        address_obj.title = json_data.title
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )

    def delete(self, address_id):
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address_obj = Address.query.filter_by(user_id=user_id, id=address_id, is_deleted=False).first()
        address_obj.is_deleted = True
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


class AddressViewsStatusSet(Resource):
    def put(self, address_id):
        """
        put /users/addresses/<string:address_id>/status/
        设置默认地址
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        old_address_obj = Address.query.filter_by(user_id=user_id, default_address=True).first()
        if old_address_obj.default_address:
            old_address_obj.default_address = False
        new_address_obj = Address.query.filter_by(user_id=user_id, is_deleted=False, id=address_id).first()
        new_address_obj.default_address = True
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "id": address_id
            }
        )


# @user_bp.route('/', methods=["POST"])
# def user_register():
#     request_json = request.get_json()
#     user = User(
#         username=request_json.get("username"),
#         password=request_json.get("password"),
#         mobile=request_json.get("mobile")
#     )
#     db.session.add(user)
#     db.session.commit()
#     data = {
#         "code": 200,
#         "msg": "success",
#         "data": {
#             "token": "xxx",
#             "username": request_json.get("username"),
#             "id": user.id
#         }
#     }
#     return jsonify(data)
#
#
# @user_bp.route('/usernames/<string:username>/count/', methods=["GET"])
# def count(username):
#     count = User.query.filter_by(username=username).count()
#     data = {
#         "code": 200,
#         "msg": "success",
#         "data": count
#     }
#     return jsonify(data)
#
#
# @user_bp.route('/auths/', methods=['POST'])
# def auths():
#     request_json = request.get_json()
#     user_obj = User.query.filter_by(username=request_json.get("username")).first()
#     if user_obj:
#         if request_json.get("password") == user_obj.password:
#             data = {
#                 "token": 200,
#                 "msg": "success",
#                 "username": request_json.get("username")
#             }
#         else:
#             data = {
#                 "err_msg": "password is False"
#             }
#     else:
#         user_mobile_obj = User.query.filter_by(mobile=request_json.get("mobile")).first()
#         if user_mobile_obj:
#             if request_json.get("password") == user_obj.password:
#                 data = {
#                     "token": 200,
#                     "msg": "success",
#                     "username": request_json.get("username")
#                 }
#             else:
#                 data = {
#                     "err_msg": "password is False"
#                 }
#         else:
#             data = {
#                 "err_msg": "username or password is False"
#             }
#     return jsonify(data


def registerAPI(api):
    api.add_resource(RegisterCreateUserView, "/users/")
    api.add_resource(RegisterMobileView, "/users/usernames/<string:username>/count/")
    api.add_resource(UserAuthorizationView, "/users/auths/")
    api.add_resource(UserCenterInfoView, "/users/infos/")
    api.add_resource(UserUpdateEmailView, "/users/emails/")
    api.add_resource(AddressViewSet, "/users/addresses/")
    api.add_resource(AddressViewUpdateSet, "/users/addresses/<string:address_id>/")
    api.add_resource(AddressViewsStatusSet, "/users/addresses/<string:address_id>/status/")
