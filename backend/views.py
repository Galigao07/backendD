import datetime
import pdb
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
import pytz
from backend.models import (CompanySetup, User,POS_Terminal,PosCashiersLogin,PosSalesTransSeniorCitizenDiscount,SalesTransCreditCard,SalesTransEPS,PosSalesTransCreditSale,BankCompany)
from backend.serializers import (UserSerializer,POS_TerminalSerializer,PosCashiersLoginpSerializer,PosSalesTransSeniorCitizenDiscountSerializer)
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
import json
import base64 

from django.contrib.auth.hashers import make_password, check_password

import platform
import subprocess
from datetime import date
from django.db.models import Max
# Get current date
from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime,GetCompanyConfig
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django_user_agents.utils import get_user_agent
from cryptography.hazmat.primitives import padding
from pyprinter import Printer
import win32print
import win32api

from django.test import TestCase
from reportlab.lib.units import mm,cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import traceback
import textwrap
from backend.models import (Employee,User,POSSettings,POSProductPrinter,PosSalesInvoiceList,PosSalesInvoiceListing,PosSalesTrans,PosClientSetup,LeadSetup)
from backend.serializers import (POSSettingsSerializer,PosSalesInvoiceListSerializer,PosSalesInvoiceListingSerializer,PosSalesTransSerializer)
import os
import fitz  # PyMuPDF
import win32ui
import win32com.client
import subprocess
import winreg
from PyPDF2 import PdfReader
from django.http import JsonResponse,FileResponse
from rest_framework.response import Response

def getCompanyData():
    # first_autonum = CompanySetup.objects.values_list('autonum', flat=True).first()
    first_autonum = CompanySetup.objects.first()
    return first_autonum


def getClientSetup():
    # first_autonum = CompanySetup.objects.values_list('autonum', flat=True).first()
    first_autonum = PosClientSetup.objects.first()
    return first_autonum

def getLeadSetup():
    # first_autonum = CompanySetup.objects.values_list('autonum', flat=True).first()
    first_autonum = LeadSetup.objects.first()
    return first_autonum

