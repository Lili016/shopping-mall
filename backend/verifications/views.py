from random import randint

from flask import Response, jsonify, request
from flask_restful import Resource

from backend.utils.send_sms import send_sms_code
from libs.captcha.captcha import captcha
from libs.redis_conn import get_redis_connection


class RegisterImageCodeView(Resource):
    def get(self, image_code_id):
        """
        get /verifications/imagecodes/<string:image_code_id>/
         获取图片验证码
        """
        text, image = captcha.generate_captcha()
        print(text)
        redis_conn = get_redis_connection(3)
        redis_conn.setex(image_code_id, 60, text)
        response = Response(image, mimetype="image/jpeg")
        return response


class RegisterSmscodeView(Resource):
    def get(self, mobile):
        """
        get /verifications/smscodes/<string:mobile>/
        this.mobile + '/?text=' + this.image_code+'&image_code_id='+ this.image_code_id
        获取手机验证码
        text=用户输入的图片验证码    image_code_id=存入数据库中的正确的图片验证码
        """
        text = request.args.get("text")
        image_code_id = request.args.get("image_code_id")
        redis_conn = get_redis_connection(3)
        redis_text = redis_conn.get(image_code_id)
        if not redis_text:
            # raise Exception("验证码已失效")
            pass
        if redis_text.decode().lower() != text.lower():
            # raise Exception("验证码输入错误")
            pass

        # 发送6位验证码
        sms_code = "%06d" % randint(0, 999999)
        print(sms_code)
        redis_conn = get_redis_connection(4)
        redis_conn.setex(mobile, 60, sms_code)

        # send_sms_code(mobile, sms_code)

        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


def registerAPI(api):
    api.add_resource(RegisterImageCodeView, "/verifications/imagecodes/<string:image_code_id>/")
    api.add_resource(RegisterSmscodeView, "/verifications/smscodes/<string:mobile>/")
