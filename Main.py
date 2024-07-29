import pandas as pd
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
import base64

# Read the CSV data
csv_file_path = 'assests/All Bills.csv'
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
logo_path = 'assests/weboin.png'
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
