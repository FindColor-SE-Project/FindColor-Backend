from flask import jsonify, request
from backend.models.ProductModel import Product
from backend.database.Database import db


def get_all_products():
    try:
        products = [product.to_dict() for product in Product.query.all()]
        return products
    except Exception as e:
        return {'error': 'Error to retrieve the data'}, 500


def add_product(data):
    try:
        required_fields = ['productID', 'productName', 'brandLogo', 'brandName',
                           'productCategory', 'colorShade', 'productImage', 'productDescription', 'colorTone']

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {'error': f'Missing field(s): {", ".join(missing_fields)}'}, 400

        duplicate_product_id = Product.query.filter_by(productID=data['productID']).first()
        duplicate_product_name = Product.query.filter_by(productName=data['productName']).first()
        duplicate_product_image = Product.query.filter_by(productImage=data['productImage']).first()

        errors = []
        if duplicate_product_id:
            errors.append('ProductID already exists.')
        if duplicate_product_name:
            errors.append('ProductName already exists.')
        if duplicate_product_image:
            errors.append('ProductImage already exists.')

        if errors:
            return {'error': ' '.join(errors)}, 400

        new_product = Product(
            productID=data['productID'],
            productName=data['productName'],
            brandLogo=data['brandLogo'],
            brandName=data['brandName'],
            productCategory=data['productCategory'],
            colorShade=data['colorShade'],
            productImage=data['productImage'],
            productDescription=data['productDescription'],
            colorTone=data['colorTone'],
        )

        db.session.add(new_product)
        db.session.commit()

        return new_product.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

# def delete_product(product_id):
#     try:
#         product = Product.query.filter_by(productID=product_id).first()
#         if product:
#             db.session.delete(product)
#             db.session.commit()
#             return {'message': 'Product deleted successfully'}, 200
#         else:
#             return {'error': 'Product not found'}, 404
#     except Exception as e:
#         db.session.rollback()
#         return {'error': str(e)}, 400
