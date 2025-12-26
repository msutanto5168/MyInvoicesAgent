from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

import io
import base64


def lambda_handler(event, context):
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
    pdf.drawString(leftmargin, topmargin - 154, event.get('bill_to_name', 'Hardik Patel'))
    pdf.drawString(leftmargin, topmargin - 168, event.get('bill_to_company', 'Jai Sainath Pty LTD, ABN: 88158023039'))
    pdf.drawString(leftmargin, topmargin - 182, event.get('bill_to_address', '2C Ernest Street'))
    pdf.drawString(leftmargin, topmargin - 196, event.get('bill_to_suburb', 'Bayswater VIC 3153'))
    pdf.drawString(leftmargin, topmargin - 210, "Phone: 0430 450 819  Email: hardik_1210@yahoo.com")    


    # -------------------------------
    # RIGHT Header Section
    # -------------------------------
    pdf.setFillColor(light_grey)
    pdf.setFont(fontbold, 24)
    pdf.drawRightString(rightmargin, topmargin - 40, "RENT INVOICE")

    
    # Date and invoice info on right
    pdf.setFillColor(colors.black)
    pdf.setFont(fontbold, 9)

    # Headings
    pdf.drawString(rightmargin - 170, topmargin - 80, "DATE:")
    pdf.drawString(rightmargin - 170, topmargin - 94, "DUE DATE:")
    pdf.drawString(rightmargin - 170, topmargin - 108, "INVOICE #")
    pdf.drawString(rightmargin - 170, topmargin - 122, "FOR:")

    pdf.setFont(font, 9)
    pdf.drawRightString(rightmargin, topmargin - 80, f"{event['date']}")
    pdf.drawRightString(rightmargin, topmargin - 94, f"{event['due_date']}")        
    pdf.drawRightString(rightmargin, topmargin - 108, f"{event['invoice_number']}")
    pdf.drawRightString(rightmargin, topmargin - 122, event.get('property_line1', 'Shop 7/477 Burwood'))
    pdf.drawRightString(rightmargin, topmargin - 136, event.get('property_line2', 'Highway Vermont South'))

    
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
    for item in event["items"]:
        table_data.append([
            Paragraph(item["description"], description_style),
            item.get("hours", ""),
            item.get("rate", ""),
            f"${item['amount']:,.2f}"
        ])
        subtotal += item["amount"]
    
    # Add blank rows to match original layout
    for _ in range(7 - len(event["items"])):
        table_data.append(["", "", "", "-"])

    table_data.append(["", "", "SUBTOTAL", f"${subtotal:,.2f}"])    
    table_data.append(["GST Applied to rent component only", "", "GST 10%", f"${event['gst_amount']:,.2f}"])
    table_data.append(["", "", "TOTAL", f"${subtotal + event['gst_amount']:,.2f}"])

    table = Table(table_data, colWidths=[100 * mm, 20 * mm, 20 * mm, 30 * mm])

    styles = [
        # Outer border only
        ("BOX", (0, 0), (-1, -4), 0.75, colors.black),

        # Vertical lines
        ("LINEBEFORE", (1, 0), (-1, -4), 0.5, colors.black),

        # Header background
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

        # Alignments
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "RIGHT"),
        ("ALIGN", (2, -3), (2, -1), "RIGHT"),  # Subtotal / GST / Total labels
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        # Fonts
        ("FONT", (0, 0), (-1, 0), font, 9),
        ("FONT", (0, 1), (0, -4), font, 9),
        ("FONT", (2, -1), (3, -1), fontbold, 9),
    ]

    # 🔽 Zebra striping: every alternate row (skip header)
    for row in range(1, len(table_data)-3):
        if row % 2 == 0:
            styles.append(
                ("BACKGROUND", (0, row), (-1, row), colors.whitesmoke)
            )

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
    pdf.drawCentredString(
        width / 2,
        60,
        "Thank you for your business"
    )    

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=invoice.pdf"
        },
        "isBase64Encoded": True,
        "body": base64.b64encode(buffer.read()).decode("utf-8")
    }