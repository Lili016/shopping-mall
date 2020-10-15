import base64
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def generate_token(user_id, expiration=7200):

    s = Serializer(current_app.config["SECRET_KEY"], expiration)
    data = {
        "user_id": user_id,
    }
    token = s.dumps(data).decode("utf-8")

    # token = base64.b64encode(str(data).encode("utf-8"))
    return token


def check_token(token, expiration=7200):

    s = Serializer(current_app.config["SECRET_KEY"], expiration)

    token = s.loads(token)
    # tokens = base64.b64decode(token).decode("utf-8")
    return token
