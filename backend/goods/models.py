from backend import db
from datetime import datetime


class ContentCategory(db.Model):
    __tablename__ = "tb_content_category"

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    name = db.Column(db.String(255))
    key = db.Column(db.String(255))


class Content(db.Model):
    __tablename__ = "tb_content"

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    image = db.Column(db.String(255))
    text = db.Column(db.String(255))
    sequence = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    category_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "title": self.title,
            "url": self.url,
            "image": self.image,
            "text": self.text,
            "sequence": self.sequence,
            "status": self.status,
            "category_id": self.category_id
        }


class GoodsCategory(db.Model):
    """
    商品类别
    """
    __tablename__ = "tb_goods_category"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)


class GoodsChannel(db.Model):
    """
    商品频道
    """

    __tablename__ = "tb_goods_channel"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    group_id = db.Column(db.Integer)
    url = db.Column(db.String(255))
    sequence = db.Column(db.Integer)
    category_id = db.Column(db.Integer)


class Brand(db.Model):
    """
    品牌
    """

    __tablename__ = "tb_brand"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    name = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    first_letter = db.Column(db.String(255))


class Goods(db.Model):
    """
    商品SPU
    """

    __tablename__ = "tb_goods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand_id = db.Column(db.Integer)
    sales = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    category1_id = db.Column(db.Integer)
    category2_id = db.Column(db.Integer)
    category3_id = db.Column(db.Integer)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    desc_detail = db.Column(db.TEXT)
    desc_pack = db.Column(db.TEXT)
    desc_service = db.Column(db.TEXT)

    def to_detail_dict(self):
        category1_obj = GoodsCategory.query.get(self.category1_id)
        category2_obj = GoodsCategory.query.get(self.category2_id)
        category3_obj = GoodsCategory.query.get(self.category3_id)
        goodschannel_obj = GoodsChannel.query.filter_by(
            category_id=self.category1_id
        ).first()
        return {
            "id": self.id,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "name": self.name,
            "brand_id": self.brand_id,
            "sales": self.sales,
            "comments": self.comments,
            "category1": {"id": category1_obj.id, "name": category1_obj.name},
            "category2": {"id": category2_obj.id, "name": category2_obj.name},
            "category3": {"id": category3_obj.id, "name": category3_obj.name},
            "channel": {"url": goodschannel_obj.url},
            "desc_detail": self.desc_detail,
            "desc_pack": self.desc_pack,
            "desc_service": self.desc_service,
        }


class GoodsSpecification(db.Model):
    """
    商品规格
    """

    __tablename__ = "tb_goods_specification"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    goods_id = db.Column(db.Integer)
    name = db.Column(db.String(255))


class SpecificationOption(db.Model):
    """
    规格选项
    """

    __tablename__ = "tb_specification_option"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    spec_id = db.Column(db.Integer)
    value = db.Column(db.String(255))


class SKU(db.Model):
    """
    商品SKU
    """

    __tablename__ = "tb_sku"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    name = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    price = db.Column(db.String(255))
    cost_price = db.Column(db.String(255))
    market_price = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    sales = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    is_launched = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer)
    goods_id = db.Column(db.Integer)
    default_image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "name": self.name,
            "caption": self.caption,
            "price": self.price,
            "cost_price": self.cost_price,
            "market_price": self.market_price,
            "stock": self.stock,
            "sales": self.sales,
            "comments": self.comments,
            "is_launched": self.is_launched,
            "category_id": self.category_id,
            "goods_id": self.goods_id,
            "default_image_url": self.default_image_url,
        }

    def to_cart_dict(self):
        return {
            "name": self.name,
            "caption": self.caption,
            "price": float(self.price),
            "cost_price": self.cost_price,
            "market_price": self.market_price,
            "stock": self.stock,
            "sales": self.sales,
            "comments": self.comments,
            "is_launched": self.is_launched,
            "category_id": self.category_id,
            "goods_id": self.goods_id,
            "default_image_url": self.default_image_url,
        }

    def to_order_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "default_image_url": self.default_image_url,
        }


class SKUImage(db.Model):
    """
    SKU图片
    """

    __tablename__ = "tb_sku_image"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    sku_id = db.Column(db.Integer)
    image = db.Column(db.String(255))


class SKUSpecification(db.Model):
    """
    SKU具体规格
    """

    __tablename__ = "tb_sku_specification"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)
    sku_id = db.Column(db.Integer)
    spec_id = db.Column(db.Integer)
    option_id = db.Column(db.Integer)