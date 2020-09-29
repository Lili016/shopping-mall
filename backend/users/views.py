from flask import jsonify, request
from flask_restful import Resource
from munch import Munch
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db
from backend.areas.models import Area
from backend.users.models import User, Address
from backend.utils.send_email import send_email
from backend.utils.token import generate_token, check_token
from libs.redis_conn import get_redis_connection


class RegisterMobileView(Resource):
    def get(self, username):
        """
        get /users/usernames/<string:username>/count/
        验证用户名是否已经存在
        """
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
        """
        post /users/
        用户注册接口
        """
        json_data = Munch(request.json)
        redis_conn = get_redis_connection(4)
        redis_code = redis_conn.get(json_data.mobile)
        if not redis_code:
            # raise Exception("验证码失效")
            print("111222221")
        if redis_code.decode() != json_data.sms_code:
            # raise Exception("验证码输入错误")
            print("1111")
        password_hash = generate_password_hash(json_data.password)
        user = User(
            username=json_data.username,
            password=password_hash,
            mobile=json_data.mobile
        )
        db.session.add(user)
        db.session.commit()
        token = generate_token(user.id, 60 * 60 * 2)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "id": user.id,
                "username": json_data.username,
                "token": token
            }
        )

    def put(self):
        """
        修改密码
        """
        json_data = request.json
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        if check_password_hash(user_obj.password, json_data["oldpassword"]):
            raise Exception("旧密码输入错误")
        if json_data["newpassword1"] != json_data["newpassword2"]:
            raise Exception("两次密码输入不同")
        password_hash = generate_password_hash(json_data["oldpassword"])
        user_obj.password = password_hash
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})


class UserAuthorizationView(Resource):
    def post(self):
        """
        post /users/auths/
        用户登录接口
        """
        json_data = request.json
        user_obj = User.query.filter_by(username=json_data.get("username")).first()
        if not user_obj:
            raise Exception("用户不存在")
        if check_password_hash(user_obj.password, json_data["password"]):
            raise Exception("密码输入错误")

        token = generate_token(user_obj.id)

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "token": token,
                "user_id": user_obj.id,
                "username": user_obj.username
            }
        )


class UserCenterInfoView(Resource):
    def get(self):
        """
        get /users/infos/
        用户中心  显示用户基本信息
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "id": user_obj.id,
                "username": user_obj.username,
                "mobile": user_obj.mobile,
                "email": user_obj.email,
                "email_active": user_obj.email_active
            }
        )


class UserUpdateEmailView(Resource):
    def put(self):
        """
        put /users/emails/
        设置用户邮箱
        """
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

        return jsonify({"code": 200, "msg": "success"})

    def get(self):
        """
        激活邮箱
        """
        token = request.args.get("token")
        user_id = check_token(token)["user_id"]
        user_obj = User.query.get(user_id)
        user_obj.email_active = True
        db.session.commit()

        return jsonify({"code": 200, "msg": "success"})


class AddressViewSet(Resource):
    def post(self):
        """
        post /users/addresses/
        新增地址
        """
        json_data = Munch(request.json)
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        count = Address.query.filter_by(user_id=user_id, is_deleted=False).count()
        if not count:
            address = Address(
                user_id=user_id,
                province_id=json_data.province_id,
                city_id=json_data.city_id,
                district_id=json_data.district_id,
                receiver=json_data.receiver,
                title=json_data.title,
                mobile=json_data.mobile,
                tel=json_data.tel,
                place=json_data.place,
                email=json_data.email,
                default_address=True
            )
            db.session.add(address)
            db.session.commit()
        else:
            address = Address(
                user_id=user_id,
                province_id=json_data.province_id,
                city_id=json_data.city_id,
                district_id=json_data.district_id,
                receiver=json_data.receiver,
                title=json_data.title,
                mobile=json_data.mobile,
                tel=json_data.tel,
                place=json_data.place,
                email=json_data.email,
            )
            db.session.add(address)
            db.session.commit()

        return jsonify({"code": 200, "msg": "success"})

    def get(self):
        """
        查看地址
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address = []
        all_address_obj = Address.query.filter_by(user_id=user_id, is_deleted=False).all()
        default_address_id = ""
        for one_address_obj in all_address_obj:
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
                "email": one_address_obj.email
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


class AddressViewUpdateSet(Resource):
    def put(self, addresses_id):
        """
        put /users/addresses/<string:addresses_id>/
        修改地址
        """
        json_data = Munch(request.json)
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address_obj = Address.query.filter_by(user_id=user_id, id=addresses_id, is_deleted=False).first()
        address_obj.province_id = json_data.province_id
        address_obj.city_id = json_data.city_id
        address_obj.district_id = json_data.district_id
        address_obj.receiver = json_data.receiver
        address_obj.title = json_data.title
        address_obj.mobile = json_data.mobile
        address_obj.tel = json_data.tel
        address_obj.place = json_data.place
        address_obj.email = json_data.email
        db.session.commit()

        return jsonify({"code": 200, "msg": "success"})

    def delete(self, addresses_id):
        """
        删除地址
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        address_obj = Address.query.filter_by(user_id=user_id, is_deleted=False, id=addresses_id).first()
        address_obj.is_deleted = True
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})


class AddressViewsStatusSet(Resource):
    def put(self, addresses_id):
        """
        put /users/addresses/<string:addresses_id>/status/
        设置默认地址
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        old_address_obj = Address.query.filter_by(user_id=user_id, default_address=True).first()
        old_address_obj.default_address = False
        new_address_obj = Address.query.get(addresses_id)
        new_address_obj.default_address = True
        db.session.commit()

        return jsonify({"code": 200, "msg": "success"})


def registerAPI(api):
    api.add_resource(RegisterCreateUserView, "/users/")
    api.add_resource(RegisterMobileView, "/users/usernames/<string:username>/count/")
    api.add_resource(UserAuthorizationView, "/users/auths/")
    api.add_resource(UserCenterInfoView, "/users/infos/")
    api.add_resource(UserUpdateEmailView, "/users/emails/")
    api.add_resource(AddressViewSet, "/users/addresses/")
    api.add_resource(AddressViewUpdateSet, "/users/addresses/<string:addresses_id>/")
    api.add_resource(AddressViewsStatusSet, "/users/addresses/<string:addresses_id>/status/")

