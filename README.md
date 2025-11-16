# UPI QR Code Reader and Generator

A Python-based tool to decode, parse, modify, and encode UPI (Unified Payments Interface) payment QR codes. This project allows you to read UPI QR codes, extract payment information, modify parameters, and generate new QR codes.

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