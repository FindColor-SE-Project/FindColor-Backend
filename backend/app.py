import sys
import os

# เพิ่มพาธของโฟลเดอร์ FindColor-Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from backend.database.Database import db
import pymysql
from backend.views.ProductView import product_bp

pymysql.install_as_MySQLdb()

app = Flask(__name__)

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:099*3941115@localhost/test_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(product_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)
