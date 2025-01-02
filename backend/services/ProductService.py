from flask import jsonify, request
from models.ProductModel import (Product)
from database.Database import db


def get_all_products():
    try:
        products = [product.to_dict() for product in Product.query.all()]
        return products
    except Exception as error:
        return {'error': 'Error to retrieve products data.'}, 500