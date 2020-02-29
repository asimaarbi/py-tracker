from flask_marshmallow import Marshmallow

from models import Product

ma = Marshmallow()


class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ("name", "description", "track_id", "lat_long", "book_from", "deliver_to",
                  "book_date", "delivery_date", "vehicle_num", "file")
