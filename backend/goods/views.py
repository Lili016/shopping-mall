from collections import OrderedDict
from flask import Blueprint, render_template
from backend.goods.models import ContentCategory, Content, GoodsCategory, GoodsChannel, GoodsSpecification, \
    SKUSpecification, SpecificationOption, SKU, Goods

goods_blueprint = Blueprint("goods", __name__)


# 首页商品分类
@goods_blueprint.route("/categories/", methods=["GET"])
def get_categories():
    """
    GET /goods/categories/
    商品分类数据
    """
    categories = OrderedDict()
    all_goods_channel_obj = GoodsChannel.query.all()
    for one_goods_channel_obj in all_goods_channel_obj:
        group_id = one_goods_channel_obj.group_id
        if group_id not in categories:
            categories[group_id] = {"channels": [], "sub_cats": []}
        one_category_obj = GoodsCategory.query.get(one_goods_channel_obj.category_id)
        categories[group_id]["channels"].append(
            {
                "id": one_category_obj.id,
                "name": one_category_obj.name,
                "url": one_goods_channel_obj.url
            }
        )
        second_category = GoodsCategory.query.filter_by(parent_id=one_category_obj.id).all()
        for second in second_category:
            second_sub_cats = {
                "id": second.id,
                "name": second.name,
                "sub_cats": []
            }
            three_category = GoodsCategory.query.filter_by(parent_id=second.id).all()
            for three in three_category:
                second_sub_cats["sub_cats"] = {
                    "id": three.id,
                    "name": three.name
                }
            categories[group_id]["sub_cats"].append(second_sub_cats)

    # 广告和首页数据
    contents = {}
    content_categories = ContentCategory.query.all()
    for one_content_categories in content_categories:
        contents[one_content_categories.key] = []
        all_contents = Content.query.filter_by(category_id=one_content_categories.id).all()
        for one_contents in all_contents:
            # content = {
            #     "id": one_contents.id,
            #     "create_time": one_contents.create_time,
            #     "update_time": one_contents.update_time,
            #     "title": one_contents.title,
            #     "url": one_contents.url,
            #     "image": one_contents.image,
            #     "text": one_contents.text,
            #     "sequence": one_contents.sequence,
            #     "status": one_contents.status,
            #     "category_id": one_contents.category_id
            # }
            # contents[one_content_categories.key].append(content)

            contents[one_content_categories.key].append(one_contents.to_dict())

    return render_template("/index.html", contents=contents, categories=categories)


"""
/goods/categories/1/skus/
"""


# 商品详情页
@goods_blueprint.route("/categories/<int:sku_id>/skus/", methods=["GET"])
def get_categories_detail(sku_id):
    categories = OrderedDict()
    all_goods_channel = GoodsChannel.query.all()
    for one_goods_channel in all_goods_channel:
        group_id = one_goods_channel.group_id
        if group_id not in categories:
            categories[group_id] = {"channels": [], "sub_cats": []}
        one_category = GoodsCategory.query.get(one_goods_channel.group_id)
        categories[group_id]["channels"].append({
            "id": one_category.id,
            "name": one_category.name,
            "url": one_goods_channel.url
        })
        all_second_category = GoodsCategory.query.filter_by(parent_id=one_category.id).all()
        for one_second_category in all_second_category:
            second_sub_cats = {
                "id": one_second_category.id,
                "name": one_second_category.name,
                "sub_cats": []
            }
            all_three_category = GoodsCategory.query.filter_by(parent_id=one_second_category.id).all()
            for one_three_category in all_three_category:
                second_sub_cats["sub_cats"].append(
                    {
                        "id": one_three_category.id,
                        "name": one_three_category.name
                    }
                )
            categories[group_id]["sub_cats"].append(second_sub_cats)

    # 广告和首页数据
    contents = {}
    content_categories = ContentCategory.query.all()
    for cat in content_categories:
        all_contents = Content.query.filter_by(category_id=cat.id, status=True).all()
        contents[cat.key] = []
        for content in all_contents:
            contents[cat.key].append(content.to_dict())

    sku_obj = SKU.query.get(sku_id)
    # 获取当前商品数据
    sku = sku_obj.to_dict()
    # 商品SPU类别
    goods = Goods.query.get(sku_obj.goods_id).to_detail_dict()

    specs = []
    all_gs_obj = GoodsSpecification.query.filter_by(goods_id=sku_obj.goods_id).all()
    for one_gs in all_gs_obj:
        ss_obj = SKUSpecification.query.filter_by(
            sku_id=sku_id, spec_id=one_gs.id
        ).first()

        sopt_objs = SpecificationOption.query.filter_by(spec_id=ss_obj.spec_id).all()

        options = []
        select = 0
        for sopt_obj in sopt_objs:
            if sopt_obj.id == ss_obj.option_id:
                select = 0
            else:
                select += 1

            options.append({
                "value": sopt_obj.value,
                "sku_id": sku_id,
                "select": select
            })

        specs.append({
            "name": one_gs.name,
            "options": options,
        })

    return render_template(
        "/detail.html",
        contents=contents,
        categories=categories,
        goods=goods,
        specs=specs,
        sku=sku
    )
