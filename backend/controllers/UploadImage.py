import uuid

from flask import Blueprint, jsonify, request
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user_files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

upload_bp = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def uploadImage():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file part.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File uploaded successfully.'}), 201
