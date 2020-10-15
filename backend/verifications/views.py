from random import randint
from flask import Blueprint, Response, request, jsonify
from flask_restful import Resource

# from backend import image_code_dict
from backend.utils.send_sms import send_sms_code
from libs.captcha.captcha import captcha
from libs.redis_conn import get_redis_connection


# verification_bp = Blueprint("verifications", __name__)


class RegisterImageCodeView(Resource):
    def get(self, image_code_id):
        text, image = captcha.generate_captcha()
        print(text)
        redis_conn = get_redis_connection(1)
        redis_conn.setex("img_%s" % image_code_id, 60, text)

        response = Response(image, mimetype="image/jpeg")
        return response


class RegisterSmscodeView(Resource):
    def get(self, mobile):
        text = request.args.get("text")
        image_code_id = request.args.get("image_code_id")

        redis_conn = get_redis_connection(1)
        redis_text = redis_conn.get("img_%s" % image_code_id)
        if redis_text is None:
            raise Exception('')
        if redis_text.decode().lower() != text.lower():
            raise Exception("")

        sms_code = "%06d" % randint(0, 999999)
        print(sms_code)
        redis_conn = get_redis_connection(2)
        redis_conn.setex("sms_%s" % mobile, 300, sms_code)

        # send_sms_code(mobile, sms_code)
        # executor.submit(send_sms_code, mobile, sms_code)
        return " "


def registerAPI(api):
    api.add_resource(RegisterImageCodeView, "/verifications/imagecodes/<string:image_code_id>/")
    api.add_resource(RegisterSmscodeView, "/verifications/smscodes/<string:mobile>/")


# @verification_bp.route("/imagecodes/<string:image_code_id>/", methods=['GET'])
# def verification_image(image_code_id):
#     verification, image = captcha.generate_captcha()
#     image_code_dict[image_code_id] = verification
#     response = Response(image, mimetype="image/jpeg")
#     return response


# @verification_bp.route("/smscodes/<string:mobile>/", methods=['GET'])
# def verification_smscodes(mobile):
#     text = request.args.get("text")
#     image_code_id = request.args.get("image_code_id")
#     if text == image_code_id:
#         data = {
#             "code": 200,
#             "msg": "success"
#         }
#     else:
#         data = {
#             "code": 200,
#             "err_msg": "not success"
#         }
#
#     return jsonify(data)