#    PDFSalesOrder(cart_items,so_no,table_no,QueNo,guest_count,customer)
def PDFSalesOrder(data,SO,TableNo,QueNo,GuestCount,Customer,order_type,cashierID,PrinterName,PrintLocation):
    try:
        Cashier_Name = ''
        cashier = User.objects.filter(id_code=cashierID).first()
        if cashier:
            Cashier_Name = cashier.fullname
        
        total_qty = 0
        hyphen_line = "-" * 55  # 55 hyphens in a row
        x_start = 10 * mm  # Starting x-coordinate
        x_end = x_start + 55 * mm  # Ending x-coordinate (55 characters long)

       
        # Determine the width and height based on the data length
      
        line_height = 0.4 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 79 * mm  # Width adjusted for 79 mm roll paper
        # Set the initial height for the first page

        # Calculate the required height based on the data length
        height = (len(data) + 20) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

        # Create a canvas with calculated size
        c = canvas.Canvas("SalesOrder.pdf", pagesize=(width, height))

        # Set up a font and size
     
        c.setFont("Helvetica-Bold", 8.5)

        # Calculate x-coordinate for center alignment of "SALES INVOICE"
        text_width = c.stringWidth("SALES ORDER", "Helvetica-Bold", 10)
        y_position = height - margin - line_height 
        x_center = (width - text_width) / 2
        y_position -= line_height
        c.drawString(x_center, y_position, "SALES ORDER")
        y_position -= line_height
        y_position -= line_height
        c.drawString(10 * mm, y_position, "Cusomer: " f'{Customer}')
        if TableNo != 0:
            y_position -= line_height
            c.drawString(10 * mm, y_position, f"Table No.: {TableNo}")

            # Right align "Guest Count"
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)
        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Table No.: " f'{TableNo}')
        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Guest Count: " f'{GuestCount}')
        
        
        if QueNo != 0:
            y_position -= line_height
            c.drawString(10 * mm, y_position, "QueNo: " f'{QueNo}')
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)
        y_position -= line_height
        y_position -= line_height
        text_width = c.stringWidth(order_type, "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{order_type}')
        y_position -= line_height
        # Draw Line
        c.line(x_start, y_position - 2, x_end, y_position - 2)
    
        # Update y_position for the next line
        y_position -= line_height
        text_width = c.stringWidth(f'{PrintLocation}', "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{PrintLocation}')
        y_position -= line_height
        text_width = c.stringWidth(f'SO#{SO}', "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        # Draw the Sales Order number (SO#)
        c.drawString(x_center, y_position, f'SO#{SO}')

        # Update y_position for the next line
        y_position -= line_height

        # Get the current date and time
        date_time = GetPHilippineDateTime()
        text_width = c.stringWidth(date_time, "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        # Draw the date and time
        c.drawString(x_center, y_position, f'{date_time}')

        # Update y_position for the next content
        y_position -= (line_height - 0.2 * cm)
      
        c.line(x_start, y_position, x_end, y_position)
        # c.drawString(10 * mm, y_position, hyphen_line)  # Adjust x position as needed
        y_position -= line_height
      
        for item in data:
            description = json.dumps(item['description'], ensure_ascii=False)
            quantity = json.dumps(item['quantity'], ensure_ascii=False)
            description = description.replace('"', '')  # Remove double quotes
            total_qty = total_qty + int(item['quantity'])
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            quantity_str = str(quantity).ljust(3)  
            text_to_draw = f"{quantity_str} {description}"

            wrapped_description = textwrap.wrap(description, width=25)

            if wrapped_description:
                text_to_draw = f"{quantity_str} {wrapped_description[0]}"
                c.drawString(10 * mm, y_position, text_to_draw)
                y_position -= line_height

                # Draw the rest of the wrapped lines without quantity
            for line in wrapped_description[1:]:
                text_to_draw = f"{' ' * len(quantity_str)} {line}"
                c.drawString(10 * mm, y_position, text_to_draw)
                y_position -= line_height


        c.line(x_start, y_position, x_end, y_position)
        y_position -= line_height
        c.drawString(10 * mm, y_position,'Items:' + str(total_qty))
        y_position -= line_height
        c.drawString(10 * mm, y_position,'Cashier:' + Cashier_Name)
        c.drawString(10 * mm, y_position,'' )

        # Save the PDF
        print('already save pdf')
        c.save()
        # print_pdf_to_printer(PrinterName,'SalesOrder.pdf')
    except Exception as e:
        print(e)
        traceback.print_exc()
    

def PDFSalesOrderaLL(data,SO,TableNo,QueNo,GuestCount,Customer,order_type,cashierID,PrinterName,PrintLocation):
    try:
        Cashier_Name = ''
        cashier = User.objects.filter(id_code=cashierID).first()
        if cashier:
            Cashier_Name = cashier.fullname
        
        total_qty = 0
        hyphen_line = "-" * 55  # 55 hyphens in a row
        x_start = 10 * mm  # Starting x-coordinate
        x_end = x_start + 55 * mm  # Ending x-coordinate (55 characters long)

       
        # Determine the width and height based on the data length
      
        line_height = 0.4 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 79 * mm  # Width adjusted for 79 mm roll paper
        # Set the initial height for the first page

        # Calculate the required height based on the data length
        height = (len(data) + 20) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

        # Create a canvas with calculated size
        c = canvas.Canvas("SalesOrderaLL.pdf", pagesize=(width, height))

        # Set up a font and size
     
        c.setFont("Helvetica-Bold", 8.5)

        # Calculate x-coordinate for center alignment of "SALES INVOICE"
        text_width = c.stringWidth("SALES ORDER", "Helvetica-Bold", 10)
        y_position = height - margin - line_height 
        x_center = (width - text_width) / 2
        y_position -= line_height
        c.drawString(x_center, y_position, "SALES ORDER")
        y_position -= line_height
        y_position -= line_height
        c.drawString(10 * mm, y_position, "Cusomer: " f'{Customer}')
        if TableNo != 0:
            y_position -= line_height
            c.drawString(10 * mm, y_position, f"Table No.: {TableNo}")

            # Right align "Guest Count"
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)
        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Table No.: " f'{TableNo}')
        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Guest Count: " f'{GuestCount}')
        
        
        if QueNo != 0:
            y_position -= line_height
            c.drawString(10 * mm, y_position, "QueNo: " f'{QueNo}')
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)
        y_position -= line_height
        y_position -= line_height
        text_width = c.stringWidth(order_type, "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{order_type}')
        y_position -= line_height
        # Draw Line
        c.line(x_start, y_position - 2, x_end, y_position - 2)
    
        # Update y_position for the next line
        y_position -= line_height
        text_width = c.stringWidth(f'{PrintLocation}', "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{PrintLocation}')
        y_position -= line_height
        text_width = c.stringWidth(f'SO#{SO}', "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        # Draw the Sales Order number (SO#)
        c.drawString(x_center, y_position, f'SO#{SO}')

        # Update y_position for the next line
        y_position -= line_height

        # Get the current date and time
        date_time = GetPHilippineDateTime()
        text_width = c.stringWidth(date_time, "Helvetica-Bold", 10)
        x_center = (width - text_width) / 2
        # Draw the date and time
        c.drawString(x_center, y_position, f'{date_time}')

        # Update y_position for the next content
        y_position -= (line_height - 0.2 * cm)
      
        c.line(x_start, y_position, x_end, y_position)
        # c.drawString(10 * mm, y_position, hyphen_line)  # Adjust x position as needed
        y_position -= line_height
      
        for item in data:
            description = json.dumps(item['description'], ensure_ascii=False)
            quantity = json.dumps(item['quantity'], ensure_ascii=False)
            description = description.replace('"', '')  # Remove double quotes
            total_qty = total_qty + int(item['quantity'])
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            quantity_str = str(quantity).ljust(3)  
            text_to_draw = f"{quantity_str} {description}"

            wrapped_description = textwrap.wrap(description, width=25)

            if wrapped_description:
                text_to_draw = f"{quantity_str} {wrapped_description[0]}"
                c.drawString(10 * mm, y_position, text_to_draw)
                y_position -= line_height

                # Draw the rest of the wrapped lines without quantity
            for line in wrapped_description[1:]:
                text_to_draw = f"{' ' * len(quantity_str)} {line}"
                c.drawString(10 * mm, y_position, text_to_draw)
                y_position -= line_height


        c.line(x_start, y_position, x_end, y_position)
        y_position -= line_height
        c.drawString(10 * mm, y_position,'Items:' + str(total_qty))
        y_position -= line_height
        c.drawString(10 * mm, y_position,'Cashier:' + Cashier_Name)
        c.drawString(10 * mm, y_position,'' )

        # Save the PDF
        print('already save pdf')
        c.save()
        # print_pdf_to_printer(PrinterName,'SalesOrder.pdf')
    except Exception as e:
        print(e)
        traceback.print_exc()
    
def print_pdf_to_printerGohostScript(printer_name, pdf_path):
    try:
        # Full path to the Ghostscript executable
        ghostscript_path = r'C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe'

        # Define the Ghostscript command
        ghostscript_command = [
            ghostscript_path,
            '-dBATCH',
            '-dNOPAUSE',
            '-sDEVICE=ps2write',
            '-sOutputFile=' + pdf_path.replace('.pdf', '.ps'),
            pdf_path
        ]
        
        # Debugging: print the command to verify it
        print("Ghostscript command:", " ".join(ghostscript_command))

        # Run the Ghostscript command
        subprocess.run(ghostscript_command, check=True)
        
        # Path to the PostScript file
        ps_path = pdf_path.replace('.pdf', '.ps')
        
        # Check if the PostScript file was created
        if not os.path.exists(ps_path):
            raise FileNotFoundError(f"PostScript file was not created: {ps_path}")
        
        # Read the PostScript file content
        with open(ps_path, 'rb') as ps_file:
            ps_data = ps_file.read()
        
        # Create a printer handle for the specified printer
        printer_handle = win32print.OpenPrinter(printer_name)
        
        # Start a print job
        job_info = ("SalesOrder", None, "RAW")
        job_handle = win32print.StartDocPrinter(printer_handle, 1, job_info)
        
        # Start a new page
        win32print.StartPagePrinter(printer_handle)
        
        # Send the PostScript data to the printer
        win32print.WritePrinter(printer_handle, ps_data)
        
        # End the page and the print job
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        
        # Close the printer handle
        win32print.ClosePrinter(printer_handle)
        
        # Clean up the temporary PostScript file
        os.remove(ps_path)
        
        print("Printing complete.")
        
    except subprocess.CalledProcessError as gs_error:
        print("Ghostscript error: ", gs_error)
    except FileNotFoundError as fnf_error:
        print("File not found error: ", fnf_error)
    except Exception as e:
        print("Exception occurred: ", e)

def print_pdf_to_printer(printer_name, pdf_path):
    try:
        # Path to SumatraPDF executable
        sumatra_path = r'C:\Program Files\SumatraPDF\SumatraPDF.exe'  # Update this path if needed

        # Define the command to print the PDF
        print_command = [
            sumatra_path,
            '-print-to', printer_name,
            '-print-settings', 'noscale',  # Print using actual size
            pdf_path
        ]
        
        
        # Debugging: print the command to verify it
        print("Print command:", " ".join(print_command))

        # Run the print command
        subprocess.run(print_command, check=True)
        
        print("Printing complete.")
        
    except subprocess.CalledProcessError as sumatra_error:
        print("SumatraPDF error: ", sumatra_error)
    except Exception as e:
        print("Exception occurred: ", e)


def print_pdf_to_printer1(printer_name, pdf_path):
    try:
        # Open the PDF file
        with fitz.open(pdf_path) as pdf_document:
            # Create a printer handle for the specified printer
            printer_handle = win32print.OpenPrinter(printer_name)
            
            # Start a print job
            job_info = win32print.StartDocPrinter(printer_handle, 1, ("SalesOrder", None, "RAW"))
            
            # Start a new page
            win32print.StartPagePrinter(printer_handle)
            
            # Extract text from each page and send it to the printer
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)
                page_text = page.get_text()
                win32print.WritePrinter(printer_handle, page_text.encode("utf-8"))
            
            # End the page and the print job
            # cut_command = b'\x1D\x56\x00'  # ESC/POS command for full cut
            # win32print.WritePrinter(printer_handle, cut_command)   
            cut_command = b'\x1d\x56\x42\x00'
            win32print.WritePrinter(printer_handle, cut_command)  
            win32print.EndPagePrinter(printer_handle)
            win32print.EndDocPrinter(printer_handle)
            
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)

        print("Printing complete.")
        
    except Exception as e:
        print("Exception occurred: ", e)
def print_pdf_salesOrder():
    """Prints the SalesOrder.pdf file to the default printer."""
    try:
        # Get the default printer
        printer_setup = GetCompanyConfig('multiple_printer')
        print('printer_setup',printer_setup)

        if printer_setup == 'False':
            printer_name = win32print.GetDefaultPrinter()
            print(f"Default printer: {printer_name}")
            
            # Replace this with the path to your PDF file
            pdf_file_path = "SalesOrder.pdf"
            
            # Print the PDF file to the default printer
            print(f"Printing '{pdf_file_path}' to '{printer_name}'...")
            print_pdf_to_printer(printer_name, pdf_file_path)
        else:
            printer_list = POSProductPrinter.objects.all()
            for printer_name in printer_list:
                print(f"printer_name: {printer_name.printer_name}")
            
            # Replace this with the path to your PDF file
                pdf_file_path = "SalesOrder.pdf"
            
                # Print the PDF file to the default printer
                print(f"Printing '{pdf_file_path}' to '{printer_name.printer_name}'...")
                print_pdf_to_printer(printer_name.printer_name, pdf_file_path)



        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


def PDFReceipt(doc_no,doc_type,cusData):
        try:
            margin_left = 2 * mm
            margin_right = 10 * mm
            margin_top = 2 * mm
            margin_bottom = 2 * mm
            Total_due = 0
            Total_Payment = 0
            Amount_Tendered = 0

            x_start = 2 * mm  # Starting x-coordinate
            x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)

            Cashier_ID = 0

            Item_Dicount = False
            SC_Dicount = False
            Transaction_Dicount = False
            Trade_Dicount = False

            data = ''
            total_qty = 0

            CusTIN = cusData['CusTIN']
            CusAddress =  cusData['CusAddress']
            CusBusiness = cusData['CusBusiness']
            Customer =  cusData['CustomerName']

            Order_Type= 'DINE IN'
            TableNo = int(float(cusData['TableNo']))
            GuestCount = int(float(cusData['Guest_Count']))
            QueNo = int(float(cusData['QueNo']))

            

            vat = 0
            vatable = 0
            vat_exempt = 0
            vat_zero_rated = 0
            non_vat = 0

            change_amount = 0
            cash_payment = 0

            credit_card_payment = 0
            debit_card_payment = 0
            gcash_payment = 0
            other_payment = 0
            multiple_payment = 0
            payment_method = 'CASH'
            is_credit_card_payment = False
            is_debit_card_payment = False
            is_cash_payment = False



            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            

            # GET DATA IN SALES INVOICE LIST
            data_list = PosSalesInvoiceList.objects.filter(doc_no=doc_no,doc_type=doc_type).first()
            if data_list:
                if data_list.discount_type == 'IM':
                    Item_Dicount = True
                elif data_list.discount_type == 'SC':
                    SC_Dicount = True
                if data_list.total_cash != 0:
                    cash_payment = data_list.total_cash
                    is_cash_payment = True
                if data_list.total_credit_card != 0:
                    credit_card_payment = data_list.total_credit_card
                    is_credit_card_payment = True
                if data_list.total_eps !=0:
                    debit_card_payment = data_list.total_eps
                    is_debit_card_payment = True
                if data_list.total_cash !=  0:
                    cash_payment = data_list.total_cash
                # data_tmp = PosSalesInvoiceListSerializer(data_list,many=True).data

                # if data_tmp:
                #     data_tmp.

            # GET DATA IN SALES INVOICE LISTING
            data_listing = PosSalesInvoiceListing.objects.filter(doc_no=doc_no,doc_type=doc_type)
            if data_listing:
                data = PosSalesInvoiceListingSerializer(data_listing,many=True).data

            # GET DATA IN TABLE POS SALES TRANS
            pos_sales_trans = PosSalesTrans.objects.filter(sales_trans_id=int(float(doc_no)),document_type='SI').first()
            if pos_sales_trans:
                Amount_Tendered = pos_sales_trans.amount_tendered
                Cashier_ID = pos_sales_trans.cashier_id
                # cash_payment = Amount_Tendered
                # pos_sales_trans_data = PosSalesTransSerializer(pos_sales_trans,many=True).data

            companyCode = getCompanyData()
            clientSetup = getClientSetup()

            # Determine the width and height based on the data length
            line_height = 0.4 * cm
            line_height_dash = 0.1 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            # Set the initial height for the first page
            card_height= 0


            #---- GET THE HEIGTH OF CARD DETAILS
            if is_credit_card_payment:
                Credit_card_list = SalesTransCreditCard.objects.filter(sales_trans_id=int(float(doc_no)),terminal_no = machineInfo.terminal_no,cashier_id=Cashier_ID)
                card_height += Credit_card_list.count() * 6

            if is_debit_card_payment:
                Debit_card_list = SalesTransEPS.objects.filter(sales_trans_id=int(float(doc_no)),terminal_no = machineInfo.terminal_no,cashier_id=Cashier_ID)
                card_height += Debit_card_list.count() * 4

            # Calculate the required height based on the data length
            height = ((len(data)* 2) + 60 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas("Receipt.pdf", pagesize=(width, height))

            # Set up a font and size
        
            c.setFont("Helvetica", 8.5)
            y_position = height - margin - line_height 


            text_width = c.stringWidth(f'{clientSetup.company_name}', "Helvetica", 8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}', "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}', "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}', "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}', "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}', "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}', "Helvetica", 10)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height
    

            # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("SALES INVOICE", "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "SALES INVOICE")
            y_position -= line_height
            y_position -= line_height

            c.drawString(10 * mm, y_position, "Cusomer: " f'{Customer}')
            if TableNo != 0:
                
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"Table No.: {TableNo}")

                # Right align "Guest Count"
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            if QueNo != 0:
                Order_Type = 'TAKE OUT'
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"QueNo.: {QueNo}")
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text, "Helvetica", 12)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            y_position -= line_height

            text_width = c.stringWidth(f'{Order_Type}', "Helvetica-Bold",  8.5)
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'{Order_Type}')
            y_position -= line_height

            c.setDash(3, 2) 
            c.line(x_start, y_position, x_end, y_position)
            text_width = c.stringWidth(f'SI#{int(float(doc_no))}', "Helvetica-Bold",  8.5)
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'SI#{int(float(doc_no))}')
            y_position -= line_height

            # Get the current date and time
            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time, "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            # Draw the date and time
            c.drawString(x_center, y_position, f'{date_time}')

            # Update y_position for the next content
            y_position -= (line_height - 0.2 * cm)

        # 3 points on, 2 points off
            c.line(x_start, y_position, x_end, y_position)
            # c.line(x_start, y_position, x_end, y_position)
            # c.drawString(10 * mm, y_position, hyphen_line)  # Adjust x position as needed
            y_position -= line_height
        
            for item in data:
                pc_price = json.dumps(item['pc_price'], ensure_ascii=False)
                sub_total= json.dumps(item['sub_total'], ensure_ascii=False)
                description = json.dumps(item['description'], ensure_ascii=False)
                quantity = json.dumps(int(float(item['rec_qty'])), ensure_ascii=False)
                description = description.replace('"', '')  # Remove double quotes
                pc_price = pc_price.replace('"', '')  # 
                sub_total = sub_total.replace('"', '')  # 

                total_qty = total_qty + float(item['rec_qty'])
                Total_due = Total_due + float(item['sub_total'])
                c.setFont("Helvetica", 8.5)
                c.setFillColor(colors.black)
                quantity_str = str(quantity).ljust(3)  
                text_to_draw = f"{description}"
                qty_and_price = f"{quantity_str}    @{pc_price}"

                wrapped_description = textwrap.wrap(text_to_draw, width=32)

                if wrapped_description:
                    text_to_draw = f"{wrapped_description[0]}"
                    c.drawString(10 * mm, y_position, text_to_draw)
                    # y_position -= line_height
                    # Draw the rest of the wrapped lines without quantity
                for line in wrapped_description[1:]:
                    y_position -= line_height
                    text_to_draw = f"{line}"
                    c.drawString(10 * mm, y_position, text_to_draw)
                sub_total_char_width = c.stringWidth(f'{sub_total}', "Helvetica", 8.5)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, f'{float(sub_total):,.2f}')
                y_position -= line_height
                c.drawString(10 * mm, y_position,f'{qty_and_price}')
                y_position -= line_height
                #*********** Senior Discount *************
                if Item_Dicount == True:
                    if float(item['disc_amt']) !=0:
                        discount_amount = json.dumps(item['disc_amt'], ensure_ascii=False)
                        discount_rate= json.dumps(item['desc_rate'], ensure_ascii=False)
                        discount_amount = discount_amount.replace('"', '')  # 
                        discount_rate = discount_rate.replace('"', '')  # 
                        c.drawString(10 * mm, y_position,'Less:        ' + str(int(float(discount_rate)))+'%')
                        c.drawRightString(width - margin_right, y_position, f'-{float(discount_amount):,.2f}')
                        Total_due -= float(discount_amount)
                        y_position -= line_height


            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Items:' + str(int(float(total_qty))))
            total_due_char_width = c.stringWidth(f'{Total_due}', "Helvetica", 8.5)  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height

            #*********** Senior Discount *************
            if SC_Dicount == True:
                Less_Vat = 0
                Net_of_vat = 0
                Less_Discount = 0
                Amount_covered = 0

                SC_Covered = PosSalesTransSeniorCitizenDiscount.objects.filter(sales_trans_id=int(float(doc_no)),)

                if SC_Covered:
                    for amount in SC_Covered:
                        Amount_covered +=  float(str(amount.amount_covered).replace(',',''))


                Less_Vat = (Amount_covered / 1.12) * 0.12
                Net_of_vat = float(str(Total_due).replace(',','')) - Less_Vat
                Less_Discount =(Amount_covered / 1.12) * 0.20
                data_for_vatable = float(str(Total_due).replace(',','')) - Amount_covered
                Total_due = float(str(Total_due).replace(',','')) - (Less_Discount + Less_Vat)

                vatable = (data_for_vatable / 1.12)
                vat_exempt = (Amount_covered - (Less_Vat + Less_Discount))
                vat = (vatable * .12)


                y_position -= line_height
                c.drawString(10 * mm, y_position,'Less 20% VAT:' + f'{Amount_covered}')
                c.drawRightString(width - margin_right, y_position, f'{float(Less_Vat):,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position,'Net of VAT:')
                c.drawRightString(width - margin_right, y_position, f'{float(Net_of_vat):,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position,'Less 20% Discount:')
                c.drawRightString(width - margin_right, y_position, f'{float(Less_Discount):,.2f}')
                y_position -= line_height
                c.line(x_start, y_position, x_end, y_position)
                y_position -= line_height
                c.drawString(10 * mm, y_position,'TOTAL DUE:')
                c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
                y_position -= line_height
                y_position -= line_height

            # ************** VAT DATA ****************
            y_position -= line_height
        
            if Item_Dicount == True:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat
            else:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat


            c.drawString(10 * mm, y_position,'Vatable:')
            c.drawRightString(width - margin_right, y_position, f'{float(vatable):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'VAT Exempt:')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_exempt):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Non-VAT:')
            c.drawRightString(width - margin_right, y_position, f'{float(non_vat):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'VAT Zero Rated:')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_zero_rated):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'VAT:')
            c.drawRightString(width - margin_right, y_position, f'{float(vat):,.2f}')
            # L**************END VAT ****************

            # L************** NEW double dash line ****************
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            # L************** END double dash line ****************

            y_position -= line_height
            c.drawString(10 * mm, y_position,'TOTAL DUE:')
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height
          
            if is_cash_payment:
                y_position -= line_height
                c.drawString(10 * mm, y_position,'CASH:')
                if is_credit_card_payment or is_debit_card_payment: 
                    
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                else:
                    cash_payment = Amount_Tendered
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                y_position -= line_height
                if is_credit_card_payment | is_debit_card_payment:
                    pass
                else:
                    c.drawString(10 * mm, y_position,'CHANGE:')
                    change_amount = cash_payment - Total_due
                    c.drawRightString(width - margin_right, y_position, f'{float(change_amount):,.2f}')
            if is_credit_card_payment:
                Credit_card_list = SalesTransCreditCard.objects.filter(sales_trans_id=int(float(doc_no)),terminal_no = machineInfo.terminal_no,cashier_id=Cashier_ID)
                if Credit_card_list:
                    for item in Credit_card_list:
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Credit Card:')
                        c.drawRightString(width - margin_right, y_position, f'{float(item.amount):,.2f}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Credit Card No.:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_no}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Card Issuer:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_name}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Bank:')
                        bankName = BankCompany.objects.filter(id_code=int(float(item.bank))).first()
                        if bankName:
                            c.drawRightString(width - margin_right, y_position, f'{bankName.company_description}')
                            y_position -= line_height
                        c.drawString(10 * mm, y_position,'Expiry Date:')
                        c.drawRightString(width - margin_right, y_position, f'{item.expiry_date}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Card Holder:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_holder}')
                        y_position -= line_height
            if is_debit_card_payment:
                debit_card_list = SalesTransEPS.objects.filter(sales_trans_id=int(float(doc_no)),terminal_no = machineInfo.terminal_no,cashier_id=Cashier_ID)
                if debit_card_list:
                    for item in debit_card_list:
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Debit Card:')
                        c.drawRightString(width - margin_right, y_position, f'{float(item.amount):,.2f}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Debit Card No:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_no}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Bank:')
                        bankName = BankCompany.objects.filter(id_code=int(float(item.bank))).first()
                        if bankName:
                            c.drawRightString(width - margin_right, y_position, f'{bankName.company_description}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Card Holder:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_holder}')
                        y_position -= line_height
            if payment_method =='CREDIT SALES':
                y_position -= line_height
                c.drawString(10 * mm, y_position,'CHARGE:')
                c.drawRightString(width - margin_right, y_position, f'{float(credit_card_payment):,.2f}')

            y_position -= line_height
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Cashier:')
            c.drawString(10 * mm, y_position,'' )
            cashierData = User.objects.filter(id_code = int(float(Cashier_ID))).first()
            if cashierData:
                c.drawRightString(width - margin_right, y_position, f'{cashierData.fullname}')
            y_position -= line_height
            c.drawRightString(width - margin_right, y_position,f'TERMINAL #' + f'{machineInfo.terminal_no}' + f'{doc_no}')
            y_position -= line_height


            if SC_Dicount == True:
                SC_Covered = PosSalesTransSeniorCitizenDiscount.objects.filter(sales_trans_id=int(float(doc_no)),)
                if SC_Covered:
                    for SC_data in SC_Covered:
                        c.drawString(10 * mm, y_position,'Senior Name:')
                        c.drawRightString(width - margin_right, y_position, f'{SC_data.senior_member_name}')

                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'ID:')
                        c.drawRightString(width - margin_right, y_position, f'{SC_data.id_no}')

                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'TIN:')
                        c.drawRightString(width - margin_right, y_position, f'{SC_data.tin_no}')


            c.setDash()
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Customer Name:')
            c.drawRightString(width - margin_right, y_position, f'hernanie D. Galigao Jr')

            name_width = c.stringWidth('Customer Name:', 'Helvetica', 8)
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, 'hernanie D. Galigao Jr')
            value_width = c.stringWidth('hernanie D. Galigao Jr', 'Helvetica', 8)
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Address:')
            c.drawRightString(width - margin_right, y_position, f'KORONADAL CITY')

            name_width = c.stringWidth('Address:', 'Helvetica', 8)
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, 'KORONADAL CITY')
            value_width = c.stringWidth('KORONADAL CITY', 'Helvetica', 8)
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'TIN:')
            c.drawRightString(width - margin_right, y_position, f'1111-2222-3333-555')

            name_width = c.stringWidth('TIN:', 'Helvetica', 8)
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, '1111-2222-3333-555')
            value_width = c.stringWidth('1111-2222-3333-555', 'Helvetica', 8)
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Business Style:')
            c.drawRightString(width - margin_right, y_position, f'RESTAURANT')

            name_width = c.stringWidth('Business Style:', 'Helvetica', 8)
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, 'RESTAURANT')
            value_width = c.stringWidth('RESTAURANT', 'Helvetica', 8)
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)
            y_position -= line_height
            y_position -= line_height
            
            c.setDash(3,2)
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth("THIS SERVES AS AN OFFICIAL RECEIPT", "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THIS SERVES AS AN OFFICIAL RECEIPT")
            y_position -= line_height
            y_position -= line_height
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth("THANK YOU, COME AGAIN... ", "Helvetica",  8.5)
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THANK YOU, COME AGAIN... ")
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            y_position -= line_height
            lead = getLeadSetup()

            if lead:
                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name2}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address2}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.tin}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.tin}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.accreditation_no}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.accreditation_no}')


                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_issued}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_issued}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_valid}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_valid}')


                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.PTU_no}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.PTU_no}')

                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.date_issue}', "Helvetica",  8)
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.date_issue}')
            # Save the PDF
            print('already save pdf Sales Invoice')
            c.save()   
        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['GET'])
