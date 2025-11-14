
import pdb
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
import pytz
# from backend.models import (CompanySetup, User,POS_Terminal,PosCashiersLogin,PosSalesTransSeniorCitizenDiscount,SalesTransCreditCard,SalesTransEPS,PosSalesTransCreditSale,BankCompany)
# from backend.serializers import (UserSerializer,POS_TerminalSerializer,PosCashiersLoginpSerializer,PosSalesTransSeniorCitizenDiscountSerializer)
from backend.models import *
from backend.serializers import *
from rest_framework.decorators import api_view

from django.middleware.csrf import get_token
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
import json
import base64 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

import platform
import subprocess
from datetime import date, timedelta,datetime
from django.utils import timezone
from django.db.models import Max
# Get current date
from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime,GetCompanyConfig
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django_user_agents.utils import get_user_agent
from cryptography.hazmat.primitives import padding
from pyprinter import Printer

from django.db.models import Sum, Case, When, F, FloatField,Count
from django.test import TestCase
from reportlab.lib.units import mm,cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import traceback
import textwrap
from backend.models import *
from backend.serializers import *
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import FileResponse
import subprocess
from django.conf import settings
from django.http import JsonResponse,FileResponse
from rest_framework.response import Response
from django.db import connection

from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework import status, permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.auth.authentication import CookieJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

@api_view(['GET'])
def check_access_token(request):
    auth = CookieJWTAuthentication()
    try:
        user, token = auth.authenticate(request)
        if user:
            return Response({"valid": True})
        else:
            return Response({"valid": False})
    except InvalidToken:
        return Response({"valid": False})

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


# def print_pdf_to_printer(printer_name, pdf_path):
#     try:
#         # Path to SumatraPDF executable
#         sumatra_path = r'C:\Program Files\SumatraPDF\SumatraPDF.exe'  # Update this path if needed

#         # Define the command to print the PDF
#         print_command = [
#             sumatra_path,
#             '-print-to', printer_name,
#             '-print-settings', 'noscale',  # Print using actual size
#             pdf_path
#         ]
        
        
#         # Debugging: print the command to verify it
#         print("Print command:", " ".join(print_command))

#         # Run the print command
#         subprocess.run(print_command, check=True)
        
#         print("Printing complete.")
        
#     except subprocess.CalledProcessError as sumatra_error:
#         print("SumatraPDF error: ", sumatra_error)
#     except Exception as e:
#         print("Exception occurred: ", e)


# def print_pdf_to_printer1(printer_name, pdf_path):
#     try:
#         # Open the PDF file
#         with fitz.open(pdf_path) as pdf_document:
#             # Create a printer handle for the specified printer
#             printer_handle = win32print.OpenPrinter(printer_name)
            
#             # Start a print job
#             job_info = win32print.StartDocPrinter(printer_handle, 1, ("SalesOrder", None, "RAW"))
            
#             # Start a new page
#             win32print.StartPagePrinter(printer_handle)
            
#             # Extract text from each page and send it to the printer
#             for page_number in range(pdf_document.page_count):
#                 page = pdf_document.load_page(page_number)
#                 page_text = page.get_text()
#                 win32print.WritePrinter(printer_handle, page_text.encode("utf-8"))
            
#             # End the page and the print job
#             # cut_command = b'\x1D\x56\x00'  # ESC/POS command for full cut
#             # win32print.WritePrinter(printer_handle, cut_command)   
#             cut_command = b'\x1d\x56\x42\x00'
#             win32print.WritePrinter(printer_handle, cut_command)  
#             win32print.EndPagePrinter(printer_handle)
#             win32print.EndDocPrinter(printer_handle)
            
#             # Close the printer handle
#             win32print.ClosePrinter(printer_handle)

#         print("Printing complete.")
        
#     except Exception as e:
#         print("Exception occurred: ", e)
# def print_pdf_salesOrder():
#     """Prints the SalesOrder.pdf file to the default printer."""
#     try:
#         # Get the default printer
#         printer_setup = GetCompanyConfig('multiple_printer')
#         print('printer_setup',printer_setup)

#         if printer_setup == 'False':
#             printer_name = win32print.GetDefaultPrinter()
#             print(f"Default printer: {printer_name}")
            
#             # Replace this with the path to your PDF file
#             pdf_file_path = "SalesOrder.pdf"
            
#             # Print the PDF file to the default printer
#             print(f"Printing '{pdf_file_path}' to '{printer_name}'...")
#             print_pdf_to_printer(printer_name, pdf_file_path)
#         else:
#             printer_list = POSProductPrinter.objects.all()
#             for printer_name in printer_list:
#                 print(f"printer_name: {printer_name.printer_name}")
            
#             # Replace this with the path to your PDF file
#                 pdf_file_path = "SalesOrder.pdf"
            
#                 # Print the PDF file to the default printer
#                 print(f"Printing '{pdf_file_path}' to '{printer_name.printer_name}'...")
#                 print_pdf_to_printer(printer_name.printer_name, pdf_file_path)



        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         traceback.print_exc()



#    PDFSalesOrder(cart_items,so_no,table_no,QueNo,guest_count,customer)
##*************CREATE SALES ORDER RECEIPT - PER CATEGORY SETUP ***************
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
      
        line_height = 0.3 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 79 * mm  # Width adjusted for 79 mm roll paper
        # Set the initial height for the first page

        # Calculate the required height based on the data length
        height = (len(data) + 20) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

        # Create a canvas with calculated size
        c = canvas.Canvas(f"SalesOrder{cashierID}.pdf", pagesize=(width, height))

        # Set up a font and size
     
        c.setFont("Courier", 8)
        c.setLineWidth(0.5)
        # Calculate x-coordinate for center alignment of "SALES INVOICE"
        text_width = c.stringWidth("SALES ORDER")
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
            text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)

        
        
        if QueNo != 0:
            y_position -= line_height
            c.drawString(10 * mm, y_position, "QueNo: " f'{QueNo}')
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
            c.drawRightString(width - margin, y_position, guest_count_text)
        y_position -= line_height
        y_position -= line_height
        text_width = c.stringWidth(order_type)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{order_type}')
        y_position -= line_height
        # Draw Line
        c.line(x_start, y_position - 2, x_end, y_position - 2)
    
        # Update y_position for the next line
        y_position -= line_height
        text_width = c.stringWidth(f'{PrintLocation}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{PrintLocation}')
        y_position -= line_height
        text_width = c.stringWidth(f'SO#{SO}')
        x_center = (width - text_width) / 2
        # Draw the Sales Order number (SO#)
        c.drawString(x_center, y_position, f'SO#{SO}')

        # Update y_position for the next line
        y_position -= line_height

        # Get the current date and time
        date_time = GetPHilippineDateTime()
        text_width = c.stringWidth(date_time)
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
            c.setFont("Courier", 9)
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
    
##*************CREATE SALES ORDER RECEIPT - CASHIER***************
def PDFSalesOrderaLL(data,SO,TableNo,QueNo,GuestCount,Customer,order_type,cashierID,PrinterName,PrintLocation):
    try:
        Cashier_Name = ''
        cashier = User.objects.filter(id_code=cashierID).first()
        if cashier:
            Cashier_Name = cashier.fullname
        
        total_qty = 0
        hyphen_line = "-" * 55  # 55 hyphens in a row
        margin_right = 10 * mm
        x_start = 2 * mm  # Starting x-coordinate
        x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)
        line_height = 0.3 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 85 * mm  # Width adjusted for 79 mm roll paper
        # Set the initial height for the first page

        # Calculate the required height based on the data length
        height = (len(data) + 20) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

        # Create a canvas with calculated size
        c = canvas.Canvas(f"SalesOrderaLL{cashierID}.pdf", pagesize=(width, height))

        # Set up a font and size
     
        c.setFont("Courier", 8)
        c.setLineWidth(0.5)
        c.setDash(2,1)
        # Calculate x-coordinate for center alignment of "SALES INVOICE"
        text_width = c.stringWidth("SALES ORDER")
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
            text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, guest_count_text)

        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Table No.: " f'{TableNo}')
        #     y_position -= line_height
        #     c.drawString(10 * mm, y_position, "Guest Count: " f'{GuestCount}')
        
        
        if QueNo != 0 and QueNo != '' and QueNo != '0':
            y_position -= line_height
            c.drawString(10 * mm, y_position, "QueNo: " f'{QueNo}')
            guest_count_text = f"Guest Count: {GuestCount}"
            text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, guest_count_text)
        y_position -= line_height
        y_position -= line_height
        text_width = c.stringWidth(order_type)
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{order_type}')
        y_position -= line_height
        # Draw Line
        c.line(x_start, y_position - 2, x_end, y_position - 2)
    
        # Update y_position for the next line
        y_position -= line_height
        text_width = c.stringWidth(f'{PrintLocation}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{PrintLocation}')
        y_position -= line_height
        text_width = c.stringWidth(f'SO#{SO}')
        x_center = (width - text_width) / 2
        # Draw the Sales Order number (SO#)
        c.drawString(x_center, y_position, f'SO#{SO}')

        # Update y_position for the next line
        y_position -= line_height

        # Get the current date and time
        date_time = GetPHilippineDateTime()
        text_width = c.stringWidth(date_time)
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
            c.setFont("Courier", 9)
            c.setFillColor(colors.black)
            quantity_str = str(quantity).replace('"', '').strip()
            quantity_str = float(quantity_str)
            #check if decimal part > 0
            if quantity_str % 1 > 0:
                quantity_str = float(quantity_str)
            else:
                quantity_str = int(quantity_str)
            text_to_draw = f"{quantity_str} {description}"

            wrapped_description = textwrap.wrap(description, width=25)

            if wrapped_description:
                text_to_draw = f"{quantity_str} {wrapped_description[0]}"
                c.drawString(10 * mm, y_position, text_to_draw)
                y_position -= line_height

                # Draw the rest of the wrapped lines without quantity
            for line in wrapped_description[1:]:
                quantity_str = str(quantity).ljust(3) 
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
        print('already save pdf sales order')
        c.save()
        # print_pdf_to_printer(PrinterName,'SalesOrder.pdf')
    except Exception as e:
        print(e)
        traceback.print_exc()
    

##*************CREATE OR/SI RECEIPT ***************
def PDFReceipt(request,doc_no,doc_type,cusData):
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
            gift_check_payment = 0
            online_payment = 0
            other_payment = 0
            multiple_payment = 0
            payment_method = 'CASH'
            is_credit_card_payment = False
            is_debit_card_payment = False
            is_cash_payment = False
            is_gift_check_payment = False
            is_online_payment = False
            is_other_payment = False
            Service_Charge = 0
            total_sc_discount = 0
            total_item_discount = 0
            total_trade_discount = 0
            total_transaction_discount = 0
            total_pwd_discount = 0
            total_athlete_discount = 0
            



            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        
            

            # GET DATA IN SALES INVOICE LIST
            data_list = PosSalesInvoiceList.objects.filter(doc_no=doc_no,doc_type=doc_type,terminal_no=machineInfo.terminal_no
                                                           ,site_code =machineInfo.site_no).first()
            if data_list:
                Service_Charge = data_list.ServiceCharge_TotalAmount
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
                if data_list.gift_check != 0:
                    gift_check_payment = data_list.gift_check 
                    is_gift_check_payment = True
                if data_list.online_payment != 0:
                    online_payment = data_list.online_payment
                    is_online_payment = True
                if data_list.other_payment != 0:
                    other_payment = data_list.other_payment
                    is_other_payment  = True
                # data_tmp = PosSalesInvoiceListSerializer(data_list,many=True).data

                # if data_tmp:
                #     data_tmp.

            # GET DATA IN SALES INVOICE LISTING
            data_listing = PosSalesInvoiceListing.objects.filter(doc_no=doc_no,doc_type=doc_type,terminal_no=machineInfo.terminal_no
                                                           ,site_code =machineInfo.site_no, isvoid ='NO')
            if data_listing:
                data = PosSalesInvoiceListingSerializer(data_listing,many=True).data

            # GET DATA IN TABLE POS SALES TRANS
            pos_sales_trans = PosSalesTrans.objects.filter(sales_trans_id=int(float(doc_no)),document_type='SI',terminal_no=machineInfo.terminal_no
                                                           ,site_code = int(machineInfo.site_no)).first()
            
            if pos_sales_trans:
                Amount_Tendered = pos_sales_trans.amount_tendered
                Cashier_ID = pos_sales_trans.cashier_id
                # cash_payment = Amount_Tendered
                # pos_sales_trans_data = PosSalesTransSerializer(pos_sales_trans,many=True).data
            companyCode = getCompanyData()
            clientSetup = getClientSetup()

            # Determine the width and height based on the data length
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
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
            print('sc discount',SC_Dicount)
            if SC_Dicount:
                print('with SC discount')
                height = ((len(data)* 2) + 70 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
            else:
                height = ((len(data)* 2) + 60 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
            # height = ((len(data)* 2) + 60 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"Receipt{int(float(doc_no))}.pdf", pagesize=(width, height))

            # Set up a font and size
        
            c.setFont("Courier", 8)
            c.setLineWidth(0.5)
            c.setDash(2,1)
            y_position = height - margin - line_height 


            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height
    

            # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("SALES INVOICE")
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
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            if QueNo != 0:
                Order_Type = 'TAKE OUT'
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"QueNo.: {QueNo}")
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            y_position -= line_height

            text_width = c.stringWidth(f'{Order_Type}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'{Order_Type}')
            y_position -= line_height


            c.line(x_start, y_position, x_end, y_position)
            text_width = c.stringWidth(f'SI#{int(float(doc_no))}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'SI#{int(float(doc_no))}')
            y_position -= line_height

            # Get the current date and time
            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
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
                sub_total_char_width = c.stringWidth(f'{sub_total}')  # Use appropriate font and size
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
            total_due_char_width = c.stringWidth(f'{Total_due}')  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height

            # #*********** Service Charge *************
            # if Service_Charge != 0:
            #     Total_due += float(Service_Charge)
            #*********** Senior Discount *************
            if SC_Dicount == True:
                Less_Vat = 0
                Net_of_vat = 0
                Less_Discount = 0
                Amount_covered = 0
                # Get all SC amounts for this transaction
                SC_Covered = PosSalesTransSeniorCitizenDiscount.objects.filter(sales_trans_id=int(float(doc_no)),)
                SCGuestCount = 0
                if SC_Covered:
                    for amount in SC_Covered:
                        Amount_covered =  float(str(amount.amount_covered).replace(',',''))
                        SCGuestCount = 1 + SCGuestCount

                # Compute SC + VAT
                result = compute_total_due(
                    Total_due=Total_due,
                    Amount_covered=Amount_covered,
                    SCGuestCount=SCGuestCount,
                    GuestCount=GuestCount
                )

                x = Total_due / GuestCount

                if GuestCount != SCGuestCount:
                    vatable_val = float(x) * float(GuestCount - SCGuestCount)
                    
                    vatable_val = (vatable_val / 1.12) / SCGuestCount
                else:
                    vatable_val = 0
                    
                    vatable_val = 0


                # Extract numeric values
                Less_Vat_val = result["Less_Vat"]
                Net_of_vat_val = result["Net_of_vat"]
                Less_Discount_val = result["Less_Discount"]
                vat_exempt_val = result["total_vat_exempt"]
                vat_val = result["total_vat"]        # this is the VAT amount (12%)
                SC_Total_due_val = result["total_due"]
                total_sc_discount_val = result["total_sc_discount"]
                # Create formatted strings for printing
                Less_Vat = Less_Vat_val
                Net_of_vat = Net_of_vat_val
                Less_Discount = Less_Discount_val
                vat_exempt = vat_exempt_val
                vatable = vatable_val
                vat = vat_val
                SC_Total_due = SC_Total_due_val
                total_sc_discount = total_sc_discount_val
                
               
                # Print values
                y_position -= line_height
                c.drawString(10 * mm, y_position, f'Less 20% VAT: {Amount_covered}')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Net of VAT:')
                c.drawRightString(width - margin_right, y_position, f'{result["Net_of_vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Less 20% Discount:')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Discount"]:,.2f}')
                y_position -= line_height
               
                Total_due_net = float(result["total_due"])
                Total_due = Total_due_net
                if Service_Charge != 0:
                    
                    
                    c.drawString(10 * mm, y_position,'Service Charge:')
                    c.drawRightString(width - margin_right, y_position, f'{float(Service_Charge):,.2f}')
                    y_position -= line_height
                    Total_due_net = Total_due_net + Service_Charge
                    Total_due = Total_due_net

                c.line(x_start, y_position, x_end, y_position)
                y_position -= line_height
                c.drawString(10 * mm, y_position,'TOTAL DUE:')
                c.drawRightString(width - margin_right, y_position, f'{float(Total_due_net):,.2f}')

            # ************** VAT DATA ****************
            y_position -= line_height
        
            if Item_Dicount == True:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat
            elif SC_Dicount == True:
                vat = vat
                vatable = vatable
        
            else:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat


            c.drawString(10 * mm, y_position, 'Vatable:')
            c.drawRightString(width - margin_right, y_position, f'{vatable:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT Exempt:')
            c.drawRightString(width - margin_right, y_position, f'{vat_exempt:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'Non-VAT:')
            c.drawRightString(width - margin_right, y_position, f'{non_vat:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT Zero Rated:')
            c.drawRightString(width - margin_right, y_position, f'{vat_zero_rated:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT:')
            c.drawRightString(width - margin_right, y_position, f'{vat:,.2f}')
            y_position -= line_height

            if Service_Charge != 0:
                
                    c.drawString(10 * mm, y_position,'Service Charge:')
                    c.drawRightString(width - margin_right, y_position, f'{float(Service_Charge):,.2f}')
                    y_position -= line_height
            # L**************END VAT ****************

            # L************** NEW double dash line ****************
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            # L************** END double dash line ****************

            if SC_Dicount == False:
                Total_due = Total_due + Service_Charge

            y_position -= line_height
            c.drawString(10 * mm, y_position,'TOTAL DUE:')
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height
          
            if is_cash_payment:
                y_position -= line_height
                c.drawString(10 * mm, y_position,'CASH:')
                if cash_payment > 0 and is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment: 
                    
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                else:
                    cash_payment = Amount_Tendered
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                y_position -= line_height
                if is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment:
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
                        full_card_number = item.card_no
                        masked_card_number = '*' * (len(full_card_number) - 4) + full_card_number[-4:]  # Mask all but the last four digits

                        c.drawString(10 * mm, y_position,'Credit Card No.:')
                        c.drawRightString(width - margin_right, y_position, f'{masked_card_number}')
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
                        full_card_number = item.card_no
                        masked_card_number = '*' * (len(full_card_number) - 4) + full_card_number[-4:]  # Mask all but the last four digits

                        c.drawString(10 * mm, y_position,'Debit Card No:')
                        c.drawRightString(width - margin_right, y_position, f'{masked_card_number}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Bank:')
                        bankName = BankCompany.objects.filter(id_code=int(float(item.bank))).first()
                        if bankName:
                            c.drawRightString(width - margin_right, y_position, f'{bankName.company_description}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Card Holder:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_holder}')
                        y_position -= line_height

            if is_gift_check_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'GIFT CHCEK:')
                c.drawRightString(width - margin_right, y_position, f'{float(gift_check_payment):,.2f}')
                y_position -= line_height
            
            if is_online_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'ONLINE:')
                c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
                y_position -= line_height

            if is_other_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'OTHER:')
                c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
                y_position -= line_height

            if payment_method =='CREDIT SALES':
                y_position -= line_height
                c.drawString(10 * mm, y_position,'CHARGE:')
                c.drawRightString(width - margin_right, y_position, f'{float(credit_card_payment):,.2f}')
            if is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment and cash_payment > 0   :
                c.drawString(10 * mm, y_position,'CHANGE:')
                change_amount = (cash_payment + online_payment + other_payment + gift_check_payment + debit_card_payment + credit_card_payment)- Total_due
                c.drawRightString(width - margin_right, y_position, f'{float(change_amount):,.2f}')

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
            c.drawRightString(width - margin_right, y_position, f'{Customer}')

            name_width = c.stringWidth('Customer Name:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{Customer}')
            value_width = c.stringWidth(f'{Customer}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Address:')
            c.drawRightString(width - margin_right, y_position, f'{CusAddress}')

            name_width = c.stringWidth('Address:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusAddress}')
            value_width = c.stringWidth(f'{CusAddress}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'TIN:')
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')

            name_width = c.stringWidth('TIN:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')
            value_width = c.stringWidth(f'{CusTIN}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Business Style:')
            c.drawRightString(width - margin_right, y_position, f'{CusBusiness}')

            name_width = c.stringWidth('Business Style:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position,  f'{CusBusiness}')
            value_width = c.stringWidth(f'{CusBusiness}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)
            y_position -= line_height
            y_position -= line_height
            

            text_width = c.stringWidth("THIS SERVES AS AN OFFICIAL RECEIPT")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THIS SERVES AS AN OFFICIAL RECEIPT")
            y_position -= line_height
            y_position -= line_height
            text_width = c.stringWidth("THANK YOU, COME AGAIN... ")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THANK YOU, COME AGAIN... ")

            y_position -= line_height
            y_position -= line_height
            lead = getLeadSetup()

            if lead:
                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name}')
                if lead.company_name2 !='':
                    y_position -= line_height
                    text_width = c.stringWidth(f'{lead.company_name2}')
                    x_center = (width - text_width) / 2
                    c.drawString(x_center, y_position, f'{lead.company_name2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address}')
                if lead.company_address2 !='':
                    y_position -= line_height
                    text_width = c.stringWidth(f'{lead.company_address2}')
                    x_center = (width - text_width) / 2
                    c.drawString(x_center, y_position, f'{lead.company_address2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.tin}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.tin}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.accreditation_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.accreditation_no}')


                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_issued}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_issued}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_valid}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_valid}')


                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.PTU_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.PTU_no}')

                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.date_issue}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.date_issue}')
            # Save the PDF
            print('already save pdf Sales Invoice')
            c.save()   
        except Exception as e:
            print(e)
            traceback.print_exc()

