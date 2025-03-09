import os
from flask import Flask, request, jsonify
import webbrowser
from map_generator import generate_and_save_map
from document_handler import handle_document_upload

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nation Simulator</title>
</head>
<body>
    <h1>Welcome to the Nation Simulator</h1>
    <button onclick="generateMap()">Generate Map</button>
    <br><br>
    <img id="map" src="" style="display:none;" width="500px">
    <br><br>
    <h2>Upload Historical Documents</h2>
    <input type="file" id="fileInput">
    <button onclick="uploadFile()">Upload</button>
    <br>
    <p id="uploadMessage"></p>
    
    <script>
        function generateMap() {
            fetch("/generate_map")
            .then(response => response.json())
            .then(data => {
                document.getElementById("map").src = data.map_url;
                document.getElementById("map").style.display = "block";
            });
        }
        
        function uploadFile() {
            let fileInput = document.getElementById("fileInput");
            let file = fileInput.files[0];
            
            if (!file) {
                alert("Please select a file to upload.");
                return;
            }
            
            let formData = new FormData();
            formData.append("file", file);
            
            fetch("/upload", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("uploadMessage").innerText = data.message;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return html_content, 200, {'Content-Type': 'text/html'}

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