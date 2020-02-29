import os.path as op

from flask import Flask
from flask_restful import Api

from models import db
from serializers import ma

from resources import ProductResource

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)
ma.init_app(app)
db.create_all(app=app)

if __name__ == '__main__':
    api.add_resource(ProductResource, '/api/product/')
    app.run(host='0.0.0.0', debug=True)
