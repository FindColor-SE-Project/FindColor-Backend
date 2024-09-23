from flask import Blueprint, jsonify, request
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user_files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def uploadImage():
