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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        html, body {{
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            overflow: hidden;
        }}
        #mapContainer {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 250px;
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
            width: 80vw;
            max-width: 800px;
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            position: relative;
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
            border: none;
            background: #007BFF;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{
            background: #0056b3;
        }}
        #responseBox {{
            width: 80vw;
            max-width: 800px;
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 5px;
        }}
        #submitDecisionBtn {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 20px;
            padding: 8px 15px;
        }}
        #uploadTab {{
            position: fixed;
            top: 50%;
            right: 0;
            transform: translateY(-50%);
            background: #333;
            color: white;
            padding: 10px;
            cursor: pointer;
        }}
        #uploadPanel {{
            position: fixed;
            top: 0;
            right: -300px;
            width: 300px;
            height: 100%;
            background: white;
            box-shadow: -2px 0px 5px rgba(0, 0, 0, 0.5);
            transition: right 0.3s ease-in-out;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div id="mapContainer">
        <img id="map" src="{initial_map}">
    </div>
    
    <div id="responseBox">
        <p id="aiResponse">AI Response will appear here...</p>
    </div>
    
    <div id="decisionBox">
        <textarea id="userInput" placeholder="Enter your decision here..."></textarea>
        <button id="submitDecisionBtn" onclick="submitDecision()">✅</button>
    </div>
    
    <div id="uploadTab" onclick="toggleUploadPanel()">Documents</div>
    <div id="uploadPanel">
        <h2>Upload Documents</h2>
        <input type="file" id="fileInput">
        <button onclick="uploadFile()">Upload</button>
        <p id="uploadMessage"></p>
    </div>
    
    <script>
        function toggleUploadPanel() {{
            let uploadPanel = document.getElementById("uploadPanel");
            if (uploadPanel.style.right === "-300px") {{
                uploadPanel.style.right = "0px";
            }} else {{
                uploadPanel.style.right = "-300px";
            }}
        }}
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return html_content, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run(debug=True)