##*************CREATE REPRINTS OR/SI RECEIPT ***************
def ReprintPDFReceipt(request,doc_no,doc_type,cusData):
        try:
            print('initialize pdf')
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
            gift_check_payment = 0
            online_payment = 0
            other_payment = 0
            multiple_payment = 0
            payment_method = 'CASH'
            is_credit_card_payment = False
            is_debit_card_payment = False
            is_cash_payment = False
            is_gift_check_payment = False
            is_online_payment = False
            is_other_payment = False
            Service_Charge = 0
            total_sc_discount = 0
            total_item_discount = 0
            total_trade_discount = 0
            total_transaction_discount = 0
            total_pwd_discount = 0
            total_athlete_discount = 0
            



            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
    
            

            # GET DATA IN SALES INVOICE LIST
            data_list = PosSalesInvoiceList.objects.filter(doc_no=doc_no,doc_type=doc_type,terminal_no=machineInfo.terminal_no
                                                           ,site_code =machineInfo.site_no).first()
            if data_list:
                Service_Charge = data_list.ServiceCharge_TotalAmount
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
                if data_list.gift_check != 0:
                    gift_check_payment = data_list.gift_check 
                    is_gift_check_payment = True
                if data_list.online_payment != 0:
                    online_payment = data_list.online_payment
                    is_online_payment = True
                if data_list.other_payment != 0:
                    other_payment = data_list.other_payment
                    is_other_payment  = True
                # data_tmp = PosSalesInvoiceListSerializer(data_list,many=True).data

                # if data_tmp:
                #     data_tmp.

            # GET DATA IN SALES INVOICE LISTING
            data_listing = PosSalesInvoiceListing.objects.filter(doc_no=doc_no,doc_type=doc_type,terminal_no=machineInfo.terminal_no
                                                           ,site_code =machineInfo.site_no, isvoid ='NO')
            if data_listing:
                data = PosSalesInvoiceListingSerializer(data_listing,many=True).data

            # GET DATA IN TABLE POS SALES TRANS
            pos_sales_trans = PosSalesTrans.objects.filter(sales_trans_id=int(float(doc_no)),document_type='SI',terminal_no=machineInfo.terminal_no
                                                           ,site_code = int(machineInfo.site_no)).first()
            
            if pos_sales_trans:
                Amount_Tendered = pos_sales_trans.amount_tendered
                Cashier_ID = pos_sales_trans.cashier_id
                # cash_payment = Amount_Tendered
                # pos_sales_trans_data = PosSalesTransSerializer(pos_sales_trans,many=True).data
            

            companyCode = getCompanyData()
            clientSetup = getClientSetup()

            # Determine the width and height based on the data length
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
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
            if SC_Dicount:
                height = ((len(data)* 2) + 70 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
            else:
                height = ((len(data)* 2) + 60 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"ReprintReceipt{int(float(doc_no))}.pdf", pagesize=(width, height))

            # Set up a font and size
            c.setFont("Courier", 8)
            c.setLineWidth(0.5)
            c.setDash(2,1)
            # 
            y_position = height - margin - line_height 


            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height

            text_width = c.stringWidth("RE-PRINT")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "RE-PRINT")
            y_position -= line_height

    

            # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("SALES INVOICE")
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
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            if QueNo != 0:
                Order_Type = 'TAKE OUT'
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"QueNo.: {QueNo}")
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            y_position -= line_height

            text_width = c.stringWidth(f'{Order_Type}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'{Order_Type}')
            y_position -= line_height

          
            c.line(x_start, y_position, x_end, y_position)
            text_width = c.stringWidth(f'SI#{int(float(doc_no))}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'SI#{int(float(doc_no))}')
            y_position -= line_height

            # Get the current date and time
            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
            x_center = (width - text_width) / 2
            # Draw the date and time
            c.drawString(x_center, y_position, f'{date_time}')

            # Update y_position for the next content
            y_position -= (line_height - 0.2 * cm)

        # 3 points on, 2 points off
            c.line(x_start, y_position, x_end, y_position)
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
                sub_total_char_width = c.stringWidth(f'{sub_total}')  # Use appropriate font and size
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
            total_due_char_width = c.stringWidth(f'{Total_due}')  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height

            # #*********** Service Charge *************
            # if Service_Charge != 0:
            #     Total_due += float(Service_Charge)
            #*********** Senior Discount *************
            if SC_Dicount == True:
                Less_Vat = 0
                Net_of_vat = 0
                Less_Discount = 0
                Amount_covered = 0
                # Get all SC amounts for this transaction
                SC_Covered = PosSalesTransSeniorCitizenDiscount.objects.filter(sales_trans_id=int(float(doc_no)),)
                SCGuestCount = 0
                if SC_Covered:
                    for amount in SC_Covered:
                        Amount_covered =  float(str(amount.amount_covered).replace(',',''))
                        SCGuestCount = 1 + SCGuestCount
                result = compute_total_due(
                    Total_due=Total_due,
                    Amount_covered=Amount_covered,
                    SCGuestCount=SCGuestCount,
                    GuestCount=GuestCount
                )

                x = Total_due / GuestCount

                if GuestCount != SCGuestCount:
                    vatable_val = float(x) * float(GuestCount - SCGuestCount)
                    
                    vatable_val = (vatable_val / 1.12) / SCGuestCount
                else:
                    vatable_val = 0
                    
                    vatable_val = 0


                # Extract numeric values
                Less_Vat_val = result["Less_Vat"]
                Net_of_vat_val = result["Net_of_vat"]
                Less_Discount_val = result["Less_Discount"]
                vat_exempt_val = result["total_vat_exempt"]
                vat_val = result["total_vat"]        # this is the VAT amount (12%)
                SC_Total_due_val = result["total_due"]
                total_sc_discount_val = result["total_sc_discount"]
                # Create formatted strings for printing
                Less_Vat = Less_Vat_val
                Net_of_vat = Net_of_vat_val
                Less_Discount = Less_Discount_val
                vat_exempt = vat_exempt_val
                vatable = vatable_val
                vat = vat_val
                SC_Total_due = SC_Total_due_val
                total_sc_discount = total_sc_discount_val
                
               
                # Print values
                y_position -= line_height
                c.drawString(10 * mm, y_position, f'Less 20% VAT: {Amount_covered}')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Net of VAT:')
                c.drawRightString(width - margin_right, y_position, f'{result["Net_of_vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Less 20% Discount:')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Discount"]:,.2f}')
                y_position -= line_height

                Total_due_net = float(result["total_due"])
                Total_due = Total_due_net
                if Service_Charge != 0:
                    
                    
                    c.drawString(10 * mm, y_position,'Service Charge:')
                    c.drawRightString(width - margin_right, y_position, f'{float(Service_Charge):,.2f}')
                    y_position -= line_height
                    Total_due_net = Total_due_net + Service_Charge
                    Total_due = Total_due_net

                c.line(x_start, y_position, x_end, y_position)
                y_position -= line_height
                c.drawString(10 * mm, y_position,'TOTAL DUE:')
                c.drawRightString(width - margin_right, y_position, f'{float(Total_due_net):,.2f}')
                y_position -= line_height
                

            # ************** VAT DATA ****************
            y_position -= line_height
        
            if Item_Dicount == True:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat
            elif SC_Dicount == True:
                vat = vat
                vatable = vatable
        
            else:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat



            c.drawString(10 * mm, y_position, 'Vatable:')
            c.drawRightString(width - margin_right, y_position, f'{vatable:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT Exempt:')
            c.drawRightString(width - margin_right, y_position, f'{vat_exempt:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'Non-VAT:')
            c.drawRightString(width - margin_right, y_position, f'{non_vat:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT Zero Rated:')
            c.drawRightString(width - margin_right, y_position, f'{vat_zero_rated:,.2f}')

            y_position -= line_height
            c.drawString(10 * mm, y_position, 'VAT:')
            c.drawRightString(width - margin_right, y_position, f'{vat:,.2f}')
            y_position -= line_height


            if Service_Charge != 0:
                
                    c.drawString(10 * mm, y_position,'Service Charge:')
                    c.drawRightString(width - margin_right, y_position, f'{float(Service_Charge):,.2f}')
                    y_position -= line_height
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
                if cash_payment > 0 and is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment: 
                    
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                else:
                    cash_payment = Amount_Tendered
                    c.drawRightString(width - margin_right, y_position, f'{float(cash_payment):,.2f}')
                y_position -= line_height
                if is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment:
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
                        full_card_number = item.card_no
                        masked_card_number = '*' * (len(full_card_number) - 4) + full_card_number[-4:]  # Mask all but the last four digits

                        c.drawString(10 * mm, y_position,'Credit Card No.:')
                        c.drawRightString(width - margin_right, y_position, f'{masked_card_number}')
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
                        full_card_number = item.card_no
                        masked_card_number = '*' * (len(full_card_number) - 4) + full_card_number[-4:]  # Mask all but the last four digits

                        c.drawString(10 * mm, y_position,'Debit Card No:')
                        c.drawRightString(width - margin_right, y_position, f'{masked_card_number}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Bank:')
                        bankName = BankCompany.objects.filter(id_code=int(float(item.bank))).first()
                        if bankName:
                            c.drawRightString(width - margin_right, y_position, f'{bankName.company_description}')
                        y_position -= line_height
                        c.drawString(10 * mm, y_position,'Card Holder:')
                        c.drawRightString(width - margin_right, y_position, f'{item.card_holder}')
                        y_position -= line_height

            if is_gift_check_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'GIFT CHCEK:')
                c.drawRightString(width - margin_right, y_position, f'{float(gift_check_payment):,.2f}')
                y_position -= line_height
            
            if is_online_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'ONLINE:')
                c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
                y_position -= line_height

            if is_other_payment:
                # y_position -= line_height
                c.drawString(10 * mm, y_position,'OTHER:')
                c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
                y_position -= line_height

            if payment_method =='CREDIT SALES':
                y_position -= line_height
                c.drawString(10 * mm, y_position,'CHARGE:')
                c.drawRightString(width - margin_right, y_position, f'{float(credit_card_payment):,.2f}')
            if is_credit_card_payment | is_debit_card_payment | is_other_payment | is_online_payment | is_gift_check_payment:
                c.drawString(10 * mm, y_position,'CHANGE:')
                change_amount = (cash_payment + online_payment + other_payment + gift_check_payment + debit_card_payment + credit_card_payment)- Total_due
                c.drawRightString(width - margin_right, y_position, f'{float(change_amount):,.2f}')

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
            c.drawRightString(width - margin_right, y_position, f'{Customer}')

            name_width = c.stringWidth('Customer Name:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{Customer}')
            value_width = c.stringWidth(f'{Customer}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Address:')
            c.drawRightString(width - margin_right, y_position, f'{CusAddress}')

            name_width = c.stringWidth('Address:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusAddress}')
            value_width = c.stringWidth(f'{CusAddress}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'TIN:')
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')

            name_width = c.stringWidth('TIN:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')
            value_width = c.stringWidth(f'{CusTIN}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Business Style:')
            c.drawRightString(width - margin_right, y_position, f'{CusBusiness}')

            name_width = c.stringWidth('Business Style:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusBusiness}')
            value_width = c.stringWidth(f'{CusBusiness}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)
            y_position -= line_height
            y_position -= line_height
            
  
            y_position -= line_height
            text_width = c.stringWidth("THIS SERVES AS AN OFFICIAL RECEIPT")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THIS SERVES AS AN OFFICIAL RECEIPT")
            y_position -= line_height

            y_position -= line_height
            text_width = c.stringWidth("THANK YOU, COME AGAIN... ")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THANK YOU, COME AGAIN... ")
            y_position -= line_height
            y_position -= line_height
            lead = getLeadSetup()

            if lead:
                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name}')
                if lead.company_name2 != '':
                    y_position -= line_height
                    text_width = c.stringWidth(f'{lead.company_name2}')
                    x_center = (width - text_width) / 2
                    c.drawString(x_center, y_position, f'{lead.company_name2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address}')
                if lead.company_address2 !='':
                    y_position -= line_height
                    text_width = c.stringWidth(f'{lead.company_address2}')
                    x_center = (width - text_width) / 2
                    c.drawString(x_center, y_position, f'{lead.company_address2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.tin}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.tin}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.accreditation_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.accreditation_no}')


                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_issued}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_issued}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_valid}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_valid}')


                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.PTU_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.PTU_no}')

                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.date_issue}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.date_issue}')
            # Save the PDF
            print('already save Reprint pdf Sales Invoice')
            c.save()   
        except Exception as e:
            print(e)
            traceback.print_exc()

def compute_total_due(Total_due, Amount_covered, SCGuestCount, GuestCount, VAT_rate=0.12, SC_discount_rate=0.20):
    Total_due = float(Total_due)
    Amount_covered = float(Amount_covered)

    get_sc_discount = PosDiscountSetup.objects.filter(description='SC').first()

    if get_sc_discount:
        desc_rate = float(get_sc_discount.disc_rate)
    else:
        desc_rate = 20

    SC_discount_rate = desc_rate / 100

    # Senior portion
    if SCGuestCount > 0:
        per_sc = Amount_covered / SCGuestCount
        Less_Vat_per_sc = per_sc / (1 + VAT_rate) * VAT_rate
        Less_Discount_per_sc = per_sc / (1 + VAT_rate) * SC_discount_rate

        total_less_vat = Less_Vat_per_sc * SCGuestCount
        total_less_discount = Less_Discount_per_sc * SCGuestCount

        total_vat_exempt = Amount_covered - (total_less_vat + total_less_discount)
    else:
        total_less_vat = 0
        total_less_discount = 0
        total_vat_exempt = 0

    # Non-senior portion
    non_sc_amount = Total_due - Amount_covered
    if non_sc_amount > 0:
        vatable_base = non_sc_amount / (1 + VAT_rate)
        total_vat = vatable_base * VAT_rate
        non_sc_total = vatable_base + total_vat
    else:
        total_vat = 0
        non_sc_total = 0

    # Final total due
    net_total_due = total_vat_exempt + non_sc_total

    return {
        "total_due": round(net_total_due, 2),
        "total_vat": round(total_vat, 2),
        "total_vat_exempt": round(total_vat_exempt, 2),
        "total_sc_discount": round(total_less_discount, 2),
        "Less_Vat": round(total_less_vat, 2),
        "Less_Discount": round(total_less_discount, 2),
        "Net_of_vat": round(Total_due - total_less_vat, 2)
    }

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def PrintBill(request):
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

            Cashier_ID = request.user.id_code

            Item_Dicount = False
            SC_Dicount = False
            Transaction_Dicount = False
            Trade_Dicount = False

            data = ''
            total_qty = 0

            vat = 0
            vatable = 0
            vat_exempt = 0
            vat_zero_rated = 0
            non_vat = 0
            waiter_id = 0
         
            GuestCount =0
            Order_Type ='DINE IN'

            SO_NO =''


            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            
     
            tableno = request.GET.get('tableno','0')
            queno = request.GET.get('queno','0')
            if tableno == '':
                tableno = None
            if queno == '':
                queno = None
            TableNo = int(tableno) if tableno is not None else 0
            QueNo = int(queno) if queno is not None else 0
            data = []
            if tableno is not None:
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =tableno)
                if paid.exists():
                    for order in paid:
                        document_no = order.document_no
                        GuestCount = order.guest_count
                        waiter_id = order.waiter_id
                        
                        if SO_NO == '':
                            SO_NO = order.SO_no
                        else:
                            SO_NO = SO_NO + ',' + order.SO_no

                        matched_records = PosSalesTransDetails.objects.filter(sales_trans_id=document_no,terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) )
                        if matched_records.exists():
                            data.extend(matched_records.values())
                            if matched_records.filter(is_SC='YES').exists():
                                is_SC = True
                            else:
                                is_SC = False




            else:
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,q_no = queno)
                if paid.exists():
                     for order in paid:
                        document_no = order.document_no
                        GuestCount = order.guest_count
                        waiter_id = order.waiter_id
                        
                        if SO_NO == '':
                            SO_NO = order.SO_no
                        else:
                            SO_NO = SO_NO + ',' + order.SO_no

                        matched_records = PosSalesTransDetails.objects.filter(sales_trans_id=document_no,terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
                        if matched_records.exists():
                            data.extend(matched_records.values())
                            if matched_records.filter(is_SC='YES').exists():
                                is_SC = True
                            else:
                                is_SC = False
                        

            # Determine the width and height based on the data length
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            # Set the initial height for the first page
            card_height= 0


            # Calculate the required height based on the data length
            if is_SC == True:
                height = ((len(data)* 2) + 30 + card_height) * line_height + 2 * margin 
            else:
                height = ((len(data)* 2) + 23 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"BILLS{int(float(Cashier_ID))}.pdf", pagesize=(width, height))

            # Set up a font and size
        
            
            y_position = height - margin - line_height 

            
            c.setFont("Courier", 8)
            c.setDash(2,1)
            c.setLineWidth(0.5)
            # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("BILL")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "BILLS")
            y_position -= line_height
            y_position -= line_height
            
            if TableNo != 0:
                
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"Table No.: {TableNo}")

                # Right align "Guest Count"
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            if QueNo != 0:
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"QueNo.: {QueNo}")
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            y_position -= line_height
            c.setFont("Courier", 8.5)
            text_width = c.stringWidth(f'{Order_Type}')
            x_center = (width - text_width) / 2
            y_position -= line_height
        
            c.drawString(x_center, y_position, f'{Order_Type}')
            y_position -= line_height
            c.line(x_start, y_position, x_end, y_position)
            text_width = c.stringWidth(f'SO#{SO_NO}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'SO#{SO_NO}')
            y_position -= line_height

            # Get the current date and time
            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
            x_center = (width - text_width) / 2
            # Draw the date and time
            c.drawString(x_center, y_position, f'{date_time}')

            # Update y_position for the next content
            y_position -= (line_height - 0.2 * cm)

        # 3 points on, 2 points off
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
        
            for item in data:
                
                desc_rate = json.dumps(item['desc_rate'], ensure_ascii=False)
                desc_rate = desc_rate.replace('"', '')  # 
                if float(desc_rate) !=0:
                    Item_Dicount = True
                is_SC = json.dumps(item['is_SC'], ensure_ascii=False)
                is_SC = is_SC.replace('"', '') 

                if str(is_SC) == 'YES':
                    SC_Dicount = True
                pc_price = json.dumps(item['price'], ensure_ascii=False)
                description = json.dumps(item['description'], ensure_ascii=False)
                quantity = json.dumps(int(float(item['quantity'])), ensure_ascii=False)
                description = description.replace('"', '')  # Remove double quotes
                pc_price = pc_price.replace('"', '')  # 
                quantity = quantity.replace('"', '')  #
                sub_total = float(pc_price) * float(quantity)  # 


                total_qty = total_qty + float(item['quantity'])
                Total_due = Total_due + float(sub_total)
                
                c.setFillColor(colors.black)
                quantity_str = str(quantity).ljust(3)  
                text_to_draw = f"{description}"
                qty_and_price = f"{quantity_str}    @{pc_price}"

                wrapped_description = textwrap.wrap(text_to_draw, width=32)

                if wrapped_description:
                    text_to_draw = f"{wrapped_description[0]}"
                    c.drawString(10 * mm, y_position, text_to_draw)
                for line in wrapped_description[1:]:
                    y_position -= line_height
                    text_to_draw = f"{line}"
                    c.drawString(10 * mm, y_position, text_to_draw)
                sub_total_char_width = c.stringWidth(f'{sub_total}')  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, f'{float(sub_total):,.2f}')
                y_position -= line_height
                c.drawString(10 * mm, y_position,f'{qty_and_price}')
                y_position -= line_height
                #*********** Senior Discount *************
                if Item_Dicount == True and SC_Dicount == False:
                    if float(item['item_disc']) !=0:
                        discount_amount = json.dumps(item['item_disc'], ensure_ascii=False)
                        discount_rate= json.dumps(item['desc_rate'], ensure_ascii=False)
                        discount_amount = discount_amount.replace('"', '')  # 
                        discount_rate = discount_rate.replace('"', '')  # 
                        c.setFont("Courier", 6)
                        c.drawString(10 * mm, y_position,'Less:        ' + str(int(float(discount_rate)))+'%')
                        c.drawRightString(width - margin_right, y_position, f'-{float(discount_amount):,.2f}')
                        Total_due -= float(discount_amount)
                        y_position -= line_height


            
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Items:' + str(int(float(total_qty))))
            total_due_char_width = c.stringWidth(f'{Total_due}')  # Use appropriate font and size
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
            y_position -= line_height
            
            if SC_Dicount == True:
                Less_Vat = 0
                Net_of_vat = 0
                Less_Discount = 0
                Amount_covered = 0
                    # Get all SC amounts for this transaction
                SC_Covered = TmpPosWebScDiscountList.objects.filter(so_no=int(float(SO_NO)),)
                SCGuestCount = 0
                if SC_Covered:
                    for amount in SC_Covered:
                        Amount_covered =  float(str(amount.SAmountCovered).replace(',',''))
                        SCGuestCount = amount.SeniorCount
                        GuestCount = amount.SGuestCount
                result = compute_total_due(
                    Total_due=Total_due,
                    Amount_covered=Amount_covered,
                    SCGuestCount=SCGuestCount,
                    GuestCount=GuestCount
                    )

                x = Total_due / GuestCount

                if GuestCount != SCGuestCount:
                    vatable_val = float(x) * float(GuestCount - SCGuestCount)
                        
                    vatable_val = (vatable_val / 1.12) / SCGuestCount
                else:
                    vatable_val = 0
                        
                    vatable_val = 0


                    # Extract numeric values
                Less_Vat_val = result["Less_Vat"]
                Net_of_vat_val = result["Net_of_vat"]
                Less_Discount_val = result["Less_Discount"]
                vat_exempt_val = result["total_vat_exempt"]
                vat_val = result["total_vat"]        # this is the VAT amount (12%)
                SC_Total_due_val = result["total_due"]
                total_sc_discount_val = result["total_sc_discount"]
                    # Create formatted strings for printing
                Less_Vat = Less_Vat_val
                Net_of_vat = Net_of_vat_val
                Less_Discount = Less_Discount_val
                vat_exempt = vat_exempt_val
                vatable = vatable_val
                vat = vat_val
                SC_Total_due = SC_Total_due_val
                total_sc_discount = total_sc_discount_val
                    
                
                    # Print values
                y_position -= line_height
                c.drawString(10 * mm, y_position, f'Less 20% VAT: {Amount_covered}')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Net of VAT:')
                c.drawRightString(width - margin_right, y_position, f'{result["Net_of_vat"]:,.2f}')

                y_position -= line_height
                c.drawString(10 * mm, y_position, 'Less 20% Discount:')
                c.drawRightString(width - margin_right, y_position, f'{result["Less_Discount"]:,.2f}')
                Total_due_net = float(result["total_due"])
                Total_due = Total_due_net

                y_position -= line_height_dash
                c.line(x_start, y_position, x_end, y_position)
                # L************** END double dash line ****************

                y_position -= line_height
                c.drawString(10 * mm, y_position,'TOTAL DUE:')
                c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')
                y_position -= line_height


            

            # ************** VAT DATA ****************
        
            if Item_Dicount == True:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat
            else:
                vat =(float(str(Total_due).replace(',','')) / 1.12) * .12
                vatable = float(str(Total_due).replace(',','')) - vat

            # L**************END VAT ****************

            # L************** NEW double dash line ****************
   
          

 
            y_position -= line_height

            c.drawString(10 * mm, y_position,'Cashier:')
            c.drawString(10 * mm, y_position,'' )
            cashierData = User.objects.filter(id_code = int(float(Cashier_ID))).first()
            if cashierData:
                c.drawRightString(width - margin_right, y_position, f'{cashierData.fullname}')
            y_position -= line_height

            c.drawString(10 * mm, y_position,'Waiter:')
            c.drawString(10 * mm, y_position,'' )
            cashierData = PosWaiterList.objects.filter(waiter_id = int(float(waiter_id))).first()
            if cashierData:
                c.drawRightString(width - margin_right, y_position, f'{cashierData.waiter_name}')
            y_position -= line_height

            c.drawRightString(width - margin_right, y_position,f'TERMINAL #' + f'{machineInfo.terminal_no}')
            y_position -= line_height

            c.save()
            file_path = f"BILLS{int(float(Cashier_ID))}.pdf"  # ✅ Correct f-string
            if not os.path.isfile(file_path):
                print('File not found')
                return Response({'error': 'File not found.'}, status=404)

            # Open the file in binary read mode
            f = open(file_path, 'rb')
            response = FileResponse(f, as_attachment=True, filename=f"BILLS{int(float(Cashier_ID))}.pdf")

            # ✅ Attach a callback to delete the file after the response is closed
            def cleanup_file(response):
                try:
                    f.close()
                    os.remove(file_path)
                    print(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file: {e}")
                return response

            response.close = lambda *args, **kwargs: cleanup_file(response)

            return response
        except Exception as e:
            print(e)
            traceback.print_exc()

##************* PRINT OR/SI RECEIPT ***************
@api_view(['GET'])
def download_pdf(request):
    try:
        OR_no = request.GET.get('or', '')
        file_path = f"Receipt{int(float(OR_no))}.pdf"  # ✅ Correct f-string

        if not os.path.isfile(file_path):
            print('File not found')
            return Response({'error': 'File not found.'}, status=404)

        # Open the file in binary read mode
        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"Receipt{OR_no}.pdf")

        # ✅ Attach a callback to delete the file after the response is closed
        def cleanup_file(response):
            try:
                f.close()
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print(f"Error: {e}")
        return Response({'error': str(e)}, status=500)

