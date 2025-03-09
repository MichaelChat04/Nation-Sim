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

# Automatically generate a map at the start of a session
def initialize_map():
    return generate_and_save_map()

# Generate the map at startup
initial_map = initialize_map()

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nation Simulator</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            height: 100vh;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        #mapContainer {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 80%;
            max-width: 800px;
            height: auto;
            margin-bottom: 20px;
            background: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        #mapContainer img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}
        #decisionBox {{
            width: 80%;
            max-width: 800px;
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        textarea {{
            width: 100%;
            height: 150px;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }}
        button {{
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 10px;
            border: none;
            background: #007BFF;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <div id="mapContainer">
        <img id="map" src="{initial_map}">
    </div>
    
    <div id="decisionBox">
        <textarea id="userInput" placeholder="Enter your decision here..."></textarea>
        <br>
        <button onclick="submitDecision()">Submit Decision</button>
        <p id="aiResponse"></p>
        <br>
        <input type="file" id="fileInput">
        <button onclick="uploadFile()">Upload</button>
        <p id="uploadMessage"></p>
    </div>
    
    <script>
        function uploadFile() {{
            let fileInput = document.getElementById("fileInput");
            let file = fileInput.files[0];
            
            if (!file) {{
                alert("Please select a file to upload.");
                return;
            }}
            
            let formData = new FormData();
            formData.append("file", file);
            
            fetch("/upload", {{
                method: "POST",
                body: formData
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById("uploadMessage").innerText = data.message;
            }});
        }}
        
        function submitDecision() {{
            let userInput = document.getElementById("userInput").value;
            
            fetch("/submit_decision", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{ user_input: userInput }})
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById("aiResponse").innerText = "AI Response: " + data.response;
            }});
        }}
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

@app.route('/submit_decision', methods=['POST'])
def submit_decision():
    user_input = request.json.get("user_input", "")
    ai_response = "Processing your decision based on historical data..."  # Placeholder response
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)