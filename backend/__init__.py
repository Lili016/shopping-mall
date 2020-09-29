from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from conf.config import STATIC_FOLDER, TEMPLATES_FOLDER, TestConfig

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATES_FOLDER,
            static_url_path=""
            )

app.config.from_object(TestConfig)
db = SQLAlchemy(app)
CORS(app)


@app.route('/', methods=["GET"])
def index():
    return app.send_static_file("index.html")


def create_app():
    api = Api(app)

    from backend.verifications.views import registerAPI
    registerAPI(api)

    from backend.users.views import registerAPI
    registerAPI(api)

    from backend.areas.views import registerAPI
    registerAPI(api)

    from .goods.views import goods_bp
    app.register_blueprint(goods_bp, url_prefix="/goods")

    return app
