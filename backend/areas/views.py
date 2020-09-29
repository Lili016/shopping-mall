from flask import request, jsonify
from flask_restful import Resource

from backend.areas.models import Area


class AreasReadOnlyModelView(Resource):
    def get(self):
        """
        get /areas/infos/
        返回所有省级城市
        """
        provinces = []
        all_provinces_obj = Area.query.filter_by(parent_id=None).all()
        for one_province_obj in all_provinces_obj:
            provinces.append(
                {
                    "id": one_province_obj.id,
                    "name": one_province_obj.name,
                    "parent_id": one_province_obj.parent_id
                }
            )
        return jsonify(provinces)


class AreasPKModelView(Resource):
    def get(self, province_id):
        """
        get  /areas/infos/<string:province_id>/
        获取省级以下所有城市
        """
        city = []
        all_city_obj = Area.query.filter_by(parent_id=province_id).all()
        for one_city_obj in all_city_obj:
            city.append(
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
                "subs": city
            }
        )


def registerAPI(api):
    api.add_resource(AreasReadOnlyModelView, "/areas/infos/")
    api.add_resource(AreasPKModelView, "/areas/infos/<string:province_id>/")
