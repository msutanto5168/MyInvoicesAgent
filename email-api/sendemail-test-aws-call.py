"""
Local test harness for the Email API
This calls the deployed AWS API Gateway endpoint instead of invoking Lambda directly
"""

import json
import os
import sys
import requests

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
EMAIL_API_URL = "https://api.invoiceagent.com.au/send-email"
API_KEY = "kxLuYXzZ5Q747edWznjq1aROT9lhFua85uoJL1bB"

EMAIL_RECIPIENT = "michael.sutanto@gmail.com"

# Sample PDF data (base64 encoded)
SAMPLE_PDF_DATA = "JVBERi0xLjQKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgKG9wZW5zb3VyY2UpCjEgMCBvYmoKPDwK..."

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# ------------------------------------------------------------------
# Helper to call API
# ------------------------------------------------------------------
def call_email_api(payload: dict):
    print("\nCalling Email API...")
    print(f"URL: {EMAIL_API_URL}")
    print(f"Payload:\n{json.dumps(payload, indent=2)}")

    response = requests.post(
        EMAIL_API_URL,
        headers=HEADERS,
        data=json.dumps(payload),
        timeout=30
    )

    print(f"\nHTTP Status: {response.status_code}")

    try:
        body = response.json()
        print("Response Body:")
        print(json.dumps(body, indent=2))
    except ValueError:
        print("Raw Response:")
        print(response.text)
        body = None

    return response.status_code, body


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------
def test_simple_email():
    """Test sending a simple email (no attachment)"""
    print("\n" + "=" * 60)
    print("TEST 1: Simple Email (No Attachment)")
    print("=" * 60)

    payload = {
        "to": EMAIL_RECIPIENT,
        "subject": "Test Email - Simple",
        "email_body": """Hi Hardik,

Please find attached the rent invoice for January 2026. Please pay by the 1st of January.

* Rent for January 2026 = $5500

Breakdown:

* Rent = $5000 + GST 10% = $5500

Please pay to the following account:

    Michael Sutanto
    BSB: 083-028
    ACC: 17-800-9379

Thanks,
Michael"""
    }

    status, body = call_email_api(payload)

    if status == 200:
        print("✅ SUCCESS: Email sent successfully")
    else:
        print("❌ FAILED: Email send failed")


def test_email_with_pdf_attachment():
    """Test sending an email with PDF attachment"""
    print("\n" + "=" * 60)
    print("TEST 2: Email with PDF Attachment")
    print("=" * 60)

    payload = {
        "to": EMAIL_RECIPIENT,
        "subject": "Rental Invoice - January 2026",
        "email_body": """Hi Hardik,

Please find attached the rent invoice for January 2026. Please pay by the 1st of January.

* Rent for January 2026 = $5,348.70

Breakdown:

* Rent = $4,862.45 + GST 10% = $5,348.70

Please pay to the following account:

    Michael Sutanto
    BSB: 083-028
    ACC: 17-800-9379

Thanks,
Michael""",
        "pdf_data": SAMPLE_PDF_DATA,
        "pdf_filename": "Rental_Invoice_January2026_Shop7_477_BurwoodHighway_VermontSouth.pdf"
    }

    status, body = call_email_api(payload)

    if status == 200 and body and body.get("hasAttachment"):
        print("✅ SUCCESS: Email with attachment sent successfully")
    elif status == 200:
        print("⚠️  WARNING: Email sent but attachment missing")
    else:
        print("❌ FAILED: Email send failed")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("\n📝 Configuration Check")
    print(f"Working Directory: {os.getcwd()}")
    print(f"API URL: {EMAIL_API_URL}")

    print("\n🚀 Running tests...\n")

    # Uncomment what you want to test
    # test_simple_email()
    test_email_with_pdf_attachment()
