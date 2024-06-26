from flask import Blueprint, jsonify, request
from backend.controllers.ProductController import get_all_products, add_product

product_bp = Blueprint('product', __name__)


@product_bp.route('/data', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify(products)


@product_bp.route('/data', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = add_product(data)
    return jsonify(new_product), 201
