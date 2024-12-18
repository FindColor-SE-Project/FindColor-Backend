from flask import Blueprint, jsonify, request
from services.ProductService import get_all_products
product_bp = Blueprint('product', __name__)


@product_bp.route('/data', methods=['GET'])
def get_products():
    result = get_all_products()
    if isinstance(result, dict) and 'error' in result:
        return jsonify({"error": "Error to retrieve products data."}), 500
    return jsonify(result), 200