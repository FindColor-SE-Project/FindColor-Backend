import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from backend.database.Database import db
import pymysql
from backend.controllers.ProductController import product_bp
from backend.controllers.UserController import user_bp

pymysql.install_as_MySQLdb()

app = Flask(__name__)


def create_app():
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:373600@localhost/ep-example'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:099*3941115@localhost/test_flask'
    app.config['SQLALCHEMY_BINDS'] = {
        'user': 'mysql+pymysql://root:099*3941115@localhost/test1'
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(product_bp)
        app.register_blueprint(user_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)
