import os
import PyPDF2
import json
from flask import request, jsonify

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DOCUMENT_DATABASE = 'document_data.json'

# Function to extract text from PDFs
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

# Function to save extracted document data
def save_document_data(content, filename):
    data = {}
    if os.path.exists(DOCUMENT_DATABASE):
        with open(DOCUMENT_DATABASE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    data[filename] = content
    with open(DOCUMENT_DATABASE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Handle document uploads
def handle_document_upload(request, upload_folder):
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
        save_document_data(content, file.filename)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            save_document_data(content, file.filename)

    return jsonify({"message": "Document uploaded and processed successfully."})

# Retrieve stored knowledge
def retrieve_relevant_data(user_input):
    if not os.path.exists(DOCUMENT_DATABASE):
        return "No knowledge base found. Please upload documents first."

    with open(DOCUMENT_DATABASE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return "Error loading knowledge base."

    relevant_info = ""
    for doc, content in data.items():
        if any(keyword in content.lower() for keyword in user_input.lower().split()):
            relevant_info += f"\nFrom {doc}: {content[:500]}...\n"

    return relevant_info if relevant_info else "No relevant data found."
