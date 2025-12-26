from xhtml2pdf import pisa

def generate_invoice_pdf(
    date,
    due_date,
    invoice_number,
    items,  # List of dicts: [{"description": "...", "amount": 4862.45}, ...]
    gst_amount,
    output_filename="invoice.pdf"
):
    """
    Generate a rental invoice PDF.
    
    Args:
        date: Invoice date (string or datetime)
        due_date: Payment due date (string or datetime)
        invoice_number: Invoice number (string)
        items: List of invoice items with 'description' and 'amount'
        gst_amount: GST amount (float)
        output_filename: Output PDF filename
    """
    
    # Calculate subtotal from items
    subtotal = sum(item['amount'] for item in items)
    total = subtotal + gst_amount
    
    # Generate item rows HTML - create 9 rows total
    item_rows = ""
    for i in range(9):
        if i < len(items):
            item = items[i]
            item_rows += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #000; height: 25px;">{item['description']}</td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: center; width: 60px;"></td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: center; width: 60px;"></td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: right; width: 100px;">${item['amount']:,.2f}</td>
                </tr>
            """
        else:
            item_rows += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #000; height: 25px;"></td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: center; width: 60px;">-</td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: center; width: 60px;">-</td>
                    <td style="padding: 8px; border: 1px solid #000; text-align: right; width: 100px;">-</td>
                </tr>
            """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #000;
            }}
            
            table {{
                border-collapse: collapse;
            }}
            
            .header {{
                width: 100%;
                margin-bottom: 20px;
            }}
            
            .header td {{
                vertical-align: top;
                padding: 0;
            }}
            
            .header-left {{
                width: 60%;
                font-size: 10pt;
                line-height: 1.5;
            }}
            
            .company-name {{
                font-weight: bold;
                margin-bottom: 3px;
            }}
            
            .header-right {{
                width: 40%;
                text-align: right;
                font-size: 10pt;
            }}
            
            .date-line {{
                margin-bottom: 3px;
            }}
            
            .invoice-number-box {{
                margin-top: 15px;
                text-align: center;
            }}
            
            .invoice-label {{
                font-weight: bold;
                font-size: 10pt;
            }}
            
            .invoice-number {{
                font-size: 20pt;
                font-weight: bold;
                margin-top: 5px;
            }}
            
            .title {{
                text-align: center;
                font-size: 18pt;
                font-weight: bold;
                letter-spacing: 4px;
                margin: 25px 0;
            }}
            
            .info-section {{
                width: 100%;
                margin-bottom: 20px;
            }}
            
            .info-section td {{
                vertical-align: top;
                padding: 0;
            }}
            
            .bill-to {{
                width: 48%;
                padding-right: 2%;
            }}
            
            .for-section {{
                width: 48%;
                padding-left: 2%;
            }}
            
            .section-header {{
                font-weight: bold;
                margin-bottom: 8px;
                border-bottom: 2px solid #000;
                padding-bottom: 3px;
            }}
            
            .section-content {{
                font-size: 10pt;
                line-height: 1.6;
            }}
            
            .items-table {{
                width: 100%;
                margin: 20px 0;
            }}
            
            .items-table th {{
                background-color: #e0e0e0;
                border: 1px solid #000;
                padding: 8px;
                font-weight: bold;
                text-align: left;
            }}
            
            .items-table th.center {{
                text-align: center;
            }}
            
            .items-table th.right {{
                text-align: right;
            }}
            
            .totals-container {{
                width: 100%;
                margin-top: 20px;
            }}
            
            .totals {{
                float: right;
                width: 320px;
            }}
            
            .totals-table {{
                width: 100%;
            }}
            
            .totals-table td {{
                padding: 5px 10px;
                font-size: 11pt;
            }}
            
            .totals-label {{
                text-align: right;
            }}
            
            .totals-amount {{
                text-align: right;
                font-weight: bold;
                width: 110px;
            }}
            
            .gst-note {{
                font-size: 9pt;
                font-weight: normal;
                font-style: italic;
            }}
            
            .total-row td {{
                border-top: 2px solid #000;
                padding-top: 10px;
                font-weight: bold;
                font-size: 12pt;
            }}
            
            .payment {{
                clear: both;
                margin-top: 60px;
                border: 2px solid #000;
                padding: 15px;
                background-color: #f5f5f5;
            }}
            
            .payment p {{
                margin: 3px 0;
                line-height: 1.6;
            }}
            
            .payment-title {{
                font-weight: bold;
                margin-bottom: 8px;
            }}
            
            .thankyou {{
                text-align: center;
                font-weight: bold;
                font-size: 12pt;
                margin-top: 40px;
                letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <!-- Header -->
        <table class="header">
            <tr>
                <td class="header-left">
                    <div class="company-name">J GAO &amp; M SUTANTO &amp; N.R SUTANTO</div>
                    <div>ABN: 7140291689356 (Registered for GST)</div>
                    <div>7 Granite Way</div>
                    <div>Keilor East VIC 3033</div>
                    <div>Phone: 0439 074 031 Email: michael.sutanto@gmail.com</div>
                </td>
                <td class="header-right">
                    <div class="date-line"><strong>DATE:</strong> {date}</div>
                    <div class="date-line"><strong>DUE DATE:</strong> {due_date}</div>
                    <div class="invoice-number-box">
                        <div class="invoice-label">INVOICE #</div>
                        <div class="invoice-number">{invoice_number}</div>
                    </div>
                </td>
            </tr>
        </table>
        
        <!-- Title -->
        <div class="title">RENT INVOICE</div>
        
        <!-- Bill To and For -->
        <table class="info-section">
            <tr>
                <td class="bill-to">
                    <div class="section-header">BILL TO:</div>
                    <div class="section-content">
                        <strong>Hardik Patel</strong><br/>
                        Jai Sainath Pty LTD, ABN: 88158023039<br/>
                        2C Ernest Street<br/>
                        Bayswater VIC 3153<br/>
                        Phone: 0430 450 819 Email: hardik_1210@yahoo.com
                    </div>
                </td>
                <td class="for-section">
                    <div class="section-header">FOR:</div>
                    <div class="section-content">
                        <strong>Shop 7/477 Burwood<br/>Highway Vermont South</strong>
                    </div>
                </td>
            </tr>
        </table>
        
        <!-- Items Table -->
        <table class="items-table">
            <thead>
                <tr>
                    <th>DESCRIPTION</th>
                    <th class="center" style="width: 60px;">HOURS</th>
                    <th class="center" style="width: 60px;">RATE</th>
                    <th class="right" style="width: 100px;">AMOUNT</th>
                </tr>
            </thead>
            <tbody>
                {item_rows}
            </tbody>
        </table>
        
        <!-- Totals -->
        <div class="totals-container">
            <div class="totals">
                <table class="totals-table">
                    <tr>
                        <td class="totals-label">SUBTOTAL</td>
                        <td class="totals-amount">${subtotal:,.2f}</td>
                    </tr>
                    <tr>
                        <td class="totals-label gst-note">GST Applied to rent component only</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td class="totals-label">GST 10%</td>
                        <td class="totals-amount">${gst_amount:,.2f}</td>
                    </tr>
                    <tr class="total-row">
                        <td class="totals-label">TOTAL</td>
                        <td class="totals-amount">${total:,.2f}</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <!-- Payment Info -->
        <div class="payment">
            <p class="payment-title">Please pay to the following account:</p>
            <p>Michael Sutanto</p>
            <p>BSB: 083-028</p>
            <p>ACC: 17-800-9379</p>
        </div>
        
        <!-- Thank You -->
        <div class="thankyou">THANK YOU FOR YOUR BUSINESS!</div>
    </body>
    </html>
    """
    
    # Generate PDF
    with open(output_filename, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
        return False
    else:
        print(f"Invoice PDF generated successfully: {output_filename}")
        return True


# Example usage
if __name__ == "__main__":
    # Define invoice data
    invoice_data = {
        "date": "December 24, 2025",
        "due_date": "January 1, 2026",
        "invoice_number": "00219",
        "items": [
            {
                "description": "Rent for shop 7/477 Burwood Highway January 01 - January 31 2026",
                "amount": 4862.45
            }
            # Add more items as needed
            # {
            #     "description": "Additional service",
            #     "amount": 500.00
            # }
        ],
        "gst_amount": 486.25
    }
    
    # Generate the PDF
    generate_invoice_pdf(
        date=invoice_data["date"],
        due_date=invoice_data["due_date"],
        invoice_number=invoice_data["invoice_number"],
        items=invoice_data["items"],
        gst_amount=invoice_data["gst_amount"],
        output_filename="Rental_Invoice_January2026.pdf"
    )