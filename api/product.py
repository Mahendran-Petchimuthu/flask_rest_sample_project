from email.policy import default
from itertools import product
from math import prod
from urllib import request
from xmlrpc.client import Boolean
from flask_restful import Resource, reqparse
from db.models.product import ProductModel
import arrow

field_mapping = {
                 'name':'name',
                 'description':'description',
                 'jwtSecret':'jwt_secret',
                 'encryptionKey':'encryption_key',
                 'isActive':'is_active'
                }

class Product(Resource):

    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('productId', type = int, required = True, help = 'No product is not provided')
        self.req_parse.add_argument('name', type = str, required = True, help = 'Product name is not provided')
        self.req_parse.add_argument('description', type = str, required = True, help = 'Product description is not provided')
        self.req_parse.add_argument('jwtSecret', type = str, required = True, help = 'JWT secret is not provided')
        self.req_parse.add_argument('encryptionKey', type = str, required = True, help = 'Encryption key is not provided')
        self.req_parse.add_argument('isActive', type = Boolean, required = False, default=False)
        super(Product,self).__init__()

    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.json()
        return {'message': 'Product not found'}, 404

    def put(self, id):
        data = self.req_parse.parse_args()
        product = ProductModel.find_by_id(id)
                
        if product:
            for k, v in data.items():
                if k in field_mapping and v != None:
                    setattr(product,field_mapping[k], v)
        
            product.modify_time = int(arrow.get().timestamp()*1000)
            product.save_to_db()
            return product.json()
        return {'message': 'Product not found'}, 404

    def delete(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            product.delete_from_db()

        return {'message': 'Product deleted'}


class ProductList(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('name', type = str, required = True, help = 'Product name is not provided')
        self.req_parse.add_argument('description', type = str, required = True, help = 'Product description is not provided')
        self.req_parse.add_argument('jwtSecret', type = str, required = True, help = 'JWT secret is not provided')
        self.req_parse.add_argument('encryptionKey', type = str, required = True, help = 'Encryption key is not provided')
        self.req_parse.add_argument('isActive', type = Boolean, required = False, default=False)
        super(ProductList,self).__init__()
    
    def get(self):
        return list(map(lambda x: x.json(), ProductModel.query.all()))

    def post(self):
        data = self.reqparse.parse_args()
        
        if ProductModel.find_by_name(data.name):
            return {'message': "A product with name '{}' already exists.".format(data.name)}, 400
        
        current_time_stamp = int(arrow.get().timestamp()*1000)
        data.createTime = current_time_stamp
        data.modifyTime = current_time_stamp

        product = ProductModel(**data)
        try:
            product.save_to_db()
        except Exception as e:
            print(e)
            return {"message": "An error occurred creating the product."}, 500

        return product.json(), 201