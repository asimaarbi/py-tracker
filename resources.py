import os
import uuid

import qrcode
from pathlib import Path

from flask_restful import reqparse, Resource

from models import Product, db
from serializers import ProductSchema


class ProductResource(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', help='Name', type=str, required=True)
        parser.add_argument('description', help='Product Description', type=str, required=True)
        parser.add_argument('lat_long', help='Map - Lat, Long', type=str, required=True)
        parser.add_argument('book_from', help='Booking Location', type=str, required=True)
        parser.add_argument('deliver_to', help='Delivery Location', type=str, required=True)
        parser.add_argument('delivery_date', help='Delivery Date', type=str, required=True)
        parser.add_argument('vehicle_num', help='Vehicle Number', type=str, required=True)
        args = parser.parse_args(strict=True)

        mystring = ''.join(str(uuid.uuid4()).split('-'))
        qr = qrcode.make(mystring)
        qr.save(f'{mystring}.png')
        custom_args = {}
        for k, v in args.items():
            if v:
                custom_args.update({k: v})

        product = Product(**custom_args)
        product.qr_code = mystring
        product.file = f'{mystring}.png'
        db.session.add(product)
        db.session.commit()

        schema = ProductSchema()
        return schema.dump(product), 201

    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('lat_long', help='Map - Lat, Long', type=str, required=True)
        parser.add_argument('vehicle_num', help='vehicle_num', type=str, required=True)
        args = parser.parse_args(strict=True)
        products = Product.query.filter(Product.vehicle_num == args['vehicle_num']).all()
        if not products:
            return "", 404
        for product in products:
            for k, v in args.items():
                if v:
                    setattr(product, k, v)
            db.session.commit()

        return 'Updated', 200

    def delete(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('track_id', type=str, help='track_id', required=False)
        parser.add_argument('qr_code', type=str, help='qr_code', required=False)
        args = parser.parse_args(strict=True)

        product = Product.query.filter(
            (Product.qr_code == args['qr_code']) | (Product.track_id == args['track_id'])).first()
        if not product:
            return "", 404
        db.session.delete(product)
        db.session.commit()
        Path(os.path.join("./", product.file)).unlink()

        return "", 204

    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('track_id', type=str, help='track_id', required=False)
        parser.add_argument('qr_code', type=str, help='qr_code', required=False)
        parser.add_argument('vehicle_num', type=str, help='vehicle_num', required=False)
        args = parser.parse_args(strict=True)

        if args['qr_code'] or args['track_id'] or args['vehicle_num']:
            product = Product.query.filter(
                ((Product.vehicle_num == args['vehicle_num']) | (Product.qr_code == args['qr_code']) | (
                        Product.track_id == args['track_id']))).all()
            if not product:
                return "", 404
            schema = ProductSchema(many=True)
            return schema.dump(product)
        print(Product.query.all())
        schema = ProductSchema(many=True)
        return schema.dump(Product.query.all()), 200
