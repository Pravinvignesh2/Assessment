# import pandas as pd
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import Paragraph
# import os

# # Read the CSV data
# csv_file_path = 'All Bills.csv'
# all_bills_df = pd.read_csv(csv_file_path)

# # Clean column names by stripping any extra spaces
# all_bills_df.columns = all_bills_df.columns.str.strip()

# def create_invoice_pdf(invoice_data, output_path):
#     c = canvas.Canvas(output_path, pagesize=A4)
#     width, height = A4

#     # Colors and styles
#     dark_blue = colors.HexColor("#1F3C73")
#     light_yellow = colors.HexColor("#F7D358")
#     grey = colors.HexColor("#F2F2F2")

#     # Header with company logo
#     logo_path = 'weboin.png'
#     c.drawImage(logo_path, 50, 720, width=2*inch, height=1*inch, mask='auto')

#     # Invoice title
#     c.setFillColor(dark_blue)
#     c.setFont("Helvetica-Bold", 24)
#     c.drawString(50, 820, "INVOICE")

#     # Invoice number and date
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(light_yellow)
#     c.drawString(50, 800, f"INVOICE # {str(invoice_data['INVOICE No.'])}")
#     c.setFont("Helvetica", 12)
#     c.setFillColor(colors.black)
#     c.drawString(50, 785, f"Issued on {str(invoice_data['DATE'])}")

#     # Client details
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(dark_blue)
#     c.drawString(50, 765, str(invoice_data.get('CLIENT', '')))
#     c.setFont("Helvetica", 10)
#     c.setFillColor(colors.black)
#     address = str(invoice_data.get('ADDRESS', '')).replace(',', ',\n')
#     client_details = f"{address}\nCONTACT NO: {str(invoice_data.get('CONTACT', ''))}\nGST: {str(invoice_data.get('GSTIN', ''))}"
#     text_object = c.beginText(50, 750)
#     text_object.textLines(client_details)
#     c.drawText(text_object)

#     # Table data
#     data = [
#         ["DESCRIPTION", "QTY", "PRICE", "SGST @9%", "CGST @9%", "TOTAL"],
#         [str(invoice_data.get('DESCRIPTION', '')), 
#          str(invoice_data.get('QTY', '')), 
#          str(invoice_data.get('PRICE', '')), 
#          str(invoice_data.get('SGST18%', '')), 
#          str(invoice_data.get('CGST(18%)', '')), 
#          str(invoice_data.get('TOTAL AMOUNT', ''))]
#     ]

#     table = Table(data, colWidths=[2*inch, 0.7*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), dark_blue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), light_yellow),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), grey),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))

#     # Adjust table position to ensure it fits within the page
#     table.wrapOn(c, width - 100, height - 300)
#     table.drawOn(c, 50, 500)

#     # Footer with tax amounts and total
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(50, 450, f"CGST @9%: Rs. {str(invoice_data.get('CGST(18%)', ''))}")
#     c.drawString(50, 435, f"SGST @9%: Rs. {str(invoice_data.get('SGST18%', ''))}")
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, 420, f"TOTAL AMOUNT: Rs. {str(invoice_data.get('TOTAL AMOUNT', ''))}")

#     # Company details
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(dark_blue)
#     c.drawString(50, 150, "WEBOIN TECHNOLOGIES PRIVATE LIMITED")
#     c.setFont("Helvetica", 10)
#     c.setFillColor(colors.black)
#     company_details = "813, NIZARA BONANZA, 6TH FLOOR,\nANNASALAI, CHENNAI - 600002\nGST Number: 33AADCW0171E1ZS"
#     text_object = c.beginText(50, 135)
#     text_object.textLines(company_details)
#     c.drawText(text_object)

#     c.showPage()
#     c.save()

# # Create invoices directory if not exists
# output_dir = 'invoices'
# os.makedirs(output_dir, exist_ok=True)

# # Generate PDFs for each invoice
# for index, row in all_bills_df.iterrows():
#     invoice_number = row['INVOICE No.']
    
#     # Check if invoice_number is NaN
#     if pd.notna(invoice_number):
#         try:
#             invoice_number = int(invoice_number)
#             output_path = os.path.join(output_dir, f"Invoice_{invoice_number}.pdf")
#             create_invoice_pdf(row, output_path)
#         except ValueError:
#             print(f"Invalid invoice number: {invoice_number}. Skipping this entry.")
#     else:
#         print(f"Missing invoice number for row {index}. Skipping this entry.")

# print(f"Invoices have been generated and saved to the '{output_dir}' directory.")

import pandas as pd
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
import base64

# Read the CSV data
csv_file_path = 'All Bills.csv'
all_bills_df = pd.read_csv(csv_file_path)

# Clean column names by stripping any extra spaces
all_bills_df.columns = all_bills_df.columns.str.strip()

# Create the output directory
output_dir = 'invoices'
os.makedirs(output_dir, exist_ok=True)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Load the HTML template
template = env.get_template('invoice_template.html')

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to the company logo
logo_path = 'weboin.png'
logo_base64 = get_base64_image(logo_path)

def create_invoice_pdf(invoice_data, output_path):
    # Render the HTML template with data
    html_out = template.render(
        invoice_no=invoice_data['INVOICE No.'],
        date=invoice_data['DATE'],
        client_name=invoice_data['NAME'],
        client_address=invoice_data['ADDRESS'],
        client_contact=invoice_data['CONTACT'],
        client_gst=invoice_data['GSTIN'],
        description=invoice_data['DESCRIPTION'],
        qty=invoice_data['QTY'],
        price=invoice_data['PRICE'],
        total=invoice_data['TOTAL AMOUNT'],
        cgst=invoice_data['CGST(18%)'],
        sgst=invoice_data['SGST18%'],
        total_amount=invoice_data['TOTAL AMOUNT'],
        logo_base64=logo_base64
    )

    # Generate the PDF with additional options
    options = {
        'enable-local-file-access': None,
        'no-outline': None,
        'quiet': ''
    }
    pdfkit.from_string(html_out, output_path, options=options)

# Generate PDFs for each invoice
for index, row in all_bills_df.iterrows():
    invoice_number = row['INVOICE No.']
    
    # Check if invoice_number is NaN
    if pd.notna(invoice_number):
        try:
            invoice_number = int(invoice_number)
            output_path = os.path.join(output_dir, f"Invoice_{invoice_number}.pdf")
            create_invoice_pdf(row, output_path)
        except ValueError:
            print(f"Invalid invoice number: {invoice_number}. Skipping this entry.")
    else:
        print(f"Missing invoice number for row {index}. Skipping this entry.")

print(f"Invoices have been generated and saved to the '{output_dir}' directory.")
