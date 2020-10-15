from backend import db


class Selected(db.Model):
    __tablename__ = "tb_cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sku_id = db.Column(db.Integer)
    count = db.Column(db.Integer)
    is_selected = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)


if __name__ == '__main__':
    db.create_all()
