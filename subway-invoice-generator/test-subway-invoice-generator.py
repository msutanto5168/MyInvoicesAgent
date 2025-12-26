import json
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
    "gst_amount": 486.25
}

# Call the lambda handler
response = lambda_handler(test_event, None)

# Save the PDF
if response['statusCode'] == 200:
    import base64
    pdf_data = base64.b64decode(response['body'])
    with open('lambda_test_invoice.pdf', 'wb') as f:
        f.write(pdf_data)
    print("✅ Invoice generated: lambda_test_invoice.pdf")
else:
    print(f"❌ Error: {response}")