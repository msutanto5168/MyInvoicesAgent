"""
Local test harness for the email Lambda function
This imports and calls the Lambda function directly without API Gateway
"""

import json
import sys
import os

# Add the path to your lambda function if it's in a different directory
# sys.path.append('/path/to/your/lambda/function')

# Import your lambda function
# Make sure the file is named sendemail.py or update the import accordingly
try:
    from sendemail import lambda_handler
except ImportError:
    print("❌ ERROR: Could not import lambda_handler from sendemail.py")
    print("   Make sure sendemail.py is in the same directory or update the import path")
    sys.exit(1)

# Sample PDF data (base64 encoded)
SAMPLE_PDF_DATA = "JVBERi0xLjQKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgKG9wZW5zb3VyY2UpCjEgMCBvYmoKPDwKL0YxIDIgMCBSIC9GMiAzIDAgUiAvRjMgNCAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcgL05hbWUgL0YxIC9TdWJ0eXBlIC9UeXBlMSAvVHlwZSAvRm9udAo+PgplbmRvYmoKMyAwIG9iago8PAovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nIC9OYW1lIC9GMiAvU3VidHlwZSAvVHlwZTEgL1R5cGUgL0ZvbnQKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZE9ibGlxdWUgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcgL05hbWUgL0YzIC9TdWJ0eXBlIC9UeXBlMSAvVHlwZSAvRm9udAo+PgplbmRvYmoKNSAwIG9iago8PAovQ29udGVudHMgOSAwIFIgL01lZGlhQm94IFsgMCAwIDU5NS4yNzU2IDg0MS44ODk4IF0gL1BhcmVudCA4IDAgUiAvUmVzb3VyY2VzIDw8Ci9Gb250IDEgMCBSIC9Qcm9jU2V0IFsgL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSSBdCj4+IC9Sb3RhdGUgMCAvVHJhbnMgPDwKCj4+IAogIC9UeXBlIC9QYWdlCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9QYWdlTW9kZSAvVXNlTm9uZSAvUGFnZXMgOCAwIFIgL1R5cGUgL0NhdGFsb2cKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL0F1dGhvciAoYW5vbnltb3VzKSAvQ3JlYXRpb25EYXRlIChEOjIwMjUxMjI2MTExODEwKzAwJzAwJykgL0NyZWF0b3IgKGFub255bW91cykgL0tleXdvcmRzICgpIC9Nb2REYXRlIChEOjIwMjUxMjI2MTExODEwKzAwJzAwJykgL1Byb2R1Y2VyIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSBcKG9wZW5zb3VyY2VcKSkgCiAgL1N1YmplY3QgKHVuc3BlY2lmaWVkKSAvVGl0bGUgKHVudGl0bGVkKSAvVHJhcHBlZCAvRmFsc2UKPj4KZW5kb2JqCjggMCBvYmoKPDwKL0NvdW50IDEgL0tpZHMgWyA1IDAgUiBdIC9UeXBlIC9QYWdlcwo+PgplbmRvYmoKOSAwIG9iago8PAovRmlsdGVyIFsgL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlIF0gL0xlbmd0aCAxNTE5Cj4+CnN0cmVhbQpHYXQ9K2dOKiI9JjpPOlNGT2JdSDhCTj8lZVZuX1smN1hcLV8jYDZkUCxeKTtiPTJkXFk3VGdUbiRlRF4pQUovYydHa0paZSdrNDUxSGNFWElWQUY+UjAuUFlxIjBnUUFgLGNSJ29pOm8jKCQ3ZGFVbFNjPVUmOUsiN1M8JmsmTGJWN05KVG8lSzc9Y2Y1VENhX0klNmlqKlNPKG4yTChEQj0mXC0hPDRHQSsjZkJDJS5mamYmSTFvYDdCQk9MbFpvPXFHJV0vJzcwUipARmddOGQkZjtudW4yWFtMQDFrY0A7azFZYmZgMXJlOmZzK05BTkdYQmxhOC1AQy9KcjwiSCtaO2lMYU1rNUVkUFVubCJROzBVZV4nP0VkLF5VIy0jSzM0RE5mX2thblldRWhfLCJTW0VwIUpGQyVoRTZVKy9YVCVsQmI4UltqWExdVEMmSWRQb0BUSkxvO1sqJk9Fa0g+M3JQTmVuOyItQEk3K0pjPm04PltvRigpPTFuN1xYUShIcy9sUUNlISYxcktVJD90X1FEWXUuKE85SlUhLlEoWXUxWEE3TTE0NypRY3E+LHRxS2VZWUBANWNGPlxWaDJYSSQtMzJwITo0ViouLkNkXmZcciY8X1JAaENfLkRiUk9TTTdgamg5MFRHKmJGO3RKW1trJyRWMkk6IixjSEZ1WE5tdTUtMDxTL2ppJ1ciYDBeTyIxYG5dKmpJM1glWHJQMCtKTWxWaF9eVTNyR1g1NClYSjg1O2RiQidvWCxwXEpbKFc+OW42VUtSYW5DUVhfXEdSJmhGVm4xWyRjPk9xcysoYnBpVzlzKlpDWlxGYCk1PGw9RjImPjxeRiJxUlllV0tVKFpdRT1nYVkvN1AyLyUwWFZgMidtbiFNcF1dLnBUYk1UTGFfTWtcPiw4XF1iW2ExVD9VYDtpZjNmJHVANTxsWz07Qz9VU0ppMT5HQG9ub1ZoS2FNRip1cVtWTjtFaVlGJj51UFtNRXVEaTpfblJyZ0dbNj9yP09rJzRCWUJFP1khK1w+c09iLlVsNlxMMHBuVWVZVTw1MktXJUo5biddRWkoZWBOciFzS0lsT0JmIVY8KjM+cS07T1g1WCJqQ3JwVGg5TSlKUDlDcktfYTpfZzozTUVCQ1ZnVVk+KzhHTkY2bXAvP04yRWAzZkQrQnEuOCZAWmBjQmlmMGghdV5qbW9tVks1RHJQRi5aOUJtS1QyIUJmJTpDbkk3XztbX2ZWREI4TUJgLi1hMCdGXEA5VD01Yz5WNzBsWC81cXBGYlUyX2U8WyonRjRPNSVtL2ldPWZPaUxTSlBHRE5nPitWXSFuZ2VjPC9OVFJMMTNCTidRcChJWlpnQ1BbbSotIilQLlNjXy5rTnVLPEQyPT9xTl08SzVrRlRRQ1A2VkJKISdAblRpK1Rcb1QwaTlbIUYiZi05PUg9YUEqTFFQPExsNk9GPmdwcFksajRjUCpgRSc4QVcrPCprLFk9JmxBV0lqODRqJG9cMj01YytAKWskRkZDNy5WWi5NTFtkYjdtP2EvQktJPDlIYG5fKlVEZXE0OllWIWkrR1ZRTkU7UllxW1hkayYycnVsX1YlamNfWmFFcnBbOEE1KHIkXVEwblErRig/W05WZDhfMUQ6cCslbjQvLydjLygwI2s9akBUREwxRipZVFVGcWdxQlRAYGw4PV9zUCU5QzEoUV1HZ2FvXVBKdGQjO1szMFlHRXIxaUZxWmBmZ0Q3NWcnTzxULkZbJmEvaUpBI0REcz5LaWRzLWgsMDo4ISlzb3BSXVUnSlkqM3BUTU9EajguclVyTzxrJTM4VlJ0XFs2S0dXdFswXFs6O0cjZSdLKDtFPXNCKl1pSkdkVSdvLU5VWD40bjk/VDJGIypyMidZPTduTFJicSkwYlNPVjBTN1lEJFE4UG5vaExzX0hybjckIytualI0V1gtYWloRUgwXWtBaERwZnNbaUQ1KkYwM0g4cVhBP11LIV5CYC8jYGtLSzZOcyJZJW5UJTMvSH4+ZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgMTAKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDYxIDAwMDAwIG4gCjAwMDAwMDAxMTIgMDAwMDAgbiAKMDAwMDAwMDIxOSAwMDAwMCBuIAowMDAwMDAwMzMxIDAwMDAwIG4gCjAwMDAwMDA0NTAgMDAwMDAgbiAKMDAwMDAwMDY1MyAwMDAwMCBuIAowMDAwMDAwNzIxIDAwMDAwIG4gCjAwMDAwMDA5ODIgMDAwMDAgbiAKMDAwMDAwMTA0MSAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9JRCAKWzxlMmY1NDc0N2M1YjcxODYzOTIxNWM4YjQyZjI1NzBjOT48ZTJmNTQ3NDdjNWI3MTg2MzkyMTVjOGI0MmYyNTcwYzk+XQolIFJlcG9ydExhYiBnZW5lcmF0ZWQgUERGIGRvY3VtZW50IC0tIGRpZ2VzdCAob3BlbnNvdXJjZSkKCi9JbmZvIDcgMCBSCi9Sb290IDYgMCBSCi9TaXplIDEwCj4+CnN0YXJ0eHJlZgoyNjUxCiUlRU9GCg=="
EMAIL_RECIPIENT = "michael.sutanto@gmail.com"


