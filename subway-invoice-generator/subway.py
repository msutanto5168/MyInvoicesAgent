from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.styles import ParagraphStyle

import io
import base64
import json
from datetime import datetime


def lambda_handler(event, context):
    # CORS headers for all responses
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,x-api-key",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    # Handle OPTIONS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }
    
    # -------------------------------
    # Parse incoming payload
    # -------------------------------
    body = event.get("body", event)
    if isinstance(body, str):
        body = json.loads(body)

    # Safe extraction of fields
    date = body.get("date", "")
    due_date = body.get("due_date", "")
    invoice_number = body.get("invoice_number", "")
    items = body.get("items", [])
    gst_amount = body.get("gst_amount", 0.0)
    bill_to_name = body.get("bill_to_name", "Hardik Patel")
    bill_to_company = body.get("bill_to_company", "Jai Sainath Pty LTD, ABN: 88158023039")
    bill_to_address = body.get("bill_to_address", "2C Ernest Street")
    bill_to_suburb = body.get("bill_to_suburb", "Bayswater VIC 3153")
    property_line1 = body.get("property_line1", "Shop 7/477 Burwood")
    property_line2 = body.get("property_line2", "Highway Vermont South")

    # -------------------------------
    # Generate dynamic filename
    # -------------------------------
    def generate_filename(date_str, property_line1, property_line2):
        """Generate filename in format: Rental_Invoice_January2026_Shop7_477_BurwoodHighway_VermonthSouth.pdf"""
        try:
            # Parse date string (assumes format like "December 24, 2025")
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            month_year = date_obj.strftime("%B%Y")  # e.g., "January2026"
        except:
            # Fallback if date parsing fails
            month_year = "Unknown"
        
        # Clean and format property address
        # Remove special characters and spaces, replace with underscores
        property_clean = property_line1.replace("/", "_").replace(" ", "")
        property2_clean = property_line2.replace(" ", "")
        
        filename = f"Rental_Invoice_{month_year}_{property_clean}_{property2_clean}.pdf"
        return filename
    
    filename = generate_filename(date, property_line1, property_line2)

    # -------------------------------
    # Create PDF
    # -------------------------------
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    leftmargin = 60
    topmargin = height - 80
    rightmargin = width - 60

    font = "Helvetica"
    fontbold = font + "-Bold"
    fontboldOblique = font + "-BoldOblique"
    dark_grey = Color(0.2, 0.2, 0.2)  
    light_grey = Color(0.7, 0.7, 0.7)  


    # -------------------------------
    # LOGO
    # -------------------------------
    # logo_path = "subway-logo.png"   # must exist in Lambda package or /tmp
    # logo_width = 120               # points (adjust as needed)
    # logo_height = 50               # points (adjust as needed)

    # logo_x = (width - logo_width) / 2
    # logo_y = height - logo_height - 30  # top margin spacing

    # pdf.drawImage(
    #     logo_path,
    #     logo_x,
    #     logo_y,
    #     width=logo_width,
    #     height=logo_height,
    #     preserveAspectRatio=True,
    #     mask="auto"
    # )

    # -------------------------------
    # LEFT Header Section
    # -------------------------------
    pdf.setFillColor(colors.black)
    pdf.setFont(fontbold, 12)
    pdf.drawString(leftmargin, topmargin - 40, "J GAO & M SUTANTO & N.R SUTANTO")

    pdf.setFillColor(dark_grey)
    pdf.setFont(fontboldOblique, 10)
    pdf.drawString(leftmargin, topmargin - 62, "ABN: 7140291689356 (Registered for GST)")

    pdf.setFont(font, 9)
    pdf.drawString(leftmargin, topmargin - 84, "7 Granite Way")
    pdf.drawString(leftmargin, topmargin - 98, "Keilor East VIC 3033")
    pdf.drawString(leftmargin, topmargin - 112, "Phone: 0439 074 031  Email: michael.sutanto@gmail.com")    

    pdf.setFont(fontbold, 9)
    pdf.drawString(leftmargin, topmargin - 140, "BILL TO:")
    pdf.setFont(font, 9)
    pdf.drawString(leftmargin, topmargin - 154, bill_to_name)
    pdf.drawString(leftmargin, topmargin - 168, bill_to_company)
    pdf.drawString(leftmargin, topmargin - 182, bill_to_address)
    pdf.drawString(leftmargin, topmargin - 196, bill_to_suburb)
    pdf.drawString(leftmargin, topmargin - 210, "Phone: 0430 450 819  Email: hardik_1210@yahoo.com")    

    # -------------------------------
    # RIGHT Header Section
    # -------------------------------
    pdf.setFillColor(light_grey)
    pdf.setFont(fontbold, 24)
    pdf.drawRightString(rightmargin, topmargin - 40, "RENT INVOICE")

    pdf.setFillColor(colors.black)
    pdf.setFont(fontbold, 9)
    pdf.drawString(rightmargin - 170, topmargin - 80, "DATE:")
    pdf.drawString(rightmargin - 170, topmargin - 94, "DUE DATE:")
    pdf.drawString(rightmargin - 170, topmargin - 108, "INVOICE #")
    pdf.drawString(rightmargin - 170, topmargin - 122, "FOR:")

    pdf.setFont(font, 9)
    pdf.drawRightString(rightmargin, topmargin - 80, date)
    pdf.drawRightString(rightmargin, topmargin - 94, due_date)
    pdf.drawRightString(rightmargin, topmargin - 108, invoice_number)
    pdf.drawRightString(rightmargin, topmargin - 122, property_line1)
    pdf.drawRightString(rightmargin, topmargin - 136, property_line2)

    # -------------------------------
    # TABLE DATA
    # -------------------------------
    description_style = ParagraphStyle(
        name="DescriptionStyle",
        fontName=font,       
        fontSize=9,
        leading=11,          
    )

    table_data = [["DESCRIPTION", "HOURS", "RATE", "AMOUNT"]]

    subtotal = 0.0
    for item in items:
        table_data.append([
            Paragraph(item["description"], description_style),
            item.get("hours", ""),
            item.get("rate", ""),
            f"${item['amount']:,.2f}"
        ])
        subtotal += item["amount"]
    
    for _ in range(7 - len(items)):
        table_data.append(["", "", "", "-"])

    table_data.append(["", "", "SUBTOTAL", f"${subtotal:,.2f}"])    
    table_data.append(["GST Applied to rent component only", "", "GST 10%", f"${gst_amount:,.2f}"])
    table_data.append(["", "", "TOTAL", f"${subtotal + gst_amount:,.2f}"])

    table = Table(table_data, colWidths=[100 * mm, 20 * mm, 20 * mm, 30 * mm])

    styles = [
        ("BOX", (0, 0), (-1, -4), 0.75, colors.black),
        ("LINEBEFORE", (1, 0), (-1, -4), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "RIGHT"),
        ("ALIGN", (2, -3), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONT", (0, 0), (-1, 0), font, 9),
        ("FONT", (0, 1), (0, -4), font, 9),
        ("FONT", (2, -1), (3, -1), fontbold, 9),
    ]

    for row in range(1, len(table_data)-3):
        if row % 2 == 0:
            styles.append(("BACKGROUND", (0, row), (-1, row), colors.whitesmoke))

    table.setStyle(TableStyle(styles))
    table.wrapOn(pdf, leftmargin, topmargin)
    table.drawOn(pdf, leftmargin, topmargin - 450)    

    # -------------------------------
    # PAYMENT INFO
    # -------------------------------
    pdf.setFont(font, 9)
    pdf.drawString(leftmargin, 160, "Please pay to the following account:")
    pdf.drawString(leftmargin + 10, 135, "Michael Sutanto")
    pdf.drawString(leftmargin + 10, 120, "BSB: 083-028")
    pdf.drawString(leftmargin + 10, 105, "ACC: 17-800-9379")

    pdf.setFillColor(dark_grey)
    pdf.setFont(fontbold, 10)
    pdf.drawCentredString(width / 2, 60, "Thank you for your business")    

    pdf.showPage()
    pdf.save()
    
    # Get PDF bytes ONCE
    buffer.seek(0)  # ← Reset to beginning
    pdf_bytes = buffer.read()  # ← Read once and store

    # -------------------------------
    # RETURN RESPONSE
    # -------------------------------
    return {
        "statusCode": 200,
        "headers": {
            **cors_headers,  # ← Include CORS headers
            "Content-Type": "application/pdf",
            "Content-Disposition": f"inline; filename={filename}"  # ← Dynamic filename
        },
        "isBase64Encoded": True,
        "body": base64.b64encode(pdf_bytes).decode("utf-8")  # ← Use pdf_bytes
    }