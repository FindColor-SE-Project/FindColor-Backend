from backend.try_on.blush import apply_blush_color
from backend.try_on.lips import apply_lips_color
from backend.try_on.eyeshadow import apply_eyeshadow_color
from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
import os

makeup_bp = Blueprint('makeup', __name__)

@makeup_bp.route('/apply-lips', methods=['POST'])
def apply_lips():
    try:
        data = request.json
        if 'image' not in data or 'r' not in data or 'g' not in data or 'b' not in data:
            return jsonify({"error": "Missing required data fields"}), 400

        r, g, b = data['r'], data['g'], data['b']
        image_data = data['image']

        if image_data.startswith("data:image/jpeg;base64,"):
            image_data = image_data.split(",")[1]

        try:
            image_data = base64.b64decode(image_data)
            np_img = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({"error": "Failed to decode image"}), 400
        except Exception as decode_error:
            return jsonify({"error": "Image decoding error"}), 500

        try:
            final_makeup_lips = apply_lips_color(img, r, g, b)
        except Exception as lips_error:
            return jsonify({"error": "Lips application error"}), 500

        _, buffer = cv2.imencode('.jpg', final_makeup_lips)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({"image": image_base64})
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@makeup_bp.route('/apply-blush', methods=['POST'])
def apply_blush():
    try:
        # Inspect the incoming request data for debugging
        data = request.json
        # print("Received data:", data)  # Log the data to verify structure
        print("Current working directory:", os.getcwd())

        # Check for required keys
        if 'image' not in data or 'r' not in data or 'g' not in data or 'b' not in data:
            return jsonify({"error": "Missing required data fields"}), 400

        r, g, b = data['r'], data['g'], data['b']

        # Decode the Base64 image from the request
        image_data = data['image']

        # If there's a "data:image/jpeg;base64," prefix, remove it
        if image_data.startswith("data:image/jpeg;base64,"):
            image_data = image_data.split(",")[1]

        try:
            # Decode Base64 image data
            image_data = base64.b64decode(image_data)
            np_img = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if img is None:
                print("Image decoding failed, image might be corrupted or not Base64 encoded properly.")
                return jsonify({"error": "Failed to decode image"}), 400
        except Exception as decode_error:
            print("Error decoding image:", decode_error)
            return jsonify({"error": "Image decoding error"}), 500

        # Apply the blush with frontend RGB values
        try:
            final_makeup_cheek = apply_blush_color(img, r, g, b)
        except Exception as blush_error:
            print("Error applying blush color:", blush_error)
            return jsonify({"error": "Blush application error"}), 500

        # Encode the final image to Base64
        _, buffer = cv2.imencode('.jpg', final_makeup_cheek)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        print({"image": f"data:image/jpeg;base64,{image_base64}"})
        return jsonify({"image": image_base64})
    except Exception as e:
        print("Unexpected server error:", e)
        return jsonify({"error": "Server error", "details": str(e)}), 500

@makeup_bp.route('/apply-eyeshadow', methods=['POST'])
def apply_eyeshadow():
    try:
        data = request.json
        if 'image' not in data or 'r' not in data or 'g' not in data or 'b' not in data:
            return jsonify({"error": "Missing required data fields"}), 400

        r, g, b = data['r'], data['g'], data['b']
        image_data = data['image']

        if image_data.startswith("data:image/jpeg;base64,"):
            image_data = image_data.split(",")[1]

        try:
            image_data = base64.b64decode(image_data)
            np_img = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({"error": "Failed to decode image"}), 400
        except Exception as decode_error:
            return jsonify({"error": "Image decoding error"}), 500

        try:
            final_makeup_eyeshadow = apply_eyeshadow_color(img, r, g, b)
        except Exception as eyeshadow_error:
            return jsonify({"error": "Eyeshadow application error"}), 500

        _, buffer = cv2.imencode('.jpg', final_makeup_eyeshadow)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({"image": image_base64})
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@makeup_bp.route('/link_test', methods=['POST'])
def link_test():
    return jsonify({"message": "It actually works!!"})