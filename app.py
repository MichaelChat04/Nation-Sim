import os
from flask import Flask, send_file, request, jsonify
import webbrowser
from map_generator import generate_and_save_map
from document_handler import handle_document_upload

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return send_file("templates/index.html")

@app.route('/generate_map', methods=['GET'])
def generate_map_endpoint():
    map_url = generate_and_save_map()
    return jsonify({"message": "Map generated!", "map_url": map_url})

@app.route('/upload', methods=['POST'])
def upload_file():
    return handle_document_upload(request, app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