def test_simple_email():
    """Test sending a simple email without attachment"""
    print("\n" + "="*50)
    print("TEST 1: Simple Email (No Attachment)")
    print("="*50)

    email_message = """Hi Hardik,

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
    
    event = {
        "to": EMAIL_RECIPIENT,  # Change this to your verified email
        "subject": "Test Email - Simple",
        "email_body": email_message
    }
    
    context = {}  # Context object (not used but required by Lambda)
    
    print(f"\nCalling lambda_handler locally...")
    print(f"Event: {json.dumps(event, indent=2)}")
    
    try:
        response = lambda_handler(event, context)
        
        print(f"\nResponse Status: {response['statusCode']}")
        print(f"Response Body: {json.dumps(json.loads(response['body']), indent=2)}")
        
        if response['statusCode'] == 200:
            print("✅ SUCCESS: Email sent successfully!")
        else:
            print("❌ FAILED: Email sending failed")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


def test_email_with_pdf_attachment():
    """Test sending an email with PDF attachment (using base64 encoded PDF)"""
    print("\n" + "="*50)
    print("TEST 3: Email with PDF Attachment")
    print("="*50)
    
    event = {
        "to": EMAIL_RECIPIENT,  # Change this
        "subject": "Rental Invoice - January 2026",
        "email_body": """Hi Hardik,

