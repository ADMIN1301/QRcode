"""
QR Code Handler for UPI Payment QR Codes
Decode and encode UPI payment QR codes
"""

import cv2
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import urllib.parse
from typing import Dict, Optional


class UPIQRHandler:
    """Handle UPI QR code operations - decode and encode"""
    
    def __init__(self):
        self.upi_data = {}
    
    def decode_qr(self, image_path: str) -> Optional[str]:
        """
        Decode QR code from an image file
        
        Args:
            image_path: Path to the QR code image
            
        Returns:
            Decoded string data or None if decoding fails
        """
        try:
            # Read the image
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error: Could not read image from {image_path}")
                return None
            
            # Decode QR code
            decoded_objects = decode(img)
            
            if not decoded_objects:
                print("No QR code found in the image")
                return None
            
            # Get the data from the first QR code found
            qr_data = decoded_objects[0].data.decode('utf-8')
            print(f"Decoded QR code: {qr_data}")
            
            return qr_data
            
        except Exception as e:
            print(f"Error decoding QR code: {e}")
            return None
    
    def parse_upi_string(self, upi_string: str) -> Dict[str, str]:
        """
        Parse UPI payment string and extract parameters
        
        UPI format: upi://pay?pa=<VPA>&pn=<Name>&am=<Amount>&cu=<Currency>&tn=<Note>
        
        Args:
            upi_string: UPI payment string
            
        Returns:
            Dictionary containing UPI parameters
        """
        upi_params = {}
        
        try:
            # Check if it's a UPI string
            if not upi_string.startswith('upi://'):
                print("Not a UPI payment string")
                return upi_params
            
            # Parse the URL
            parsed = urllib.parse.urlparse(upi_string)
            query_params = urllib.parse.parse_qs(parsed.query)
            
            # Extract common UPI parameters
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
            
            self.upi_data = upi_params
            
            print("\n=== UPI Payment Details ===")
            for key, value in upi_params.items():
                print(f"{key}: {value}")
            print("==========================\n")
            
            return upi_params
            
        except Exception as e:
            print(f"Error parsing UPI string: {e}")
            return upi_params
    
    def create_upi_string(self, upi_params: Dict[str, str]) -> str:
        """
        Create UPI payment string from parameters
        
        Args:
            upi_params: Dictionary containing UPI parameters
            
        Returns:
            UPI payment string
        """
        # Reverse mapping
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
        
        # Build query parameters
        query_parts = []
        for key, value in upi_params.items():
            upi_key = param_mapping.get(key, key)
            encoded_value = urllib.parse.quote(str(value))
            query_parts.append(f"{upi_key}={encoded_value}")
        
        # Create UPI string
        upi_string = f"upi://pay?{'&'.join(query_parts)}"
        
        return upi_string
    
    def encode_qr(self, data: str, output_path: str = "output_qr.png", 
                  box_size: int = 10, border: int = 4) -> bool:
        """
        Encode data into a QR code and save as image
        
        Args:
            data: String data to encode
            output_path: Path to save the QR code image
            box_size: Size of each box in pixels
            border: Border size in boxes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,  # Controls the size of the QR code
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border,
            )
            
            # Add data
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save image
            img.save(output_path)
            print(f"QR code saved to: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Error encoding QR code: {e}")
            return False
    
    def decode_and_encode(self, input_image: str, output_image: str = "regenerated_qr.png",
                         modify_params: Optional[Dict[str, str]] = None) -> bool:
        """
        Decode a QR code, optionally modify UPI parameters, and encode it again
        
        Args:
            input_image: Path to input QR code image
            output_image: Path to save regenerated QR code
            modify_params: Dictionary of parameters to modify (optional)
            
        Returns:
            True if successful, False otherwise
        """
        # Decode the original QR code
        decoded_data = self.decode_qr(input_image)
        if not decoded_data:
            return False
        
        # If it's a UPI string, parse it
        if decoded_data.startswith('upi://'):
            upi_params = self.parse_upi_string(decoded_data)
            
            # Modify parameters if provided
            if modify_params:
                print(f"\nModifying parameters: {modify_params}")
                upi_params.update(modify_params)
            
            # Create new UPI string
            new_data = self.create_upi_string(upi_params)
        else:
            # If not UPI, just use the original data
            new_data = decoded_data
        
        # Encode to new QR code
        success = self.encode_qr(new_data, output_image)
        
        return success


def main():
    """Example usage"""
    handler = UPIQRHandler()
    
    # Example 1: Create a UPI QR code from scratch
    print("=== Creating UPI QR Code ===")
    upi_params = {
        'payee_address': 'example@upi',
        'payee_name': 'Merchant Name',
        'amount': '100',
        'currency': 'INR',
        'transaction_note': 'Payment for services'
    }
    
    upi_string = handler.create_upi_string(upi_params)
    handler.encode_qr(upi_string, "sample_upi_qr.png")
    
    # Example 2: Decode and re-encode (modify if needed)
    print("\n=== Decode and Re-encode ===")
    # Uncomment below to decode an existing QR code
    # handler.decode_and_encode("input_qr.png", "output_qr.png", 
    #                           modify_params={'amount': '200'})


if __name__ == "__main__":
    main()
