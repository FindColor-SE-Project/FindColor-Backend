from flask import jsonify, request

from backend.models.ProductModel import Product
from backend.database.Database import db


def get_all_products():
    return [product.to_dict() for product in Product.query.all()]


def add_product(data):
    data = request.get_json()
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
        productCollection=data['productCollection'],
        # collectionName=data['collectionName'],
        # colorShadeImage=data['colorShadeImage'],
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201
