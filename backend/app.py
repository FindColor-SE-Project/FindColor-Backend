from flask import Flask, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_article():
    data = database.get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)