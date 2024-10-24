import cv2
from flask import Blueprint, jsonify, request, Flask
import mysql.connector
from flask_cors import CORS
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

user_bp = Blueprint('user', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def userDB():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='099*3941115',
        database='test1'
    )


@user_bp.route('/user', methods=['POST'])
def insert_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file part.'}), 400

    # ตรวจสอบว่าไฟล์มีนามสกุลที่ถูกต้อง
    if file and allowed_file(file.filename):
        # ตรวจสอบประเภทไฟล์
        if file.content_type not in ['image/jpeg', 'image/png']:
            return jsonify({'message': 'File type not allowed. Only PNG and JPEG are accepted.'}), 400

        filename = file.filename
        file_data = file.read()  # อ่านข้อมูลไฟล์เป็น binary

        # เชื่อมต่อกับฐานข้อมูลและบันทึกข้อมูลไฟล์ลงในตาราง images
        conn = userDB()
        cursor = conn.cursor()

        try:
            # เพิ่มข้อมูลไฟล์ลงในฐานข้อมูล (บันทึกเป็น binary)
            sql = "INSERT INTO user (filename, filepath) VALUES (%s, %s)"
            cursor.execute(sql, (filename, file_data))
            conn.commit()
        except mysql.connector.Error as err:
            return jsonify({'message': f"Error: {err}"}), 500
        finally:
            cursor.close()
            conn.close()

        return jsonify({'message': 'File uploaded successfully.'}), 201
    return jsonify({'message': 'File type not allowed. Only PNG and JPEG are accepted.'}), 400

@user_bp.route('/user', methods=['GET'])
def get_images():
    conn = userDB()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT filename, filepath FROM user")
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
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
