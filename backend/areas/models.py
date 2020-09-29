from backend import db


class Area(db.Model):
    __tablename__ = "tb_areas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)


if __name__ == '__main__':
    db.create_all()
