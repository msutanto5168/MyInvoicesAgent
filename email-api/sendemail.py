import json
import boto3
import base64
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Initialize SES client
ses_client = boto3.client('ses', region_name='ap-southeast-2')

def lambda_handler(event, context):
    """
    Lambda function to send email via AWS SES with optional PDF attachment
    
    Expected event format:
    {
        "to": "recipient@example.com",
        "subject": "Email Subject",
        "email_body": "Email body content (plain text or HTML)",
        "pdf_data": "base64_encoded_pdf_string",  # Optional: base64 encoded PDF
        "pdf_filename": "invoice.pdf"  # Optional: custom filename for PDF
    }
    
    If pdf_data is provided, it will be attached to the email.
    """
    
    try:

        print("Received event:", json.dumps(event))        

        # Parse the incoming event
        if 'body' in event and event['body']:
            # API Gateway format
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            # Direct invocation format
            body = event
        
        # Extract email parameters
        to_email = body.get('to')
        subject = body.get('subject')
        email_body = body.get('email_body')
        pdf_data = body.get('pdf_data')  # Optional: base64 encoded PDF string
        pdf_filename = body.get('pdf_filename', 'invoice.pdf')  # Optional: custom filename
        
        # Validate required fields
        if not to_email or not subject or not email_body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing required fields: to, subject, and email_body are required'
                })
            }
        
        # Check if we need to attach a PDF
        pdf_attachment = None
        
        if pdf_data:
            try:
                # Decode the base64 PDF data
                if isinstance(pdf_data, str):
                    pdf_attachment = base64.b64decode(pdf_data)
                else:
                    # If it's already bytes, use as-is
                    pdf_attachment = pdf_data
                    
            except Exception as e:
                print(f"Error decoding PDF data: {str(e)}")
                # Continue without attachment if PDF decoding fails
                pdf_attachment = None
        
        # Send email with or without attachment
        if pdf_attachment:
            response = send_email_with_attachment(
                to_email, 
                subject, 
                email_body, 
                pdf_attachment, 
                pdf_filename
            )
        else:
            response = send_simple_email(to_email, subject, email_body)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'messageId': response['MessageId'],
                'message': 'Email sent successfully',
                'hasAttachment': pdf_attachment is not None
            })
        }
        
    except ClientError as e:
        # Handle SES-specific errors
        error_message = e.response['Error']['Message']
        print(f"SES Error: {error_message}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Failed to send email: {error_message}'
            })
        }
        
    except Exception as e:
        # Handle any other errors
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'An unexpected error occurred: {str(e)}'
            })
        }


def send_simple_email(to_email, subject, email_body):
    """Send a simple email without attachments"""
    html_email = invoice_text_to_html(email_body)

    return ses_client.send_email(
        Source='noreply@invoiceagent.com.au',
        Destination={
            'ToAddresses': [to_email]
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {                
                'Html': {
                    'Data': html_email,
                    'Charset': 'UTF-8'
                }
            }
        }
    )


def send_email_with_attachment(to_email, subject, email_body, pdf_bytes, pdf_filename):
    """Send an email with PDF attachment using raw email"""
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'noreply@invoiceagent.com.au'
    msg['To'] = to_email


    html_email = MIMEText(invoice_text_to_html(email_body), 'html', 'utf-8')
    msg.attach(html_email)
    
    # Add PDF attachment
    pdf_part = MIMEApplication(pdf_bytes, _subtype='pdf')
    pdf_part.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
    msg.attach(pdf_part)
    
    # Send raw email
    return ses_client.send_raw_email(
        Source='noreply@invoiceagent.com.au',
        Destinations=[to_email],
        RawMessage={
            'Data': msg.as_string()
        }
    )

def invoice_text_to_html(text: str) -> str:
    lines = text.strip().split("\n")
    html_parts = []

    in_list = False
    in_bank_block = False
    bank_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Empty line
        if not line.strip():
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            i += 1
            continue

        # Bullet points
        if line.lstrip().startswith("* "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{line.lstrip()[2:]}</li>")
            i += 1
            continue

        # Bank details (indented)
        if line.startswith("    "):
            in_bank_block = True
            bank_lines.append(line.strip())
            i += 1
            continue

        # Flush bank block
        if in_bank_block:
            html_parts.append(
                "<div style='margin-left: 36px;'>"
                + "<br>".join(bank_lines)
                + "</div>"
            )
            bank_lines = []
            in_bank_block = False

        # Close list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

        # Signature detection: Thanks, + next line
        if line.strip().lower() == "thanks," and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            html_parts.append(f"<p>Thanks,<br>{next_line}</p>")
            i += 2
            continue

        if line.strip().lower().startswith("please pay"):
            html_parts.append(f"<br><p>{line}</p>")
            i += 1
            continue

        # Normal paragraph
        html_parts.append(f"<p>{line}</p>")
        i += 1

    # Final flush
    if in_list:
        html_parts.append("</ul>")

    if in_bank_block:
        html_parts.append(
            "<div style='margin-left: 36px;'>"
            + "<br>".join(bank_lines)
            + "</div>"
        )

    return "\n".join(html_parts)