def download_pdf(request):
    if request.method == 'GET':
        try:
            # Get the absolute path of the file
            # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backendD', 'Receipt.pdf'))
            file_path ='Receipt.pdf'
            # Check if the file exists
            print('file_path',file_path)
            if not os.path.isfile(file_path):
                print('xxxxxx')
                return Response({'error': 'File not found.'}, status=404)

            # Open the file and return it as a response
            f = open(file_path, 'rb')
            response = FileResponse(f, as_attachment=True, filename='Receipt.pdf')
            return response
            # return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Receipt.pdf')
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error': 'An error occurred while processing the request.'}, status=500)

@api_view(['GET'])
def download_sales_order_pdf(request):
    if request.method == 'GET':
        try:
            # Get the absolute path of the file
            # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backendD', 'Receipt.pdf'))
            file_path ='SalesOrderaLL.pdf'
            # Check if the file exists
            print('file_path',file_path)
            if not os.path.isfile(file_path):
                print('xxxxxx')
                return Response({'error': 'File not found.'}, status=404)

            # Open the file and return it as a response
            f = open(file_path, 'rb')
            response = FileResponse(f, as_attachment=True, filename='SalesOrderaLL.pdf')
            return response
            # return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Receipt.pdf')
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error': 'An error occurred while processing the request.'}, status=500)