##************* REPRINT OR/SI RECEIPT ***************

@api_view(['GET'])
def download_Reprint_pdf(request):
    try:
        OR_no = request.GET.get('or', '')
        file_path = f"ReprintReceipt{int(float(OR_no))}.pdf"  # ✅ Correct f-string

        if not os.path.isfile(file_path):
            print('File not found')
            return Response({'error': 'File not found.'}, status=404)

        # Open the file in binary read mode
        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"Receipt{OR_no}.pdf")

        # ✅ Attach a callback to delete the file after the response is closed
        def cleanup_file(response):
            try:
                f.close()
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print(f"Error: {e}")
        return Response({'error': str(e)}, status=500)

##*************CREATE CHARGE RECEIPT ***************
def PDFChargeReceipt(request,doc_no,doc_type,cusData):
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


            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            

            # GET DATA IN SALES INVOICE LIST
            data_list = PosSalesInvoiceList.objects.filter(doc_no=doc_no,doc_type=doc_type).first()
            if data_list:
                if data_list.discount_type == 'IM':
                    Item_Dicount = True
                elif data_list.discount_type == 'SC':
                    SC_Dicount = True


            # GET DATA IN SALES INVOICE LISTING
            data_listing = PosSalesInvoiceListing.objects.filter(doc_no=doc_no,doc_type=doc_type,isvoid ='NO')
            if data_listing:
                data = PosSalesInvoiceListingSerializer(data_listing,many=True).data

            # GET DATA IN TABLE POS SALES TRANS
            pos_sales_trans = PosSalesTrans.objects.filter(sales_trans_id=int(float(doc_no)),document_type='CI').first()
            if pos_sales_trans:
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

            # Calculate the required height based on the data length
            height = ((len(data)* 2) + 60 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"ChargeReceipt{int(float(doc_no))}.pdf", pagesize=(width, height))

            # Set up a font and size
        
            
            y_position = height - margin - line_height 


            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height
    

            # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("CHARGE INVOICE")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "CHARGE INVOICE")
            y_position -= line_height
            y_position -= line_height

            c.drawString(10 * mm, y_position, "Cusomer: " f'{Customer}')
            if TableNo != 0:
                
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"Table No.: {TableNo}")

                # Right align "Guest Count"
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            if QueNo != 0:
                Order_Type = 'TAKE OUT'
                y_position -= line_height
                c.drawString(10 * mm, y_position, f"QueNo.: {QueNo}")
                guest_count_text = f"Guest Count: {GuestCount}"
                text_width = c.stringWidth(guest_count_text)  # Use appropriate font and size
                c.drawRightString(width - margin_right, y_position, guest_count_text)

            y_position -= line_height

            text_width = c.stringWidth(f'{Order_Type}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'{Order_Type}')
            y_position -= line_height

            c.setDash(3, 2) 
            c.line(x_start, y_position, x_end, y_position)
            text_width = c.stringWidth(f'CI#{int(float(doc_no))}')
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, f'CI#{int(float(doc_no))}')
            y_position -= line_height

            # Get the current date and time
            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
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
                sub_total_char_width = c.stringWidth(f'{sub_total}')  # Use appropriate font and size
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
            total_due_char_width = c.stringWidth(f'{Total_due}')  # Use appropriate font and size
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

            y_position -= line_height
            c.drawString(10 * mm, y_position,'CHARGE:')
            c.drawRightString(width - margin_right, y_position, f'{float(Total_due):,.2f}')


            y_position -= line_height
            c.drawString(10 * mm, y_position,'ROOM CHARGE DETAILS:')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Guest name:')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Room/Folio:')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Stay Duration:')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Expected Check Out:')
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Status:')




            
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
                y_position -= line_height
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
            y_position -= line_height
            y_position -= line_height_dash
            c.line(x_start + 10 * mm , y_position, x_end - 10 * mm, y_position)
            y_position -= line_height
            text_width = c.stringWidth("Approved By")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "Approved By")

           
            y_position -= line_height
            y_position -= line_height
            y_position -= line_height
            y_position -= line_height_dash
            c.line(x_start + 10 * mm , y_position, x_end - 10 * mm, y_position)
            text_width = c.stringWidth("Customer Acknowledgement")
            x_center = (width - text_width) / 2
            y_position -= line_height
            c.drawString(x_center, y_position, "Customer Acknowledgement")
            y_position -= line_height
            text_width = c.stringWidth("(Signature over printed name)")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "(Signature over printed name)")
            y_position -= line_height



       
            y_position -= line_height
            c.drawString(10 * mm, y_position,'Customer Name:')
            c.drawRightString(width - margin_right, y_position, f'{Customer}')

            name_width = c.stringWidth('Customer Name:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{Customer}')
            value_width = c.stringWidth(f'{Customer}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Address:')
            c.drawRightString(width - margin_right, y_position, f'{CusAddress}')

            name_width = c.stringWidth('Address:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position,  f'{CusAddress}')
            value_width = c.stringWidth( f'{CusAddress}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'TIN:')
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')

            name_width = c.stringWidth('TIN:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusTIN}')
            value_width = c.stringWidth(f'{CusTIN}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)


            y_position -= line_height
            c.drawString(10 * mm, y_position,'Business Style:')
            c.drawRightString(width - margin_right, y_position, f'{CusBusiness}')

            name_width = c.stringWidth('Business Style:')
            end_of_name_x = 10 * mm + name_width + 5  # Adding some space between name and line
            c.drawRightString(width - margin_right, y_position, f'{CusBusiness}')
            value_width = c.stringWidth(f'{CusBusiness}')
            end_of_value_x = width - margin_right  # End at the right margin
            c.line(end_of_name_x, y_position - 2, end_of_value_x, y_position - 2)
            y_position -= line_height
            y_position -= line_height
            
            c.setDash(3,2)
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth("THIS SERVES AS AN OFFICIAL RECEIPT")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THIS SERVES AS AN OFFICIAL RECEIPT")
            y_position -= line_height
            y_position -= line_height
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth("THANK YOU, COME AGAIN... ")
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "THANK YOU, COME AGAIN... ")
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            y_position -= line_height
            lead = getLeadSetup()

            if lead:
                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_name2}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_name2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.company_address2}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.company_address2}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.tin}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.tin}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.accreditation_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.accreditation_no}')


                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_issued}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_issued}')

                y_position -= line_height
                text_width = c.stringWidth(f'{lead.date_valid}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{lead.date_valid}')


                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.PTU_no}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.PTU_no}')

                y_position -= line_height
                text_width = c.stringWidth(f'{machineInfo.date_issue}')
                x_center = (width - text_width) / 2
                c.drawString(x_center, y_position, f'{machineInfo.date_issue}')
            # Save the PDF
            print('already save pdf Charge Invoice')
            c.save()   
        except Exception as e:
            print(e)
            traceback.print_exc()




#*******************    CASHIERS CASH BREAKDOWN PDF *********************
def PDFCashBreakDown(request,login_record):
    try:
            margin_left = 2 * mm
            margin_right = 10 * mm
            margin_top = 2 * mm
            margin_bottom = 2 * mm
            x_start = 10 * mm  # Starting x-coordinate
            x_end =  85 * mm  - x_start # Ending x-coordinate (55 characters long)
            GTotal = 0
            terminaNo = 0
            Cashier_ID = request.user.id_code
            Cashier_name = request.user.fullname

            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            
            companyCode = getCompanyData()
            clientSetup = getClientSetup()

            # Determine the width and height based on the data length
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            # Set the initial height for the first page
            card_height= 0
            data = [
                {"denomination": "Php 1,000.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 500.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 200.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 100.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 50.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 20.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 10.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 5.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 1.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 0.25", "qty": 0, "total": '0.00'},
                {"denomination": "Php 0.05", "qty": 0, "total": '0.00'},
            ]




            # Calculate the required height based on the data length
            height = ((len(data)* 2) + 20 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"CashCount{int(float(Cashier_ID))}.pdf", pagesize=(width, height))

            # Set up a font and size
            
            y_position = height - margin - line_height 
            c.setFont("Courier", 8)
            c.setDash(2,1)
            c.setLineWidth(0.5)
            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height
    


            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
            # Draw the date and time
            c.drawString(x_start, y_position, f'{date_time}')
            y_position -= line_height

            text_width = c.stringWidth(f'Terminal No.:{machineInfo.terminal_no}')
            c.drawString(x_start, y_position, f'Terminal No.:{machineInfo.terminal_no}')
            y_position -= line_height
            y_position -= line_height

                   # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("CASH COUNT")
            
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "CASH COUNT")
            y_position -= line_height
            y_position -= line_height
            

            text_width = c.stringWidth(f'CASHIER NAME:{Cashier_name}')
            c.drawString(x_start, y_position, f'CASHIER NAME:{Cashier_name}')
            y_position -= line_height
       
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height

            text_width = c.stringWidth(f'Qty')
            c.drawString(x_start, y_position, f'Qty')

            text_width = c.stringWidth(f'Denomination')
            x_center = (width - text_width) / 2
            x_center_deno = x_center
            c.drawString(x_center, y_position, f'Denomination')

            text_width = c.stringWidth(f'Total')
            c.drawRightString(width - margin_right, y_position, f'Total')
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            for item in data:
                y_position -= line_height
                result = PosCashBreakdown.objects.filter(login_record=login_record,denomination = item["denomination"]).first()
                if result:
                    print('results',result)
            
                    text_width = c.stringWidth(f'{result.quantity}')
                    c.drawString(x_start, y_position, f'{result.quantity}')

                    text_width = c.stringWidth(f'{result.denomination}')
                    c.drawString(x_center_deno, y_position, f'{result.denomination}')
                    formatted = f"{result.total:,.2f}"
                    text_width = c.stringWidth(formatted)
                    c.drawRightString(width - margin_right, y_position, formatted)
                    GTotal += float(result.total)
                else:
                    text_width = c.stringWidth(f'{item["qty"]}')
                    c.drawString(x_start, y_position, f'{item["qty"]}')

                    text_width = c.stringWidth(f'{item["denomination"]}')
                    c.drawString(x_center_deno, y_position, f'{item["denomination"]}')

                    text_width = c.stringWidth(f'{item["total"]}')
                    c.drawRightString(width - margin_right, y_position, f'{item["total"]}')
            
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Grand Total:')
            c.drawString(x_start, y_position, f'Grand Total:')
            formatted = f"{GTotal:,.2f}" 
            text_width = c.stringWidth(formatted)
            c.drawRightString(width - margin_right, y_position, formatted)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            y_position -= line_height




            y_position -= line_height
            text_width = c.stringWidth(f'{Cashier_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{Cashier_name}')
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Terminal Cashier')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'Terminal Cashier')
            y_position -= line_height
            y_position -= line_height

            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Teasury Personnel')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'Teasury Personnel')
            print('already save pdf CashCOunt')
            c.save() 
            
    except Exception as e:
        print('error',e)
        traceback.print_exc()

@api_view(['GET'])
def download_pdf_cash_count(request):
    try:
        id = request.user.id_code
        file_path = f"CashCount{int(id)}.pdf"  # ✅ Correct f-string

        if not os.path.isfile(file_path):
            print('File not found')
            return Response({'error': 'File not found.'}, status=404)

        # Open the file in binary read mode
        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"CashCount{id}.pdf")

        # ✅ Attach a callback to delete the file after the response is closed
        def cleanup_file(response):
            try:
                f.close()
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print(f"Error: {e}")
        return Response({'error': str(e)}, status=500)



#*******************    CASH BREAKDOWN APPROVED PDF *********************
def PDFCashBreakDownApproved(request,login_record,cashier_name):
    try:
            margin_left = 2 * mm
            margin_right = 10 * mm
            margin_top = 2 * mm
            margin_bottom = 2 * mm
            x_start = 10 * mm  # Starting x-coordinate
            x_end =  85 * mm - x_start  # Ending x-coordinate (55 characters long)
            GTotal = 0
            terminaNo = 0
            Cashier_ID = request.user.id_code
            Personnel = request.user.fullname
            Cashier_name = cashier_name

            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            
            companyCode = getCompanyData()
            clientSetup = getClientSetup()

            # Determine the width and height based on the data length
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            # Set the initial height for the first page
            card_height= 0
            data = [
                {"denomination": "Php 1,000.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 500.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 200.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 100.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 50.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 20.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 10.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 5.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 1.00", "qty": 0, "total": '0.00'},
                {"denomination": "Php 0.25", "qty": 0, "total": '0.00'},
                {"denomination": "Php 0.05", "qty": 0, "total": '0.00'},
            ]




            # Calculate the required height based on the data length
            height = ((len(data)* 2) + 20 + card_height) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

            # Create a canvas with calculated size
            c = canvas.Canvas(f"CashBreakDown{int(float(Cashier_ID))}.pdf", pagesize=(width, height))

            # Set up a font and size
            
            y_position = height - margin - line_height 
            c.setFont("Courier", 8)
            c.setDash(2,1)
            c.setLineWidth(0.5)
            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height
    


            date_time = GetPHilippineDateTime()
            text_width = c.stringWidth(date_time)
            # Draw the date and time
            c.drawString(x_start, y_position, f'{date_time}')
            y_position -= line_height

            text_width = c.stringWidth(f'Terminal No.:{machineInfo.terminal_no}')
            c.drawString(x_start, y_position, f'Terminal No.:{machineInfo.terminal_no}')
            y_position -= line_height
            y_position -= line_height

                   # Calculate x-coordinate for center alignment of "SALES INVOICE"
            text_width = c.stringWidth("CASH COUNT")
            
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, "CASH COUNT")
            y_position -= line_height
            y_position -= line_height
            

            text_width = c.stringWidth(f'CASHIER NAME:{Cashier_name}')
            c.drawString(x_start, y_position, f'CASHIER NAME:{Cashier_name}')
            y_position -= line_height
       
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height

            text_width = c.stringWidth(f'Qty')
            c.drawString(x_start, y_position, f'Qty')

            text_width = c.stringWidth(f'Denomination')
            x_center = (width - text_width) / 2
            x_center_deno = x_center
            c.drawString(x_center, y_position, f'Denomination')

            text_width = c.stringWidth(f'Total')
            c.drawRightString(width - margin_right, y_position, f'Total')
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            for item in data:
                y_position -= line_height
                result = PosCashBreakdown.objects.filter(login_record=login_record,denomination = item["denomination"]).first()
                if result:
 
            
                    text_width = c.stringWidth(f'{result.quantity}')
                    c.drawString(x_start, y_position, f'{result.quantity}')

                    text_width = c.stringWidth(f'{result.denomination}')
                    c.drawString(x_center_deno, y_position, f'{result.denomination}')
                    formatted = f"{result.total:,.2f}"
                    text_width = c.stringWidth(formatted)
                    c.drawRightString(width - margin_right, y_position, formatted)
                    GTotal += float(result.total)
                else:
                    text_width = c.stringWidth(f'{item["qty"]}')
                    c.drawString(x_start, y_position, f'{item["qty"]}')

                    text_width = c.stringWidth(f'{item["denomination"]}')
                    c.drawString(x_center_deno, y_position, f'{item["denomination"]}')

                    text_width = c.stringWidth(f'{item["total"]}')
                    c.drawRightString(width - margin_right, y_position, f'{item["total"]}')
            
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Grand Total:')
            c.drawString(x_start, y_position, f'Grand Total:')
            formatted = f"{GTotal:,.2f}" 
            text_width = c.stringWidth(formatted)
            c.drawRightString(width - margin_right, y_position, formatted)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            y_position -= line_height




            text_width = c.stringWidth(f'{Cashier_name}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{Cashier_name}')
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Terminal Cashier')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'Terminal Cashier')
            y_position -= line_height
            y_position -= line_height


            text_width = c.stringWidth(f'{Personnel}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{Personnel}')
            y_position -= line_height_dash
            c.line(x_start, y_position, x_end, y_position)
            y_position -= line_height
            text_width = c.stringWidth(f'Teasury Personnel')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'Teasury Personnel')
            print('already save pdf CashCOunt')
            c.save() 
            
    except Exception as e:
        print('error',e)
        traceback.print_exc()

