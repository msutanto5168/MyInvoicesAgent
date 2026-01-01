import json
import base64
import requests
import re

# 🔐 Your API details
API_URL = "https://api.invoiceagent.com.au/subway-invoice"
API_KEY = "kxLuYXzZ5Q747edWznjq1aROT9lhFua85uoJL1bB"

# Test payload
payload = {
    "date": "December 24, 2025",
    "due_date": "January 1, 2026",
    "invoice_number": "00219",
    "items": [{
        "description": (
            "Rent for shop 7/477 Burwood Highway "
            "January 01 - January 31 2026 testing extra characters here"
        ),
        "amount": 4862.45
    }],
    "gst_amount": 486.25,
    "property_line1": "Shop 7/477 Burwood",
    "property_line2": "Highway Vermont South"
}

# HTTP request
response = requests.post(
    API_URL,
    headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    },
    data=json.dumps(payload)
)

# Handle response
if response.status_code == 200:
    # Extract filename from Content-Disposition header
    content_disposition = response.headers.get('Content-Disposition', '')
    
    # Parse filename from header (format: "inline; filename=Rental_Invoice_...")
    filename_match = re.search(r'filename=([^;]+)', content_disposition)
    
    if filename_match:
        filename = filename_match.group(1).strip()
    else:
        filename = 'aws_api_invoice_test.pdf'  # Fallback
    
    # Decode and save PDF
    pdf_bytes = base64.b64decode(response.text)
    with open(filename, "wb") as f:
        f.write(pdf_bytes)

    print(f"✅ Invoice generated: {filename}")
    print(f"   Content-Disposition: {content_disposition}")
else:
    print("❌ Error")
    print("Status:", response.status_code)
    print("Response:", response.text)