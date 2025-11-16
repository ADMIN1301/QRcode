# UPI QR Code Reader and Generator

A complete web-based tool to decode, parse, modify, and encode UPI (Unified Payments Interface) payment QR codes. Built with Flask and Python, featuring a modern, responsive web interface.

## 🌟 Features

- ✅ **Web Interface**: Beautiful, responsive UI accessible via browser
- ✅ **Decode QR Codes**: Upload and read QR codes, extract payment data
- ✅ **Parse UPI Data**: Extract and display all UPI parameters:
  - Payee UPI address
  - Payee name
  - Amount
  - Currency
  - Transaction notes
  - And more...
- ✅ **Generate QR Codes**: Create new UPI QR codes with custom parameters
- ✅ **Modify QR Codes**: Upload, modify parameters, and regenerate QR codes
- ✅ **Download**: Save generated QR codes as PNG images
- ✅ **Real-time Processing**: Instant QR code generation and decoding

## 🚀 Quick Start

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y libgl1 libglib2.0-0 libzbar0
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

That's it! 🎉

## 📱 How to Use

### 🔍 Decode QR Codes

1. Click **"Decode QR"** tab
2. Click the upload area or drag & drop your QR code image
3. Supported formats: PNG, JPG, JPEG, GIF, BMP
4. Click **"Decode QR Code"**
5. View extracted UPI payment details

### ✨ Generate QR Codes

1. Click **"Generate QR"** tab
2. Fill in the payment details:
   - **UPI ID**: Your UPI address (e.g., merchant@paytm)
   - **Payee Name**: Merchant or receiver name
   - **Amount**: Payment amount in ₹ (optional)
   - **Currency**: INR (default)
   - **Transaction Note**: Description (optional)
3. Click **"Generate QR Code"**
4. View and download your QR code

### 🔧 Modify QR Codes

1. Click **"Modify QR"** tab
2. Upload an existing UPI QR code
3. Modify any parameters you want to change:
   - Leave blank to keep original values
   - Only fill in fields you want to change
4. Click **"Modify & Generate"**
5. View the updated QR code with new parameters
6. Download the modified QR code

## 📂 Project Structure

```
QRcode/
├── app.py              # Flask web application
├── qr_handler.py       # QR code handling library (standalone)
├── example.py          # Command-line usage examples
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface
├── uploads/            # Temporary uploaded files
├── generated/          # Generated QR codes
└── README.md          # Documentation
```

## 🛠️ Requirements

### System Dependencies
- Python 3.7+
- libgl1 (OpenGL library)
- libglib2.0-0 (GLib library)
- libzbar0 (ZBar barcode reader)

### Python Packages
- Flask >= 3.0.0
- qrcode[pil] >= 7.4.2
- opencv-python >= 4.8.0
- pyzbar >= 0.1.9
- Pillow >= 10.0.0
- Werkzeug >= 3.0.0

## 🔧 API Endpoints

### POST /decode
Decode an uploaded QR code image.
- **Input**: Form data with `file` (image)
- **Output**: JSON with decoded data and UPI parameters

### POST /generate
Generate a new QR code from UPI parameters.
- **Input**: JSON with UPI parameters
- **Output**: JSON with base64 image and download URL

### POST /modify
Decode, modify, and re-encode a QR code.
- **Input**: Form data with `file` and modification parameters
- **Output**: JSON with modified QR code and parameters

### GET /download/<filename>
Download a generated QR code file.
- **Output**: PNG image file

## 💡 UPI String Format

UPI payment strings follow this standard format:
```
upi://pay?pa=<VPA>&pn=<Name>&am=<Amount>&cu=<Currency>&tn=<Note>
```

### Supported Parameters

| Parameter | Code | Description | Example |
|-----------|------|-------------|---------|
| Payee Address | `pa` | UPI ID/Virtual Payment Address | `merchant@paytm` |
| Payee Name | `pn` | Name of merchant/receiver | `My Store` |
| Amount | `am` | Transaction amount | `500` |
| Currency | `cu` | Currency code | `INR` |
| Transaction Note | `tn` | Payment description | `Order #12345` |
| Transaction Ref | `tr` | Reference ID | `TXN001` |
| Merchant Code | `mc` | Merchant category code | `1234` |
| Transaction ID | `tid` | Unique transaction ID | `TID123` |

