import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, "frontend/build")
TEMPLATES_FOLDER = os.path.join(BASE_DIR, "frontend/templates")


class TestConfig(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.11.168:8000/shopping_mall"


class ProdConfig(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.11.168:8000/shopping_mall"