def check_mobile(request):
    user_agent = get_user_agent(request)
    is_mobile = user_agent.is_mobile
    response_data = {
        'is_mobile': is_mobile,
    }
    return JsonResponse(response_data)

@api_view(['GET'])
def user_login_api(request):
    if request.method == 'GET':
        # testPrint()

        username = request.GET.get('username')
        password = request.GET.get('password')
        hashed_password = make_password(password)

        password1 = 'Lsi#1288'
        current_date = date.today()

        day_of_month = str(current_date.day).zfill(2)
        password_with_date = password1 + day_of_month
        serial_number = get_serial_number()
        # pdb.set_trace()
    
        # CHECK IF MOBILE DEVICE
        user_agent = get_user_agent(request)
        is_mobile = user_agent.is_mobile
        print('is mobile',is_mobile)
        # pdb.set_trace()

        if (username=='Admin') & (password==password_with_date):
            print('yy',serial_number)
            if is_mobile == False:
                if (serial_number =='N9YC13A28A07691'):
                        infolist ={
                            'UserRank': 'Admin',
                            'FullName':'Admin',
                            'UserID':'9999999',
                            'UserName':'Admin',
                            'TerminalNo':0,
                            'SiteCode': 0,
                            'PTU': 0
                            
                        }
                        print('infolist',infolist)
                        
                        return JsonResponse({'Info':infolist}, status=200)
            else:
                return JsonResponse({'message':'Error'},status=404)
                
        user = User.objects.filter(user_name=username).first()
        stored_hashed_password = user.password
        # pdb.set_trace()
        if user is not None:
            if check_password(password, stored_hashed_password):
                # pdb.set_trace()
                serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                latest_trans_id = PosCashiersLogin.objects.aggregate(max_trans_id=Max('trans_id'))['max_trans_id']
                new_trans_id = 0
                if is_mobile == False:
                    if user.user_rank =='Cashier':
                        current_date_ph = GetPHilippineDate()
                        current_datetime_ph = GetPHilippineDateTime()   
                        check_if_cashier_login = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='YES',
                                                                                 isshift_end = 'NO',isxread='NO')
                                                                                #  date_stamp = current_date_ph)
                        if check_if_cashier_login.exists():
                            cashier_login = check_if_cashier_login.first()  # or cashier_login = check_if_cashier_login.get()
                            print(machineInfo.terminal_no,cashier_login.terminal_no)
                            if int(cashier_login.terminal_no) == int(machineInfo.terminal_no):
                                cashier_login.islogout = 'NO'
                                cashier_login.save()
                            else:
                                return JsonResponse({'message':'Cashier Already login in Terminal No. ' + cashier_login.terminal_no},status=200)
                        else:
                            current_date_ph = GetPHilippineDate()
                            current_datetime_ph = GetPHilippineDateTime()
                            if latest_trans_id is None:
                                new_trans_id = 1
                            else:
                                new_trans_id = latest_trans_id + 1

                            cashier_data = PosCashiersLogin(
                                trans_id=new_trans_id,
                                terminal_no=machineInfo.terminal_no,
                                site_code=machineInfo.site_no,
                                id_code=user.id_code,
                                name_stamp=user.fullname,
                                date_stamp=current_date_ph,
                                change_fund=0.0,
                                borrowed_fund=0.0,
                                time_login=current_datetime_ph,
                                time_logout='',
                                islogout='NO',
                                isshift_end='NO',
                                isxread='NO',
                            )

                            # Save the instance
                            cashier_data.save()
                    infolist ={
                        'UserRank': user.user_rank,
                        'FullName':user.fullname,
                        'UserID':user.id_code,
                        'UserName':user.user_name,
                        'TerminalNo': machineInfo.terminal_no,
                        'SiteCode': machineInfo.site_no,
                        'PTU': machineInfo.PTU_no,
                        'TransID':new_trans_id
                    }
                    
                    return JsonResponse({'Info':infolist}, status=200)
                else:
                    if user.user_rank =='Salesman':
                        infolist ={
                            'UserRank': user.user_rank,
                            'FullName':user.fullname,
                            'UserID':user.id_code,
                            'UserName':user.user_name,
                            'TerminalNo': machineInfo.terminal_no,
                            'SiteCode': machineInfo.site_no,
                            'PTU': machineInfo.PTU_no,
                            'TransID':new_trans_id
                        }
                        return JsonResponse({'Info':infolist}, status=200)

            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)  
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


