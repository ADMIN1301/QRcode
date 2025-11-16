"""
Example usage of UPI QR Code Handler
Demonstrates various operations with QR codes
"""

from qr_handler import UPIQRHandler


def example_1_create_upi_qr():
    """Example 1: Create a UPI payment QR code from scratch"""
    print("=" * 50)
    print("EXAMPLE 1: Create UPI QR Code from scratch")
    print("=" * 50)
    
    handler = UPIQRHandler()
    
    # Define UPI payment parameters
    upi_params = {
        'payee_address': 'merchant@paytm',  # UPI ID
        'payee_name': 'Merchant Store',      # Merchant name
        'amount': '500',                      # Amount in INR
        'currency': 'INR',                    # Currency code
        'transaction_note': 'Order #12345'   # Transaction description
    }
    
    # Create UPI string
    upi_string = handler.create_upi_string(upi_params)
    print(f"\nGenerated UPI String:\n{upi_string}\n")
    
    # Generate QR code
    handler.encode_qr(upi_string, "created_upi_qr.png")
    print("\n✓ QR code created successfully!\n")


def example_2_decode_qr():
    """Example 2: Decode an existing QR code"""
    print("=" * 50)
    print("EXAMPLE 2: Decode existing QR Code")
    print("=" * 50)
    
    handler = UPIQRHandler()
    
    # First create a sample QR code to decode
    upi_params = {
        'payee_address': 'test@upi',
        'payee_name': 'Test Merchant',
        'amount': '250',
        'currency': 'INR'
    }
    upi_string = handler.create_upi_string(upi_params)
    handler.encode_qr(upi_string, "sample_qr_to_decode.png")
    
    # Now decode it
    print("\nDecoding QR code from: sample_qr_to_decode.png")
    decoded_data = handler.decode_qr("sample_qr_to_decode.png")
    
    if decoded_data:
        print(f"\nRaw decoded data:\n{decoded_data}\n")
        
        # Parse UPI data if it's a UPI string
        if decoded_data.startswith('upi://'):
            handler.parse_upi_string(decoded_data)
            print("\n✓ QR code decoded successfully!\n")


def example_3_decode_and_modify():
    """Example 3: Decode QR code, modify parameters, and re-encode"""
    print("=" * 50)
    print("EXAMPLE 3: Decode, Modify, and Re-encode")
    print("=" * 50)
    
    handler = UPIQRHandler()
    
    # Create original QR code
    original_params = {
        'payee_address': 'shop@upi',
        'payee_name': 'My Shop',
        'amount': '100',
        'currency': 'INR',
        'transaction_note': 'Original Payment'
    }
    
    print("\nOriginal UPI Parameters:")
    for key, value in original_params.items():
        print(f"  {key}: {value}")
    
    upi_string = handler.create_upi_string(original_params)
    handler.encode_qr(upi_string, "original_qr.png")
    print("\n✓ Original QR code created: original_qr.png")
    
    # Decode, modify amount and note, then re-encode
    print("\n" + "-" * 50)
    print("Modifying amount to 200 and updating transaction note...")
    print("-" * 50)
    
    modifications = {
        'amount': '200',
        'transaction_note': 'Modified Payment'
    }
    
    handler.decode_and_encode(
        "original_qr.png",
        "modified_qr.png",
        modify_params=modifications
    )
    print("\n✓ Modified QR code created: modified_qr.png\n")


def example_4_decode_real_qr():
    """Example 4: Decode a real UPI QR code (user provides the image)"""
    print("=" * 50)
    print("EXAMPLE 4: Decode your own QR Code")
    print("=" * 50)
    
    print("""
To use this example:
1. Save your UPI QR code image as 'my_qr_code.png' in this directory
2. Uncomment the code below
3. Run this script again
""")
    
    # Uncomment below to decode your own QR code
    """
    handler = UPIQRHandler()
    
    # Decode your QR code
    decoded_data = handler.decode_qr("my_qr_code.png")
    
    if decoded_data and decoded_data.startswith('upi://'):
        # Parse and display UPI details
        upi_params = handler.parse_upi_string(decoded_data)
        
        # Re-encode with modifications (optional)
        # modify_params = {'amount': '999'}
        # handler.decode_and_encode("my_qr_code.png", "new_qr.png", modify_params)
    """


def example_5_create_dynamic_qr():
    """Example 5: Create QR code with user input"""
    print("=" * 50)
    print("EXAMPLE 5: Create QR Code with dynamic input")
    print("=" * 50)
    
    print("""
This example shows how to create a QR code with user input.
Uncomment the code below to try it interactively.
""")
    
    # Uncomment below for interactive QR code creation
    """
    handler = UPIQRHandler()
    
    print("\nEnter UPI Payment Details:")
    upi_params = {
        'payee_address': input("UPI ID (e.g., merchant@paytm): "),
        'payee_name': input("Payee Name: "),
        'amount': input("Amount (INR): "),
        'currency': 'INR',
        'transaction_note': input("Transaction Note: ")
    }
    
    upi_string = handler.create_upi_string(upi_params)
    output_file = input("\nOutput filename (e.g., my_qr.png): ")
    
    handler.encode_qr(upi_string, output_file)
    print(f"\n✓ QR code created: {output_file}\n")
    """


def main():
    """Run all examples"""
    print("\n")
    print("*" * 50)
    print("UPI QR CODE HANDLER - EXAMPLES")
    print("*" * 50)
    print("\n")
    
    # Run examples
    example_1_create_upi_qr()
    print("\n")
    
    example_2_decode_qr()
    print("\n")
    
    example_3_decode_and_modify()
    print("\n")
    
    example_4_decode_real_qr()
    print("\n")
    
    example_5_create_dynamic_qr()
    print("\n")
    
    print("*" * 50)
    print("All examples completed!")
    print("Check the generated QR code images in this directory.")
    print("*" * 50)


if __name__ == "__main__":
    main()
