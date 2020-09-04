from flask import Blueprint, Response, request, jsonify
from backend import image_code_dict
from lib.captcha.captcha import captcha

verification_bp = Blueprint("verifications", __name__)


@verification_bp.route("/imagecodes/<string:image_code_id>/", methods=['GET'])
def verification_image(image_code_id):
    verification, image = captcha.generate_captcha()
    image_code_dict[image_code_id] = verification
    response = Response(image, mimetype="image/jpeg")
    return response


@verification_bp.route("/smscodes/<string:mobile>", methods=['GET'])
def verification_smscodes(mobile):
    text = request.args.get("text")
    image_code_id = request.args.get("image_code_id")
    if text == image_code_id:
        data = {
            "code": 200,
            "msg": "success"
        }
    else:
        data = {
            "code": 200,
            "err_msg": "not success"
        }

    return jsonify(data)