## 📝 Command Line Usage (Optional)

For programmatic use, you can use the `qr_handler.py` module:

```python
from qr_handler import UPIQRHandler

handler = UPIQRHandler()

# Create UPI QR code
upi_params = {
    'payee_address': 'merchant@paytm',
    'payee_name': 'My Store',
    'amount': '500',
    'currency': 'INR',
    'transaction_note': 'Payment'
}

upi_string = handler.create_upi_string(upi_params)
handler.encode_qr(upi_string, "my_qr.png")

# Decode QR code
decoded = handler.decode_qr("my_qr.png")
upi_data = handler.parse_upi_string(decoded)

# Modify and re-encode
handler.decode_and_encode(
    "original.png",
    "modified.png",
    modify_params={'amount': '1000'}
)
```

Run examples:
```bash
python example.py
```

## 🎯 Use Cases

1. **Merchant Payments**: Generate dynamic QR codes for different amounts
2. **Payment Testing**: Create test QR codes for payment gateway development
3. **QR Analysis**: Decode and analyze existing UPI QR codes
4. **Bulk Generation**: Programmatically create multiple QR codes
5. **Payment Modification**: Update amounts or notes in existing QR codes

## 🔒 Security Notes

- Always validate UPI addresses before generating QR codes
- Verify payment amounts and recipient details
- Use HTTPS in production environments
- Don't expose merchant credentials in code
- Validate all user inputs

## 🐛 Troubleshooting

### "ImportError: libGL.so.1"
Install OpenGL library:
```bash
sudo apt-get install -y libgl1
```

### "No QR code found in the image"
- Ensure image contains a clear, visible QR code
- Check image quality and resolution
- Try a different image format
- Ensure proper lighting in the photo

### "pyzbar not working"
Install ZBar library:
```bash
# Ubuntu/Debian
sudo apt-get install -y libzbar0

# macOS
brew install zbar

# Windows
# Download from: http://zbar.sourceforge.net/
```

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 🌐 Production Deployment

For production use:

1. **Use a production WSGI server** (Gunicorn, uWSGI):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up HTTPS** with a reverse proxy (Nginx, Apache)

3. **Disable debug mode** in `app.py`:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

4. **Configure file upload limits** based on your needs

5. **Set up proper file cleanup** for uploads and generated folders

## 📄 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**⚠️ Disclaimer**: This tool is for educational and development purposes. Always ensure compliance with payment regulations and security standards when handling financial transactions.

**Made with ❤️ for seamless UPI QR code operations**

## Features

- ✅ **Decode QR Codes**: Read QR codes from images and extract data
- ✅ **Parse UPI Data**: Parse UPI payment strings and extract parameters like:
  - Payee UPI address
  - Payee name
  - Amount
  - Currency
  - Transaction notes
  - And more...
- ✅ **Modify Parameters**: Change UPI payment details (amount, notes, etc.)
- ✅ **Generate QR Codes**: Create new UPI QR codes with custom parameters
- ✅ **Decode and Re-encode**: Read existing QR codes and generate modified versions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `qrcode[pil]` - QR code generation
- `opencv-python` - Image processing
- `pyzbar` - QR code decoding
- `Pillow` - Image handling

### Additional System Dependencies

For `pyzbar` to work, you may need to install zbar:

**Ubuntu/Debian:**
```bash
sudo apt-get install libzbar0
```

**macOS:**
```bash
brew install zbar
```

**Windows:**
Download from: http://zbar.sourceforge.net/

## Usage

### Basic Example