Please find attached the rent invoice for  November 2025.  Please pay by the 1st of  November.  

* Rent for November 2025 =  $5,348.70
* Water Usage Aug - Oct 2025 = $92.77

Breakdown:

* Rent = $4862.45 + GST 10% + $92.77 = $5,441.47

Please pay to the following account: 

    Michael Sutanto 
    BSB: 083-028 
    ACC: 17-800-9379  


Thanks,
Michael""",
        "pdf_data": SAMPLE_PDF_DATA,  # Base64 encoded PDF
        "pdf_filename": "Rental_Invoice_January2026_Shop7_477_BurwoodHighway_VermontSouth.pdf"
    }
    
    context = {}
    
    print(f"\nCalling lambda_handler locally...")
    print(f"Subject: {event['subject']}")
    print(f"PDF Filename: {event['pdf_filename']}")
    print(f"PDF Data Length: {len(event['pdf_data'])} characters")
    
    try:
        response = lambda_handler(event, context)
        
        print(f"\nResponse Status: {response['statusCode']}")
        print(f"Response Body: {json.dumps(json.loads(response['body']), indent=2)}")
        
        if response['statusCode'] == 200:
            result = json.loads(response['body'])
            if result.get('hasAttachment'):
                print("✅ SUCCESS: Email with PDF attachment sent successfully!")
            else:
                print("⚠️  WARNING: Email sent but without attachment")
        else:
            print("❌ FAILED: Email sending failed")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

def test_email_with_pdf_attachment2():
    """Test sending an email with PDF attachment (using base64 encoded PDF)"""
    print("\n" + "="*50)
    print("TEST 3: Email with PDF Attachment")
    print("="*50)
    
    event = {
        "to": EMAIL_RECIPIENT,  # Change this
        "subject": "Rental Invoice - January 2026",
        "email_body": """Hi Hardik,

Please find attached the rent invoice for January 2026. Please pay by the 1st of January.

* Rent for January 2026 = $5,348.70

Breakdown:

* Rent = $4862.45 + GST 10% = $5348.70

Please pay to the following account:

    Michael Sutanto
    BSB: 083-028
    ACC: 17-800-9379

Thanks,
Michael""",
        "pdf_data": SAMPLE_PDF_DATA,  # Base64 encoded PDF
        "pdf_filename": "Rental_Invoice_January2026_Shop7_477_BurwoodHighway_VermontSouth.pdf"
    }
    
    context = {}
    
    print(f"\nCalling lambda_handler locally...")
    print(f"Subject: {event['subject']}")
    print(f"PDF Filename: {event['pdf_filename']}")
    print(f"PDF Data Length: {len(event['pdf_data'])} characters")
    
    try:
        response = lambda_handler(event, context)
        
        print(f"\nResponse Status: {response['statusCode']}")
        print(f"Response Body: {json.dumps(json.loads(response['body']), indent=2)}")
        
        if response['statusCode'] == 200:
            result = json.loads(response['body'])
            if result.get('hasAttachment'):
                print("✅ SUCCESS: Email with PDF attachment sent successfully!")
            else:
                print("⚠️  WARNING: Email sent but without attachment")
        else:
            print("❌ FAILED: Email sending failed")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n📝 Configuration Check:")
    print(f"   Working Directory: {os.getcwd()}")
    
    # Check if sendemail.py exists
    if not os.path.exists("sendemail.py"):
        print("\n❌ ERROR: sendemail.py not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print("   Please ensure sendemail.py is in the same directory as this test script")
        sys.exit(1)
    
    # Choose which tests to run
    print("\n🚀 Running tests...\n")
    
    # Run individual tests
    # test_simple_email()
    # test_email_with_pdf_attachment()
    