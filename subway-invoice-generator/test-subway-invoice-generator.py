import json
import base64
import re
from subway import lambda_handler  # Replace with your actual filename

# Test data
test_event = {
    "date": "December 24, 2025",
    "due_date": "January 1, 2026",
    "invoice_number": "00219",
    "items": [{
        "description": "Rent for shop 7/477 Burwood Highway January 01 - January 31 2026 testing extra characters here",
        "amount": 4862.45
    }],
    "gst_amount": 486.25,
    "property_line1": "Shop 7/477 Burwood",
    "property_line2": "Highway Vermont South"
}

# Call the lambda handler
response = lambda_handler(test_event, None)

# Save the PDF with dynamic filename
if response['statusCode'] == 200:
    # Extract filename from Content-Disposition header
    content_disposition = response['headers'].get('Content-Disposition', '')
    
    # Parse filename from header (format: "inline; filename=Rental_Invoice_...")
    filename_match = re.search(r'filename=([^;]+)', content_disposition)
    
    if filename_match:
        filename = filename_match.group(1).strip()
    else:
        filename = 'lambda_test_invoice.pdf'  # Fallback
    
    # Decode and save PDF
    pdf_data = base64.b64decode(response['body'])
    with open(filename, 'wb') as f:
        f.write(pdf_data)
    
    print(f"✅ Invoice generated: {filename}")
    print(f"   Content-Disposition: {content_disposition}")
else:
    print(f"❌ Error: {response}")