@api_view(['GET'])
def download_pdf_cash_breakdown_approved(request):
    try:
        id = request.user.id_code
        file_path = f"CashBreakDown{int(id)}.pdf"  # ✅ Correct f-string

        if not os.path.isfile(file_path):
            print('File not found')
            return Response({'error': 'File not found.'}, status=404)

        # Open the file in binary read mode
        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"CashBreakDown{id}.pdf")

        # ✅ Attach a callback to delete the file after the response is closed
        def cleanup_file(response):
            try:
                f.close()
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print(f"Error: {e}")
        return Response({'error': str(e)}, status=500)






# @api_view(['GET'])
# @permission_classes([AllowAny])
# def download_sales_order_pdf(request):
#     if request.method == 'GET':
#         try:
#             CashierID = request.GET.get('CashierID','')
#             # Get the absolute path of the file
#             # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backendD', 'Receipt.pdf'))
#             file_path =f'SalesOrderaLL{CashierID}.pdf'
#             # Check if the file exists
#             print('file_path',file_path)
#             if not os.path.isfile(file_path):
#                 print('xxxxxx')
#                 return Response({'error': 'File not found.'}, status=404)

#             # Open the file and return it as a response
#             f = open(file_path, 'rb')
#             response = FileResponse(f, as_attachment=True, filename='SalesOrderaLL.pdf')
#             return response
#             # return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Receipt.pdf')
        
#         except Exception as e:
#             print(e)
#             traceback.print_exc()
#             return Response({'error': 'An error occurred while processing the request.'}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def download_sales_order_pdf(request):
    try:
        CashierID = request.GET.get('CashierID', '')
        if CashierID =='':
            CashierID = request.user.id_code
        file_path = f"SalesOrderaLL{CashierID}.pdf"

        if not os.path.isfile(file_path):
            print('File not found')
            return Response({'error': 'File not found.'}, status=404)

        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename='SalesOrderaLL.pdf')

        # ✅ Attach cleanup logic
        def cleanup_file(response):
            try:
                f.close()  # close file first
                os.remove(file_path)  # delete file
                print(f"✅ Deleted file: {file_path}")
            except Exception as e:
                print(f"⚠️ Error deleting file: {e}")
            return response

        # Override close method to call cleanup after sending
        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print("❌ Exception:", e)
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def download_charge_receipt_pdf(request):
    if request.method == 'GET':
        try:
            # Get the absolute path of the file
            # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backendD', 'Receipt.pdf'))
            file_path ='ChargeReceipt.pdf'
            # Check if the file exists
            print('file_path',file_path)
            if not os.path.isfile(file_path):
                print('xxxxxx')
                return Response({'error': 'File not found.'}, status=404)

            # Open the file and return it as a response
            f = open(file_path, 'rb')
            response = FileResponse(f, as_attachment=True, filename='ChargeReceipt.pdf')
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

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_api(request):
    try:
        if request.method == 'POST':

            username = request.data.get('username')
            password = request.data.get('password')
            serial_number = request.data.get('SERIALNO')
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            ul = ProductSiteSetup.objects.filter(site_code = int(machineInfo.site_no)).first()
            ul_code = 0
            ul_desc = ''
            if ul:
                
                ul_info = UnitLocation.objects.filter(ul_code=ul.ul_code,active ='Y').first()
                if ul_info:
                    ul_code = ul_info.ul_code
                    ul_desc = ul_info.location_description

                
            hashed_password = make_password(password)


            password1 = 'Lsi#1288'
            current_date = date.today()

            day_of_month = str(current_date.day).zfill(2)
            yesterday = current_date - timedelta(days=1)

            # Format as YYYY-MM-DD
            last_day_stamp = yesterday.strftime("%Y-%m-%d")

            password_with_date = password1 + day_of_month 


            # serial_number = get_serial_number()
            # pdb.set_trace()
        
            # CHECK IF MOBILE DEVICE
            user_agent = get_user_agent(request)
            is_mobile = user_agent.is_mobile
            
            if username.lower() == 'admin' and password == password_with_date:
            # if (username.lower()=='admin') & (password==password_with_date):
                # print('yy',serial_number)
                if is_mobile == False:
                            infolist ={
                                'UserRank': 'Admin',
                                'FullName':'Super Admin',
                                'UserID':'9999',
                                'UserName':'Admin',
                                'TerminalNo':0,
                                'SiteCode': 0,
                                'PTU': 0 ,
                                'location':f'{ul_code}  ' - '  {ul_desc}'
                                

                            }
                            # is_delete = User.objects.get(id_code='9999',sys_type ='POS')
                            # if is_delete:
                            #     is_delete.delete()
                            with connection.cursor() as cursor:
                                sql = "DELETE FROM tbl_user WHERE id_code = %s AND sys_type = %s"
                                cursor.execute(sql, ['9999', 'POS'])
                            user, created = User.objects.get_or_create(
                            user_name=username,
                            defaults={
                                'password':make_password(password_with_date),
                                'fullname': 'Super Admin',
                                'user_rank': 'Super Admin',
                                'id_code': '9999',
                                'sys_type': 'POS',
                                'active': 'Y' })
                            

                            user = authenticate(request, username=username, password=password_with_date)
                            if user is None:
                                return Response({"error": "Invalid username or password"}, status=401)

                            try:
                                # Create JWT refresh token
                                try:
                                    refresh = RefreshToken.for_user(user)
                                except Exception as e:
                                    print(e)
                                # refresh = RefreshToken.for_user(user)
                                refresh['id_code'] = user.autonum  # or any custom claim
                                # Add custom claims
                                refresh['SERIALNO'] = serial_number
                              
                            except Exception as e:
                                return Response({"error": "Failed to create token", "detail": str(e)}, status=500)

                            # Create response with user info
                            try:
                                response = Response({"Info": infolist})
                                # Set HttpOnly cookies
                                response.set_cookie(
                                    key="access_token",
                                    value=str(refresh.access_token),
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                    path="/"
                                )

                                response.set_cookie(
                                    key="refresh_token",
                                    value=str(refresh),
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                 path="/"
                                )
                                return response
                            except Exception as e:
                                print(e)
                else:
                    return JsonResponse({'message':'Error'},status=404)
                    
            user = authenticate(request, username=username, password=password)

            
            
            
            if user is not None:
                stored_hashed_password = user.password
                # stored_hashed_password = make_password(password_with_date)
                if check_password(password, stored_hashed_password):
                    # pdb.set_trace()
                    
                    latest_trans_id = PosCashiersLogin.objects.aggregate(max_trans_id=Max('trans_id'))['max_trans_id']
                    new_trans_id = 0
                    if user.user_rank =='Cashier' and is_mobile == True:
                        return JsonResponse({'message': 'Invalid credentials'}, status=401)
                    if is_mobile == False:
                        if user.user_rank =='Cashier':
                            current_date_ph = GetPHilippineDate()
                            current_datetime_ph = GetPHilippineDateTime()   

                            check_if_cashier_login_last_day = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='YES',
                                                                                            isshift_end = 'YES',isxread='NO')  
                            if check_if_cashier_login_last_day.exists(): 
                                return JsonResponse({'message':'Zread is Required'},status=200)                                    
                            
                            check_if_cashier_login = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='YES',
                                                                                    isshift_end = 'NO',isxread='NO')
                                               #  date_stamp = current_date_ph)
                            if check_if_cashier_login.exists():
                                cashier_login = check_if_cashier_login.first()  # or cashier_login = check_if_cashier_login.get()
                                if int(cashier_login.terminal_no) == int(machineInfo.terminal_no):
                                    cashier_login.islogout = 'NO'
                                    new_trans_id = cashier_login.trans_id
                                    cashier_login.save()
                                    
                                else:
                                    return JsonResponse({'message':'Cashier Already login in Terminal No. ' + cashier_login.terminal_no},status=200)
                            else:
                                check_if_cashier_login_unexpected = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='NO',
                                                                                    isshift_end = 'NO',isxread='NO')
                                if check_if_cashier_login_unexpected.exists():
                                    cashier_login = check_if_cashier_login_unexpected.first()  # or cashier_login = check_if_cashier_login.get()
                                    if int(cashier_login.terminal_no) == int(machineInfo.terminal_no):
                                        cashier_login.islogout = 'NO'
                                        new_trans_id = cashier_login.trans_id
                                        cashier_login.save() 
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
                                        user_rank = 'Cashier',
                                        date_stamp=current_date_ph,
                                        # change_fund=0.0,
                                        # borrowed_fund=0.0,
                                        time_login=current_datetime_ph,
                                        time_logout='',
                                        islogout='NO',
                                        isshift_end='NO',
                                        isxread='NO',
                                    )
                                    cashier_data.save()
                                    client= getClientSetup()
                                     

                                    try:
                                        current_datetime_phx = datetime.strptime(current_datetime_ph, '%m/%d/%Y %H:%M:%S %p')
                                            # Format: convert to "2025-11-12 14:35:49"
                                        datetime_stampx = current_datetime_phx.strftime('%Y-%m-%d %H:%M:%S')
                                        TblPosDailyRecords.objects.create(
                                            id=new_trans_id,  # Must be unique; required
                                            prepared_by=user.id_code,
                                            datetime_stamp=datetime_stampx,
                                            site_code=int(machineInfo.site_no),
                                            ul_code=machineInfo.ul_code,
                                            company_code=client.company_code,
                                            terminal_no=int(machineInfo.terminal_no),
                                            machine_no=machineInfo.Machine_no,
                                            tin_no=client.tin,
                                            sn_no=machineInfo.Serial_no,
                                            min_no=machineInfo.Model_no,
                                            register_no=machineInfo.PTU_no,
                                            iszread="NO",
                                        )
                                    except Exception as e:
                                        print(e)
                            infolist ={
                                'UserRank': user.user_rank,
                                'FullName':user.fullname,
                                'UserID':user.id_code,
                                'UserName':user.user_name,
                                'TerminalNo': machineInfo.terminal_no,
                                'SiteCode': machineInfo.site_no,
                                'PTU': machineInfo.PTU_no,
                                'TransID':new_trans_id,
                                'location':f'{ul_code}  -   {ul_desc}'
                            }
                            
                            if user is None:
                                return Response({"error": "Invalid username or password"}, status=401)

                            try:
                                # Create JWT refresh token
                                try:
                                    refresh = RefreshToken.for_user(user)
                                except Exception as e:
                                    print(e)
                                refresh['id_code'] = user.autonum  # or any custom claim
                                refresh['SERIALNO'] = serial_number
                                refresh['trans_id'] = new_trans_id

                              
                            except Exception as e:
                                return Response({"error": "Failed to create token", "detail": str(e)}, status=500)

                            # Create response with user info
                            try:
                                access_token = str(refresh.access_token)
                                response = Response({"Info": infolist})
                                # Set HttpOnly cookies
                                print('refresh',access_token)
                                response.set_cookie(
                                    key="access_token",
                                    value=access_token,
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),    # adjust based on your frontend
                                    path="/"
                                )

                                response.set_cookie(
                                    key="refresh_token",
                                    value=str(refresh),
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                    path="/"
                                )
                                return response
                            except Exception as e:
                                print(e)
                        
                            # return JsonResponse({'Info':infolist}, status=200)
                        else:
                            if user.user_rank =='Salesman':
                                current_date_ph = GetPHilippineDate()
                                current_datetime_ph = GetPHilippineDateTime()   
                                check_if_cashier_login = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='NO')
                                                                                        #  date_stamp = current_date_ph)
                                if check_if_cashier_login.exists():
                                    cashier_login = check_if_cashier_login.first()  # or cashier_login = check_if_cashier_login.get()
                                    return JsonResponse({'message':'Salesman already login in different device. '},status=200)
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
                                        user_rank = 'Salesman',
                                        date_stamp=current_date_ph,
                                        change_fund=0.0,
                                        borrowed_fund=0.0,
                                        time_login=current_datetime_ph,
                                        time_logout='',
                                        islogout='NO',
                                        isshift_end='NO',
                                        isxread='NO',
                                    )
                                    cashier_data.save()
                                infolist ={
                                    'UserRank': user.user_rank,
                                    'FullName':user.fullname,
                                    'UserID':user.id_code,
                                    'UserName':user.user_name,
                                    'TerminalNo': machineInfo.terminal_no,
                                    'SiteCode': machineInfo.site_no,
                                    'PTU': machineInfo.PTU_no,
                                    'TransID':new_trans_id,
                                    'location':f'{ul_code}  -   {ul_desc}'
                                }
                                # user = authenticate(request, username=username, password=password_with_date)
                                if user is None:
                                    return Response({"error": "Invalid username or password"}, status=401)

                                try:
                                    # Create JWT refresh token
                                    try:
                                        refresh = RefreshToken.for_user(user)
                                    except Exception as e:
                                        print(e)
                                    # refresh = RefreshToken.for_user(user)
                                    refresh['id_code'] = user.autonum  # or any custom claim
                                    # Add custom claims
                                    refresh['SERIALNO'] = serial_number
                                
                                except Exception as e:
                                    return Response({"error": "Failed to create token", "detail": str(e)}, status=500)

                                # Create response with user info
                                try:
                                    response = Response({"Info": infolist})
                                    # Set HttpOnly cookies
                                    response.set_cookie(
                                        key="access_token",
                                        value=str(refresh.access_token),
                                        httponly=True,
                                        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                        secure=getattr(settings, "JWT_COOKIE_SECURE", False),    # adjust based on your frontend
                                        path="/"
                                    )

                                    response.set_cookie(
                                        key="refresh_token",
                                        value=str(refresh),
                                        httponly=True,
                                        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                        secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                        path="/"
                                    )
                                    print(response)
                                    return response
                                except Exception as e:
                                    print(e)
                                # return JsonResponse({'Info':infolist}, status=200)
                            else:
                                infolist ={
                                    'UserRank': user.user_rank,
                                    'FullName':user.fullname,
                                    'UserID':user.id_code,
                                    'UserName':user.user_name,
                                    'TerminalNo': machineInfo.terminal_no,
                                    'SiteCode': machineInfo.site_no,
                                    'PTU': machineInfo.PTU_no,
                                    'TransID':new_trans_id,
                                    'location':f'{ul_code}  -   {ul_desc}'
                                }
                                # user = authenticate(request, username=username, password=password_with_date)
                                if user is None:
                                    return Response({"error": "Invalid username or password"}, status=401)

                                try:
                                    # Create JWT refresh token
                                    try:
                                        refresh = RefreshToken.for_user(user)
                                    except Exception as e:
                                        print(e)
                                    # refresh = RefreshToken.for_user(user)
                                    refresh['id_code'] = user.autonum  # or any custom claim
                                    # Add custom claims
                                    refresh['SERIALNO'] = serial_number
                                
                                except Exception as e:
                                    return Response({"error": "Failed to create token", "detail": str(e)}, status=500)

                                # Create response with user info
                                try:
                                    response = Response({"Info": infolist})
                                    # Set HttpOnly cookies
                                    response.set_cookie(
                                        key="access_token",
                                        value=str(refresh.access_token),
                                        httponly=True,
                                        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                        secure=getattr(settings, "JWT_COOKIE_SECURE", False),    # adjust based on your frontend
                                        path="/"
                                    )

                                    response.set_cookie(
                                        key="refresh_token",
                                        value=str(refresh),
                                        httponly=True,
                                        samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                        secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                        path="/"
                                    )
                                    return response
                                except Exception as e:
                                    print(e)
                                    traceback.print_exc()

                    else:
                        current_date_ph = GetPHilippineDate()
                        current_datetime_ph = GetPHilippineDateTime()   
                        check_if_cashier_login = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='NO',
                                                                                    date_stamp = current_date_ph)
                        if check_if_cashier_login.exists():
                                cashier_login = check_if_cashier_login.first()  # or cashier_login = check_if_cashier_login.get()
                                return JsonResponse({'message':'Salesman Already login in Terminal No. ' + cashier_login.terminal_no},status=200)
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
                                    user_rank = 'Salesman',
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
                                'TransID':new_trans_id,
                                'location':f'{ul_code}  -   {ul_desc}'
                            }
                       

                        # user = authenticate(request, username=username, password=password_with_date)
                        if user is None:
                            return Response({"error": "Invalid username or password"}, status=401)

                        try:
                                # Create JWT refresh token
                            try:
                                refresh = RefreshToken.for_user(user)
                            except Exception as e:
                                print(e)
                                # refresh = RefreshToken.for_user(user)
                            refresh['id_code'] = user.autonum  # or any custom claim
                                # Add custom claims
                            refresh['SERIALNO'] = serial_number
                            refresh['id_code'] = 9999
                              
                        except Exception as e:
                            return Response({"error": "Failed to create token", "detail": str(e)}, status=500)

                            # Create response with user info
                        try:
                            response = Response({"Info": infolist})
                                # Set HttpOnly cookies
                            response.set_cookie(
                                key="access_token",
                                    value=str(refresh.access_token),
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),    # adjust based on your frontend
                                    path="/"
                                )

                            response.set_cookie(
                                    key="refresh_token",
                                    value=str(refresh),
                                    httponly=True,
                                    samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
                                    secure=getattr(settings, "JWT_COOKIE_SECURE", False),
                                    path="/"
                                )
                            print(response)
                            return response
                        except Exception as e:
                            print(e)
                        return JsonResponse({'Info':infolist}, status=200)

                else:
                    return JsonResponse({'message': 'Invalid credentials'}, status=401)  
            else:
                # Login failed
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Exception as e:
        print(e)
        traceback.print_exc()

# def testPrint():  
#     try:
#         # Initialize the Printer object with the specific printer name
#         print('qqqqqqqqqqqqqqqqqqqq')
        
#         # Specify the name of the printer
#         printer_name = 'EPSON TM-U220 Receipt'
        
#         # Text to be printed
#         text_to_print = (
#         "Hello, world!\nThis is a test print.\nPrinting on multiple lines.\n"
#         )
        
    
#         print(printer_name)
        
#         # Open a handle to the printer
#         printer_handle = win32print.OpenPrinter(printer_name)
        
#         # Start a document
#         job_id = win32print.StartDocPrinter(printer_handle, 1, ("Test Job", None, "RAW"))
#         win32print.StartPagePrinter(printer_handle)
        
#         # Print the text

#         win32print.WritePrinter(printer_handle, text_to_print.encode('utf-8'))
#         cut_command = b'\x1d\x56\x42\x00'
#         win32print.WritePrinter(printer_handle, cut_command)       
#         # End the document and close the printer handle
#         win32print.EndPagePrinter(printer_handle)
#         win32print.EndDocPrinter(printer_handle)
#         win32print.ClosePrinter(printer_handle)
#     except Exception as e:
#         print(e)
        


@api_view(['GET'])
def CheckTerminalLogIn(request):
    if request.method == 'GET':
        print('Check Login')
        pdb.set_trace()
    
        try:
            serial_number = getattr(request, "SERIALNO", None)
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
            


@api_view(["POST"])
def user_logout_api(request):
    if request.method =='POST':
        try:
            UserID = request.data.get("UserID")
            TransID = request.data.get("TransID")
            # UserID = request.Get.get("UserID")
            # TransID = request.Get.get("TransID")
            print('UserID',UserID,TransID)
            # password = request.GET.get("password")

            user = User.objects.filter(id_code=UserID).first()

            serial_number = getattr(request, "SERIALNO", None)
            machine = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()
            if user.user_rank == 'Cashier':
    
                # cashier_data = PosCashiersLogin.objects.get(id_code=UserID,islogout='NO')
                cashier_data = PosCashiersLogin.objects.get(id_code=UserID,trans_id=TransID)
                
                if cashier_data:

                    cashier_data.time_logout = current_datetime_ph
                    cashier_data.islogout = "YES"
                    cashier_data.save()

            else:
                cashier_data = PosCashiersLogin.objects.get(id_code=UserID,islogout='NO')
                if cashier_data:
                    cashier_data.time_logout = current_datetime_ph
                    cashier_data.islogout = "YES"
                    cashier_data.save()
            response = JsonResponse({'message': 'Logged out successfully'})
    
            response.delete_cookie("access_token", path="/")
            response.delete_cookie("refresh_token", path="/")
            response.delete_cookie("csrftoken", path="/")
            return response
            # return JsonResponse({"message": "Logout Successfully"}, status=200)

        except (User.DoesNotExist, IntegrityError):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({"message": "Method not allowed"}, status=405)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_endshift_api(request):
    if request.method =='POST':
        try:

            # pdb.set_trace()
            UserID = request.data.get("UserID")
            TransID = request.data.get("TransID")
            user = User.objects.filter(id_code=UserID).first()

            serial_number = getattr(request, "SERIALNO", None)
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
            traceback.print_exc()
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            traceback.print_exc()
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception:
            traceback.print_exc()
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
                    'id_code':user.id_code,
                    'UserRank': user.user_rank,
                    'FullName':user.fullname,   
                }
                

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

