import io

from flask import Blueprint, jsonify, request, Flask
import mysql.connector
from flask_cors import CORS
import base64

from services.CropImage import crop_OvalShape, detect_and_crop_head

from models.UserModel import User

app = Flask(__name__)
CORS(app)

user_bp = Blueprint('user', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

def __init__(self):
    self.user_data = {
        'id': User.id,
        'filename': User.filename,
        'image_data': User.filepath,
        'created_at': User.created_at,
        'seasonColorTone': User.seasonColorTone
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def userDB():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='373600',
        database='test1'
    )

@user_bp.route('/user', methods=['POST'])
def insert_image():

    file = request.files['file']

    if file and allowed_file(file.filename):
        if file.content_type not in ['image/jpeg', 'image/png']:
            return jsonify({'message': 'File type not allowed. Only PNG and JPEG are accepted.'}), 400

        filename = file.filename
        file_data = file.read()  # อ่านข้อมูลไฟล์เป็น binary

        # Detect and crop image if necessary
        cropped_image = detect_and_crop_head(io.BytesIO(file_data))

        if cropped_image is None:
            return jsonify({'message': 'No face was detected in the image. Please upload an image again.'}), 400

        # Save cropped image to a binary stream for saving to database
        output_image = io.BytesIO()
        cropped_image.save(output_image, format='JPEG')
        output_image.seek(0)
        cropped_image_data = output_image.read()

        # เชื่อมต่อกับฐานข้อมูลและบันทึกข้อมูลไฟล์ลงในตาราง images
        conn = userDB()
        cursor = conn.cursor()

        try:
            # เพิ่มข้อมูลไฟล์ลงในฐานข้อมูล โดยไม่ระบุ seasonColorTone
            sql = "INSERT INTO user (filename, image_data) VALUES (%s, %s)"
            cursor.execute(sql, (filename, cropped_image_data))
            conn.commit()
            return jsonify({'message': 'File uploaded successfully.'}), 201
        except mysql.connector.Error as err:
            return jsonify({'message': f"Error: {err}"}), 500
        finally:
            cursor.close()
            conn.close()

    return jsonify({'message': 'File type not allowed. Only PNG and JPEG are accepted.'}), 400


@user_bp.route('/user', methods=['GET'])
def get_image():
    conn = userDB()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT filename, image_data FROM user")
        images = cursor.fetchall()
        for image in images:
            image['image_data'] = base64.b64encode(image['image_data']).decode('utf-8')  # แปลงเป็น Base64
        return jsonify(images), 200
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/user/crop_image', methods=['POST'])
def crop_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected.'}), 400
    if file and allowed_file(file.filename):
        cropped_img_base64 = crop_OvalShape(file)
        if cropped_img_base64:
            return jsonify({'image': cropped_img_base64}), 200
        else:
            return jsonify({'message': 'No face detected.'}), 404
    return jsonify({'message': 'File type not allowed.'}), 400


@user_bp.route('/user/seasonColorTone', methods=['POST'])
def save_seasonColorTone():
    data = request.json
    seasonColorTone = data.get('seasonColorTone')

    # แทนที่ `user_id` ที่มาจาก frontend ด้วยการใช้ `id` จากฐานข้อมูลโดยตรง
    conn = userDB()
    cursor = conn.cursor()

    try:
        # สมมติว่าคุณต้องการใช้ id ของไฟล์ล่าสุดที่อัปโหลด
        cursor.execute("SELECT id FROM user ORDER BY created_at DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            sql = "UPDATE user SET seasonColorTone = %s WHERE id = %s"
            cursor.execute(sql, (seasonColorTone, user_id))
            conn.commit()
            return jsonify({'message': 'Season updated successfully.', 'user_id': user_id}), 200
        else:
            return jsonify({'message': 'No user found.'}), 404
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/user/seasonColorTone', methods=['GET'])
def get_seasonColorTone():
    conn = userDB()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT seasonColorTone FROM user ORDER BY created_at DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            return jsonify({'seasonColorTone': result[0]}), 200
        else:
            return jsonify({'message': 'No seasonColorTone found.'}), 404
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/user', methods=['DELETE'])
def delete_image():
    conn = userDB()
    cursor = conn.cursor()

    try:
        # ลบข้อมูลทั้งหมดในตาราง user
        sql = "DELETE FROM user"
        cursor.execute(sql)
        conn.commit()
        return jsonify({'message': 'The image deleted successfully.'}), 200
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

# ลงทะเบียน Blueprint
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
