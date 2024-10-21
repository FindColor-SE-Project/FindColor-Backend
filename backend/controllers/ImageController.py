import cv2
from flask import Blueprint, jsonify, request, Flask
import mysql.connector
from flask_cors import CORS
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

upload_bp = Blueprint('upload', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def imageDB():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='099*3941115',
        database='test1'
    )


@upload_bp.route('/upload', methods=['POST'])
def insert_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file part.'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_data = file.read()  # อ่านข้อมูลไฟล์เป็น binary

        # เชื่อมต่อกับฐานข้อมูลและบันทึกข้อมูลไฟล์ลงในตาราง images
        conn = imageDB()
        cursor = conn.cursor()

        try:
            # เพิ่มข้อมูลไฟล์ลงในฐานข้อมูล (บันทึกเป็น binary)
            sql = "INSERT INTO images (filename, filepath) VALUES (%s, %s)"
            cursor.execute(sql, (filename, file_data))
            conn.commit()
        except mysql.connector.Error as err:
            return jsonify({'message': f"Error: {err}"}), 500
        finally:
            cursor.close()
            conn.close()

        return jsonify({'message': 'File uploaded successfully.'}), 201

    return jsonify({'message': 'File type not allowed. Only PNG and JPG are accepted.'}), 400


@upload_bp.route('/upload', methods=['GET'])
def get_images():
    conn = imageDB()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT filename, filepath FROM images")
        images = cursor.fetchall()
        for image in images:
            image['filepath'] = base64.b64encode(image['filepath']).decode('utf-8')  # แปลงเป็น Base64
        return jsonify(images), 200
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

# ลงทะเบียน Blueprint
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(port=8000, debug=True)