def PrintXread(request,trans_id,cashier_name):
    try:
        serial_number = getattr(request, "SERIALNO", None)
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()

        _date = PosCashiersLogin.objects.filter(trans_id=trans_id).first()
        current_date_ph = GetPHilippineDate()
        current_datetime_ph = GetPHilippineDateTime()
        filter_str = _date.date_stamp if _date and _date.date_stamp else current_date_ph

        # Start and end of day as strings
        date_from= filter_str + " 00:00:00"
        date_to  = filter_str + " 23:59:59"


        trans_id = trans_id
        xread_date = ''
        id_code = int(_date.id_code)
        cashier_name = cashier_name

        # --- Sales Summary ---
        gross_sales = 0.00
        item_discount = 0.00
        trade_discount = 0.00
        sc_pwd_discount = 0.00
        transaction_discount = 0.00
        refund_return = 0.00
        net_of_discounts = 0.00
        service_charge = 0.00
        other_income = 0.00
        net_total = 0.00

        # --- Payment Breakdown ---
        cash_payment = 0.00
        credit_card_payment = 0.00
        current_check_payment = 0.00
        postdated_check_payment = 0.00
        debit_card_payment = 0.00
        credit_sales = 0.00
        gift_check_payment = 0.00
        online_payment = 0.00
        other_payment = 0.00
        total_payment = 0.00

        # --- Returns ---
        cash_refund = 0.00
        charge_back = 0.00
        charge_refund = 0.00
        check_refund = 0.00
        credit_memo = 0.00
        exchange_amount = 0.00
        total_refund = 0.00

        # === Return Type Counts ===
        cash_refund_count = 0
        charge_back_count = 0
        charge_refund_count = 0
        check_refund_count = 0
        credit_memo_count = 0
        exchange_amount_count = 0



        # --- Cashier Accountability ---
        cash_sales = 0.00
        change_fund = 0.00
        borrowed_fund = 0.00
        cash_pull_out = 0.00
        cash_refund_account = 0.00



        gross_sales = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            cashier_id=id_code,
            status='S',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
                ).aggregate(
                    gross_sales=Sum(F('sub_total') - F('vat_exempted'))
                )['gross_sales'] or 0
        

        discounts = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            cashier_id=id_code,
            status='S',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
        ).aggregate(
            # Item Discount
            item_discount=Sum(
                Case(
                    When(discount_type='IM', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            item_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='IM', discount__gt=0)
            ),

            # Trade Discount
            trade_discount=Sum(
                Case(
                    When(discount_type='TD', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            trade_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='TD', discount__gt=0)
            ),

            # Senior/PWD Discount
            sc_pwd_discount=Sum(
                Case(
                    When(discount_type='SC', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            sc_pwd_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='SC', discount__gt=0)
            ),

            # Transaction Discount
            transaction_discount=Sum(
                Case(
                    When(discount_type='TN', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            transaction_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='TN', discount__gt=0)
            ),
        )
        item_discount = discounts['item_discount'] or 0
        item_discount_count = discounts['item_discount_count'] or 0

        trade_discount = discounts['trade_discount'] or 0
        trade_discount_count = discounts['trade_discount_count'] or 0

        sc_pwd_discount = discounts['sc_pwd_discount'] or 0
        sc_pwd_discount_count = discounts['sc_pwd_discount_count'] or 0

        transaction_discount = discounts['transaction_discount'] or 0
        transaction_discount_count = discounts['transaction_discount_count'] or 0



        totals = (
            PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                cashier_id=id_code,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            )
            .aggregate(
                service_charge_total=Sum('ServiceCharge_TotalAmount', output_field=FloatField()),
                service_charge_count=Count('autonum', filter=Q(ServiceCharge_TotalAmount__gt=0)),

                other_income_total=Sum('other_income', output_field=FloatField()),
                other_income_count=Count('autonum', filter=Q(other_income__gt=0)),

                total_cash_total=Sum('total_cash', output_field=FloatField()),
                total_cash_count=Count('autonum', filter=Q(total_cash__gt=0)),

                total_check_total=Sum('total_check', output_field=FloatField()),
                total_check_count=Count('autonum', filter=Q(total_check__gt=0)),

                total_pdc_total=Sum('total_pdc', output_field=FloatField()),
                total_pdc_count=Count('autonum', filter=Q(total_pdc__gt=0)),

                total_eps_total=Sum('total_eps', output_field=FloatField()),
                total_eps_count=Count('autonum', filter=Q(total_eps__gt=0)),

                total_credit_card_total=Sum('total_credit_card', output_field=FloatField()),
                total_credit_card_count=Count('autonum', filter=Q(total_credit_card__gt=0)),

                total_credit_sales_total=Sum('total_credit_sales', output_field=FloatField()),
                total_credit_sales_count=Count('autonum', filter=Q(total_credit_sales__gt=0)),

                online_payment_total=Sum('online_payment', output_field=FloatField()),
                online_payment_count=Count('autonum', filter=Q(online_payment__gt=0)),

                gift_check_total=Sum('gift_check', output_field=FloatField()),
                gift_check_count=Count('autonum', filter=Q(gift_check__gt=0)),

                other_payment_total=Sum('other_payment', output_field=FloatField()),
                other_payment_count=Count('autonum', filter=Q(other_payment__gt=0)),
            )
        )



        service_charge_total = totals['service_charge_total'] or 0
        service_charge_count = totals['service_charge_count'] or 0

        other_income = totals['other_income_total'] or 0
        other_income_count = totals['other_income_count'] or 0

        total_cash = totals['total_cash_total'] or 0
        total_cash_count = totals['total_cash_count'] or 0

        total_check = totals['total_check_total'] or 0
        total_check_count = totals['total_check_count'] or 0

        total_pdc = totals['total_pdc_total'] or 0
        total_pdc_count = totals['total_pdc_count'] or 0

        total_eps = totals['total_eps_total'] or 0
        total_eps_count = totals['total_eps_count'] or 0

        total_credit_card = totals['total_credit_card_total'] or 0
        total_credit_card_count = totals['total_credit_card_count'] or 0

        total_credit_sales = totals['total_credit_sales_total'] or 0
        total_credit_sales_count = totals['total_credit_sales_count'] or 0

        online_payment = totals['online_payment_total'] or 0
        online_payment_count = totals['online_payment_count'] or 0

        gift_check = totals['gift_check_total'] or 0
        gift_check_count = totals['gift_check_count'] or 0

        other_payment = totals['other_payment_total'] or 0
        other_payment_count = totals['other_payment_count'] or 0
        

        # === Optional: Grand Totals ===
        grand_total = (
            other_income + total_cash + total_check +
            total_pdc + total_eps + total_credit_card + total_credit_sales +
            online_payment + gift_check + other_payment
        )

        grand_total_count = (
             other_income_count + total_cash_count + total_check_count +
            total_pdc_count + total_eps_count + total_credit_card_count +
            total_credit_sales_count + online_payment_count + gift_check_count +
            other_payment_count
        )



        fund = PosCashiersLogin.objects.filter(
            id_code=id_code,
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
        ).aggregate(
            change_fund=Sum('change_fund', output_field=FloatField()),
            borrowed_fund=Sum('borrowed_fund', output_field=FloatField())
        )

        
        change_fund = fund['change_fund'] or 0
        borrowed_fund = fund['borrowed_fund'] or 0



        margin_left = 2 * mm
        margin_right = 10 * mm
        margin_top = 2 * mm
        margin_bottom = 2 * mm
        Total_due = 0
        Total_Payment = 0
        Amount_Tendered = 0

        x_start = 2 * mm  # Starting x-coordinate
        x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)
        clientSetup = getClientSetup()
        line_height = 0.3 * cm
        line_height_dash = 0.05 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 85 * mm  # Width adjusted for 79 mm roll paper
        height = (86) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
        y_position = height - margin - line_height 
        # Create a canvas with calculated size
        c = canvas.Canvas(f"xread{int(float(id_code))}.pdf", pagesize=(width, height))
        c.setFont("Courier", 8)
        c.setLineWidth(0.5)
        c.setDash(2,1)
        text_width = c.stringWidth(f'{clientSetup.company_name}')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'{clientSetup.company_name}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.company_address}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{clientSetup.company_address}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.company_address2}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.tin}')
        x_center = (width - text_width) / 2
        c.drawCentredString(width/2, y_position, f'{clientSetup.tin}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.tel_no}')
        x_center = (width - text_width) / 2
        c.drawCentredString(width/2, y_position, f'{clientSetup.tel_no}')
        y_position -= line_height

        text_width = c.stringWidth(f'{machineInfo.Machine_no}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
        y_position -= line_height

        text_width = c.stringWidth(f'{machineInfo.Serial_no}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
        y_position -= line_height
        y_position -= line_height


   


       

        start_line = x_start + 5 * mm
        end_line = x_end - 5 * mm
        
        dt_obj = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        date_sales = datetime.strftime(dt_obj,'%m/%d/%Y')


        c.drawString(10 * mm, y_position, f'Admin: {request.user.fullname}')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        c.drawString(10 * mm, y_position, f'Cashier: {cashier_name}')
        y_position -= line_height
        c.drawString(10 * mm, y_position, f'Date of Sales: {date_sales}')
        y_position -= line_height
        y_position -= line_height
        

        text_width = c.stringWidth(f'X-READING REPORT')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'X-READING REPORT')
        y_position -= line_height
        y_position -= line_height

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        count_width = 4  # space reserved for count numbers (adjust as needed)
# Use f-string formatting to pad count with spaces
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Gross Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(gross_sales):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{item_discount_count:<{count_width}} Item Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(item_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{trade_discount_count:<{count_width}} Trade Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(trade_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{sc_pwd_discount_count:<{count_width}} SC Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(sc_pwd_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{transaction_discount_count:<{count_width}} Transaction Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(transaction_discount):,.2f}')
        
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        net_of_discounts = float(gross_sales) - (item_discount + trade_discount + sc_pwd_discount + transaction_discount)
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET OF DISCOUNTS:')
        c.drawRightString(width - margin_right, y_position, f'{float(net_of_discounts):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{service_charge_count:<{count_width}} Service Charge:')
        c.drawRightString(width - margin_right, y_position, f'{float(service_charge_total):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{other_income_count:<{count_width}} Other Income:')
        c.drawRightString(width - margin_right, y_position, f'{float(other_income):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        net_total = float(net_of_discounts) + other_income + service_charge_total

        c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET:')
        c.drawRightString(width - margin_right, y_position, f'{float(net_total):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height
        #--------------------------------------------------------------------



        

        c.drawString(10 * mm, y_position, 'Breakdown (Tender of Payment)')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'{total_cash_count:<{count_width}} Cash:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_credit_card_count:<{count_width}} Credit Card:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_credit_card):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_check_count:<{count_width}} Check:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_check):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_pdc_count:<{count_width}} Postdated Check:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_pdc):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_eps_count:<{count_width}} Debit Card:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_eps):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_credit_sales_count:<{count_width}} Credit Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_credit_sales):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{gift_check_count:<{count_width}} Gift Checks:')
        c.drawRightString(width - margin_right, y_position, f'{float(gift_check):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{online_payment_count:<{count_width}} Online Payment:')
        c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{other_payment_count:<{count_width}} Other Payment:')
        c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
        #--------------------------------------------------------------------


        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height

        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(grand_total):,.2f}')
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height



     

        # Cash Refund

        c.drawString(10 * mm, y_position, f'Return Type')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------

        c.drawString(10 * mm, y_position, f'{cash_refund_count:<{count_width}} Cash refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
        y_position -= line_height

        # Charge Back
        c.drawString(10 * mm, y_position, f'{charge_back_count:<{count_width}} Charge back:')
        c.drawRightString(width - margin_right, y_position, f'{float(charge_back):,.2f}')
        y_position -= line_height

        # Charge Refund
        c.drawString(10 * mm, y_position, f'{charge_refund_count:<{count_width}} Charge refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(charge_refund):,.2f}')
        y_position -= line_height

        # Check Refund
        c.drawString(10 * mm, y_position, f'{check_refund_count:<{count_width}} Check refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(check_refund):,.2f}')
        y_position -= line_height

        # Credit Memo
        c.drawString(10 * mm, y_position, f'{credit_memo_count:<{count_width}} Credit memo:')
        c.drawRightString(width - margin_right, y_position, f'{float(credit_memo):,.2f}')
        y_position -= line_height

        # Exchange
        c.drawString(10 * mm, y_position, f'{exchange_amount_count:<{count_width}} Exchange:')
        c.drawRightString(width - margin_right, y_position, f'{float(exchange_amount):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------

        total_refund = cash_refund + charge_back + charge_refund + check_refund + credit_memo + exchange_amount


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_refund):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height

        #--------------------------------------------------------------------



        c.drawString(10 * mm, y_position, f'Cashier\'s Cash Accountability')
  

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
        y_position -= line_height

  
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Change Fund:')
        c.drawRightString(width - margin_right, y_position, f'{float(change_fund):,.2f}')
        y_position -= line_height

    
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Borrowed Fund:')
        c.drawRightString(width - margin_right, y_position, f'{float(borrowed_fund):,.2f}')
        y_position -= line_height


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Pull Out:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_pull_out):,.2f}')
        y_position -= line_height

     
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
        y_position -= line_height

        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height

        cashier_accountability = (total_cash + change_fund + borrowed_fund ) - (cash_pull_out + cash_refund)
        c.drawString(10 * mm, y_position, f'TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(cashier_accountability):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        #--------------------------------------------------------------------
        y_position -= line_height


        c.drawString(10 * mm, y_position, f'Cash Breakdown')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash     
        #--------------------------------------------------------------------   
        Denomination_list = [
            {"denomination": "Php 1,000.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 500.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 200.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 100.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 50.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 20.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 10.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 5.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 1.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 0.25", "qty": 0, "total": '0.00'},
            {"denomination": "Php 0.05", "qty": 0, "total": '0.00'},
            ]

        
 
        GTotal = 0
        for item in Denomination_list:
            y_position -= line_height
            result = PosCashBreakdown.objects.filter(login_record=trans_id,denomination = item["denomination"]).first()
            if result:
            
                text_width = c.stringWidth(f'{result.quantity}')
                c.drawString(10 * mm, y_position, f'{result.quantity}')

                text_width = c.stringWidth(f'{result.denomination}')
                c.drawString(x_center_deno, y_position, f'{result.denomination}')
                formatted = f"{result.total:,.2f}"
                text_width = c.stringWidth(formatted)
                c.drawRightString(width - margin_right, y_position, formatted)
                GTotal += float(result.total)
            else:
                text_width = c.stringWidth(f'{item["qty"]}')
                c.drawString(10 * mm, y_position, f'{item["qty"]}')

                text_width = c.stringWidth(f'{item["denomination"]}')
                c.drawString(x_center_deno, y_position, f'{item["denomination"]}')

                text_width = c.stringWidth(f'{item["total"]}')
                c.drawRightString(width - margin_right, y_position, f'{item["total"]}')

        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'TOTAL')
        c.drawRightString(width - margin_right, y_position, f'{float(GTotal):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        y_position -= line_height
        #--------------------------------------------------------------------

        c.drawString(10 * mm, y_position, f'Cashier\'s Short/Over')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line,y_position)
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'Cash Accountability')
        c.drawRightString(width - margin_right, y_position, f'{float(cashier_accountability):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'Cash breakdowns')
        c.drawRightString(width - margin_right, y_position, f'{float(GTotal):,.2f}')
        y_position -= line_height


        short_over = cashier_accountability - GTotal
        if short_over < 0:
            c.drawString(10 * mm, y_position, 'Over')
            value_to_display = abs(short_over)  # remove negative sign
        else:
            c.drawString(10 * mm, y_position, 'Short')
            value_to_display = short_over  # already positive

            # Draw the value right-aligned (example)
        c.drawRightString(width - margin_right, y_position, f'{value_to_display:,.2f}')
    

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height
        y_position -= line_height



        c.setDash()
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        text_width = c.stringWidth(f'Terminal Cashier')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'Terminal Cashier')
        y_position -= line_height
        y_position -= line_height
        y_position -= line_height

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        text_width = c.stringWidth(f'Treasury Personnel')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'Treasury Personnel')
        y_position -= line_height
        print('Xread pdf Successfully Save')
        c.save()

    except Exception as e:
        print(e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def download_xread_pdf(request):
    try:
        id_code = request.GET.get('id_code', '0')

        file_path = f"xread{id_code}.pdf"

        if not os.path.isfile(file_path):
            return Response({'error': 'File not found.'}, status=404)

        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"xread{id_code}.pdf")

        # ✅ Attach cleanup logic
        def cleanup_file(response):
            try:
                f.close()  # close file first
                os.remove(file_path)  # delete file
                print(f"✅ Deleted file: {file_path}")
            except Exception as e:
                print(f"⚠️ Error deleting file: {e}")
            return response

        # Override close method to call cleanup after sending
        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print("❌ Exception:", e)
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def PrintZread(request):
    if request.method == 'GET':
        print('zread')
        try:
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()
            filter_str = request.GET.get('DateFrom',None)

            latest_zread = PosZReading.objects.aggregate(max_zread=Max('zread_no'),old_grand_total=Max('new_grand_total'))
            zread_no = (latest_zread['max_zread'] or 0) + 1
            old_grand_total = (latest_zread['old_grand_total'] or 0)
            new_grand_total = 0



            # Start and end of day as strings
            # date_from= filter_str + " 00:00:00"
            # date_to  = filter_str + " 23:59:59"

            date_from = datetime.strptime(filter_str + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            date_to   = datetime.strptime(filter_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            
            xread_date = current_date_ph

            # --- Sales Summary ---
            gross_sales = 0.00
            item_discount = 0.00
            trade_discount = 0.00
            sc_pwd_discount = 0.00
            transaction_discount = 0.00
            refund_return = 0.00
            net_of_discounts = 0.00
            service_charge = 0.00
            other_income = 0.00
            net_total = 0.00

            # --- Payment Breakdown ---
            cash_payment = 0.00
            credit_card_payment = 0.00
            current_check_payment = 0.00
            postdated_check_payment = 0.00
            debit_card_payment = 0.00
            credit_sales = 0.00
            gift_check_payment = 0.00
            online_payment = 0.00
            other_payment = 0.00
            total_payment = 0.00

            # --- Returns ---
            cash_refund = 0.00
            charge_back = 0.00
            charge_refund = 0.00
            check_refund = 0.00
            credit_memo = 0.00
            exchange_amount = 0.00
            total_refund = 0.00

            # === Return Type Counts ===
            cash_refund_count = 0
            charge_back_count = 0
            charge_refund_count = 0
            check_refund_count = 0
            credit_memo_count = 0
            exchange_amount_count = 0



            # --- Cashier Accountability ---
            cash_sales = 0.00
            change_fund = 0.00
            borrowed_fund = 0.00
            cash_pull_out = 0.00
            cash_refund_account = 0.00

            gross_sales = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
                    ).aggregate(
                        gross_sales=Sum(F('sub_total') - F('vat_exempted'))
                    )['gross_sales'] or 0
        
            discounts = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                site_code=int(machineInfo.site_no)
            ).aggregate(
                # Item Discount
                item_discount=Sum(
                    Case(
                        When(discount_type='IM', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                item_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='IM', discount__gt=0)
                ),

                # Trade Discount
                trade_discount=Sum(
                    Case(
                        When(discount_type='TD', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                trade_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='TD', discount__gt=0)
                ),

                # Senior/PWD Discount
                sc_pwd_discount=Sum(
                    Case(
                        When(discount_type='SC', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                sc_pwd_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='SC', discount__gt=0)
                ),

                # Transaction Discount
                transaction_discount=Sum(
                    Case(
                        When(discount_type='TN', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                transaction_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='TN', discount__gt=0)
                ),
            )
            item_discount = discounts['item_discount'] or 0
            item_discount_count = discounts['item_discount_count'] or 0

            trade_discount = discounts['trade_discount'] or 0
            trade_discount_count = discounts['trade_discount_count'] or 0

            sc_pwd_discount = discounts['sc_pwd_discount'] or 0
            sc_pwd_discount_count = discounts['sc_pwd_discount_count'] or 0

            transaction_discount = discounts['transaction_discount'] or 0
            transaction_discount_count = discounts['transaction_discount_count'] or 0



            totals = (
                PosSalesInvoiceList.objects.filter(
                    doc_date__gte=date_from,
                    doc_date__lt=date_to,
                    status='S',
                    terminal_no=int(machineInfo.terminal_no),
                    site_code=int(machineInfo.site_no)
                )
                .aggregate(
                    service_charge_total=Sum('ServiceCharge_TotalAmount', output_field=FloatField()),
                    service_charge_count=Count('autonum', filter=Q(ServiceCharge_TotalAmount__gt=0)),

                    other_income_total=Sum('other_income', output_field=FloatField()),
                    other_income_count=Count('autonum', filter=Q(other_income__gt=0)),

                    total_cash_total=Sum('total_cash', output_field=FloatField()),
                    total_cash_count=Count('autonum', filter=Q(total_cash__gt=0)),

                    total_check_total=Sum('total_check', output_field=FloatField()),
                    total_check_count=Count('autonum', filter=Q(total_check__gt=0)),

                    total_pdc_total=Sum('total_pdc', output_field=FloatField()),
                    total_pdc_count=Count('autonum', filter=Q(total_pdc__gt=0)),

                    total_eps_total=Sum('total_eps', output_field=FloatField()),
                    total_eps_count=Count('autonum', filter=Q(total_eps__gt=0)),

                    total_credit_card_total=Sum('total_credit_card', output_field=FloatField()),
                    total_credit_card_count=Count('autonum', filter=Q(total_credit_card__gt=0)),

                    total_credit_sales_total=Sum('total_credit_sales', output_field=FloatField()),
                    total_credit_sales_count=Count('autonum', filter=Q(total_credit_sales__gt=0)),

                    online_payment_total=Sum('online_payment', output_field=FloatField()),
                    online_payment_count=Count('autonum', filter=Q(online_payment__gt=0)),

                    gift_check_total=Sum('gift_check', output_field=FloatField()),
                    gift_check_count=Count('autonum', filter=Q(gift_check__gt=0)),

                    other_payment_total=Sum('other_payment', output_field=FloatField()),
                    other_payment_count=Count('autonum', filter=Q(other_payment__gt=0)),
                )
            )



            service_charge_total = totals['service_charge_total'] or 0
            service_charge_count = totals['service_charge_count'] or 0

            other_income = totals['other_income_total'] or 0
            other_income_count = totals['other_income_count'] or 0

            total_cash = totals['total_cash_total'] or 0
            total_cash_count = totals['total_cash_count'] or 0

            total_check = totals['total_check_total'] or 0
            total_check_count = totals['total_check_count'] or 0

            total_pdc = totals['total_pdc_total'] or 0
            total_pdc_count = totals['total_pdc_count'] or 0

            total_eps = totals['total_eps_total'] or 0
            total_eps_count = totals['total_eps_count'] or 0

            total_credit_card = totals['total_credit_card_total'] or 0
            total_credit_card_count = totals['total_credit_card_count'] or 0

            total_credit_sales = totals['total_credit_sales_total'] or 0
            total_credit_sales_count = totals['total_credit_sales_count'] or 0

            online_payment = totals['online_payment_total'] or 0
            online_payment_count = totals['online_payment_count'] or 0

            gift_check = totals['gift_check_total'] or 0
            gift_check_count = totals['gift_check_count'] or 0

            other_payment = totals['other_payment_total'] or 0
            other_payment_count = totals['other_payment_count'] or 0
            

            # === Optional: Grand Totals ===
            grand_total = (
                other_income + total_cash + total_check +
                total_pdc + total_eps + total_credit_card + total_credit_sales +
                online_payment + gift_check + other_payment
            )

            grand_total_count = (
                other_income_count + total_cash_count + total_check_count +
                total_pdc_count + total_eps_count + total_credit_card_count +
                total_credit_sales_count + online_payment_count + gift_check_count +
                other_payment_count
            )




            margin_left = 2 * mm
            margin_right = 10 * mm
            margin_top = 2 * mm
            margin_bottom = 2 * mm
            Total_due = 0
            Total_Payment = 0
            Amount_Tendered = 0
      

            x_start = 2 * mm  # Starting x-coordinate
            x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)
            clientSetup = getClientSetup()
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            height = (90) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
            y_position = height - margin - line_height 
            # Create a canvas with calculated size
            c = canvas.Canvas(f"zread{int(float(zread_no))}.pdf", pagesize=(width, height))
            c.setFont("Courier", 8)
            c.setLineWidth(0.5)
            c.setDash(2,1)
            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            x_center_deno = x_center
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawCentredString(width/2, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawCentredString(width/2, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height




        

            start_line = x_start + 5 * mm
            end_line = x_end - 5 * mm


            current_date_ph_str = current_date_ph
            date_from_str = datetime.strftime(date_from,"%m/%d/%Y")



            # Parse using 24-hour format
            
            c.drawString(10 * mm, y_position, f'Admin: {request.user.fullname}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Date of Z-Reading: {current_datetime_ph}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Date of Sales: {date_from_str}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Terminal No: {int(machineInfo.terminal_no)}')
            y_position -= line_height
            y_position -= line_height

            
            text_width = c.stringWidth(f'Z-READING SUMMARY # {zread_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'Z-READING SUMMARY # {zread_no}')
            y_position -= line_height
            y_position -= line_height
            
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            count_width = 4  # space reserved for count numbers (adjust as needed)
    # Use f-string formatting to pad count with spaces
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Gross Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(gross_sales):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{item_discount_count:<{count_width}} Item Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(item_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{trade_discount_count:<{count_width}} Trade Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(trade_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{sc_pwd_discount_count:<{count_width}} SC Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(sc_pwd_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{transaction_discount_count:<{count_width}} Transaction Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(transaction_discount):,.2f}')
            
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            net_of_discounts = float(gross_sales) - (item_discount + trade_discount + sc_pwd_discount + transaction_discount)
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET OF DISCOUNTS')
            c.drawRightString(width - margin_right, y_position, f'{float(net_of_discounts):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{service_charge_count:<{count_width}} Service Charge')
            c.drawRightString(width - margin_right, y_position, f'{float(service_charge_total):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{other_income_count:<{count_width}} Other Income')
            c.drawRightString(width - margin_right, y_position, f'{float(other_income):,.2f}')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            net_total = float(net_of_discounts) + other_income + service_charge_total

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET')
            c.drawRightString(width - margin_right, y_position, f'{float(net_total):,.2f}')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height
            #--------------------------------------------------------------------



            

            c.drawString(10 * mm, y_position, 'Breakdown (Tender of Payment)')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'{total_cash_count:<{count_width}} Cash')
            c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_credit_card_count:<{count_width}} Credit Card')
            c.drawRightString(width - margin_right, y_position, f'{float(total_credit_card):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_check_count:<{count_width}} Check')
            c.drawRightString(width - margin_right, y_position, f'{float(total_check):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_pdc_count:<{count_width}} Postdated Check')
            c.drawRightString(width - margin_right, y_position, f'{float(total_pdc):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_eps_count:<{count_width}} Debit Card')
            c.drawRightString(width - margin_right, y_position, f'{float(total_eps):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_credit_sales_count:<{count_width}} Credit Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(total_credit_sales):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{gift_check_count:<{count_width}} Gift Checks')
            c.drawRightString(width - margin_right, y_position, f'{float(gift_check):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{online_payment_count:<{count_width}} Online Payment')
            c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{other_payment_count:<{count_width}} Other Payment')
            c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
            #--------------------------------------------------------------------


            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height

            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL')
            c.drawRightString(width - margin_right, y_position, f'{float(grand_total):,.2f}')
            #--------------------------------------------------------------------
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height



        

            # Cash Refund

            c.drawString(10 * mm, y_position, f'Return Type')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------

            c.drawString(10 * mm, y_position, f'{cash_refund_count:<{count_width}} Cash refund')
            c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
            y_position -= line_height

            # Charge Back
            c.drawString(10 * mm, y_position, f'{charge_back_count:<{count_width}} Charge back')
            c.drawRightString(width - margin_right, y_position, f'{float(charge_back):,.2f}')
            y_position -= line_height

            # Charge Refund
            c.drawString(10 * mm, y_position, f'{charge_refund_count:<{count_width}} Charge refund')
            c.drawRightString(width - margin_right, y_position, f'{float(charge_refund):,.2f}')
            y_position -= line_height

            # Check Refund
            c.drawString(10 * mm, y_position, f'{check_refund_count:<{count_width}} Check refund')
            c.drawRightString(width - margin_right, y_position, f'{float(check_refund):,.2f}')
            y_position -= line_height

            # Credit Memo
            c.drawString(10 * mm, y_position, f'{credit_memo_count:<{count_width}} Credit memo')
            c.drawRightString(width - margin_right, y_position, f'{float(credit_memo):,.2f}')
            y_position -= line_height

            # Exchange
            c.drawString(10 * mm, y_position, f'{exchange_amount_count:<{count_width}} Exchange')
            c.drawRightString(width - margin_right, y_position, f'{float(exchange_amount):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------

            total_refund = cash_refund + charge_back + charge_refund + check_refund + credit_memo + exchange_amount


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL')
            c.drawRightString(width - margin_right, y_position, f'{float(total_refund):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height

            #--------------------------------------------------------------------


            vat_amount = 0
            vat_amount_count = 0
            non_vat_amount = 0
            non_vat_amount_count = 0
            vatable_amount = 0
            vatable_amount_count = 0
            zero_rated_amount = 0
            zero_rated_amount_count = 0
            vat_exempt_amount = 0
            vat_exempt_amount_count = 0
            total_sales= 0



            vat_amount_return = 0
            vat_amount_return_count = 0
            non_vat_return_amount = 0
            non_vat_return_count = 0
            vatable_return_amount = 0
            vatable_return_count = 0
            zero_rated_return_amount = 0
            zero_rated_return_count = 0
            vat_exempt_return_amount = 0
            vat_exempt_return_count = 0
            total_return= 0

            #******************* SALES ******************
            vat_ = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vat_count=Count('zread_no', filter=Q(vat__gt=0))
            )

            vat_amount = vat_['vat_amount'] or 0
            vat_amount_count = vat_['vat_count'] or 0

            non_vat_ = PosSalesInvoiceListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                vatable='Nv',
                isvoid='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                non_vat_amount=Sum(F('disc_amt'), output_field=FloatField(), default=0),
                non_vat_amount_count=Count('zread_no', filter=Q(disc_amt__gt=0))
            )

            non_vat_amount = non_vat_['non_vat_amount'] or 0
            non_vat_amount_count = non_vat_['non_vat_amount_count'] or 0


            vatable_ = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vatable_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vatable_amount_count=Count('zread_no', filter=Q(vat__gt=0))
            )
            vat_amt = vatable_.get('vatable_amount')
            if vat_amt:
                vatable_amount = float(vat_amt) / 0.12
            else:
                vatable_amount = 0
            # vatable_amount = float(vatable_['vatable_amount']) / 0.12  or 0
            vatable_amount_count = vatable_['vatable_amount_count'] or 0


            vat_exempt = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_exempt_amount=Sum(F('vat_exempt'), output_field=FloatField(), default=0),
                vat_exempt_amount_count=Count('zread_no', filter=Q(vat__gt=0))
                
            )

            vat_exempt_amount = vat_exempt['vat_exempt_amount'] or 0
            vat_exempt_amount_count = vat_exempt['vat_exempt_amount_count'] or 0

            total_sales = vat_amount + non_vat_amount + vatable_amount + zero_rated_amount + vat_exempt_amount

            #******************* RETURNS ******************
            vat_return = PosSalesReturnList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vat_count=Count('zread_no', filter=Q(vat__gt=0))
            )

            vat_amount_return = vat_return['vat_amount'] or 0
            vat_amount_return_count = vat_return['vat_count'] or 0

            non_vat_return = PosSalesReturnListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                vatable='Nv',
                isvoid='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                non_vat_amount=Sum(F('disc_amt'), output_field=FloatField(), default=0),
                non_vat_amount_count=Count('zread_no', filter=Q(disc_amt__gt=0))
            )

            non_vat_return_amount = non_vat_return['non_vat_amount'] or 0
            non_vat_return_count = non_vat_return['non_vat_amount_count'] or 0


            vatable_return = PosSalesReturnList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vatable_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vatable_amount_count=Count('zread_no', filter=Q(vat__gt=0))
            )
            vatable_amount_r = vatable_return.get('vatable_amount')
            if vatable_amount_r:
                vatable_return_amount = float(vatable_amount_r) / 0.12
            else:
                vatable_return_amount = 0
            # vatable_return_amount = float(vatable_return['vatable_amount']) / 0.12  or 0
            vatable_return_count = vatable_return['vatable_amount_count'] or 0


            vat_exempt_return = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_exempt_amount=Sum(F('vat_exempt'), output_field=FloatField(), default=0),
                vat_exempt_amount_count=Count('zread_no', filter=Q(vat__gt=0))
                
            )

            vat_exempt_return_amount = vat_exempt_return['vat_exempt_amount'] or 0
            vat_exempt_return_count = vat_exempt_return['vat_exempt_amount_count'] or 0

            total_return = vat_amount_return + non_vat_return_amount + vatable_return_amount + zero_rated_return_amount + vat_exempt_return_amount



            c.drawString(10 * mm, y_position, f'Breakdown (VAT)')

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'SALES')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Amount')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_amount):,.2f}')
            y_position -= line_height

    
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NON-VAT Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(non_vat_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VATable Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(vatable_amount):,.2f}')
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Zero Rated Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(zero_rated_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Exempt Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_exempt_amount):,.2f}')
            y_position -= line_height

            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'TOTAL - SALES')
            c.drawRightString(width - margin_right, y_position, f'{float(total_sales):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'RETURNS')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Amount Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_amount_return):,.2f}')
            y_position -= line_height

    
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NON-VAT Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(non_vat_return_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VATable Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vatable_return_amount):,.2f}')
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Zero Rated Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(zero_rated_return_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Exempt Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_exempt_return_amount):,.2f}')
            y_position -= line_height

            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'TOTAL - RETURNS')
            c.drawRightString(width - margin_right, y_position, f'{float(total_return):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            net_vat = total_sales - total_return
            c.drawString(10 * mm, y_position, f'Net VAT')
            c.drawRightString(width - margin_right, y_position, f'{float(net_vat):,.2f}')
            y_position -= line_height
            y_position -= line_height



            # Filter transactions

            sales_transactions = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                doc_type='POS-SI',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).order_by('doc_no')
        
            # Check if any transactions exist
            if sales_transactions.exists():
                sales_first_transaction = sales_transactions.first()
                sales_last_transaction = sales_transactions.last()
                sales_count = sales_transactions.count()

                sales_first_no = sales_first_transaction.doc_no
                sales_last_no = sales_last_transaction.doc_no
            else:
                sales_first_no = None
                sales_last_no = None
                sales_count = 0




            credit_transactions = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            status='S',
            doc_type = 'POS-CI',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
            ).order_by('doc_no')

            credit_first_transaction = credit_transactions.first()
            credit_last_transaction = credit_transactions.last()
            credit_count = credit_transactions.count()

            credit_first_no = credit_first_transaction.doc_no if credit_first_transaction else None
            credit_last_no = credit_last_transaction.doc_no if credit_last_transaction else None



            transactions = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            status='S',
            site_code=int(machineInfo.site_no),
            terminal_no=int(machineInfo.terminal_no)
            ).order_by('doc_no').values_list('doc_no', flat=True)

            coun_trans = transactions.count()

            first_no = transactions.first() if transactions.exists() else None
            last_no = transactions.last() if transactions.exists() else None


            sales_first_no_int = int(sales_first_no) if sales_first_no is not None else 0
            sales_last_no_int  = int(sales_last_no)  if sales_last_no is not None else 0
            sales_count_int = int(sales_count)  if sales_count is not None else 0

            credit_first_no_int = int(credit_first_no) if credit_first_no is not None else 0
            credit_last_no_int  = int(credit_last_no)  if credit_last_no is not None else 0
            credit_count_int = int(credit_count)  if credit_count is not None else 0

            first_no_int = int(first_no) if first_no is not None else 0
            last_no_int  = int(last_no)  if last_no is not None else 0
            coun_trans_int = int(coun_trans)  if coun_trans is not None else 0






            c.drawString(10 * mm, y_position, f'Credit Invoice Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'From Credit Invoice')
            c.drawRightString(width - margin_right, y_position, f'{credit_first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'To Credit Invoice')
            c.drawRightString(width - margin_right, y_position, f'{credit_last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Total Credit Invoice Issued')
            c.drawRightString(width - margin_right, y_position, f'{credit_count_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'Sales Invoice Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'From Sales Invoice')
            c.drawRightString(width - margin_right, y_position, f'{sales_first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'To Sales Invoice')
            c.drawRightString(width - margin_right, y_position, f'{sales_last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Total Sales Invoice Issued')
            c.drawRightString(width - margin_right, y_position, f'{sales_count_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'Transaction Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'First Transaction')
            c.drawRightString(width - margin_right, y_position, f'{first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Last Transaction')
            c.drawRightString(width - margin_right, y_position, f'{last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Transaction Count')
            c.drawRightString(width - margin_right, y_position, f'{coun_trans_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Old Grand Total')
            c.drawRightString(width - margin_right, y_position, f'{float(old_grand_total):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'New Grand Total')
            new_grand_total = net_vat + float(old_grand_total)
            c.drawRightString(width - margin_right, y_position, f'{float(new_grand_total):,.2f}')


            if current_datetime_ph.endswith(" AM") or current_datetime_ph.endswith(" PM"):
                current_datetime_ph = current_datetime_ph[:-3]

            # Parse using 24-hour format
            dt_obj = datetime.strptime(current_datetime_ph, "%m/%d/%Y %H:%M:%S")

            # Format it to "YYYY-MM-DD HH:MM:SS"
            
            new_zreading = PosZReading.objects.create(
            company_code='',
            ul_code=machineInfo.ul_code,
            site_code=int(machineInfo.site_no),
            terminal_no=machineInfo.terminal_no,
            machine_no=machineInfo.Machine_no,
            date_trans=date.today(),
            zread_no=zread_no,
            doc_type='Z READ',
            total_daily_sales=net_vat,
            total_sales_return=total_return,
            total_cash=total_cash,
            total_check=total_check,
            total_pdc=total_pdc,
            total_eps=total_eps,
            total_credit_card=total_credit_card,
            total_credit_sales=total_credit_sales,
            total_online_payment=online_payment,
            total_gift_check=gift_check,
            other_payment=other_payment,
            new_grand_total=new_grand_total,
            old_grand_total=old_grand_total,
            sales_with_VAT=net_vat,
            sales_VAT_Exempt=vat_exempt_amount,
            sales_Zero_Rated=zero_rated_amount,
            sales_NON_VAT=non_vat_amount,
            or_from=sales_first_no_int,
            or_to=sales_last_no_int,
            or_total=sales_count_int,
            ci_from=credit_first_no_int,
            ci_to=credit_last_no_int,
            ci_total=credit_count_int,
            from_si_no=sales_first_no_int,
            to_si_no=sales_last_no_int,
            from_sr_no=0,
            to_sr_no=0,
            total_invoices=sales_count_int + credit_count_int,
            zread_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S"),
            )

            new_zreading.save()
            dt_from = date_from.strftime("%Y-%m-%d")
            dt_to= date_to.strftime("%Y-%m-%d")
            data = PosCashiersLogin.objects.filter(date_stamp__range=[dt_from, dt_to], isshift_end='YES',islogout='YES',isxread='YES')
            if data:
                for item in data:
                    trans_id = item.trans_id
                    TblPosDailyRecords.objects.filter(id=trans_id).update(
                        iszread='YES'
                    )

            PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)).update(
                status='A',
                zread_no =zread_no

                )

            PosSalesInvoiceListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                isvoid ='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)).update(
                status='A',
                zread_no =zread_no
                )
            
            PosSalesReturnList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)).update(
                status='A',
                zread_no =zread_no
                )
            PosSalesReturnListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                isvoid ='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)).update(
                status='A',
                zread_no =zread_no
                )

            
        
            print('Zread pdf Successfully Save')
            c.save()
            return JsonResponse({'zread_no':zread_no})
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def download_zread_pdf(request):
    try:
        zread_no = request.GET.get('zread_no', '0')

        file_path = f"zread{zread_no}.pdf"

        if not os.path.isfile(file_path):
            return Response({'error': 'File not found.'}, status=404)

        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=f"zread{zread_no}.pdf")

        # ✅ Attach cleanup logic
        def cleanup_file(response):
            try:
                f.close()  # close file first
                os.remove(file_path)  # delete file
                print(f"✅ Deleted file: {file_path}")
            except Exception as e:
                print(f"⚠️ Error deleting file: {e}")
            return response

        # Override close method to call cleanup after sending
        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response

    except Exception as e:
        print("❌ Exception:", e)
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def RePrint_Xread(request):
    try:
        trans_id = request.GET.get('trans_id')
        cashier_name = request.GET.get('cashier_name')
        serial_number = getattr(request, "SERIALNO", None)
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()

        _date = PosCashiersLogin.objects.filter(trans_id=trans_id).first()
        current_date_ph = GetPHilippineDate()
        current_datetime_ph = GetPHilippineDateTime()
        filter_str = _date.date_stamp if _date and _date.date_stamp else current_date_ph

        # Start and end of day as strings
        date_from= filter_str + " 00:00:00"
        date_to  = filter_str + " 23:59:59"


        
        xread_date = ''
        id_code = int(_date.id_code)
       

        # --- Sales Summary ---
        gross_sales = 0.00
        item_discount = 0.00
        trade_discount = 0.00
        sc_pwd_discount = 0.00
        transaction_discount = 0.00
        refund_return = 0.00
        net_of_discounts = 0.00
        service_charge = 0.00
        other_income = 0.00
        net_total = 0.00

        # --- Payment Breakdown ---
        cash_payment = 0.00
        credit_card_payment = 0.00
        current_check_payment = 0.00
        postdated_check_payment = 0.00
        debit_card_payment = 0.00
        credit_sales = 0.00
        gift_check_payment = 0.00
        online_payment = 0.00
        other_payment = 0.00
        total_payment = 0.00

        # --- Returns ---
        cash_refund = 0.00
        charge_back = 0.00
        charge_refund = 0.00
        check_refund = 0.00
        credit_memo = 0.00
        exchange_amount = 0.00
        total_refund = 0.00

        # === Return Type Counts ===
        cash_refund_count = 0
        charge_back_count = 0
        charge_refund_count = 0
        check_refund_count = 0
        credit_memo_count = 0
        exchange_amount_count = 0



        # --- Cashier Accountability ---
        cash_sales = 0.00
        change_fund = 0.00
        borrowed_fund = 0.00
        cash_pull_out = 0.00
        cash_refund_account = 0.00



        gross_sales = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            cashier_id=id_code,
            status='A',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
                ).aggregate(
                    gross_sales=Sum(F('sub_total') - F('vat_exempted'))
                )['gross_sales'] or 0
        

        discounts = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            cashier_id=id_code,
            status='A',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
        ).aggregate(
            # Item Discount
            item_discount=Sum(
                Case(
                    When(discount_type='IM', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            item_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='IM', discount__gt=0)
            ),

            # Trade Discount
            trade_discount=Sum(
                Case(
                    When(discount_type='TD', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            trade_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='TD', discount__gt=0)
            ),

            # Senior/PWD Discount
            sc_pwd_discount=Sum(
                Case(
                    When(discount_type='SC', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            sc_pwd_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='SC', discount__gt=0)
            ),

            # Transaction Discount
            transaction_discount=Sum(
                Case(
                    When(discount_type='TN', then=F('discount')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            transaction_discount_count=Count(
                'cashier_id',
                filter=Q(discount_type='TN', discount__gt=0)
            ),
        )
        item_discount = discounts['item_discount'] or 0
        item_discount_count = discounts['item_discount_count'] or 0

        trade_discount = discounts['trade_discount'] or 0
        trade_discount_count = discounts['trade_discount_count'] or 0

        sc_pwd_discount = discounts['sc_pwd_discount'] or 0
        sc_pwd_discount_count = discounts['sc_pwd_discount_count'] or 0

        transaction_discount = discounts['transaction_discount'] or 0
        transaction_discount_count = discounts['transaction_discount_count'] or 0



        totals = (
            PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                cashier_id=id_code,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            )
            .aggregate(
                service_charge_total=Sum('ServiceCharge_TotalAmount', output_field=FloatField()),
                service_charge_count=Count('autonum', filter=Q(ServiceCharge_TotalAmount__gt=0)),

                other_income_total=Sum('other_income', output_field=FloatField()),
                other_income_count=Count('autonum', filter=Q(other_income__gt=0)),

                total_cash_total=Sum('total_cash', output_field=FloatField()),
                total_cash_count=Count('autonum', filter=Q(total_cash__gt=0)),

                total_check_total=Sum('total_check', output_field=FloatField()),
                total_check_count=Count('autonum', filter=Q(total_check__gt=0)),

                total_pdc_total=Sum('total_pdc', output_field=FloatField()),
                total_pdc_count=Count('autonum', filter=Q(total_pdc__gt=0)),

                total_eps_total=Sum('total_eps', output_field=FloatField()),
                total_eps_count=Count('autonum', filter=Q(total_eps__gt=0)),

                total_credit_card_total=Sum('total_credit_card', output_field=FloatField()),
                total_credit_card_count=Count('autonum', filter=Q(total_credit_card__gt=0)),

                total_credit_sales_total=Sum('total_credit_sales', output_field=FloatField()),
                total_credit_sales_count=Count('autonum', filter=Q(total_credit_sales__gt=0)),

                online_payment_total=Sum('online_payment', output_field=FloatField()),
                online_payment_count=Count('autonum', filter=Q(online_payment__gt=0)),

                gift_check_total=Sum('gift_check', output_field=FloatField()),
                gift_check_count=Count('autonum', filter=Q(gift_check__gt=0)),

                other_payment_total=Sum('other_payment', output_field=FloatField()),
                other_payment_count=Count('autonum', filter=Q(other_payment__gt=0)),
            )
        )



        service_charge_total = totals['service_charge_total'] or 0
        service_charge_count = totals['service_charge_count'] or 0

        other_income = totals['other_income_total'] or 0
        other_income_count = totals['other_income_count'] or 0

        total_cash = totals['total_cash_total'] or 0
        total_cash_count = totals['total_cash_count'] or 0

        total_check = totals['total_check_total'] or 0
        total_check_count = totals['total_check_count'] or 0

        total_pdc = totals['total_pdc_total'] or 0
        total_pdc_count = totals['total_pdc_count'] or 0

        total_eps = totals['total_eps_total'] or 0
        total_eps_count = totals['total_eps_count'] or 0

        total_credit_card = totals['total_credit_card_total'] or 0
        total_credit_card_count = totals['total_credit_card_count'] or 0

        total_credit_sales = totals['total_credit_sales_total'] or 0
        total_credit_sales_count = totals['total_credit_sales_count'] or 0

        online_payment = totals['online_payment_total'] or 0
        online_payment_count = totals['online_payment_count'] or 0

        gift_check = totals['gift_check_total'] or 0
        gift_check_count = totals['gift_check_count'] or 0

        other_payment = totals['other_payment_total'] or 0
        other_payment_count = totals['other_payment_count'] or 0
        

        # === Optional: Grand Totals ===
        grand_total = (
            other_income + total_cash + total_check +
            total_pdc + total_eps + total_credit_card + total_credit_sales +
            online_payment + gift_check + other_payment
        )

        grand_total_count = (
             other_income_count + total_cash_count + total_check_count +
            total_pdc_count + total_eps_count + total_credit_card_count +
            total_credit_sales_count + online_payment_count + gift_check_count +
            other_payment_count
        )



        fund = PosCashiersLogin.objects.filter(
            id_code=id_code,
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
        ).aggregate(
            change_fund=Sum('change_fund', output_field=FloatField()),
            borrowed_fund=Sum('borrowed_fund', output_field=FloatField())
        )

        
        change_fund = fund['change_fund'] or 0
        borrowed_fund = fund['borrowed_fund'] or 0



        margin_left = 2 * mm
        margin_right = 10 * mm
        margin_top = 2 * mm
        margin_bottom = 2 * mm
        Total_due = 0
        Total_Payment = 0
        Amount_Tendered = 0

        x_start = 2 * mm  # Starting x-coordinate
        x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)
        clientSetup = getClientSetup()
        line_height = 0.3 * cm
        line_height_dash = 0.05 * cm
        margin = 0.1 * cm  # Adjust margins as needed
        width = 85 * mm  # Width adjusted for 79 mm roll paper
        height = (90) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
        y_position = height - margin - line_height 
        # Create a canvas with calculated size
        c = canvas.Canvas(f"ReprintXread{int(float(id_code))}.pdf", pagesize=(width, height))
        c.setFont("Courier", 8)
        c.setLineWidth(0.5)
        c.setDash(2,1)
        text_width = c.stringWidth(f'{clientSetup.company_name}')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'{clientSetup.company_name}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.company_address}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{clientSetup.company_address}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.company_address2}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.tin}')
        x_center = (width - text_width) / 2
        c.drawCentredString(width/2, y_position, f'{clientSetup.tin}')
        y_position -= line_height

        text_width = c.stringWidth(f'{clientSetup.tel_no}')
        x_center = (width - text_width) / 2
        c.drawCentredString(width/2, y_position, f'{clientSetup.tel_no}')
        y_position -= line_height

        text_width = c.stringWidth(f'{machineInfo.Machine_no}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
        y_position -= line_height

        text_width = c.stringWidth(f'{machineInfo.Serial_no}')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
        y_position -= line_height
        y_position -= line_height


   


       

        start_line = x_start + 5 * mm
        end_line = x_end - 5 * mm
        
        dt_obj = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        date_sales = datetime.strftime(dt_obj,'%m/%d/%Y')


        c.drawString(10 * mm, y_position, f'Admin: {request.user.fullname}')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        c.drawString(10 * mm, y_position, f'Cashier: {cashier_name}')
        y_position -= line_height
        c.drawString(10 * mm, y_position, f'Date of Sales: {date_sales}')
        y_position -= line_height
        c.drawString(10 * mm, y_position, f'Reprint Date: {current_datetime_ph}')
        y_position -= line_height
        y_position -= line_height
        

        text_width = c.stringWidth(f'REPRINT X-READING REPORT')
        x_center = (width - text_width) / 2
        c.drawString(x_center, y_position, f'REPRINT X-READING REPORT')
        y_position -= line_height
        y_position -= line_height

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        count_width = 4  # space reserved for count numbers (adjust as needed)
# Use f-string formatting to pad count with spaces
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Gross Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(gross_sales):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{item_discount_count:<{count_width}} Item Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(item_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{trade_discount_count:<{count_width}} Trade Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(trade_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{sc_pwd_discount_count:<{count_width}} SC Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(sc_pwd_discount):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{transaction_discount_count:<{count_width}} Transaction Discount:')
        c.drawRightString(width - margin_right, y_position, f'{float(transaction_discount):,.2f}')
        
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        net_of_discounts = float(gross_sales) - (item_discount + trade_discount + sc_pwd_discount + transaction_discount)
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET OF DISCOUNTS:')
        c.drawRightString(width - margin_right, y_position, f'{float(net_of_discounts):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{service_charge_count:<{count_width}} Service Charge:')
        c.drawRightString(width - margin_right, y_position, f'{float(service_charge_total):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{other_income_count:<{count_width}} Other Income:')
        c.drawRightString(width - margin_right, y_position, f'{float(other_income):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        net_total = float(net_of_discounts) + other_income + service_charge_total

        c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET:')
        c.drawRightString(width - margin_right, y_position, f'{float(net_total):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height
        #--------------------------------------------------------------------



        

        c.drawString(10 * mm, y_position, 'Breakdown (Tender of Payment)')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height

        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'{total_cash_count:<{count_width}} Cash:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_credit_card_count:<{count_width}} Credit Card:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_credit_card):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_check_count:<{count_width}} Check:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_check):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_pdc_count:<{count_width}} Postdated Check:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_pdc):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_eps_count:<{count_width}} Debit Card:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_eps):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{total_credit_sales_count:<{count_width}} Credit Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_credit_sales):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{gift_check_count:<{count_width}} Gift Checks:')
        c.drawRightString(width - margin_right, y_position, f'{float(gift_check):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{online_payment_count:<{count_width}} Online Payment:')
        c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'{other_payment_count:<{count_width}} Other Payment:')
        c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
        #--------------------------------------------------------------------


        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height

        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(grand_total):,.2f}')
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height



     

        # Cash Refund

        c.drawString(10 * mm, y_position, f'Return Type')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------

        c.drawString(10 * mm, y_position, f'{cash_refund_count:<{count_width}} Cash refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
        y_position -= line_height

        # Charge Back
        c.drawString(10 * mm, y_position, f'{charge_back_count:<{count_width}} Charge back:')
        c.drawRightString(width - margin_right, y_position, f'{float(charge_back):,.2f}')
        y_position -= line_height

        # Charge Refund
        c.drawString(10 * mm, y_position, f'{charge_refund_count:<{count_width}} Charge refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(charge_refund):,.2f}')
        y_position -= line_height

        # Check Refund
        c.drawString(10 * mm, y_position, f'{check_refund_count:<{count_width}} Check refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(check_refund):,.2f}')
        y_position -= line_height

        # Credit Memo
        c.drawString(10 * mm, y_position, f'{credit_memo_count:<{count_width}} Credit memo:')
        c.drawRightString(width - margin_right, y_position, f'{float(credit_memo):,.2f}')
        y_position -= line_height

        # Exchange
        c.drawString(10 * mm, y_position, f'{exchange_amount_count:<{count_width}} Exchange:')
        c.drawRightString(width - margin_right, y_position, f'{float(exchange_amount):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------

        total_refund = cash_refund + charge_back + charge_refund + check_refund + credit_memo + exchange_amount


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_refund):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height

        #--------------------------------------------------------------------



        c.drawString(10 * mm, y_position, f'Cashier\'s Cash Accountability')
  

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Sales:')
        c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
        y_position -= line_height

  
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Change Fund:')
        c.drawRightString(width - margin_right, y_position, f'{float(change_fund):,.2f}')
        y_position -= line_height

    
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Borrowed Fund:')
        c.drawRightString(width - margin_right, y_position, f'{float(borrowed_fund):,.2f}')
        y_position -= line_height


        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Pull Out:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_pull_out):,.2f}')
        y_position -= line_height

     
        c.drawString(10 * mm, y_position, f'{"":<{count_width}} Cash Refund:')
        c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
        y_position -= line_height

        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height

        cashier_accountability = (total_cash + change_fund + borrowed_fund ) - (cash_pull_out + cash_refund)
        c.drawString(10 * mm, y_position, f'TOTAL:')
        c.drawRightString(width - margin_right, y_position, f'{float(cashier_accountability):,.2f}')
        #--------------------------------------------------------------------

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        #--------------------------------------------------------------------
        y_position -= line_height


        c.drawString(10 * mm, y_position, f'Cash Breakdown')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height_dash     
        #--------------------------------------------------------------------   
        Denomination_list = [
            {"denomination": "Php 1,000.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 500.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 200.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 100.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 50.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 20.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 10.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 5.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 1.00", "qty": 0, "total": '0.00'},
            {"denomination": "Php 0.25", "qty": 0, "total": '0.00'},
            {"denomination": "Php 0.05", "qty": 0, "total": '0.00'},
            ]

        
 
        GTotal = 0
        for item in Denomination_list:
            y_position -= line_height
            result = PosCashBreakdown.objects.filter(login_record=trans_id,denomination = item["denomination"]).first()
            if result:
            
                text_width = c.stringWidth(f'{result.quantity}')
                c.drawString(10 * mm, y_position, f'{result.quantity}')

                text_width = c.stringWidth(f'{result.denomination}')
                c.drawString(x_center_deno, y_position, f'{result.denomination}')
                formatted = f"{result.total:,.2f}"
                text_width = c.stringWidth(formatted)
                c.drawRightString(width - margin_right, y_position, formatted)
                GTotal += float(result.total)
            else:
                text_width = c.stringWidth(f'{item["qty"]}')
                c.drawString(10 * mm, y_position, f'{item["qty"]}')

                text_width = c.stringWidth(f'{item["denomination"]}')
                c.drawString(x_center_deno, y_position, f'{item["denomination"]}')

                text_width = c.stringWidth(f'{item["total"]}')
                c.drawRightString(width - margin_right, y_position, f'{item["total"]}')

        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        #--------------------------------------------------------------------
        c.drawString(10 * mm, y_position, f'TOTAL')
        c.drawRightString(width - margin_right, y_position, f'{float(GTotal):,.2f}')
        #--------------------------------------------------------------------
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line,y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        y_position -= line_height
        #--------------------------------------------------------------------

        c.drawString(10 * mm, y_position, f'Cashier\'s Short/Over')
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line,y_position)
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'Cash Accountability')
        c.drawRightString(width - margin_right, y_position, f'{float(cashier_accountability):,.2f}')
        y_position -= line_height

        c.drawString(10 * mm, y_position, f'Cash breakdowns')
        c.drawRightString(width - margin_right, y_position, f'{float(GTotal):,.2f}')
        y_position -= line_height


        short_over = cashier_accountability - GTotal
        if short_over < 0:
            c.drawString(10 * mm, y_position, 'Over')
            value_to_display = abs(short_over)  # remove negative sign
        else:
            c.drawString(10 * mm, y_position, 'Short')
            value_to_display = short_over  # already positive

            # Draw the value right-aligned (example)
        c.drawRightString(width - margin_right, y_position, f'{value_to_display:,.2f}')
    

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        y_position -= line_height
        y_position -= line_height



        c.setDash()
        y_position -= line_height_dash
        c.line(start_line , y_position, end_line, y_position)
        y_position -= line_height
        text_width = c.stringWidth(f'Terminal Cashier')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'Terminal Cashier')
        y_position -= line_height
        y_position -= line_height
        y_position -= line_height

        y_position -= line_height_dash
        c.line(start_line , y_position, end_line ,y_position)
        y_position -= line_height
        text_width = c.stringWidth(f'Treasury Personnel')
        x_center = (width - text_width) / 2
        x_center_deno = x_center
        c.drawString(x_center, y_position, f'Treasury Personnel')
        y_position -= line_height
        c.save()


        file_path = f"ReprintXread{int(float(id_code))}.pdf"

        if not os.path.isfile(file_path):
            return Response({'error': 'File not found.'}, status=404)

        f = open(file_path, 'rb')
        response = FileResponse(f, as_attachment=True, filename=file_path)

        # ✅ Attach cleanup logic
        def cleanup_file(response):
            try:
                f.close()  # close file first
                os.remove(file_path)  # delete file
                print(f"✅ Deleted file: {file_path}")
            except Exception as e:
                print(f"⚠️ Error deleting file: {e}")
            return response

        # Override close method to call cleanup after sending
        response.close = lambda *args, **kwargs: cleanup_file(response)

        return response
    except Exception as e:
        print(e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def Reprint_Zread(request):
    if request.method == 'GET':
        try:
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()
            filter_str = request.GET.get('dateFrom',None)


            
            zread_no = request.GET.get('zread_no')
            terminal_no = request.GET.get('terminal_no')
            site_code = request.GET.get('site_code')
            filter_zread = PosZReading.objects.filter(
            zread_no=zread_no,
            terminal_no=terminal_no,
            site_code=site_code
            ).first()

            if filter_zread:
                old_grand_total = filter_zread.old_grand_total or 0
                new_grand_total = filter_zread.new_grand_total or 0
                date_of_zread = filter_zread.zread_time or current_datetime_ph
            else:
                old_grand_total = 0
                new_grand_total = 0
                date_of_zread =  current_datetime_ph



            date_from = datetime.strptime(filter_str + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            date_to   = datetime.strptime(filter_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            
            xread_date = current_date_ph

            # --- Sales Summary ---
            gross_sales = 0.00
            item_discount = 0.00
            trade_discount = 0.00
            sc_pwd_discount = 0.00
            transaction_discount = 0.00
            refund_return = 0.00
            net_of_discounts = 0.00
            service_charge = 0.00
            other_income = 0.00
            net_total = 0.00

            # --- Payment Breakdown ---
            cash_payment = 0.00
            credit_card_payment = 0.00
            current_check_payment = 0.00
            postdated_check_payment = 0.00
            debit_card_payment = 0.00
            credit_sales = 0.00
            gift_check_payment = 0.00
            online_payment = 0.00
            other_payment = 0.00
            total_payment = 0.00

            # --- Returns ---
            cash_refund = 0.00
            charge_back = 0.00
            charge_refund = 0.00
            check_refund = 0.00
            credit_memo = 0.00
            exchange_amount = 0.00
            total_refund = 0.00

            # === Return Type Counts ===
            cash_refund_count = 0
            charge_back_count = 0
            charge_refund_count = 0
            check_refund_count = 0
            credit_memo_count = 0
            exchange_amount_count = 0



            # --- Cashier Accountability ---
            cash_sales = 0.00
            change_fund = 0.00
            borrowed_fund = 0.00
            cash_pull_out = 0.00
            cash_refund_account = 0.00

            gross_sales = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
                    ).aggregate(
                        gross_sales=Sum(F('sub_total') - F('vat_exempted'))
                    )['gross_sales'] or 0
        
            discounts = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                site_code=int(machineInfo.site_no)
            ).aggregate(
                # Item Discount
                item_discount=Sum(
                    Case(
                        When(discount_type='IM', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                item_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='IM', discount__gt=0)
                ),

                # Trade Discount
                trade_discount=Sum(
                    Case(
                        When(discount_type='TD', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                trade_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='TD', discount__gt=0)
                ),

                # Senior/PWD Discount
                sc_pwd_discount=Sum(
                    Case(
                        When(discount_type='SC', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                sc_pwd_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='SC', discount__gt=0)
                ),

                # Transaction Discount
                transaction_discount=Sum(
                    Case(
                        When(discount_type='TN', then=F('discount')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                transaction_discount_count=Count(
                    'zread_no',
                    filter=Q(discount_type='TN', discount__gt=0)
                ),
            )
            item_discount = discounts['item_discount'] or 0
            item_discount_count = discounts['item_discount_count'] or 0

            trade_discount = discounts['trade_discount'] or 0
            trade_discount_count = discounts['trade_discount_count'] or 0

            sc_pwd_discount = discounts['sc_pwd_discount'] or 0
            sc_pwd_discount_count = discounts['sc_pwd_discount_count'] or 0

            transaction_discount = discounts['transaction_discount'] or 0
            transaction_discount_count = discounts['transaction_discount_count'] or 0



            totals = (
                PosSalesInvoiceList.objects.filter(
                    doc_date__gte=date_from,
                    doc_date__lt=date_to,
                    status='A',
                    terminal_no=int(machineInfo.terminal_no),
                    site_code=int(machineInfo.site_no)
                )
                .aggregate(
                    service_charge_total=Sum('ServiceCharge_TotalAmount', output_field=FloatField()),
                    service_charge_count=Count('autonum', filter=Q(ServiceCharge_TotalAmount__gt=0)),

                    other_income_total=Sum('other_income', output_field=FloatField()),
                    other_income_count=Count('autonum', filter=Q(other_income__gt=0)),

                    total_cash_total=Sum('total_cash', output_field=FloatField()),
                    total_cash_count=Count('autonum', filter=Q(total_cash__gt=0)),

                    total_check_total=Sum('total_check', output_field=FloatField()),
                    total_check_count=Count('autonum', filter=Q(total_check__gt=0)),

                    total_pdc_total=Sum('total_pdc', output_field=FloatField()),
                    total_pdc_count=Count('autonum', filter=Q(total_pdc__gt=0)),

                    total_eps_total=Sum('total_eps', output_field=FloatField()),
                    total_eps_count=Count('autonum', filter=Q(total_eps__gt=0)),

                    total_credit_card_total=Sum('total_credit_card', output_field=FloatField()),
                    total_credit_card_count=Count('autonum', filter=Q(total_credit_card__gt=0)),

                    total_credit_sales_total=Sum('total_credit_sales', output_field=FloatField()),
                    total_credit_sales_count=Count('autonum', filter=Q(total_credit_sales__gt=0)),

                    online_payment_total=Sum('online_payment', output_field=FloatField()),
                    online_payment_count=Count('autonum', filter=Q(online_payment__gt=0)),

                    gift_check_total=Sum('gift_check', output_field=FloatField()),
                    gift_check_count=Count('autonum', filter=Q(gift_check__gt=0)),

                    other_payment_total=Sum('other_payment', output_field=FloatField()),
                    other_payment_count=Count('autonum', filter=Q(other_payment__gt=0)),
                )
            )



            service_charge_total = totals['service_charge_total'] or 0
            service_charge_count = totals['service_charge_count'] or 0

            other_income = totals['other_income_total'] or 0
            other_income_count = totals['other_income_count'] or 0

            total_cash = totals['total_cash_total'] or 0
            total_cash_count = totals['total_cash_count'] or 0

            total_check = totals['total_check_total'] or 0
            total_check_count = totals['total_check_count'] or 0

            total_pdc = totals['total_pdc_total'] or 0
            total_pdc_count = totals['total_pdc_count'] or 0

            total_eps = totals['total_eps_total'] or 0
            total_eps_count = totals['total_eps_count'] or 0

            total_credit_card = totals['total_credit_card_total'] or 0
            total_credit_card_count = totals['total_credit_card_count'] or 0

            total_credit_sales = totals['total_credit_sales_total'] or 0
            total_credit_sales_count = totals['total_credit_sales_count'] or 0

            online_payment = totals['online_payment_total'] or 0
            online_payment_count = totals['online_payment_count'] or 0

            gift_check = totals['gift_check_total'] or 0
            gift_check_count = totals['gift_check_count'] or 0

            other_payment = totals['other_payment_total'] or 0
            other_payment_count = totals['other_payment_count'] or 0
            

            # === Optional: Grand Totals ===
            grand_total = (
                other_income + total_cash + total_check +
                total_pdc + total_eps + total_credit_card + total_credit_sales +
                online_payment + gift_check + other_payment
            )

            grand_total_count = (
                other_income_count + total_cash_count + total_check_count +
                total_pdc_count + total_eps_count + total_credit_card_count +
                total_credit_sales_count + online_payment_count + gift_check_count +
                other_payment_count
            )




            margin_left = 2 * mm
            margin_right = 10 * mm
            margin_top = 2 * mm
            margin_bottom = 2 * mm
            Total_due = 0
            Total_Payment = 0
            Amount_Tendered = 0
      

            x_start = 2 * mm  # Starting x-coordinate
            x_end = x_start + 85 * mm  # Ending x-coordinate (55 characters long)
            clientSetup = getClientSetup()
            line_height = 0.3 * cm
            line_height_dash = 0.05 * cm
            margin = 0.1 * cm  # Adjust margins as needed
            width = 85 * mm  # Width adjusted for 79 mm roll paper
            height = (95) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines
            y_position = height - margin - line_height 
            # Create a canvas with calculated size
            c = canvas.Canvas(f"ReprintZread{int(float(zread_no))}.pdf", pagesize=(width, height))
            c.setFont("Courier", 8)
            c.setLineWidth(0.5)
            c.setDash(2,1)
            text_width = c.stringWidth(f'{clientSetup.company_name}')
            x_center = (width - text_width) / 2
            x_center_deno = x_center
            c.drawString(x_center, y_position, f'{clientSetup.company_name}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.company_address2}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{clientSetup.company_address2}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tin}')
            x_center = (width - text_width) / 2
            c.drawCentredString(width/2, y_position, f'{clientSetup.tin}')
            y_position -= line_height

            text_width = c.stringWidth(f'{clientSetup.tel_no}')
            x_center = (width - text_width) / 2
            c.drawCentredString(width/2, y_position, f'{clientSetup.tel_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Machine_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Machine_no}')
            y_position -= line_height

            text_width = c.stringWidth(f'{machineInfo.Serial_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'{machineInfo.Serial_no}')
            y_position -= line_height
            y_position -= line_height


            start_line = x_start + 5 * mm
            end_line = x_end - 5 * mm


            current_date_ph_str = current_date_ph
            date_from_str = datetime.strftime(date_from,"%m/%d/%Y")

            date_of_zread = datetime.strptime(date_of_zread,"%Y-%m-%d %H:%M:%S")
            date_of_zread_str = datetime.strftime(date_of_zread,"%m/%d/%Y %H:%M:%S")



            # Parse using 24-hour format
            
            c.drawString(10 * mm, y_position, f'Admin: {request.user.fullname}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Date of Z-Reading: {date_of_zread_str}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Date of Sales: {date_from_str}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Date of Reprint: {current_datetime_ph}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Terminal No: {int(terminal_no)}')
            y_position -= line_height
            y_position -= line_height

            
            text_width = c.stringWidth(f'REPRINT Z-READING SUMMARY # {zread_no}')
            x_center = (width - text_width) / 2
            c.drawString(x_center, y_position, f'REPRINT Z-READING SUMMARY # {zread_no}')
            y_position -= line_height
            y_position -= line_height
            
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            count_width = 4  # space reserved for count numbers (adjust as needed)
    # Use f-string formatting to pad count with spaces
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Gross Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(gross_sales):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{item_discount_count:<{count_width}} Item Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(item_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{trade_discount_count:<{count_width}} Trade Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(trade_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{sc_pwd_discount_count:<{count_width}} SC Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(sc_pwd_discount):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{transaction_discount_count:<{count_width}} Transaction Discount')
            c.drawRightString(width - margin_right, y_position, f'{float(transaction_discount):,.2f}')
            
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            net_of_discounts = float(gross_sales) - (item_discount + trade_discount + sc_pwd_discount + transaction_discount)
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET OF DISCOUNTS')
            c.drawRightString(width - margin_right, y_position, f'{float(net_of_discounts):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{service_charge_count:<{count_width}} Service Charge')
            c.drawRightString(width - margin_right, y_position, f'{float(service_charge_total):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{other_income_count:<{count_width}} Other Income')
            c.drawRightString(width - margin_right, y_position, f'{float(other_income):,.2f}')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            net_total = float(net_of_discounts) + other_income + service_charge_total

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NET')
            c.drawRightString(width - margin_right, y_position, f'{float(net_total):,.2f}')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height
            #--------------------------------------------------------------------



            

            c.drawString(10 * mm, y_position, 'Breakdown (Tender of Payment)')
            #--------------------------------------------------------------------
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'{total_cash_count:<{count_width}} Cash')
            c.drawRightString(width - margin_right, y_position, f'{float(total_cash):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_credit_card_count:<{count_width}} Credit Card')
            c.drawRightString(width - margin_right, y_position, f'{float(total_credit_card):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_check_count:<{count_width}} Check')
            c.drawRightString(width - margin_right, y_position, f'{float(total_check):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_pdc_count:<{count_width}} Postdated Check')
            c.drawRightString(width - margin_right, y_position, f'{float(total_pdc):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_eps_count:<{count_width}} Debit Card')
            c.drawRightString(width - margin_right, y_position, f'{float(total_eps):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{total_credit_sales_count:<{count_width}} Credit Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(total_credit_sales):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{gift_check_count:<{count_width}} Gift Checks')
            c.drawRightString(width - margin_right, y_position, f'{float(gift_check):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{online_payment_count:<{count_width}} Online Payment')
            c.drawRightString(width - margin_right, y_position, f'{float(online_payment):,.2f}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{other_payment_count:<{count_width}} Other Payment')
            c.drawRightString(width - margin_right, y_position, f'{float(other_payment):,.2f}')
            #--------------------------------------------------------------------


            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height

            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL')
            c.drawRightString(width - margin_right, y_position, f'{float(grand_total):,.2f}')
            #--------------------------------------------------------------------
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height



        

            # Cash Refund

            c.drawString(10 * mm, y_position, f'Return Type')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------

            c.drawString(10 * mm, y_position, f'{cash_refund_count:<{count_width}} Cash refund')
            c.drawRightString(width - margin_right, y_position, f'{float(cash_refund):,.2f}')
            y_position -= line_height

            # Charge Back
            c.drawString(10 * mm, y_position, f'{charge_back_count:<{count_width}} Charge back')
            c.drawRightString(width - margin_right, y_position, f'{float(charge_back):,.2f}')
            y_position -= line_height

            # Charge Refund
            c.drawString(10 * mm, y_position, f'{charge_refund_count:<{count_width}} Charge refund')
            c.drawRightString(width - margin_right, y_position, f'{float(charge_refund):,.2f}')
            y_position -= line_height

            # Check Refund
            c.drawString(10 * mm, y_position, f'{check_refund_count:<{count_width}} Check refund')
            c.drawRightString(width - margin_right, y_position, f'{float(check_refund):,.2f}')
            y_position -= line_height

            # Credit Memo
            c.drawString(10 * mm, y_position, f'{credit_memo_count:<{count_width}} Credit memo')
            c.drawRightString(width - margin_right, y_position, f'{float(credit_memo):,.2f}')
            y_position -= line_height

            # Exchange
            c.drawString(10 * mm, y_position, f'{exchange_amount_count:<{count_width}} Exchange')
            c.drawRightString(width - margin_right, y_position, f'{float(exchange_amount):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------

            total_refund = cash_refund + charge_back + charge_refund + check_refund + credit_memo + exchange_amount


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} TOTAL')
            c.drawRightString(width - margin_right, y_position, f'{float(total_refund):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height

            #--------------------------------------------------------------------


            vat_amount = 0
            vat_amount_count = 0
            non_vat_amount = 0
            non_vat_amount_count = 0
            vatable_amount = 0
            vatable_amount_count = 0
            zero_rated_amount = 0
            zero_rated_amount_count = 0
            vat_exempt_amount = 0
            vat_exempt_amount_count = 0
            total_sales= 0



            vat_amount_return = 0
            vat_amount_return_count = 0
            non_vat_return_amount = 0
            non_vat_return_count = 0
            vatable_return_amount = 0
            vatable_return_count = 0
            zero_rated_return_amount = 0
            zero_rated_return_count = 0
            vat_exempt_return_amount = 0
            vat_exempt_return_count = 0
            total_return= 0

            #******************* SALES ******************
            vat_ = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vat_count=Count('zread_no', filter=Q(vat__gt=0))
            )

            vat_amount = vat_['vat_amount'] or 0
            vat_amount_count = vat_['vat_count'] or 0

            non_vat_ = PosSalesInvoiceListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                vatable='Nv',
                isvoid='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                non_vat_amount=Sum(F('disc_amt'), output_field=FloatField(), default=0),
                non_vat_amount_count=Count('zread_no', filter=Q(disc_amt__gt=0))
            )

            non_vat_amount = non_vat_['non_vat_amount'] or 0
            non_vat_amount_count = non_vat_['non_vat_amount_count'] or 0


            vatable_ = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='S',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vatable_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vatable_amount_count=Count('zread_no', filter=Q(vat__gt=0))
            )
            vat_amt = vatable_.get('vatable_amount')
            if vat_amt:
                vatable_amount = float(vat_amt) / 0.12
            else:
                vatable_amount = 0
            print('vatable amount',vatable_amount)
            # vatable_amount = float(vatable_['vatable_amount']) / 0.12  or 0
            vatable_amount_count = vatable_['vatable_amount_count'] or 0


            vat_exempt = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_exempt_amount=Sum(F('vat_exempt'), output_field=FloatField(), default=0),
                vat_exempt_amount_count=Count('zread_no', filter=Q(vat__gt=0))
                
            )

            vat_exempt_amount = vat_exempt['vat_exempt_amount'] or 0
            vat_exempt_amount_count = vat_exempt['vat_exempt_amount_count'] or 0

            total_sales = vat_amount + non_vat_amount + vatable_amount + zero_rated_amount + vat_exempt_amount

            #******************* RETURNS ******************
            vat_return = PosSalesReturnList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vat_count=Count('zread_no', filter=Q(vat__gt=0))
            )

            vat_amount_return = vat_return['vat_amount'] or 0
            vat_amount_return_count = vat_return['vat_count'] or 0

            non_vat_return = PosSalesReturnListing.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                vatable='Nv',
                isvoid='NO',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                non_vat_amount=Sum(F('disc_amt'), output_field=FloatField(), default=0),
                non_vat_amount_count=Count('zread_no', filter=Q(disc_amt__gt=0))
            )

            non_vat_return_amount = non_vat_return['non_vat_amount'] or 0
            non_vat_return_count = non_vat_return['non_vat_amount_count'] or 0


            vatable_return = PosSalesReturnList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vatable_amount=Sum(F('vat'), output_field=FloatField(), default=0),
                vatable_amount_count=Count('zread_no', filter=Q(vat__gt=0))
            )
            vatable_amount_r = vatable_return.get('vatable_amount')
            if vatable_amount_r:
                vatable_return_amount = float(vatable_amount_r) / 0.12
            else:
                vatable_return_amount = 0
            # vatable_return_amount = float(vatable_return['vatable_amount']) / 0.12  or 0
            vatable_return_count = vatable_return['vatable_amount_count'] or 0


            vat_exempt_return = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).aggregate(
                vat_exempt_amount=Sum(F('vat_exempt'), output_field=FloatField(), default=0),
                vat_exempt_amount_count=Count('zread_no', filter=Q(vat__gt=0))
                
            )

            vat_exempt_return_amount = vat_exempt_return['vat_exempt_amount'] or 0
            vat_exempt_return_count = vat_exempt_return['vat_exempt_amount_count'] or 0

            total_return = vat_amount_return + non_vat_return_amount + vatable_return_amount + zero_rated_return_amount + vat_exempt_return_amount



            c.drawString(10 * mm, y_position, f'Breakdown (VAT)')

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'SALES')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Amount')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_amount):,.2f}')
            y_position -= line_height

    
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NON-VAT Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(non_vat_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VATable Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(vatable_amount):,.2f}')
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Zero Rated Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(zero_rated_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Exempt Sales')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_exempt_amount):,.2f}')
            y_position -= line_height

            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'TOTAL - SALES')
            c.drawRightString(width - margin_right, y_position, f'{float(total_sales):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            c.drawString(10 * mm, y_position, f'RETURNS')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Amount Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_amount_return):,.2f}')
            y_position -= line_height

    
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} NON-VAT Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(non_vat_return_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VATable Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vatable_return_amount):,.2f}')
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'{"":<{count_width}} Zero Rated Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(zero_rated_return_amount):,.2f}')
            y_position -= line_height

        
            c.drawString(10 * mm, y_position, f'{"":<{count_width}} VAT Exempt Sales Return')
            c.drawRightString(width - margin_right, y_position, f'{float(vat_exempt_return_amount):,.2f}')
            y_position -= line_height

            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'TOTAL - RETURNS')
            c.drawRightString(width - margin_right, y_position, f'{float(total_return):,.2f}')
            #--------------------------------------------------------------------

            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line ,y_position)
            y_position -= line_height
            #--------------------------------------------------------------------
            net_vat = total_sales - total_return
            c.drawString(10 * mm, y_position, f'Net VAT')
            c.drawRightString(width - margin_right, y_position, f'{float(net_vat):,.2f}')
            y_position -= line_height
            y_position -= line_height



            # Filter transactions

            sales_transactions = PosSalesInvoiceList.objects.filter(
                doc_date__gte=date_from,
                doc_date__lt=date_to,
                status='A',
                doc_type='POS-SI',
                terminal_no=int(machineInfo.terminal_no),
                site_code=int(machineInfo.site_no)
            ).order_by('doc_no')

            # Check if any transactions exist
            if sales_transactions.exists():
                sales_first_transaction = sales_transactions.first()
                sales_last_transaction = sales_transactions.last()
                sales_count = sales_transactions.count()

                sales_first_no = sales_first_transaction.doc_no
                sales_last_no = sales_last_transaction.doc_no
            else:
                sales_first_no = None
                sales_last_no = None
                sales_count = 0




            credit_transactions = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            status='A',
            doc_type = 'POS-CI',
            terminal_no=int(machineInfo.terminal_no),
            site_code=int(machineInfo.site_no)
            ).order_by('doc_no')

            credit_first_transaction = credit_transactions.first()
            credit_last_transaction = credit_transactions.last()
            credit_count = credit_transactions.count()

            credit_first_no = credit_first_transaction.doc_no if credit_first_transaction else None
            credit_last_no = credit_last_transaction.doc_no if credit_last_transaction else None



            transactions = PosSalesInvoiceList.objects.filter(
            doc_date__gte=date_from,
            doc_date__lt=date_to,
            status='A',
            site_code=int(machineInfo.site_no),
            terminal_no=int(machineInfo.terminal_no)
            ).order_by('doc_no').values_list('doc_no', flat=True)

            coun_trans = transactions.count()

            first_no = transactions.first() if transactions.exists() else None
            last_no = transactions.last() if transactions.exists() else None


            sales_first_no_int = int(sales_first_no) if sales_first_no is not None else 0
            sales_last_no_int  = int(sales_last_no)  if sales_last_no is not None else 0
            sales_count_int = int(sales_count)  if sales_count is not None else 0

            credit_first_no_int = int(credit_first_no) if credit_first_no is not None else 0
            credit_last_no_int  = int(credit_last_no)  if credit_last_no is not None else 0
            credit_count_int = int(credit_count)  if credit_count is not None else 0

            first_no_int = int(first_no) if first_no is not None else 0
            last_no_int  = int(last_no)  if last_no is not None else 0
            coun_trans_int = int(coun_trans)  if coun_trans is not None else 0






            c.drawString(10 * mm, y_position, f'Credit Invoice Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'From Credit Invoice')
            c.drawRightString(width - margin_right, y_position, f'{credit_first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'To Credit Invoice')
            c.drawRightString(width - margin_right, y_position, f'{credit_last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Total Credit Invoice Issued')
            c.drawRightString(width - margin_right, y_position, f'{credit_count_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'Sales Invoice Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'From Sales Invoice')
            c.drawRightString(width - margin_right, y_position, f'{sales_first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'To Sales Invoice')
            c.drawRightString(width - margin_right, y_position, f'{sales_last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Total Sales Invoice Issued')
            c.drawRightString(width - margin_right, y_position, f'{sales_count_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            y_position -= line_height


            c.drawString(10 * mm, y_position, f'Transaction Summary')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line,y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'First Transaction')
            c.drawRightString(width - margin_right, y_position, f'{first_no_int:08d}')
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Last Transaction')
            c.drawRightString(width - margin_right, y_position, f'{last_no_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height

            c.drawString(10 * mm, y_position, f'Transaction Count')
            c.drawRightString(width - margin_right, y_position, f'{coun_trans_int:08d}')
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height_dash
            c.line(start_line , y_position, end_line, y_position)
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'Old Grand Total')
            c.drawRightString(width - margin_right, y_position, f'{float(old_grand_total):,.2f}')
            y_position -= line_height
            c.drawString(10 * mm, y_position, f'New Grand Total')
            new_grand_total = net_vat + float(old_grand_total)
            c.drawRightString(width - margin_right, y_position, f'{float(new_grand_total):,.2f}')

            print('done')
            c.save()

            file_path = f"ReprintZread{zread_no}.pdf"

            if not os.path.isfile(file_path):
                return Response({'error': 'File not found.'}, status=404)

            f = open(file_path, 'rb')
            response = FileResponse(f, as_attachment=True, filename=file_path)

            def cleanup_file(response):
                try:
                    f.close()  # close file first
                    os.remove(file_path)  # delete file
                    print(f"✅ Deleted file: {file_path}")
                except Exception as e:
                    print(f"⚠️ Error deleting file: {e}")
                return response

            # Override close method to call cleanup after sending
            response.close = lambda *args, **kwargs: cleanup_file(response)

            return response
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