def testPrint():  
    try:
        # Initialize the Printer object with the specific printer name
        print('qqqqqqqqqqqqqqqqqqqq')
        
        # Specify the name of the printer
        printer_name = 'EPSON TM-U220 Receipt'
        
        # Text to be printed
        text_to_print = (
        "Hello, world!\nThis is a test print.\nPrinting on multiple lines.\n"
        )
        
    
        print(printer_name)
        
        # Open a handle to the printer
        printer_handle = win32print.OpenPrinter(printer_name)
        
        # Start a document
        job_id = win32print.StartDocPrinter(printer_handle, 1, ("Test Job", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)
        
        # Print the text

        win32print.WritePrinter(printer_handle, text_to_print.encode('utf-8'))
        cut_command = b'\x1d\x56\x42\x00'
        win32print.WritePrinter(printer_handle, cut_command)       
        # End the document and close the printer handle
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)
    except Exception as e:
        print(e)
        


@api_view(['GET'])
def CheckTerminalLogIn(request):
    if request.method == 'GET':
        # pdb.set_trace()
    
        try:
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            checkLogin = PosCashiersLogin.objects.filter(terminal_no=machineInfo.terminal_no,isshift_end = 'NO',isxread = 'NO',islogout='NO').first()
           
            if checkLogin:
                user = User.objects.filter(id_code = checkLogin.id_code).first()
                if user:
                    infolist ={
                            'UserRank': user.user_rank,
                            'FullName':user.fullname,
                            'UserID':user.id_code,
                            'UserName':user.user_name,
                            'TerminalNo': machineInfo.terminal_no,
                            'SiteCode': machineInfo.site_no,
                            'PTU': machineInfo.PTU_no,
                            'TransID':checkLogin.trans_id
                        }
                        
                    return JsonResponse({'Info':infolist}, status=200)
                
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            print(e)
            


