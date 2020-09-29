from datetime import datetime

from backend import db


class ContentCategory(db.Model):
    __tablename__ = "tb_content_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    key = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)


class Content(db.Model):
    __tablename__ = "tb_content"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    image = db.Column(db.String(255))
    text = db.Column(db.String(255))
    sequence = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    category_id = db.Column(db.Integer)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "image": self.image,
            "text": self.text,
            "sequence": self.sequence,
            "status": self.status,
            "category_id": self.category_id,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
