from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from backend.goods.models import SKU
from backend.utils.token import check_token
from libs.redis_conn import get_redis_connection

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

api = Api(orders_bp)


class PlaceOrderView(Resource):
    def get(self):
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]

        redis_conn = get_redis_connection(3)
        sku_count_ids = redis_conn.hgetall(user_id)
        sku_selected_ids = redis_conn.smembers("selected_%s" % user_id)
        cart = {}
        for key, val in sku_count_ids.items():
            if key in sku_selected_ids:
                cart[int(key)] = int(val)

        sku_selected_obj = SKU.query.filter(SKU.id.in_(cart.keys())).all()
        skus = []
        for sku_selected in sku_selected_obj:
            orders = sku_selected.to_order_dict()
            orders["count"] = cart[sku_selected.id]
            skus.append(orders)

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "skus": skus,
                "freight": "10.0"
            }
        )


class OrderView(Resource):
    def post(self):
        json_data = request.json
        print(json_data)



        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


api.add_resource(PlaceOrderView, "/places/")
api.add_resource(OrderView, "/")
















