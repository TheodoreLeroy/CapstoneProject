from flask import Blueprint, request, jsonify
from ..services.face_recognition_service import process_image

bp = Blueprint('attendance', __name__)

@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    img_bytes = file.read()
    response = process_image(img_bytes)
    return jsonify(response), 200
