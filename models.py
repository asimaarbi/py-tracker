import uuid
from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(5000), nullable=True)
    qr_code = db.Column(db.String(50), nullable=True)
    track_id = db.Column(db.String(50), default=lambda: ''.join(str(uuid.uuid4()).split('-')))
    lat_long = db.Column(db.String(50), nullable=True)
    book_from = db.Column(db.String(50), nullable=True)
    deliver_to = db.Column(db.String(50), nullable=True)
    book_date = db.Column(db.String(50), default=lambda: date.today())
    delivery_date = db.Column(db.String(50), nullable=True)
    vehicle_num = db.Column(db.String(50), nullable=True)
    file = db.Column(db.String(50), nullable=True)
