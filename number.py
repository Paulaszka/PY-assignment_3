from database import db


class Numbers(db.Model):
    __tablename__ = 'numbers'

    id = db.Column(db.Integer, primary_key=True)
    feature1 = db.Column(db.Float, nullable=False)
    feature2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, nullable=False)

    def __init__(self, feature1, feature2, category):
        self.feature1 = feature1
        self.feature2 = feature2
        self.category = category
