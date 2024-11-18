from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from backend.try_on.blush import apply_blush_color

app = Flask(__name__)

@app.route('/apply-blush', methods=['POST'])
def apply_blush():
    data = request.json
    r, g, b = data['r'], data['g'], data['b']

    # Decode the Base64 image from the request
    image_data = base64.b64decode(data['image'].split(',')[1])
    np_img = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Apply the blush with frontend RGB values
    final_makeup_cheek = apply_blush_color(img, r, g, b)

    # Encode the final image to Base64
    _, buffer = cv2.imencode('.jpg', final_makeup_cheek)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return jsonify({"image": image_base64})

if __name__ == '__main__':
    app.run(port=8000)