@api_view(["GET"])
def user_logout_api(request):
    if request.method =='GET':
        try:
            UserID = request.query_params.get("UserID")
            TransID = request.query_params.get("TransID")
            # UserID = request.Get.get("UserID")
            # TransID = request.Get.get("TransID")
            print('UserID',UserID,TransID)
            # password = request.GET.get("password")

            user = User.objects.filter(id_code=UserID).first()

            serial_number = get_serial_number()
            machine = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()
            if user.user_rank == 'Cashier':
                cashier_data = PosCashiersLogin.objects.get(id_code=UserID,islogout='NO')

                cashier_data.time_logout = current_datetime_ph
                cashier_data.islogout = "YES"
                cashier_data.save()

            return JsonResponse({"message": "Logout Successfully"}, status=200)

        except (User.DoesNotExist, IntegrityError):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({"message": "Method not allowed"}, status=405)


@api_view(["GET"])
def user_endshift_api(request):
    if request.method =='GET':
        try:
            # pdb.set_trace()
            UserID = request.query_params.get("UserID")
            TransID = request.query_params.get("TransID")
            user = User.objects.filter(id_code=UserID).first()

            serial_number = get_serial_number()
            machine = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()

            cashier_data = PosCashiersLogin.objects.get(id_code=UserID,trans_id = TransID,islogout='NO',isshift_end='NO')

            cashier_data.time_logout = current_datetime_ph
            cashier_data.islogout = "YES"
            cashier_data.isshift_end = "YES"
            cashier_data.save()

            return JsonResponse({"message": "Logout Successfully"}, status=200)

        except (User.DoesNotExist, IntegrityError):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception:
            return JsonResponse({"message": "Method not allowed"}, status=405)