```python
from qr_handler import UPIQRHandler

# Create handler instance
handler = UPIQRHandler()

# Create a UPI QR code
upi_params = {
    'payee_address': 'merchant@paytm',
    'payee_name': 'Merchant Store',
    'amount': '500',
    'currency': 'INR',
    'transaction_note': 'Payment for Order #12345'
}

upi_string = handler.create_upi_string(upi_params)
handler.encode_qr(upi_string, "payment_qr.png")
```

### Decode an Existing QR Code

```python
from qr_handler import UPIQRHandler

handler = UPIQRHandler()

# Decode QR code from image
decoded_data = handler.decode_qr("my_qr_code.png")

# Parse UPI data
if decoded_data and decoded_data.startswith('upi://'):
    upi_params = handler.parse_upi_string(decoded_data)
    print(upi_params)
```

### Decode, Modify, and Re-encode

```python
from qr_handler import UPIQRHandler

handler = UPIQRHandler()

# Decode existing QR, modify amount, and create new QR
handler.decode_and_encode(
    "original_qr.png",
    "modified_qr.png",
    modify_params={'amount': '1000', 'transaction_note': 'Updated payment'}
)
```

### Run Examples

```bash
python example.py
```

This will run multiple examples demonstrating:
1. Creating UPI QR codes from scratch
2. Decoding existing QR codes
3. Modifying and re-encoding QR codes
4. Using custom parameters

## UPI String Format

UPI payment strings follow this format:
```
upi://pay?pa=<VPA>&pn=<Name>&am=<Amount>&cu=<Currency>&tn=<Note>
```

### Supported Parameters

| Parameter | Key | Description |
|-----------|-----|-------------|
| `pa` | payee_address | UPI ID/Virtual Payment Address |
| `pn` | payee_name | Name of the payee/merchant |
| `am` | amount | Transaction amount |
| `cu` | currency | Currency code (usually INR) |
| `tn` | transaction_note | Transaction description/note |
| `tr` | transaction_ref | Transaction reference ID |
| `mc` | merchant_code | Merchant category code |
| `tid` | transaction_id | Transaction ID |

## Project Structure

```
QRcode/
├── qr_handler.py       # Main QR code handler class
├── example.py          # Usage examples
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## API Reference

### `UPIQRHandler` Class

#### Methods

- **`decode_qr(image_path: str) -> Optional[str]`**
  - Decode QR code from an image file
  - Returns the decoded string or None

- **`parse_upi_string(upi_string: str) -> Dict[str, str]`**
  - Parse UPI payment string and extract parameters
  - Returns dictionary with UPI parameters

- **`create_upi_string(upi_params: Dict[str, str]) -> str`**
  - Create UPI payment string from parameters
  - Returns formatted UPI string

- **`encode_qr(data: str, output_path: str, box_size: int = 10, border: int = 4) -> bool`**
  - Encode data into a QR code image
  - Returns True if successful

- **`decode_and_encode(input_image: str, output_image: str, modify_params: Optional[Dict[str, str]] = None) -> bool`**
  - Decode QR code, optionally modify parameters, and encode again
  - Returns True if successful

## Use Cases

1. **Payment Systems**: Generate UPI QR codes for payment collection
2. **Merchant Tools**: Create dynamic QR codes with variable amounts
3. **QR Code Analysis**: Decode and analyze existing UPI QR codes
4. **Testing**: Generate test QR codes for payment gateway testing
5. **Bulk Generation**: Create multiple QR codes programmatically

## Security Considerations

- Always validate UPI addresses before generating QR codes
- Verify amounts and payment details carefully
- Don't hardcode sensitive merchant information
- Use secure channels to distribute payment QR codes

## Troubleshooting

### "No module named 'cv2'"
Install opencv-python: `pip install opencv-python`

### "No QR code found in the image"
- Ensure the image contains a clear QR code
- Check image quality and resolution
- Try with a different image format

### pyzbar not working
Install system dependencies:
- Ubuntu: `sudo apt-get install libzbar0`
- macOS: `brew install zbar`

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available for educational and commercial use.

## Author

Created for QR code operations with UPI payment integration.

---

**Note**: This tool is for educational and development purposes. Always ensure compliance with payment regulations and security standards when handling financial transactions.