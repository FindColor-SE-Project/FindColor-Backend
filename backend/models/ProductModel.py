from backend.database.Database import db


class Product(db.Model):
    __tablename__ = 'product'
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(255), nullable=False)
    brandLogo = db.Column(db.String(255), nullable=False)
    brandName = db.Column(db.String(255), nullable=False)
    productCategory = db.Column(db.String(255), nullable=False)
    colorShade = db.Column(db.String(255), nullable=False)
    productImage = db.Column(db.String(255), nullable=False)
    productDescription = db.Column(db.String(255), nullable=False)
    colorTone = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'productID': self.productID,
            'productName': self.productName,
            'brandLogo': self.brandLogo,
            'brandName': self.brandName,
            'productCategory': self.productCategory,
            'colorShade': self.colorShade,
            'productImage': self.productImage,
            'productDescription': self.productDescription,
            'colorTone': self.colorTone
        }
