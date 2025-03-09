import os
from flask import Flask, request, jsonify, send_file
import webbrowser
from map_generator import generate_and_save_map
from document_handler import handle_document_upload, retrieve_relevant_data

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Automatically generate a map at the start of a session
def initialize_map():
    return generate_and_save_map()

# Generate the map at startup
initial_map = initialize_map()

@app.route('/')
def home():
    return send_file("index.html")

@app.route('/generate_map', methods=['GET'])
def generate_map_endpoint():
    map_url = generate_and_save_map()
    return jsonify({"message": "Map generated!", "map_url": map_url})

@app.route('/upload', methods=['POST'])
def upload_file():
    return handle_document_upload(request, app.config['UPLOAD_FOLDER'])

@app.route('/submit_decision', methods=['POST'])
def submit_decision():
    user_input = request.json.get("user_input", "")
    relevant_data = retrieve_relevant_data(user_input)
    ai_response = f"Based on historical records: {relevant_data}" if relevant_data else "No relevant data found."
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
