"""
Flask Web Application for UPI QR Code Reader and Generator
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
import qrcode
from PIL import Image
import urllib.parse
import base64
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and generated folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def decode_qr_code(image_path):
    """Decode QR code from image"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None, "Could not read image"
        
        decoded_objects = pyzbar_decode(img)
        if not decoded_objects:
            return None, "No QR code found in image"
        
        qr_data = decoded_objects[0].data.decode('utf-8')
        return qr_data, None
    except Exception as e:
        return None, str(e)


def parse_upi_string(upi_string):
    """Parse UPI payment string"""
    upi_params = {}
    
    try:
        if not upi_string.startswith('upi://'):
            return None, "Not a UPI payment string"
        
        parsed = urllib.parse.urlparse(upi_string)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        param_mapping = {
            'pa': 'payee_address',
            'pn': 'payee_name',
            'am': 'amount',
            'cu': 'currency',
            'tn': 'transaction_note',
            'tr': 'transaction_ref',
            'mc': 'merchant_code',
            'tid': 'transaction_id',
            'url': 'url'
        }
        
        for key, value in query_params.items():
            param_name = param_mapping.get(key, key)
            upi_params[param_name] = value[0] if isinstance(value, list) else value
        
        return upi_params, None
    except Exception as e:
        return None, str(e)


def create_upi_string(upi_params):
    """Create UPI payment string from parameters"""
    param_mapping = {
        'payee_address': 'pa',
        'payee_name': 'pn',
        'amount': 'am',
        'currency': 'cu',
        'transaction_note': 'tn',
        'transaction_ref': 'tr',
        'merchant_code': 'mc',
        'transaction_id': 'tid',
        'url': 'url'
    }
    
    query_parts = []
    for key, value in upi_params.items():
        if value:  # Only include non-empty values
            upi_key = param_mapping.get(key, key)
            encoded_value = urllib.parse.quote(str(value))
            query_parts.append(f"{upi_key}={encoded_value}")
    
    return f"upi://pay?{'&'.join(query_parts)}"


def generate_qr_code(data, filename):
    """Generate QR code and save to file"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
        img.save(filepath)
        
        return filepath, None
    except Exception as e:
        return None, str(e)


def qr_code_to_base64(filepath):
    """Convert QR code image to base64 for display"""
    try:
        with open(filepath, 'rb') as f:
            img_data = f.read()
        return base64.b64encode(img_data).decode('utf-8')
    except Exception as e:
        return None


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/decode', methods=['POST'])
def decode():
    """Decode uploaded QR code"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Decode QR code
    qr_data, error = decode_qr_code(filepath)
    if error:
        return jsonify({'error': error}), 400
    
    # Parse if UPI string
    result = {'raw_data': qr_data}
    if qr_data.startswith('upi://'):
        upi_params, parse_error = parse_upi_string(qr_data)
        if not parse_error:
            result['upi_data'] = upi_params
            result['is_upi'] = True
        else:
            result['is_upi'] = False
    else:
        result['is_upi'] = False
    
    return jsonify(result)


@app.route('/generate', methods=['POST'])
def generate():
    """Generate QR code from UPI parameters"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Create UPI string
    upi_string = create_upi_string(data)
    
    # Generate QR code
    import time
    filename = f"qr_{int(time.time())}.png"
    filepath, error = generate_qr_code(upi_string, filename)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Convert to base64 for display
    img_base64 = qr_code_to_base64(filepath)
    
    return jsonify({
        'success': True,
        'upi_string': upi_string,
        'image_base64': img_base64,
        'download_url': url_for('download', filename=filename)
    })


@app.route('/modify', methods=['POST'])
def modify():
    """Decode, modify, and re-encode QR code"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    modifications = request.form.to_dict()
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save and decode original
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    qr_data, error = decode_qr_code(filepath)
    if error:
        return jsonify({'error': error}), 400
    
    # Parse UPI data
    if not qr_data.startswith('upi://'):
        return jsonify({'error': 'Not a UPI QR code'}), 400
    
    upi_params, parse_error = parse_upi_string(qr_data)
    if parse_error:
        return jsonify({'error': parse_error}), 400
    
    # Apply modifications
    for key, value in modifications.items():
        if key != 'file' and value:
            upi_params[key] = value
    
    # Generate new QR code
    new_upi_string = create_upi_string(upi_params)
    import time
    new_filename = f"modified_qr_{int(time.time())}.png"
    new_filepath, gen_error = generate_qr_code(new_upi_string, new_filename)
    
    if gen_error:
        return jsonify({'error': gen_error}), 400
    
    # Convert to base64
    img_base64 = qr_code_to_base64(new_filepath)
    
    return jsonify({
        'success': True,
        'original_data': upi_params,
        'new_upi_string': new_upi_string,
        'image_base64': img_base64,
        'download_url': url_for('download', filename=new_filename)
    })


@app.route('/download/<filename>')
def download(filename):
    """Download generated QR code"""
    filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 UPI QR Code Reader & Generator")
    print("="*60)
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("\n✨ Features:")
    print("   - Decode QR codes and extract UPI payment details")
    print("   - Generate new UPI QR codes")
    print("   - Modify and re-encode existing QR codes")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
