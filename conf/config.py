import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, "frontend/build")
TEMPLATES_FOLDER = os.path.join(BASE_DIR, "frontend/templates")


class TestConfig(object):
    DEBUG = False

    SECRET_KEY = "123"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:8000/text1"


class ProdConfig(object):
    DEBUG = False

    SECRET_KEY = "123"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:8000/text1"
