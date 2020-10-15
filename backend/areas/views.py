from flask import jsonify, request
from flask_restful import Resource

from backend.areas.models import Area


class AreasReadOnlyModelView(Resource):
    """
    获取并返回所有省级城市
    get /areas/infos/
    """

    def get(self):
        provinces_list = []
        all_provinces_obj = Area.query.filter_by(parent_id=None)
        for provinces_obj in all_provinces_obj:
            provinces_list.append(
                {
                    "id": provinces_obj.id,
                    "name": provinces_obj.name,
                    "parent_id": provinces_obj.parent_id
                }
            )

        return jsonify(provinces_list)


class AreasPKModelView(Resource):
    """
    获取省级以下城市
    get /areas/infos/<string:province_id>/
    """
    def get(self, province_id):
        city_list = []
        all_city_obj = Area.query.filter_by(parent_id=province_id)
        city_obj = Area.query.get(province_id)
        for one_city_obj in all_city_obj:
            city_list.append(
                {
                    "id": one_city_obj.id,
                    "name": one_city_obj.name,
                    "parent_id": one_city_obj.parent_id
                }
            )

        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "id": province_id,
                "name": city_obj.name,
                "subs": city_list
            }
        )






def registerAPI(api):
    api.add_resource(AreasReadOnlyModelView, "/areas/infos/")
    api.add_resource(AreasPKModelView, "/areas/infos/<string:province_id>/")
