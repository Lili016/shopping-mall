from flask import request, jsonify
from flask_restful import Resource

from backend import db
from backend.cart.models import Selected
from backend.goods.models import SKU
from backend.utils.token import check_token
from libs.redis_conn import get_redis_connection


class CartView(Resource):
    def get(self):
        """
        显示购物车  GET "/cart/"
        """
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]

        # # MYSQL用法
        # cart_return = []
        # all_selected_obj = Selected.query.filter_by(user_id=user_id, is_deleted=False).all()
        # for one_selected_obj in all_selected_obj:
        #     all_sku_id_obj = SKU.query.filter_by(id=one_selected_obj.sku_id).all()
        #     for one_sku_id_obj in all_sku_id_obj:
        #         sku_return = one_sku_id_obj.to_dict()
        #         sku_return["amount"] = one_selected_obj.count * float(one_sku_id_obj.price)
        #         sku_return["count"] = one_selected_obj.count
        #         sku_return["selected"] = one_selected_obj.is_selected
        #         cart_return.append(sku_return)


        # redis用法



        redis_conn = get_redis_connection(3)
        sku_count_ids = redis_conn.hgetall(user_id)
        sku_selected_ids = redis_conn.smembers("selected_%s" % user_id)

        cart = {}
        for sku_id, count in sku_count_ids.items():
            cart[int(sku_id)] = {
                "count": int(count),
                "selected": sku_id in sku_selected_ids
            }
        ids = cart.keys()
        skus = SKU.query.filter(SKU.id.in_(ids)).all()
        cart_return = []
        for sku in skus:
            sku_return = sku.to_dict()
            sku_return["amount"] = cart[sku.id]["count"] * float(sku.price)
            sku_return["count"] = cart[sku.id]["count"]
            sku_return["selected"] = cart[sku.id]["selected"]
            cart_return.append(sku_return)

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "cart": cart_return
            }
        )

    def post(self):
        """
         加入购物车  POST "/cart/"
        """
        json_data = request.json
        sku_id = json_data.get("sku_id")
        count = json_data.get("count")
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]

        # redis用法
        redis_conn = get_redis_connection(3)
        redis_conn.hset(user_id, sku_id, count)
        redis_conn.sadd("selected_%s" % user_id, sku_id)


        # # MYSQL方法
        # cart_selected_obj = Selected.query.filter_by(sku_id=sku_id, user_id=user_id).first()
        # if cart_selected_obj:
        #     if cart_selected_obj.is_deleted:
        #         cart_selected_obj.is_deleted = False
        #         cart_selected_obj.count = 1
        #     else:
        #         cart_selected_obj.count += count
        # else:
        #     mysql_selected = Selected(
        #         user_id=user_id,
        #         sku_id=sku_id,
        #         count=count
        #     )
        #     db.session.add(mysql_selected)
        # db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "count": count
            }
        )

    def put(self):
        """
        商品添加数量
        """
        # redis用法
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        json_data = request.json
        redis_conn = get_redis_connection(3)
        redis_conn.hset(user_id, json_data["sku_id"], json_data["count"])
        if json_data["selected"]:
            redis_conn.sadd("selected_%s" % user_id, json_data["sku_id"])
        if not json_data["selected"]:
            redis_conn.srem("selected_%s" % user_id, json_data["sku_id"])


        # # MYSQL方法
        # cart_selected_obj = Selected.query.filter_by(user_id=user_id, sku_id=json_data["sku_id"]).first()
        # cart_selected_obj.count = json_data["count"]
        # cart_selected_obj.is_selected = json_data["selected"]
        # db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "selected": json_data["selected"],
                "count": json_data["count"]
            }
        )

    def delete(self):
        """
        删除购物车内商品
        """
        # redis用法
        token = request.headers.get("Authorization").split(" ")[-1]
        user_id = check_token(token)["user_id"]
        json_data = request.json
        redis_conn = get_redis_connection(3)
        redis_conn.hdel(user_id, json_data["sku_id"])
        redis_conn.srem("selected_%s" % user_id, json_data["sku_id"])


        # # MYSQL方法
        # token = request.headers.get("Authorization").split(" ")[-1]
        # user_id = check_token(token)["user_id"]
        # json_data = request.json
        # del_cart_obj = Selected.query.filter_by(sku_id=json_data["sku_id"], user_id=user_id).first()
        # del_cart_obj.is_deleted = True
        # db.session.commit()

        return jsonify(
            {
                "code": 200,
                "msg": "success"
            }
        )


def registerAPI(api):
    api.add_resource(CartView, "/cart/")
