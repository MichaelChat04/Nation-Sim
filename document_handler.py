import os
from flask import request, jsonify

def handle_document_upload(request, upload_folder):
    """Handles file uploads and saves them in the uploads folder."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename})
