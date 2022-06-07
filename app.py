from flask import Flask
from flask_restful import Api

from api.product import Product, ProductList
from config import mysqlConfig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Product, '/products/<int:id>', endpoint = "product")
api.add_resource(ProductList, '/products', endpoint="products")

if __name__ == '__main__':
    from db.base import db
    db.init_app(app)
    app.run(port=5000, debug=True)