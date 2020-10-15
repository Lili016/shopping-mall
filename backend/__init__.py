from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from conf.config import STATIC_FOLDER, TEMPLATES_FOLDER, TestConfig

app = Flask(
    __name__,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATES_FOLDER,
    static_url_path=""
)
app.config.from_object(TestConfig)
db = SQLAlchemy(app)
CORS(app)
# image_code_dict = {}


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file("login.html")


def create_app():
    api = Api(app)
    from backend.verifications.views import registerAPI
    registerAPI(api)

    from backend.user.views import registerAPI
    registerAPI(api)

    from backend.areas.views import registerAPI
    registerAPI(api)

    from backend.cart.views import registerAPI
    registerAPI(api)

    from backend.orders.views import orders_bp
    app.register_blueprint(orders_bp)

    from backend.goods.views import goods_blueprint
    app.register_blueprint(goods_blueprint, url_prefix="/goods")
    # from backend.user.views import user_bp
    # app.register_blueprint(user_bp, url_prefix="/users")

    # from backend.verifications.views import verification_bp
    # app.register_blueprint(verification_bp, url_prefix="/verifications")

    return app
