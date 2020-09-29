from flask import Blueprint, render_template

from backend.goods.models import ContentCategory, Content

goods_bp = Blueprint("goods", __name__)


@goods_bp.route("/categories/", methods=["GET"])
def get_categories():
    contents = {}
    all_content_category_obj = ContentCategory.query.all()
    for one_content_category_obj in all_content_category_obj:
        contents[one_content_category_obj.key] = []
        all_content_obj = Content.query.filter_by(category_id=one_content_category_obj.id).all()
        for one_content_obj in all_content_obj:
            contents[one_content_category_obj.key].append(one_content_obj.to_dict())

    return render_template("/index.html", contents=contents, categories={})
