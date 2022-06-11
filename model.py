from settings import db
from uuid import uuid4

class point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cord = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    isDeleted = db.Column(db.Boolean, nullable=False, default=0)
    def __init__(self, cord, name):
        self.cord = cord
        self.name = name

class road(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.Integer, db.ForeignKey('point.id'), nullable=False)
    destination = db.Column(db.Integer, db.ForeignKey('point.id'), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

if __name__ == '__main__':
    db.create_all()