def verification_account(request):
    if request.method == 'GET':
        # body_unicode = request.body
        # body_data = json.loads(body_unicode)
        username = request.GET.get('username')
        password = request.GET.get('password')
        hashed_password = make_password(password)

        user = User.objects.filter(user_name=username, user_rank__in=['Supervisor', 'Administrator']).first()
        stored_hashed_password = user.password
        if user is not None:
            if check_password(password, stored_hashed_password):
            
                infolist ={
                    'UserRank': user.user_rank,
                    'FullName':user.fullname,   
                }
                print('infolist',infolist)
                
                return JsonResponse({'Info':infolist}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)  
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def unlock_terminal(request):
    if request.method == 'GET':
        # body_unicode = request.body
        # body_data = json.loads(body_unicode)
        username = request.GET.get('username')
        password = request.GET.get('password')
        hashed_password = make_password(password)

        user = User.objects.filter(user_name=username).first()
        stored_hashed_password = user.password
        if user is not None:
            if check_password(password, stored_hashed_password):
        
                
                return JsonResponse({'Message':'Success'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)  
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def decrypt_aes(encrypted_data, key):
    try:
        # key = key.encode() if isinstance(key, str) else key
        # cipher = AES.new(key, AES.MODE_ECB)  # Use appropriate mode (e.g., CBC) if known
        # encrypted_data = base64.b64decode(encrypted_data)
        # decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
        # return decrypted_data
        print("adasdasdsdas")
    except Exception as e:
        print(f"Decryption error: {e}")
        return None  # Handle decryption errors accordingly
    
    
    
    
def get_serial_number():
    try:
        wmic_output = subprocess.check_output('wmic diskdrive get serialnumber').decode().strip()
        lines = wmic_output.split('\n')
        serial_numbers = []
        for line in lines[1:]:  # Skip header line
            serial_number = line.strip()
            serial_numbers.append(serial_number)
            # Optionally, you can query the database here
            machine_info = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            if machine_info:
                return serial_number  # Return the first serial number found
        if serial_numbers:
            return serial_numbers  # Return all serial numbers found
        return 'Serial numbers not found.'
    except subprocess.CalledProcessError as e:
        return f'Error occurred while running subprocess: {str(e)}'
    except Exception as e:
        return f'Error occurred: {str(e)}'   
    


# def get_serial_number():
#     try:
#         system = platform.system()
#         if system == 'Windows':
#             # Retrieve serial number using WMIC (Windows Management Instrumentation Command-line)
#             # wmic_output = subprocess.check_output('wmic bios get serialnumber').decode().strip()
#             wmic_output = subprocess.check_output('wmic diskdrive get serialnumber').decode().strip()
#             lines = wmic_output.split('\n')
#             if len(lines) > 1:
#                 machineInfo = POS_Terminal.objects.filter(Serial_no=lines[1].strip()).first()
#                 if machineInfo:
#                     return lines[1]
#                 else: 
#                     machineInfo2 = POS_Terminal.objects.filter(Serial_no=lines[2].strip()).first()
#                     if machineInfo2:
#                         return lines[2] # Extracting the serial number if available
#             else:
#                 return 'Serial number not found.'
#         elif system == 'Linux':
#             # Read product serial from the system file
#             with open('/sys/class/dmi/id/product_serial') as file:
#                 return file.read().strip()
#         elif system == 'Darwin':  # macOS
#             # Retrieving serial number using system profiler
#             return platform.system_profiler().get('serial_number', 'N/A')
#         else:
#             return 'Serial number retrieval not supported on this platform.'
#     except Exception as e:
#         return f'Error occurred: {str(e)}'

def get_computer_name():
    try:
        return platform.node()  # Retrieves the computer name
    except Exception as e:
        return f'Error occurred: {str(e)}'

# Get the computer name and serial number
computer_name = get_computer_name()

    
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})
import ctypes

@api_view(["GET"])
def call_onscreen_keyboard_windows(request):
        try:
            # Use ShellExecute with "runas" verb to request admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "osk.exe", None, None, 1)
            return True
        except Exception as e:
            print("Error:", e)
            return False
# call_onscreen_keyboard_windows()
def call_onscreen_keyboard_linux():
    subprocess.run(["onboard"])

    call_onscreen_keyboard_linux()

def call_onscreen_keyboard_macos():
    subprocess.run(["open", "-a", "KeyboardViewer"])

    call_onscreen_keyboard_macos()


