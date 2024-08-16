from flask import Blueprint, jsonify, request
from backend.services.ProductService import get_all_products, add_product

product_bp = Blueprint('product', __name__)


@product_bp.route('/data', methods=['GET'])
def get_products():
    result = get_all_products()
    if isinstance(result, dict) and 'error' in result:
        return jsonify({"error": "Error to retrieve products for this route."}), 500
    return jsonify(result), 200


@product_bp.route('/data', methods=['POST'])
def create_product():
    data = request.get_json()
    result = add_product(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201

# @product_bp.route('/data/<int:product_id>', methods=['DELETE'])
# def delete_product_route(product_id):
#     return delete_product(product_id)
