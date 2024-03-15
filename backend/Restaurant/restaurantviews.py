import abc
import decimal
import json
import locale
import pdb
from django.http import JsonResponse
from rest_framework.response import Response
from backend.models import (Product,PosRestTable,PosSalesOrder,PosSalesTransDetails,InvRefNo,POS_Terminal,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                            CompanySetup,Customer,PosWaiterList,PosPayor,SeniorCitizenDiscount,PosExtended,PosCashBreakdown,
                            ProductCategorySetup,BankCompany,BankCard,SalesTransCreditCard,SalesTransEPS)
from backend.serializers import (ProductSerializer,ProductCategorySerializer,PosSalesOrderSerializer,PosSalesTransDetailsSerializer,PosSalesTransSerializer,
                                 PosSalesInvoiceListing,PosSalesInvoiceList,CustomerSerializer,PosWaiterListSerializer,PosPayorSerializer,PosSalesInvoiceListSerializer,
                                 SeniorCitizenDiscountSerializer,PosExtendedSerializer,PosCashBreakdownSerializer,ProductCategorySetupSerializer,
                                 BankCompanySerializer,BankCardSerializer,SalesTransCreditCardSerializer,SalesTransEPSSerializer)
from rest_framework.decorators import api_view
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
import pytz
from django.core.exceptions import ObjectDoesNotExist
import time

from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime



@api_view(['GET','POST','PUT','DELETE'])

def print_electron(request):
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        try:
            app = Application().connect(title="Print")
            print_dialog = app.window(class_name="#32770")
            print_dialog.print_button.click()
            return JsonResponse({"message": "Print Success"}, status=200)
        
        except ElementNotFoundError:
            attempts += 1
            print(f"Attempt {attempts}: Print dialog not found. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
    
    print("Failed to connect to the application after maximum attempts.")
    return JsonResponse({"error": "Failed to connect to the application"}, status=404)

     
##********** EXTENDED MONITOR TRANSACTION ********##
@api_view(['GET','POST','PUT','DELETE'])
def pos_extended(request):
    if request.method == 'GET':
        data = request.GET.get('data')
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        data_list = PosExtended.objects.filter(serial_no = machineInfo.Serial_no)
        serialize = PosExtendedSerializer(data_list,many=True)
        return Response(serialize.data)
    
    elif request.method == 'POST':
        try:
            # pdb.set_trace()
            # Parse the JSON data sent in the request body
            data = json.loads(request.body)
            print(data)
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            # data = data['data']
            TableNo = data['TableNo']
            orderType = data['OrderType']
            quantity = data['data']['quantity']
            description = data['data']['description']
            price = data['data']['price']
            total_amount = data['data']['totalAmount']
            barcode = data['data']['barcode']
            if TableNo =='':
                TableNo = 0
            data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number, barcode=barcode)
            # Check if any records exist in the queryset
            if data_exist_queryset.exists():
                # Access the first instance in the queryset (assuming there's only one matching record)
                data_exist_instance = data_exist_queryset.first()
                
                # Update the fields of the instance
                data_exist_instance.qty = quantity
                data_exist_instance.amount = total_amount
                data_exist_instance.price = price
                
                # Save the changes to the instance
                data_exist_instance.save()


            else:
     
                saveExtended = PosExtended(
                    barcode=barcode,
                    qty=quantity,
                    description=description,
                    price=price,
                    amount=total_amount,
                    serial_no=serial_number,
                    table_no=int(TableNo),
                    order_type=orderType
                )
                saveExtended.save()
            # Process the data as needed
            # For example, you can access data['data'] to get the 'data' key sent from Axios

            # Optionally, save the data to the database
            # Example: ExtendedData.objects.create(**data)

            return JsonResponse({'success': True, 'message': 'Data received successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    elif request.method == 'DELETE':
        try:
    # Parse the JSON data sent in the request body
            data = json.loads(request.body)  # Decode and load JSON data
        
    
            quantity = data['deleteData']['quantity']
            description = data['deleteData']['description']
            price = data['deleteData']['price']
            total_amount = data['deleteData']['totalAmount']
            barcode = data['deleteData']['barcode']
            
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    

            # Retrieve the queryset of existing records based on the specified conditions
            data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number, barcode=barcode)

            # Check if any records exist in the queryset
            if data_exist_queryset.exists():
                # Delete all matching records from the database
                data_exist_queryset.delete()
                return Response('Delete Successfully')

        except Exception as e:
            # Handle exceptions here
            print("An error occurred:", e)
   
@api_view(['GET','POST','PUT','DELETE'])
def pos_extended_delete_all(request):
    if request.method == 'DELETE':
        print('delete')
        try:
            # pdb.set_trace()
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number.strip())
            if data_exist_queryset.exists():
                data_exist_queryset.delete()
                return Response('Delete Successfully')

        except Exception as e:
            # Handle exceptions here
            print("An error occurred:", e)


def pos_extended_save_from_listing(data,TableNo,QueNO):
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    check_data = PosExtended.objects.filter(serial_no=machineInfo.Serial_no)
    # pdb.set_trace()
    if not check_data:
        if TableNo:
            for item in data:
                new_item = PosExtended(
                    serial_no=machineInfo.Serial_no,
                    barcode=item.get('barcode'),
                    qty=item.get('quantity'),
                    description=item.get('description'),
                    price=item.get('price'),
                    order_type = 'DINE IN',
                    amount=int(item.get('quantity')) * float(item.get('price')),
                    table_no = TableNo,
                    entry_type = 'view',)
                new_item.save()
        else:

            for item in data:
                new_item = PosExtended(
                    serial_no=machineInfo.Serial_no,
                    barcode=item.get('barcode'),
                    qty=item.get('quantity'),
                    description=item.get('description'),
                    price=item.get('price'),
                    order_type = 'TAKE OUT',
                    amount=int(item.get('quantity')) * float(item.get('price')),
                    que_no = int(float(QueNO)),
                    entry_type = 'view', )
                new_item.save()

## ********************* END HERE  ************************##
@api_view(['GET'])
def get_product_data(request):
    products = Product.objects.exclude(reg_price=0).exclude(long_desc='')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_productCategory_data(request):
    # Assuming 'category' is a field in the Product model
    # distinct_categories = Product.objects.values('category').distinct()
        # serializer = ProductCategorySerializer(distinct_categories, many=True)
    distinct_categories = ProductCategorySetup.objects.filter(pos_category='Y')
    serializer = ProductCategorySetupSerializer(distinct_categories, many=True)

    # print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_by_category(request):
    if request.method == 'GET':
        category = request.GET.get('category')
    # Query the Product model based on the category received in the URL
        if category == 'ALL':
            products = Product.objects.exclude(reg_price='0').exclude(long_desc='')

        # Serialize the products (convert to JSON or any desired format)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = Product.objects.filter(category=category).exclude(reg_price='0').exclude(long_desc='')

        # Serialize the products (convert to JSON or any desired format)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

@api_view(['GET'])
def table_list_view(request):
    site_code = request.GET.get('site_code', None)  # Assuming site_code is passed as a query parameter
    if site_code is None:
        return Response({"error": "Site code is missing"}, status=400)

    tables = PosRestTable.objects.filter(site_code=site_code).order_by('table_start')
    
    
    if not tables.exists():
        return Response({"message": f"No tables found for site code: {site_code}"})

    table_list = []
    for table in tables:
        table_count = 1 + table.table_start
        while table_count <= table.table_no + table.table_start:
            paid_list ='Y'
            
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            
            paid = PosSalesOrder.objects.filter(table_no=table_count ,paid = 'N',active = 'Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                for item in serializer.data:
                  
                    paid_list = item['paid']  # Assuming 'paid' is the correct field name
            table_list.append({"table_count": table_count, "Paid": paid_list})
            # print(table_list)
            table_count += 1

    return Response({"tables": table_list})


@api_view(['GET'])
def queing_list_view(request):
    site_code = request.GET.get('site_code', None)  # Assuming site_code is passed as a query parameter
    if site_code is None:
        return Response({"error": "Site code is missing"}, status=400)

            
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    que_list=[]        
    paid = PosSalesOrder.objects.filter(
        q_no__isnull=False,  # Exclude records where q_no is null
        paid='N',
        active='Y',
        terminal_no=machineInfo.terminal_no,
        site_code=int(machineInfo.site_no)
    ).exclude(q_no='0.000')
    if paid.exists():
        serializer = PosSalesOrderSerializer(paid, many=True)
        for item in serializer.data:
                  
            paid_list = item['paid'] 
            que_list.append({"q_no": item['q_no'] , "Paid": paid_list})
    print(que_list)
    return Response({"que": que_list})


@api_view(['GET'])
def get_sales_order_list(request):
    if request.method == 'GET':
        tableno = request.GET.get('tableno')
        queno = request.GET.get('queno')
        print(tableno,queno)

        if tableno is not None:
            if tableno == 0:
                serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
            else:
                serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =tableno)
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
        else:
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,q_no = queno)
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                return Response(serializer.data)
                  

@api_view(['GET'])
def get_sales_order_listing(request):
    # document_no = request.GET.get('document_no[]')
    # pdb.set_trace()
    TableNo = request.GET.get('tableno')
    so_no = request.GET.get('so_no')

    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    queno = request.GET.get('queno')
    print(TableNo,so_no)
    # pdb.set_trace()
    if TableNo is not None:
       
        if so_no:
            print('pos_sales_order_data',int(machineInfo.site_no),machineInfo.terminal_no)
            # pdb.set_trace()
            pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo,SO_no = so_no)
            result = []
            print('pos_sales_order_data',pos_sales_order_data)
            
            for item in pos_sales_order_data:
                matched_records = PosSalesTransDetails.objects.extra(
                    select={
                        'sales_order_document_no': 'tbl_pos_sales_order.document_no',
                        'so_no': 'tbl_pos_sales_order.SO_no'
                    },
                    tables=['tbl_pos_sales_trans_details', 'tbl_pos_sales_order'],
                    where=[
                        'tbl_pos_sales_trans_details.sales_trans_id = tbl_pos_sales_order.document_no',
                        'tbl_pos_sales_order.document_no = %s'
                    ],
                    params=[item.document_no]  
                )
                result.extend(list(matched_records.values()))
            pos_extended_save_from_listing(result ,TableNo,queno)   
        else:
            pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo)
            result = []
            
            for item in pos_sales_order_data:
                matched_records = PosSalesTransDetails.objects.extra(
                    select={
                        'sales_order_document_no': 'tbl_pos_sales_order.document_no',
                        'so_no': 'tbl_pos_sales_order.SO_no'
                    },
                    tables=['tbl_pos_sales_trans_details', 'tbl_pos_sales_order'],
                    where=[
                        'tbl_pos_sales_trans_details.sales_trans_id = tbl_pos_sales_order.document_no',
                        'tbl_pos_sales_order.document_no = %s'
                    ],
                    params=[item.document_no]  
                )
                result.extend(list(matched_records.values()))
            pos_extended_save_from_listing(result ,TableNo,queno)   
    else:
        pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,q_no =queno)
        result = []
        print('eeeeeeeeeeeeeeeeeeeee')
        for item in pos_sales_order_data:
            matched_records = PosSalesTransDetails.objects.extra(
                select={
                    'sales_order_document_no': 'tbl_pos_sales_order.document_no',
                    'so_no': 'tbl_pos_sales_order.SO_no'
                },
                tables=['tbl_pos_sales_trans_details', 'tbl_pos_sales_order'],
                where=[
                    'tbl_pos_sales_trans_details.sales_trans_id = tbl_pos_sales_order.document_no',
                    'tbl_pos_sales_order.document_no = %s'
                ],
                params=[item.document_no]  
            )
            result.extend(list(matched_records.values()))
            print('result',result)
        pos_extended_save_from_listing(result ,TableNo,queno)   
    return Response(result)


@api_view(['GET'])
def get_add_order_view(request):
    
    
    # Query the Product model based on the category received in the URL
    tableNo = request.GET.get('tableNo')
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no),table_no = tableNo)
    serializer = PosSalesOrderSerializer(paid, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_customer_list(request):
    customer = request.GET.get('customer')
    print('customer',customer)
    if customer:
        customers = Customer.objects.filter(trade_name__icontains=customer)[:30]
        serialized_data = CustomerSerializer(customers, many=True).data

        return Response({"customers": serialized_data})
    else:

        customers = Customer.objects.filter()[:30]
        serialized_data = CustomerSerializer(customers, many=True).data

        return Response({"customers": serialized_data})
    # else:
    #     return Response({"message": "No 'str' parameter provided"}, status=400)
    

@api_view(['GET'])
def get_waiter_list(request):
    waiter = request.GET.get('waiter')
    print('waiter',waiter)
    if waiter:
        waiters = PosWaiterList.objects.filter(waiter_name__icontains=waiter)
        serialized_data = PosWaiterListSerializer(waiters, many=True).data

        return Response({"waiter": serialized_data})
    else:
        waiters = PosWaiterList.objects.all()
        serialized_data = PosWaiterListSerializer(waiters, many=True).data

        return Response({"waiter": serialized_data})
        # return Response({"message": "No 'str' parameter provided"}, status=400)


@api_view(['GET'])  
def get_company_details(request):
    companyCode = getCompanyData()
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    data = []
    data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'TerminalNo':machineInfo.terminal_no,
        }
    
    return JsonResponse({'DataInfo':data}, status=200)


##*******************GET Bank Card *******************##

@api_view(['GET'])
def get_bank_card(request):
    if request.method =='GET':
        data = BankCard.objects.filter(active='Y')
        serialize = BankCardSerializer(data,many=True)
        return  Response(serialize.data) 
     
     
##*******************GET Bank Company *******************##

@api_view(['GET'])
def get_bank_list(request):
    if request.method =='GET':
        data = BankCompany.objects.filter(active='Y')
        serialize = BankCompanySerializer(data,many=True)
        return  Response(serialize.data) 
     
##**********GET TRANSACTION FOR REPRINT ********##
@api_view(['GET'])
def get_reprint_transaction(request):
    if request.method == 'GET':
        DateFrom = request.GET.get('datefrom')  # Get the 'datefrom' parameter
        DateTo = request.GET.get('dateto')      # Get the 'dateto' parameter
        TerminalNo = request.GET.get('TerminalNo')

        date_from = datetime.strptime(DateFrom, '%Y-%m-%d')
        date_to = datetime.strptime(DateTo, '%Y-%m-%d')     
        
        sale_invoice_list = PosSalesInvoiceList.objects.filter(
            doc_date__range=[date_from, date_to + timedelta(days=1)],
            terminal_no=TerminalNo
        )
        
        sale_invoice_list_data = []
        if sale_invoice_list:
            sale_invoice_list_data = PosSalesInvoiceListSerializer(sale_invoice_list, many=True).data
        
        return JsonResponse({'data': sale_invoice_list_data}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@api_view(['GET'])
def get_reprint_transaction_for_receipt(request):
    if request.method == 'GET':
        DocNo = request.GET.get('DocNo')  # Get the 'datefrom' parameter
        DocType = request.GET.get('DocType') 
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        list = PosSalesTransDetails.objects.filter(sales_trans_id=DocNo,terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
        listing = PosSalesTransDetailsSerializer(list,many=True).data
        companyCode = getCompanyData()
        
        sales_invoice = PosSalesInvoiceList.objects.filter(doc_no=DocNo,doc_type = DocType, terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no)).first()

        # if sales_invoice:
        #     print('xxxxx',sales_invoice.vat)
        # else:
        #     print("No sales invoice found.")
                
        data = []

        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':DocNo,
            'VAT': '{:,.2f}'.format(sales_invoice.vat),
            'VATable': '{:,.2f}'.format(sales_invoice.net_vat),
            'Discount': '{:,.2f}'.format(sales_invoice.discount),
            'VatExempt': '{:,.2f}'.format(sales_invoice.vat_exempted),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            # 'customer_code' : customer_code,
            # 'CustomerName' :CustomerName,
            # 'CusTIN' :CusTIN,
            # 'CusAddress' :CusAddress,
            # 'CusBusiness' : CusBusiness,
            # 'cust_type' : cust_type,
            'TerminalNo':machineInfo.terminal_no,
            # 'WaiterName':waiterName
        }
    
    return JsonResponse({'Data':listing,'DataInfo':data}, status=200)




##********** GET THE SO FROM tbl_inv_ref_no ********##
def get_sales_transaction_id(TerminalNo, DocType):
    
    try:
        inv_ref = InvRefNo.objects.get(description=DocType, terminalno=TerminalNo)
        if inv_ref.next_no > 0:
            intsales_trans_id = format(float(inv_ref.next_no) + 1, "000000")
            if inv_ref.reset_counter > 0:
                doc_type = doc_type + abc[inv_ref.reset_counter - 1]
        else:
            intsales_trans_id = '1'
            if inv_ref.reset_counter > 0:
                doc_type = doc_type + abc[inv_ref.reset_counter - 1]
    except InvRefNo.DoesNotExist:
        # If the record does not exist, create a new one
        InvRefNo.objects.create(description=DocType, terminalno=TerminalNo)
        intsales_trans_id = '1'
    
    return intsales_trans_id


##********** GET THE COMPANY DETAILS IN tbl_po********##

def getCompanyData():
    # first_autonum = CompanySetup.objects.values_list('autonum', flat=True).first()
    first_autonum = CompanySetup.objects.first()
    return first_autonum


###***************ADD SALES ORDER *******************
@api_view(['POST'])
def save_sales_order(request):
    if request.method == 'POST':
        waiter = ''
        waiterID = 0
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('data2')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
  
        customer = data_from_modal.get('Customer')
        guest_count = data_from_modal.get('GuestCount')
        waiterName = data_from_modal.get('Waiter')
        waiterID = data_from_modal.get('waiterID')
        payment_type = data_from_modal.get('PaymentType')
        QueNo = data_from_modal.get('QueNO')

        if table_no == '':
            table_no = 0
        
        # pdb.set_trace()
        try:
            rs = InvRefNo.objects.filter(description='POS SO', terminalno=TerminalNo).first()

            if rs:
                if float(rs.next_no) > 0:
                    so_no = "{:06d}".format(int(rs.next_no) + 1)
                    rs.next_no = int(rs.next_no) + 1  # Update next_no attribute
                    rs.save()  
                else:
                    so_no = "000001"
            else:
                # Create a new record if no matching record is found
                InvRefNo.objects.create(description='POS SO', terminalno=TerminalNo)
                so_no = "000001"

        except InvRefNo.DoesNotExist:
            # Handle exception if the InvRefNo model doesn't exist or other relevant error
            so_no = "000001"
       
        # current_datetime = timezone.now().astimezone(timezone.pytz.timezone('Asia/Manila'))
            # The above code is using the Python programming language to get the current date and time in the
            # local timezone. It is then formatting the datetime object into a string with the format
            # 'YYYY-MM-DD HH:MM:SS'.

        # current_datetime = timezone.now()
        
        current_datetime_utc = datetime.utcnow()

        # Set the target timezone to Asia/Manila
        target_timezone = pytz.timezone('Asia/Manila')

        # Convert UTC datetime to the Philippines timezone
        current_datetime = current_datetime_utc.replace(tzinfo=pytz.utc).astimezone(target_timezone)

        
        
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Convert the formatted string back to a datetime object
        formatted_datetime = datetime.strptime(datetime_stamp, '%Y-%m-%d %H:%M:%S')

        # Extracting date and time separately
        formatted_date = formatted_datetime.date()  # Extracts the date
        formatted_time = formatted_datetime.time()  # Extracts the time
        
        # min_sales_trans_id = PosSalesTransDetails.objects.aggregate(sales_trans_id=Min('sales_trans_id')).filter(document_type='SO')['sales_trans_id'] or 0
        

        # Retrieve the minimum sales_trans_id where document_type is 'SO'
        min_sales_trans_id_query = PosSalesTransDetails.objects.filter(document_type='SO').aggregate(min_sales_trans_id=Min('sales_trans_id'))

        # Extract the minimum sales_trans_id from the result or default to 0 if no record matches the filter
        min_sales_trans_id = min_sales_trans_id_query['min_sales_trans_id'] or 0

        min_sales_trans_id = abs(min_sales_trans_id)
        min_sales_trans_id += 1
        
        min_sales_trans_id =  min_sales_trans_id * -1
        
        min_details_id = PosSalesTransDetails.objects.aggregate(details_id=Max('details_id'))['details_id'] or 0
        
        min_details_id = min_details_id + 1
        
        line_no = 0 

        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        

        for item in cart_items:
            line_no += 1 
            quantity = item['quantity']
            description = item['description']
            price = item['price']
            barcode = item['barcode']
            
            SaveOrderToDetails = PosSalesTransDetails(
                sales_trans_id = min_sales_trans_id,
                datetime_stamp = datetime_stamp,
                document_type = 'SO',
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                details_id = min_details_id,
                line_no = line_no,
                barcode = barcode,
                alternate_code = '0',
                itemcode = barcode,
                description = description,
                price = price,
                quantity = quantity,
                item_disc = 0,
                desc_rate = '0',
                vat_ex = 0,
                price_override = 0,
                isnon_vat = 'NO',
                is_SC = 'NO',
                isvoid = 'NO',
                trans_type = 1,
                status = 'S',
                discounted_by = 'Hernanie D. Galigao Jr',
            )
             
            SaveOrderToDetails.save()
            
        # pdb.set_trace()
        SaveToSalesOrder = PosSalesOrder(
            SO_no = so_no,
            document_no = min_sales_trans_id,
            customer_type = 'W',
            customer_name = customer,
            table_no = table_no,
            q_no = QueNo,
            dinein_takeout = 'Dine In',
            guest_count = guest_count,
            waiter_id = int(waiterID),
            cashier_id = cashier_id,
            terminal_no = TerminalNo,
            site_code = int(machineInfo.site_no),
            date_trans = formatted_date ,
            time_trans = formatted_time ,
            paid = 'N',
            active = 'Y',
            
        )
        
        SaveToSalesOrder.save()
        
        SaveToPosSalesTrans = PosSalesTrans(
            login_record = 1,
            sales_trans_id = min_sales_trans_id,
            terminal_no = TerminalNo,
            site_code = int(machineInfo.site_no),
            cashier_id = cashier_id,
            datetime_stamp = datetime_stamp,
            bagger = waiter,
            sales_man = waiter,
            document_no = min_details_id,
            document_type = 'SO',
            isvoid = 'NO',
            issuspend = 'NO',
            isclosed = 'NO',
            trans_type = 1,
            prepared_by = cashier_id,
        )
        
        SaveToPosSalesTrans.save()
        
        UpdateINVRef = InvRefNo.objects.filter(description='POS SO').first()
        UpdateINVRef.next_no = so_no
        UpdateINVRef.save()
        
        data =[]

        data = {
            'documentno':min_sales_trans_id,
            'SO_NO':so_no,
            'TerminalNo':TerminalNo,
            
            
        }

        return JsonResponse({'SOdata': data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    
    
###************ CASH PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
def save_cash_payment(request):
    if request.method == 'POST':
 
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        
        DiscountType = received_data.get('DiscountType')
        DiscountData= received_data.get('DiscountData')
        QueNo= received_data.get('QueNo')
        doctype = received_data.get('doctype')
        doc_no = get_sales_transaction_id(TerminalNo,doctype)
        if table_no =='':
            table_no = 0
     
        
        
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        companyCode = getCompanyData()
        waiterName=''
 


        if data_from_modal.get('Customer') != '':
            if data_from_modal.get('customerType').upper() == "WALK-IN":
                try:
                    Payor = PosPayor.objects.get(payor_name=data_from_modal.get('Customer'))
                    customer_code = Payor.id_code
                    CustomerName = Payor.payor_name
                    CusTIN =Payor.tin
                    CusAddress =Payor.address
                    CusBusiness = Payor.business_style
                    cust_type = "P"
                except PosPayor.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN = ""
                    CusAddress = ""
                    CusBusiness = ""
            else:
                try:
                    customer = Customer.objects.get(trade_name=data_from_modal.get('Customer'))
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                    CusAddress = customer.st_address
                except Customer.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN =customer.tax_id_no
                    CusAddress =customer.st_address
                    CusBusiness = customer.business_style
                    
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
            

        disc_amt = 0
        desc_rate= 0
        vat_amt = 0
        vat_exempt = 0
        net_total = 0
        total_disc_amt = 0 ###for sales invoice list
        total_desc_rate= 0 ###for sales invoice list
        total_vat_amt = 0 ###for sales invoice list
        total_vat_exempt = 0 ###for sales invoice list
        total_net_total = 0 ###for sales invoice list
        total_sub_total = 0 ###for sales invoice list
        vatable = ''
        totalQty = 0
        desc_rate = 0

            
        

        for items in cart_items:
            productInfo = Product.objects.filter(bar_code=items['barcode']).first()

            if productInfo is not None:
                quantity = float(items['quantity'])
                price = float(items['price'])
                item_disc = float(items['item_disc'])
                total_sub_total = total_sub_total + (quantity * price)
                
                if DiscountType == 'SC':
                    vatable = 'Es'
                    desc_rate = 20
                    totalItem = quantity * price
                    
                    NetSale =  totalItem / (0.12 + 1 )
                    vat_exempt =  totalItem - NetSale
                    disc_amt  = (totalItem - vat_exempt ) * 0.2
                    net_total = (quantity * price) - (disc_amt + vat_exempt)
                    
                    print('NetSale',NetSale)
                    print('vat_exempt',vat_exempt)
                    print('disc_amt',disc_amt)
                    print('net_total',net_total)
                
                    
                else:
                    if productInfo.tax_code == 'VAT':
                        vatable = 'V'
                        desc_rate = item_disc / (quantity * price) * 100
                        vat_amt = (((quantity * price) - item_disc) / 1.12) * 0.12
                        net_total = (quantity * price) - item_disc - vat_amt
                    else:
                        vatable = 'N'
                        vat_amt = 0
                        disc_amt = item_disc
                        net_total = (quantity * price) - disc_amt
            else:
                # Handle case where productInfo is None (no product found for the barcode)
                pass  # You might want to log this or handle it according to your logic
                

            total_disc_amt = total_disc_amt + desc_rate
            total_desc_rate= total_desc_rate + desc_rate
            total_vat_amt = total_vat_amt + vat_amt

            if DiscountType == 'SC':
                total_vat_exempt = total_vat_exempt + net_total
                print('total_vat_exempt',total_vat_exempt)
            else:
                total_net_total = total_net_total + net_total
            
            # pdb.set_trace()
            totalQty = totalQty + float(items['quantity'])
            
            SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                doc_date = datetime_stamp,
                doc_no = doc_no,
                doc_type = 'POS-SI',
                line_number = items['line_no'],
                bar_code =items['barcode'],
                alternate_code = 0,
                item_code = items['barcode'],
                rec_qty = items['quantity'],
                rec_uom = productInfo.uom,
                description = items['description'],
                unit_price = items['price'],
                sub_total = float(items['quantity']) * float(items['price']),
                pc_price =  items['price'],
                qtyperuom = 1,
                disc_amt = f"{disc_amt:.3f}",
                desc_rate =f"{desc_rate:.3f}",
                vat_amt =  f"{vat_amt:.3f}",
                vat_exempt = f"{vat_exempt:.3f}",
                net_total =  f"{net_total:.3f}",
                isvoid = 'No',
                unit_cost = '0',
                vatable = vatable,
                status = 'A',
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                sn_bc = '',
                discounted_by = '',
                
            )
            SaveToPOSSalesInvoiceListing.save()

  
        net_vat = 0
        net_discount = 0
        vat_exempted = 0
        #### Take note of computation of net_vat and net_discount
        # pdb.set_trace()
        if DiscountType == 'SC':
            total_disc_amt = DiscountData['SLess20SCDiscount']
            net_vat = DiscountData['SDiscountedPrice']
            net_discount = DiscountData['SDiscountedPrice']
            vat_exempted = DiscountData['SLessVat12']
            
            
            
            
        else:   
            net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
            net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
        
        
        AmountDue_without_comma = AmountDue.replace(',', '')
        # Convert the modified string to a float
        AmountDue_float = float(AmountDue_without_comma)
        
        AmountDue_float = float(AmountDue_float)       
        AmountDue_formatted = f"{AmountDue_float:.3f}"

        print('cus-address',CusAddress)
        total_disc_amt = float(total_disc_amt)
        total_desc_rate = float(total_desc_rate)
        total_vat_exempt = float(total_vat_exempt)
        SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                site_code = int(machineInfo.site_no),
                trans_type = 'Cash Sales',
                discount_type = '',
                doc_no = doc_no,
                doc_type = 'POS-SI',
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                doc_date = datetime_stamp,
                customer_code = customer_code,
                customer_name = CustomerName,
                customer_address = CusAddress,
                business_unit = CusBusiness,
                customer_type = cust_type,
                salesman_id = '0',
                salesman = '',
                collector_id = '0',
                collector = '',
                pricing = '',
                terms = 0,
                remarks = '',
                ServiceCharge_TotalAmount = 0 ,
                total_cash =  AmountDue_formatted,
                total_qty = totalQty,
                discount = float(total_disc_amt),
                vat = float(total_vat_amt),
                vat_exempted = float(vat_exempted),
                net_vat = float(net_vat),
                net_discount = float(net_discount),
                sub_total = float(total_sub_total),
                # discount =  f"{total_disc_amt:.3f}" ,
                # vat = f"{total_vat_amt:.3f}",
                # vat_exempted =  f"{total_vat_exempt:.3f}",
                # net_vat = f"{net_vat:.3f}",
                # net_discount = f"{net_discount:.3f}",
                # sub_total = f"{total_sub_total:.3f}",
                lvl1_disc = '0',
                lvl2_disc = '0',
                lvl3_disc = '0',
                lvl4_disc = '0',
                lvl5_disc = '0',
                HMO = '',
                PHIC = '',
                status = 'S',
                prepared_id = cashier_id,
                prepared_by = CashierName,
                )
        
        SaveToPOSSalesInvoiceList.save()
        

        if OrderType == 'DINE IN':
            GetWaiterID = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    terminal_no=machineInfo.terminal_no,
                    site_code=int(machineInfo.site_no)
                ).first()
            if GetWaiterID:
                waiterID = GetWaiterID.waiter_id
                
                # Fetch waiter details if waiterID is available
                waiter_details = PosWaiterList.objects.filter(waiter_id=waiterID).first()
                
                if waiter_details:
                    waiterName = waiter_details.waiter_name
                    # Perform further operations with waiterName or other attributes
                else:
                    # Handle the case where waiter details are not found
                    waiterName = None  # or any default value or error handling
            else:
                # Handle the case where GetWaiterID is None (no matching record found)
                waiterID = None  # or any default value or error handling
                waiterName = None  # or any default value or error handling
        
            sales_orders_to_update = PosSalesOrder.objects.filter(
                table_no=table_no,
                paid='N',
                active='Y',
                terminal_no=TerminalNo,
                site_code=int(machineInfo.site_no)
            )

            # Check if there are any matching objects
            if sales_orders_to_update.exists():
                # Update all matching objects to set 'paid' to 'Y'
                sales_orders_to_update.update(paid='Y')
                
                pass

        UpdateINVRef = InvRefNo.objects.filter(description='POS SI',terminalno=TerminalNo).first()
        UpdateINVRef.next_no = doc_no
        UpdateINVRef.save()
  

        data = []
        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':doc_no,
            'VAT': '{:,.2f}'.format(total_vat_amt),
            'VATable': '{:,.2f}'.format(total_net_total),
            'Discount': '{:,.2f}'.format(total_disc_amt),
            'Discount_Rate': '{:,.2f}'.format(total_desc_rate),
            'VatExempt': '{:,.2f}'.format(total_vat_exempt),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            'customer_code' : customer_code,
            'CustomerName' :CustomerName,
            'CusTIN' :CusTIN,
            'CusAddress' :CusAddress,
            'CusBusiness' : CusBusiness,
            'cust_type' : cust_type,
            'TerminalNo':TerminalNo,
            'WaiterName':waiterName
        } 
    return Response({'data':data}, status=200)
        
        
###******************** CANCEL SALES ORDER    ***************************    
@api_view(['POST'])
def cancel_sales_order(request):
    if request.method == 'POST':
        tableno = request.data.get('params', {}).get('tableno')
        
        print('table',tableno)
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

        if not machineInfo:
            return Response({'message': 'Machine information not found'}, status=404)

        if not tableno:
            return Response({'message': 'Table number is required'}, status=400)

        paid_orders = PosSalesOrder.objects.filter(table_no=tableno,
            paid='N', active='Y', terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no)
        )

        if paid_orders.exists():
            paid_orders.update(active='N')
            return Response({'message': 'Sales orders canceled successfully'}, status=200)
        else:
            return Response({'message': 'No active unpaid orders found'}, status=404)
    else:
        return Response({'message': 'Invalid request method'}, status=405)
        

###*************** SAVE SALES ORDER ---TAKE OUT-----*******************
@api_view(['POST'])
def save_sales_order_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountTendered = received_data.get('AmountTendered')
        DiscountType = received_data.get('DiscountType')
        DiscountData= received_data.get('DiscountData')
        doctype = received_data.get('doctype')
        doc_no = get_sales_transaction_id(TerminalNo,doctype)
        print('doc_no',doc_no) 
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Convert the formatted string back to a datetime object
        formatted_datetime = datetime.strptime(datetime_stamp, '%Y-%m-%d %H:%M:%S')

        # Extracting date and time separately
        formatted_date = formatted_datetime.date()  # Extracts the date
        formatted_time = formatted_datetime.time()  # Extracts the time
        
        min_sales_trans_id = PosSalesTransDetails.objects.aggregate(sales_trans_id=Min('sales_trans_id'))['sales_trans_id'] or 0
        min_sales_trans_id = abs(min_sales_trans_id)
        min_sales_trans_id += 1
        
        min_sales_trans_id =  min_sales_trans_id * -1
        
        min_details_id = PosSalesTransDetails.objects.aggregate(details_id=Max('details_id'))['details_id'] or 0
        
        min_details_id = min_details_id + 1
        
        line_no = 0 

        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        Amt_Discount = 0
        # pdb.set_trace()
        for item in cart_items:
            line_no += 1 
            quantity = item['quantity']
            description = item['description']
            price = item['price']
            barcode = item['barcode']
            is_SC = 'NO'
            item_disc = 0
            desc_rate = 0
            vat_ex = 0
  
            
          
            
            if DiscountType == 'SC':
                Amt_Discount = DiscountData['SLess20SCDiscount']
                desc_rate = 20
                totalItem = quantity * price
                # print('price',price,'totalItem',totalItem,)
                # pdb.set_trace()
                NetSale =  float(totalItem) / (0.12 + 1 )
                vat_ex =  float(totalItem) - float(NetSale)
                item_disc  = (float(totalItem) - float(vat_ex) ) * 0.2
            
            SaveOrderToDetails = PosSalesTransDetails(
                sales_trans_id = float(doc_no),
                datetime_stamp = datetime_stamp,
                document_type = 'SI',
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                details_id = min_details_id,
                line_no = line_no,
                barcode = barcode,
                alternate_code = '0',
                itemcode = barcode,
                description = description,
                price = price,
                quantity = quantity,
                item_disc = item_disc,
                desc_rate = desc_rate,
                vat_ex = vat_ex,
                price_override = 0,
                isnon_vat = 'NO',
                is_SC = is_SC,
                isvoid = 'NO',
                trans_type = 1,
                status = 'S',
                discounted_by = 'Hernanie D. Galigao Jr',
            )
             
            SaveOrderToDetails.save()
            
            SaveToPosSalesTrans = PosSalesTrans(
            login_record = 1,
            sales_trans_id = min_sales_trans_id,
            terminal_no = TerminalNo,
            site_code = int(machineInfo.site_no),
            cashier_id = cashier_id,
            datetime_stamp = datetime_stamp,
            bagger = '',
            amount_tendered = AmountTendered,
            document_type = 'SI',
            amount_disc = Amt_Discount,
            lvl1_disc = 0,
            lvl2_disc= 0,
            lvl3_disc = 0,
            lvl4_disc = 0,
            lvl5_disc =0,
            vat_stamp =0,
            sales_man = '',
            document_no = 0,
            isvoid = 'NO',
            issuspend = 'NO',
            isclosed = 'NO',
            trans_type = 1,
            prepared_by = cashier_id,
        )
        
        SaveToPosSalesTrans.save()
        
        
        sales_details = PosSalesTransDetails.objects.filter(sales_trans_id=float(doc_no),  terminal_no = TerminalNo,  site_code =  int(machineInfo.site_no),document_type='SI')
        sales_details_data = PosSalesTransDetailsSerializer(sales_details, many=True).data
        
        return JsonResponse({'data':sales_details_data}, status=200)


        # return JsonResponse( status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


###************ CREDIT CARD PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
def save_credit_card_payment2(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        doc_no = get_sales_transaction_id(TerminalNo,'POS SI')
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        companyCode = getCompanyData()
        waiterName=''
        bankID = ''
        BankName = ''
 


        if data_from_modal.get('Customer') != '':
            if data_from_modal.get('customerType').upper() == "WALK-IN":
                try:
                    Payor = PosPayor.objects.get(payor_name=data_from_modal.get('Customer'))
                    customer_code = Payor.id_code
                    CustomerName = Payor.payor_name
                    CusTIN =Payor.tin
                    CusAddress =Payor.address
                    CusBusiness = Payor.business_style
                    cust_type = "P"
                except PosPayor.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN = ""
                    CusAddress = ""
                    CusBusiness = ""
            else:
                try:
                    customer = Customer.objects.get(trade_name=data_from_modal.get('Customer'))
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                except Customer.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN =customer.tax_id_no
                    CusAddress =customer.st_address
                    CusBusiness = customer.business_style
                    
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
            

        disc_amt = 0
        desc_rate= 0
        vat_amt = 0
        vat_exempt = 0
        net_total = 0
        total_disc_amt = 0 ###for sales invoice list
        total_desc_rate= 0 ###for sales invoice list
        total_vat_amt = 0 ###for sales invoice list
        total_vat_exempt = 0 ###for sales invoice list
        total_net_total = 0 ###for sales invoice list
        total_sub_total = 0 ###for sales invoice list
        vatable = ''
        totalQty = 0

        for items in cart_items:
            productInfo = Product.objects.filter(bar_code=items['barcode']).first()

            if productInfo is not None:
                quantity = float(items['quantity'])
                price = float(items['price'])
                item_disc = float(items['item_disc'])
                total_sub_total = total_sub_total + (quantity * price)
                if productInfo.tax_code == 'VAT':
                    vatable = 'V'
                    desc_rate = item_disc / (quantity * price) * 100
                    vat_amt = (((quantity * price) - item_disc) / 1.12) * 0.12
                    net_total = (quantity * price) - item_disc - vat_amt
                else:
                    vatable = 'N'
                    vat_amt = 0
                    disc_amt = item_disc
                    net_total = (quantity * price) - disc_amt
            else:
                # Handle case where productInfo is None (no product found for the barcode)
                pass  # You might want to log this or handle it according to your logic
                

            total_disc_amt = total_disc_amt + desc_rate
            total_desc_rate= total_desc_rate + desc_rate
            total_vat_amt = total_vat_amt + vat_amt
            total_vat_exempt = 0
            total_net_total = total_net_total + net_total
            totalQty = totalQty + float(items['quantity'])
            
            SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                doc_date = datetime_stamp,
                doc_no = doc_no,
                doc_type = 'POS-SI',
                line_number = items['line_no'],
                bar_code =items['barcode'],
                alternate_code = 0,
                item_code = items['barcode'],
                rec_qty = items['quantity'],
                rec_uom = productInfo.uom,
                description = items['description'],
                unit_price = items['price'],
                sub_total = float(items['quantity']) * float(items['price']),
                pc_price =  items['price'],
                qtyperuom = 1,
                disc_amt = f"{disc_amt:.3f}",
                desc_rate =f"{desc_rate:.3f}",
                vat_amt =  f"{vat_amt:.3f}",
                vat_exempt = f"{vat_exempt:.3f}",
                net_total =  f"{net_total:.3f}",
                isvoid = 'No',
                unit_cost = '0',
                vatable = vatable,
                status = 'A',
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                sn_bc = '',
                discounted_by = '',
                
            )
            SaveToPOSSalesInvoiceListing.save()

        net_vat = 0
        net_discount = 0
        #### Take note of computation of net_vat and net_discount
        net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
        net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
        
        
        AmountDue_without_comma = AmountDue.replace(',', '')
        # Convert the modified string to a float
        AmountDue_float = float(AmountDue_without_comma)
        
        AmountDue_float = float(AmountDue_float)       
        AmountDue_formatted = f"{AmountDue_float:.3f}"


        
        SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                site_code = int(machineInfo.site_no),
                trans_type = 'Cash Sales',
                discount_type = '',
                doc_no = doc_no,
                doc_type = 'POS-SI',
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                doc_date = datetime_stamp,
                customer_code = customer_code,
                customer_name = CustomerName,
                customer_address = CusAddress,
                business_unit = CusBusiness,
                customer_type = cust_type,
                salesman_id = '0',
                salesman = '',
                collector_id = '0',
                collector = '',
                pricing = '',
                terms = 0,
                remarks = '',
                ServiceCharge_TotalAmount = 0 ,
                total_cash =  AmountDue_formatted,
                total_qty = totalQty,
                discount =  f"{total_disc_amt:.3f}" ,
                vat = f"{total_vat_amt:.3f}",
                vat_exempted =  f"{total_vat_exempt:.3f}",
                net_vat = f"{net_vat:.3f}",
                net_discount = f"{net_discount:.3f}",
                sub_total = f"{total_sub_total:.3f}",
                lvl1_disc = '0',
                lvl2_disc = '0',
                lvl3_disc = '0',
                lvl4_disc = '0',
                lvl5_disc = '0',
                HMO = '',
                PHIC = '',
                status = 'S',
                prepared_id = cashier_id,
                prepared_by = CashierName,
                )
        
        SaveToPOSSalesInvoiceList.save()
        

        if OrderType == 'DINE IN':
            GetWaiterID = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    terminal_no=machineInfo.terminal_no,
                    site_code=int(machineInfo.site_no)
                ).first()
            if GetWaiterID:
                waiterID = GetWaiterID.waiter_id
                
                # Fetch waiter details if waiterID is available
                waiter_details = PosWaiterList.objects.filter(waiter_id=waiterID).first()
                
                if waiter_details:
                    waiterName = waiter_details.waiter_name
                    # Perform further operations with waiterName or other attributes
                else:
                    # Handle the case where waiter details are not found
                    waiterName = None  # or any default value or error handling
            else:
                # Handle the case where GetWaiterID is None (no matching record found)
                waiterID = None  # or any default value or error handling
                waiterName = None  # or any default value or error handling
        
            sales_orders_to_update = PosSalesOrder.objects.filter(
                table_no=table_no,
                paid='N',
                active='Y',
                terminal_no=TerminalNo,
                site_code=int(machineInfo.site_no)
            )

            # Check if there are any matching objects
            if sales_orders_to_update.exists():
                # Update all matching objects to set 'paid' to 'Y'
                sales_orders_to_update.update(paid='Y')
                
                pass

        UpdateINVRef = InvRefNo.objects.filter(description='POS SI',terminalno=TerminalNo).first()
        UpdateINVRef.next_no = doc_no
        UpdateINVRef.save()
        
        data = []
        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':doc_no,
            'VAT': '{:,.2f}'.format(total_vat_amt),
            'VATable': '{:,.2f}'.format(total_net_total),
            'Discount': '{:,.2f}'.format(total_disc_amt),
            'Discount_Rate': '{:,.2f}'.format(total_desc_rate),
            'VatExempt': '{:,.2f}'.format(total_vat_exempt),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            'customer_code' : customer_code,
            'CustomerName' :CustomerName,
            'CusTIN' :CusTIN,
            'CusAddress' :CusAddress,
            'CusBusiness' : CusBusiness,
            'cust_type' : cust_type,
            'TerminalNo':TerminalNo,
            'WaiterName':waiterName
        } 
    return Response({'data':data}, status=200)
##************ CREDIT CARD PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
def save_credit_card_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        # doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
        DiscountType = received_data.get('DiscountType')
        DiscountData= received_data.get('DiscountData')
        QueNo= received_data.get('QueNo')
        CreditCard = received_data.get('CreditCard')
        doctype = received_data.get('doctype')
        doc_no = get_sales_transaction_id(TerminalNo,doctype)
        # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")

        bankID = ''
        BankName = ''


        last_details_id = 0
        try:
            # Get the last details_id
            last_record = SalesTransCreditCard.objects.latest('details_id')
            last_details_id = last_record.details_id
        except ObjectDoesNotExist:
            # Handle the case where no records exist
            last_details_id = 0  # Assuming you want to start from 1, not 0

        # Increment the last_details_id by 1
        new_details_id = last_details_id + 1

        
        credit_card_payments = CreditCard['CreditCardPaymentList']
        for payment in credit_card_payments:
            card_no = payment['CardNo']
            acquire_bank = payment['AcquireBank']
            card_issuer = payment['CardIssuer']
            card_holder = payment['CardHolder']
            approval_no = payment['ApprovalNo']
            expiry_month = payment['ExpiryMonth']
            expiry_year = payment['ExpiryYear']
            amount_due = payment['AmountDue']

            # Format the datetime object as "January 1, 2024"
            expiry_date = datetime(int(expiry_year), int(expiry_month), 1)
            formatted_expiry_date = expiry_date.strftime("%B %d, %Y")

            bank_query = BankCompany.objects.filter(company_description=acquire_bank)
            bank_id_code=0

            # If a bank with the given description exists, get its id_code
            if bank_query.exists():
                bank_object = bank_query.first()  # Get the first matching bank object
                bank_id_code = bank_object.id_code
            else:
                # Handle the case where no bank with the given description exists
                bank_id_code = 0

            bankID = str(bank_id_code) + str(bankID)
            BankName = acquire_bank + ',' + BankName
            save_creditcardSales = SalesTransCreditCard (
                sales_trans_id = int(float(doc_no)),
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                document_type = 'SI',
                details_id = new_details_id,
                card_no=card_no,
                card_name = card_issuer,
                bank = bank_id_code,
                card_holder = card_holder,
                approval_no = approval_no,
                amount = amount_due,
                expiry_date = formatted_expiry_date,
            )

            save_creditcardSales.save()


        if table_no =='':
            table_no = 0
     
        
        
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        companyCode = getCompanyData()
        waiterName=''
 


        if data_from_modal.get('Customer') != '':
            if data_from_modal.get('customerType').upper() == "WALK-IN":
                try:
                    Payor = PosPayor.objects.get(payor_name=data_from_modal.get('Customer'))
                    customer_code = Payor.id_code
                    CustomerName = Payor.payor_name
                    CusTIN =Payor.tin
                    CusAddress =Payor.address
                    CusBusiness = Payor.business_style
                    cust_type = "P"
                except PosPayor.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN = ""
                    CusAddress = ""
                    CusBusiness = ""
            else:
                try:
                    customer = Customer.objects.get(trade_name=data_from_modal.get('Customer'))
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                    CusAddress = customer.st_address
                except Customer.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN =customer.tax_id_no
                    CusAddress =customer.st_address
                    CusBusiness = customer.business_style
                    
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
            

        disc_amt = 0
        desc_rate= 0
        vat_amt = 0
        vat_exempt = 0
        net_total = 0
        total_disc_amt = 0 ###for sales invoice list
        total_desc_rate= 0 ###for sales invoice list
        total_vat_amt = 0 ###for sales invoice list
        total_vat_exempt = 0 ###for sales invoice list
        total_net_total = 0 ###for sales invoice list
        total_sub_total = 0 ###for sales invoice list
        vatable = ''
        totalQty = 0
        desc_rate = 0

            
        
        print('cart_items',cart_items)
        for items in cart_items:
            productInfo = Product.objects.filter(bar_code=items['barcode']).first()

            if productInfo is not None:
                quantity = float(items['quantity'])
                price = float(items['price'])
                item_disc = float(items['item_disc'])
                total_sub_total = total_sub_total + (quantity * price)
                
                if DiscountType == 'SC':
                    vatable = 'Es'
                    desc_rate = 20
                    totalItem = quantity * price
                    
                    NetSale =  totalItem / (0.12 + 1 )
                    vat_exempt =  totalItem - NetSale
                    disc_amt  = (totalItem - vat_exempt ) * 0.2
                    net_total = (quantity * price) - (disc_amt + vat_exempt)
                    
                    print('NetSale',NetSale)
                    print('vat_exempt',vat_exempt)
                    print('disc_amt',disc_amt)
                    print('net_total',net_total)
                
                    
                else:
                    if productInfo.tax_code == 'VAT':
                        vatable = 'V'
                        desc_rate = item_disc / (quantity * price) * 100
                        vat_amt = (((quantity * price) - item_disc) / 1.12) * 0.12
                        net_total = (quantity * price) - item_disc - vat_amt
                    else:
                        vatable = 'N'
                        vat_amt = 0
                        disc_amt = item_disc
                        net_total = (quantity * price) - disc_amt
            else:
                # Handle case where productInfo is None (no product found for the barcode)
                pass  # You might want to log this or handle it according to your logic
                

            total_disc_amt = total_disc_amt + desc_rate
            total_desc_rate= total_desc_rate + desc_rate
            total_vat_amt = total_vat_amt + vat_amt

            if DiscountType == 'SC':
                total_vat_exempt = total_vat_exempt + net_total
                print('total_vat_exempt',total_vat_exempt)
            else:
                total_net_total = total_net_total + net_total
            
            # pdb.set_trace()
            totalQty = totalQty + float(items['quantity'])
            
            SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                doc_date = datetime_stamp,
                doc_no = doc_no,
                doc_type = 'POS-CI',
                line_number = items['line_no'],
                bar_code =items['barcode'],
                alternate_code = 0,
                item_code = items['barcode'],
                rec_qty = items['quantity'],
                rec_uom = productInfo.uom,
                description = items['description'],
                unit_price = items['price'],
                sub_total = float(items['quantity']) * float(items['price']),
                pc_price =  items['price'],
                qtyperuom = 1,
                disc_amt = f"{disc_amt:.3f}",
                desc_rate =f"{desc_rate:.3f}",
                vat_amt =  f"{vat_amt:.3f}",
                vat_exempt = f"{vat_exempt:.3f}",
                net_total =  f"{net_total:.3f}",
                isvoid = 'No',
                unit_cost = '0',
                vatable = vatable,
                status = 'A',
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                sn_bc = '',
                discounted_by = '',
                
            )
            SaveToPOSSalesInvoiceListing.save()

  
        net_vat = 0
        net_discount = 0
        vat_exempted = 0
        #### Take note of computation of net_vat and net_discount
        # pdb.set_trace()
        if DiscountType == 'SC':
            total_disc_amt = DiscountData['SLess20SCDiscount']
            net_vat = DiscountData['SDiscountedPrice']
            net_discount = DiscountData['SDiscountedPrice']
            vat_exempted = DiscountData['SLessVat12']
            
            
            
            
        else:   
            net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
            net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
        
        
        AmountDue_without_comma = AmountDue.replace(',', '')
        # Convert the modified string to a float
        AmountDue_float = float(AmountDue_without_comma)
        
        AmountDue_float = float(AmountDue_float)       
        AmountDue_formatted = f"{AmountDue_float:.3f}"

        print('cus-address',CusAddress)
        # pdb.set_trace()
        total_disc_amt = float(total_disc_amt)
        total_desc_rate = float(total_desc_rate)
        total_vat_exempt = float(total_vat_exempt)
        SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                site_code = int(machineInfo.site_no),
                trans_type = 'Credit Sales',
                discount_type = '',
                doc_no = doc_no,
                doc_type = 'POS-CI',
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                doc_date = datetime_stamp,
                customer_code = customer_code,
                customer_name = CustomerName,
                customer_address = CusAddress,
                business_unit = CusBusiness,
                customer_type = cust_type,
                salesman_id = '0',
                salesman = '',
                collector_id = bankID,
                collector = BankName,
                pricing = '',
                terms = 0,
                remarks = '',
                ServiceCharge_TotalAmount = 0 ,
                total_credit_card =  AmountDue_formatted,
                total_qty = totalQty,
                discount = float(total_disc_amt),
                vat = float(total_vat_amt),
                vat_exempted = float(vat_exempted),
                net_vat = float(net_vat),
                net_discount = float(net_discount),
                sub_total = float(total_sub_total),
                # discount =  f"{total_disc_amt:.3f}" ,
                # vat = f"{total_vat_amt:.3f}",
                # vat_exempted =  f"{total_vat_exempt:.3f}",
                # net_vat = f"{net_vat:.3f}",
                # net_discount = f"{net_discount:.3f}",
                # sub_total = f"{total_sub_total:.3f}",
                lvl1_disc = '0',
                lvl2_disc = '0',
                lvl3_disc = '0',
                lvl4_disc = '0',
                lvl5_disc = '0',
                HMO = '',
                PHIC = '',
                status = 'S',
                prepared_id = cashier_id,
                prepared_by = CashierName,
                )
        
        SaveToPOSSalesInvoiceList.save()
        

        if OrderType == 'DINE IN':
            GetWaiterID = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    terminal_no=machineInfo.terminal_no,
                    site_code=int(machineInfo.site_no)
                ).first()
            if GetWaiterID:
                waiterID = GetWaiterID.waiter_id
                
                # Fetch waiter details if waiterID is available
                waiter_details = PosWaiterList.objects.filter(waiter_id=waiterID).first()
                
                if waiter_details:
                    waiterName = waiter_details.waiter_name
                    # Perform further operations with waiterName or other attributes
                else:
                    # Handle the case where waiter details are not found
                    waiterName = None  # or any default value or error handling
            else:
                # Handle the case where GetWaiterID is None (no matching record found)
                waiterID = None  # or any default value or error handling
                waiterName = None  # or any default value or error handling
        
            sales_orders_to_update = PosSalesOrder.objects.filter(
                table_no=table_no,
                paid='N',
                active='Y',
                terminal_no=TerminalNo,
                site_code=int(machineInfo.site_no)
            )

            # Check if there are any matching objects
            if sales_orders_to_update.exists():
                # Update all matching objects to set 'paid' to 'Y'
                sales_orders_to_update.update(paid='Y')
                
                pass

        UpdateINVRef = InvRefNo.objects.filter(description='POS CI',terminalno=TerminalNo).first()
        UpdateINVRef.next_no = doc_no
        UpdateINVRef.save()
  

        data = []
        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':doc_no,
            'VAT': '{:,.2f}'.format(total_vat_amt),
            'VATable': '{:,.2f}'.format(total_net_total),
            'Discount': '{:,.2f}'.format(total_disc_amt),
            'Discount_Rate': '{:,.2f}'.format(total_desc_rate),
            'VatExempt': '{:,.2f}'.format(total_vat_exempt),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            'customer_code' : customer_code,
            'CustomerName' :CustomerName,
            'CusTIN' :CusTIN,
            'CusAddress' :CusAddress,
            'CusBusiness' : CusBusiness,
            'cust_type' : cust_type,
            'TerminalNo':TerminalNo,
            'WaiterName':waiterName,
            'CreditcardData':credit_card_payments
        } 
    return Response({'data':data}, status=200)
              
##************ DEBIT CARD  OR EPS PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
def save_debit_card_payment(request):
    if request.method == 'POST':
        
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        # doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
        DiscountType = received_data.get('DiscountType')
        DiscountData= received_data.get('DiscountData')
        QueNo= received_data.get('QueNo')
        DebitCard = received_data.get('DebitCard')
        doctype = received_data.get('doctype')
        doc_no = get_sales_transaction_id(TerminalNo,doctype)
        # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
        bankID = ''
        BankName = ''

        last_details_id = 0
        try:
            # Get the last details_id
            last_record = SalesTransEPS.objects.latest('details_id')
            last_details_id = last_record.details_id
        except ObjectDoesNotExist:
            # Handle the case where no records exist
            last_details_id = 0  # Assuming you want to start from 1, not 0

        # Increment the last_details_id by 1
        new_details_id = last_details_id + 1

        
        debit_card_payments = DebitCard['DebitCardPaymentList']
        for payment in debit_card_payments:
            card_no = payment['CardNo']
            acquire_bank = payment['AcquireBank']
            card_holder = payment['CardHolder']
            approval_no = payment['ApprovalNo']
            amount_due = payment['AmountDue']

            bank_query = BankCompany.objects.filter(company_description=acquire_bank)
            bank_id_code=0

            # If a bank with the given description exists, get its id_code
            if bank_query.exists():
                bank_object = bank_query.first()  # Get the first matching bank object
                bank_id_code = bank_object.id_code
            else:
                # Handle the case where no bank with the given description exists
                bank_id_code = 0
            # pdb.set_trace()
            bankID = str(bank_id_code) + str(bankID)
            BankName = acquire_bank + ',' + BankName
            save_debitcardSales = SalesTransEPS (
                sales_trans_id = int(float(doc_no)),
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                document_type = 'SI',
                details_id = new_details_id,
                card_no=card_no,
                bank = bank_id_code,
                card_holder = card_holder,
                approval_no = approval_no,
                amount = amount_due
            )

            save_debitcardSales.save()


        if table_no =='':
            table_no = 0
     
        
        
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        companyCode = getCompanyData()
        waiterName=''
 


        if data_from_modal.get('Customer') != '':
            if data_from_modal.get('customerType').upper() == "WALK-IN":
                try:
                    Payor = PosPayor.objects.get(payor_name=data_from_modal.get('Customer'))
                    customer_code = Payor.id_code
                    CustomerName = Payor.payor_name
                    CusTIN =Payor.tin
                    CusAddress =Payor.address
                    CusBusiness = Payor.business_style
                    cust_type = "P"
                except PosPayor.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN = ""
                    CusAddress = ""
                    CusBusiness = ""
            else:
                try:
                    customer = Customer.objects.get(trade_name=data_from_modal.get('Customer'))
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                    CusAddress = customer.st_address
                except Customer.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN =customer.tax_id_no
                    CusAddress =customer.st_address
                    CusBusiness = customer.business_style
                    
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
            

        disc_amt = 0
        desc_rate= 0
        vat_amt = 0
        vat_exempt = 0
        net_total = 0
        total_disc_amt = 0 ###for sales invoice list
        total_desc_rate= 0 ###for sales invoice list
        total_vat_amt = 0 ###for sales invoice list
        total_vat_exempt = 0 ###for sales invoice list
        total_net_total = 0 ###for sales invoice list
        total_sub_total = 0 ###for sales invoice list
        vatable = ''
        totalQty = 0
        desc_rate = 0

            
        

        for items in cart_items:
            productInfo = Product.objects.filter(bar_code=items['barcode']).first()

            if productInfo is not None:
                quantity = float(items['quantity'])
                price = float(items['price'])
                item_disc = float(items['item_disc'])
                total_sub_total = total_sub_total + (quantity * price)
                
                if DiscountType == 'SC':
                    vatable = 'Es'
                    desc_rate = 20
                    totalItem = quantity * price
                    
                    NetSale =  totalItem / (0.12 + 1 )
                    vat_exempt =  totalItem - NetSale
                    disc_amt  = (totalItem - vat_exempt ) * 0.2
                    net_total = (quantity * price) - (disc_amt + vat_exempt)
                    
                    print('NetSale',NetSale)
                    print('vat_exempt',vat_exempt)
                    print('disc_amt',disc_amt)
                    print('net_total',net_total)
                
                    
                else:
                    if productInfo.tax_code == 'VAT':
                        vatable = 'V'
                        desc_rate = item_disc / (quantity * price) * 100
                        vat_amt = (((quantity * price) - item_disc) / 1.12) * 0.12
                        net_total = (quantity * price) - item_disc - vat_amt
                    else:
                        vatable = 'N'
                        vat_amt = 0
                        disc_amt = item_disc
                        net_total = (quantity * price) - disc_amt
            else:
                # Handle case where productInfo is None (no product found for the barcode)
                pass  # You might want to log this or handle it according to your logic
                

            total_disc_amt = total_disc_amt + desc_rate
            total_desc_rate= total_desc_rate + desc_rate
            total_vat_amt = total_vat_amt + vat_amt

            if DiscountType == 'SC':
                total_vat_exempt = total_vat_exempt + net_total
                print('total_vat_exempt',total_vat_exempt)
            else:
                total_net_total = total_net_total + net_total
            
            # pdb.set_trace()
            totalQty = totalQty + float(items['quantity'])
            
            SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                doc_date = datetime_stamp,
                doc_no = doc_no,
                doc_type = 'POS-CI',
                line_number = items['line_no'],
                bar_code =items['barcode'],
                alternate_code = 0,
                item_code = items['barcode'],
                rec_qty = items['quantity'],
                rec_uom = productInfo.uom,
                description = items['description'],
                unit_price = items['price'],
                sub_total = float(items['quantity']) * float(items['price']),
                pc_price =  items['price'],
                qtyperuom = 1,
                disc_amt = f"{disc_amt:.3f}",
                desc_rate =f"{desc_rate:.3f}",
                vat_amt =  f"{vat_amt:.3f}",
                vat_exempt = f"{vat_exempt:.3f}",
                net_total =  f"{net_total:.3f}",
                isvoid = 'No',
                unit_cost = '0',
                vatable = vatable,
                status = 'A',
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                sn_bc = '',
                discounted_by = '',
                
            )
            SaveToPOSSalesInvoiceListing.save()

  
        net_vat = 0
        net_discount = 0
        vat_exempted = 0
        #### Take note of computation of net_vat and net_discount
        # pdb.set_trace()
        if DiscountType == 'SC':
            total_disc_amt = DiscountData['SLess20SCDiscount']
            net_vat = DiscountData['SDiscountedPrice']
            net_discount = DiscountData['SDiscountedPrice']
            vat_exempted = DiscountData['SLessVat12']
            
            
            
            
        else:   
            net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
            net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
        
        
        AmountDue_without_comma = AmountDue.replace(',', '')
        # Convert the modified string to a float
        AmountDue_float = float(AmountDue_without_comma)
        
        AmountDue_float = float(AmountDue_float)       
        AmountDue_formatted = f"{AmountDue_float:.3f}"

        print('cus-address',CusAddress)
        total_disc_amt = float(total_disc_amt)
        total_desc_rate = float(total_desc_rate)
        total_vat_exempt = float(total_vat_exempt)
        SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                site_code = int(machineInfo.site_no),
                trans_type = 'Credit Sales',
                discount_type = '',
                doc_no = doc_no,
                doc_type = 'POS-CI',
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                doc_date = datetime_stamp,
                customer_code = customer_code,
                customer_name = CustomerName,
                customer_address = CusAddress,
                business_unit = CusBusiness,
                customer_type = cust_type,
                salesman_id = '0',
                salesman = '',
                collector_id = bankID,
                collector = BankName,
                pricing = '',
                terms = 0,
                remarks = '',
                ServiceCharge_TotalAmount = 0 ,
                total_eps =  AmountDue_formatted,
                total_qty = totalQty,
                discount = float(total_disc_amt),
                vat = float(total_vat_amt),
                vat_exempted = float(vat_exempted),
                net_vat = float(net_vat),
                net_discount = float(net_discount),
                sub_total = float(total_sub_total),
                # discount =  f"{total_disc_amt:.3f}" ,
                # vat = f"{total_vat_amt:.3f}",
                # vat_exempted =  f"{total_vat_exempt:.3f}",
                # net_vat = f"{net_vat:.3f}",
                # net_discount = f"{net_discount:.3f}",
                # sub_total = f"{total_sub_total:.3f}",
                lvl1_disc = '0',
                lvl2_disc = '0',
                lvl3_disc = '0',
                lvl4_disc = '0',
                lvl5_disc = '0',
                HMO = '',
                PHIC = '',
                status = 'S',
                prepared_id = cashier_id,
                prepared_by = CashierName,
                )
        
        SaveToPOSSalesInvoiceList.save()
        

        if OrderType == 'DINE IN':
            GetWaiterID = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    terminal_no=machineInfo.terminal_no,
                    site_code=int(machineInfo.site_no)
                ).first()
            if GetWaiterID:
                waiterID = GetWaiterID.waiter_id
                
                # Fetch waiter details if waiterID is available
                waiter_details = PosWaiterList.objects.filter(waiter_id=waiterID).first()
                
                if waiter_details:
                    waiterName = waiter_details.waiter_name
                    # Perform further operations with waiterName or other attributes
                else:
                    # Handle the case where waiter details are not found
                    waiterName = None  # or any default value or error handling
            else:
                # Handle the case where GetWaiterID is None (no matching record found)
                waiterID = None  # or any default value or error handling
                waiterName = None  # or any default value or error handling
        
            sales_orders_to_update = PosSalesOrder.objects.filter(
                table_no=table_no,
                paid='N',
                active='Y',
                terminal_no=TerminalNo,
                site_code=int(machineInfo.site_no)
            )

            # Check if there are any matching objects
            if sales_orders_to_update.exists():
                # Update all matching objects to set 'paid' to 'Y'
                sales_orders_to_update.update(paid='Y')
                
                pass

        UpdateINVRef = InvRefNo.objects.filter(description='POS CI',terminalno=TerminalNo).first()
        UpdateINVRef.next_no = doc_no
        UpdateINVRef.save()
  

        data = []
        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':doc_no,
            'VAT': '{:,.2f}'.format(total_vat_amt),
            'VATable': '{:,.2f}'.format(total_net_total),
            'Discount': '{:,.2f}'.format(total_disc_amt),
            'Discount_Rate': '{:,.2f}'.format(total_desc_rate),
            'VatExempt': '{:,.2f}'.format(total_vat_exempt),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            'customer_code' : customer_code,
            'CustomerName' :CustomerName,
            'CusTIN' :CusTIN,
            'CusAddress' :CusAddress,
            'CusBusiness' : CusBusiness,
            'cust_type' : cust_type,
            'TerminalNo':TerminalNo,
            'WaiterName':waiterName,
            'DebitcardData':debit_card_payments
        } 
    return Response({'data':data}, status=200)
     
##************ Multiple PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
def save_multiple_payment(request):
    if request.method == 'POST':
        
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
        DiscountType = received_data.get('DiscountType')
        DiscountData= received_data.get('DiscountData')
        QueNo= received_data.get('QueNo')
        DebitCard = received_data.get('DebitCard')
        CreditCard = received_data.get('CreditCard')
        CashAmount = received_data.get('CashAmount')
        doctype = received_data.get('doctype')
        doc_no = get_sales_transaction_id(TerminalNo,doctype)
        # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
        bankID = ''
        BankName = ''
        CreditCardAmount = 0
        DebitCardAmount = 0
        credit_card_payments = ''
        debit_card_payments = ''
        if CreditCard:
            last_details_id = 0
            try:
                # Get the last details_id
                last_record = SalesTransCreditCard.objects.latest('details_id')
                last_details_id = last_record.details_id
            except ObjectDoesNotExist:
                # Handle the case where no records exist
                last_details_id = 0  # Assuming you want to start from 1, not 0

            # Increment the last_details_id by 1
            new_details_id = last_details_id + 1

            
            credit_card_payments = CreditCard['CreditCardPaymentList']
            for payment in credit_card_payments:
                card_no = payment['CardNo']
                acquire_bank = payment['AcquireBank']
                card_issuer = payment['CardIssuer']
                card_holder = payment['CardHolder']
                approval_no = payment['ApprovalNo']
                expiry_month = payment['ExpiryMonth']
                expiry_year = payment['ExpiryYear']
                amount_due = payment['AmountDue']


                CreditCardAmount = float(amount_due) + float(CreditCardAmount)
                # Format the datetime object as "January 1, 2024"
                expiry_date = datetime(int(expiry_year), int(expiry_month), 1)
                formatted_expiry_date = expiry_date.strftime("%B %d, %Y")

                bank_query = BankCompany.objects.filter(company_description=acquire_bank)
                bank_id_code=0

                # If a bank with the given description exists, get its id_code
                if bank_query.exists():
                    bank_object = bank_query.first()  # Get the first matching bank object
                    bank_id_code = bank_object.id_code
                else:
                    # Handle the case where no bank with the given description exists
                    bank_id_code = 0
                bankID = str(bank_id_code) + str(bankID)
                BankName = acquire_bank + ',' + BankName
                save_creditcardSales = SalesTransCreditCard (
                    sales_trans_id = int(float(doc_no)),
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    document_type = 'SI',
                    details_id = new_details_id,
                    card_no=card_no,
                    card_name = card_issuer,
                    bank = bank_id_code,
                    card_holder = card_holder,
                    approval_no = approval_no,
                    amount = amount_due,
                    expiry_date = formatted_expiry_date,
                )

                save_creditcardSales.save()



        if DebitCard:
            last_details_id = 0
            try:
                # Get the last details_id
                last_record = SalesTransEPS.objects.latest('details_id')
                last_details_id = last_record.details_id
            except ObjectDoesNotExist:
                # Handle the case where no records exist
                last_details_id = 0  # Assuming you want to start from 1, not 0

            # Increment the last_details_id by 1
            new_details_id = last_details_id + 1

            
            debit_card_payments = DebitCard['DebitCardPaymentList']
            for payment in debit_card_payments:
                card_no = payment['CardNo']
                acquire_bank = payment['AcquireBank']
                card_holder = payment['CardHolder']
                approval_no = payment['ApprovalNo']
                amount_due = payment['AmountDue']
                DebitCardAmount = float(amount_due) + float(DebitCardAmount)

                bank_query = BankCompany.objects.filter(company_description=acquire_bank)
                bank_id_code=0

                # If a bank with the given description exists, get its id_code
                if bank_query.exists():
                    bank_object = bank_query.first()  # Get the first matching bank object
                    bank_id_code = bank_object.id_code
                else:
                    # Handle the case where no bank with the given description exists
                    bank_id_code = 0
                    
                bankID = str(bank_id_code) + str(bankID)
                BankName = acquire_bank + ',' + BankName
                save_debitcardSales = SalesTransEPS (
                    sales_trans_id = int(float(doc_no)),
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    document_type = 'SI',
                    details_id = new_details_id,
                    card_no=card_no,
                    bank = bank_id_code,
                    card_holder = card_holder,
                    approval_no = approval_no,
                    amount = amount_due
                )

                save_debitcardSales.save()

 
        if table_no =='':
            table_no = 0
     
        
        
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        companyCode = getCompanyData()
        waiterName=''
 


        if data_from_modal.get('Customer') != '':
            if data_from_modal.get('customerType').upper() == "WALK-IN":
                try:
                    Payor = PosPayor.objects.get(payor_name=data_from_modal.get('Customer'))
                    customer_code = Payor.id_code
                    CustomerName = Payor.payor_name
                    CusTIN =Payor.tin
                    CusAddress =Payor.address
                    CusBusiness = Payor.business_style
                    cust_type = "P"
                except PosPayor.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN = ""
                    CusAddress = ""
                    CusBusiness = ""
            else:
                try:
                    customer = Customer.objects.get(trade_name=data_from_modal.get('Customer'))
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                    CusAddress = customer.st_address
                except Customer.DoesNotExist:
                    customer_code = "8888"
                    CustomerName = "Walk-IN"
                    cust_type = ""
                    CusTIN =customer.tax_id_no
                    CusAddress =customer.st_address
                    CusBusiness = customer.business_style
                    
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
            

        disc_amt = 0
        desc_rate= 0
        vat_amt = 0
        vat_exempt = 0
        net_total = 0
        total_disc_amt = 0 ###for sales invoice list
        total_desc_rate= 0 ###for sales invoice list
        total_vat_amt = 0 ###for sales invoice list
        total_vat_exempt = 0 ###for sales invoice list
        total_net_total = 0 ###for sales invoice list
        total_sub_total = 0 ###for sales invoice list
        vatable = ''
        totalQty = 0
        desc_rate = 0

            
        
        
        for items in cart_items:
            productInfo = Product.objects.filter(bar_code=items['barcode']).first()

            if productInfo is not None:
                quantity = float(items['quantity'])
                price = float(items['price'])
                item_disc = float(items['item_disc'])
                total_sub_total = total_sub_total + (quantity * price)
                
                if DiscountType == 'SC':
                    vatable = 'Es'
                    desc_rate = 20
                    totalItem = quantity * price
                    
                    NetSale =  totalItem / (0.12 + 1 )
                    vat_exempt =  totalItem - NetSale
                    disc_amt  = (totalItem - vat_exempt ) * 0.2
                    net_total = (quantity * price) - (disc_amt + vat_exempt)
                    
                    print('NetSale',NetSale)
                    print('vat_exempt',vat_exempt)
                    print('disc_amt',disc_amt)
                    print('net_total',net_total)
                
                    
                else:
                    if productInfo.tax_code == 'VAT':
                        vatable = 'V'
                        desc_rate = item_disc / (quantity * price) * 100
                        vat_amt = (((quantity * price) - item_disc) / 1.12) * 0.12
                        net_total = (quantity * price) - item_disc - vat_amt
                    else:
                        vatable = 'N'
                        vat_amt = 0
                        disc_amt = item_disc
                        net_total = (quantity * price) - disc_amt
            else:
                # Handle case where productInfo is None (no product found for the barcode)
                pass  # You might want to log this or handle it according to your logic
                

            total_disc_amt = total_disc_amt + desc_rate
            total_desc_rate= total_desc_rate + desc_rate
            total_vat_amt = total_vat_amt + vat_amt

            if DiscountType == 'SC':
                total_vat_exempt = total_vat_exempt + net_total
                print('total_vat_exempt',total_vat_exempt)
            else:
                total_net_total = total_net_total + net_total
            
            # pdb.set_trace()
            totalQty = totalQty + float(items['quantity'])
            
            SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                doc_date = datetime_stamp,
                doc_no = doc_no,
                doc_type = 'POS-CI',
                line_number = items['line_no'],
                bar_code =items['barcode'],
                alternate_code = 0,
                item_code = items['barcode'],
                rec_qty = items['quantity'],
                rec_uom = productInfo.uom,
                description = items['description'],
                unit_price = items['price'],
                sub_total = float(items['quantity']) * float(items['price']),
                pc_price =  items['price'],
                qtyperuom = 1,
                disc_amt = f"{disc_amt:.3f}",
                desc_rate =f"{desc_rate:.3f}",
                vat_amt =  f"{vat_amt:.3f}",
                vat_exempt = f"{vat_exempt:.3f}",
                net_total =  f"{net_total:.3f}",
                isvoid = 'No',
                unit_cost = '0',
                vatable = vatable,
                status = 'A',
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                sn_bc = '',
                discounted_by = '',
                
            )
            SaveToPOSSalesInvoiceListing.save()

  
        net_vat = 0
        net_discount = 0
        vat_exempted = 0
        #### Take note of computation of net_vat and net_discount
        # pdb.set_trace()
        if DiscountType == 'SC':
            total_disc_amt = DiscountData['SLess20SCDiscount']
            net_vat = DiscountData['SDiscountedPrice']
            net_discount = DiscountData['SDiscountedPrice']
            vat_exempted = DiscountData['SLessVat12']
            
            
            
            
        else:   
            net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
            net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
        
        
        AmountDue_without_comma = AmountDue.replace(',', '')
        # Convert the modified string to a float
        AmountDue_float = float(AmountDue_without_comma)
        
        AmountDue_float = float(AmountDue_float)       
        AmountDue_formatted = f"{AmountDue_float:.3f}"
        print('cus-address',CusAddress)
        total_disc_amt = float(total_disc_amt)
        total_desc_rate = float(total_desc_rate)
        total_vat_exempt = float(total_vat_exempt)
        SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                company_code = f"{companyCode.autonum:0>4}",
                ul_code = machineInfo.ul_code,
                site_code = int(machineInfo.site_no),
                trans_type = 'Credit Sales',
                discount_type = '',
                doc_no = doc_no,
                doc_type = 'POS-CI',
                terminal_no = TerminalNo,
                cashier_id = cashier_id,
                so_no =items['sales_trans_id'],
                so_doc_no =items['sales_trans_id'],
                doc_date = datetime_stamp,
                customer_code = customer_code,
                customer_name = CustomerName,
                customer_address = CusAddress,
                business_unit = CusBusiness,
                customer_type = cust_type,
                salesman_id = '0',
                salesman = '',
                collector_id = '0',
                collector = '',
                pricing = '',
                terms = 0,
                remarks = '',
                ServiceCharge_TotalAmount = 0 ,
                total_cash =  "{:.3}".format(float(CashAmount)),
                total_eps =  "{:.3}".format(float(DebitCardAmount)),
                total_credit_card = "{:.3f}".format(float(CreditCardAmount)),
                total_qty = totalQty,
                discount = float(total_disc_amt),
                vat = float(total_vat_amt),
                vat_exempted = float(vat_exempted),
                net_vat = float(net_vat),
                net_discount = float(net_discount),
                sub_total = float(total_sub_total),
                # discount =  f"{total_disc_amt:.3f}" ,
                # vat = f"{total_vat_amt:.3f}",
                # vat_exempted =  f"{total_vat_exempt:.3f}",
                # net_vat = f"{net_vat:.3f}",
                # net_discount = f"{net_discount:.3f}",
                # sub_total = f"{total_sub_total:.3f}",
                lvl1_disc = '0',
                lvl2_disc = '0',
                lvl3_disc = '0',
                lvl4_disc = '0',
                lvl5_disc = '0',
                HMO = '',
                PHIC = '',
                status = 'S',
                prepared_id = cashier_id,
                prepared_by = CashierName,
                )
        
        SaveToPOSSalesInvoiceList.save()
        

        if OrderType == 'DINE IN':
            GetWaiterID = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    terminal_no=machineInfo.terminal_no,
                    site_code=int(machineInfo.site_no)
                ).first()
            if GetWaiterID:
                waiterID = GetWaiterID.waiter_id
                
                # Fetch waiter details if waiterID is available
                waiter_details = PosWaiterList.objects.filter(waiter_id=waiterID).first()
                
                if waiter_details:
                    waiterName = waiter_details.waiter_name
                    # Perform further operations with waiterName or other attributes
                else:
                    # Handle the case where waiter details are not found
                    waiterName = None  # or any default value or error handling
            else:
                # Handle the case where GetWaiterID is None (no matching record found)
                waiterID = None  # or any default value or error handling
                waiterName = None  # or any default value or error handling
        
            sales_orders_to_update = PosSalesOrder.objects.filter(
                table_no=table_no,
                paid='N',
                active='Y',
                terminal_no=TerminalNo,
                site_code=int(machineInfo.site_no)
            )

            # Check if there are any matching objects
            if sales_orders_to_update.exists():
                # Update all matching objects to set 'paid' to 'Y'
                sales_orders_to_update.update(paid='Y')
                
                pass

        UpdateINVRef = InvRefNo.objects.filter(description='POS CI',terminalno=TerminalNo).first()
        UpdateINVRef.next_no = doc_no
        UpdateINVRef.save()
  

        data = []
        data = {
            'CustomerCompanyName':companyCode.company_name,
            'CustomerCompanyAddress':companyCode.company_address,
            'CustomerTIN':companyCode.company_TIN,
            'CustomerZipCode':companyCode.company_zipcode,
            'MachineNo':machineInfo.Machine_no,
            'SerialNO':machineInfo.Serial_no,
            'CustomerPTU':machineInfo.PTU_no,
            'DateIssue':machineInfo.date_issue,
            'DateValid':machineInfo.date_valid,
            'TelNo':'TEL NOS:785-462',
            'OR':doc_no,
            'VAT': '{:,.2f}'.format(total_vat_amt),
            'VATable': '{:,.2f}'.format(total_net_total),
            'Discount': '{:,.2f}'.format(total_disc_amt),
            'Discount_Rate': '{:,.2f}'.format(total_desc_rate),
            'VatExempt': '{:,.2f}'.format(total_vat_exempt),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00',
            'customer_code' : customer_code,
            'CustomerName' :CustomerName,
            'CusTIN' :CusTIN,
            'CusAddress' :CusAddress,
            'CusBusiness' : CusBusiness,
            'cust_type' : cust_type,
            'TerminalNo':TerminalNo,
            'WaiterName':waiterName,
            'DebitcardData':debit_card_payments,
            'CreditcardData':credit_card_payments,
            'CashAmount':CashAmount,

        } 
    return Response({'data':data}, status=200)
     



###*************** SAVE AFTER CASH COUNT END SHIFT-----*******************
@api_view(['GET','POST'])
def cash_breakdown(request):
    if request.method == 'GET':
        cash_breakdown = PosCashBreakdown.objects.filter(login_record='1')
        serialize = PosCashBreakdownSerializer(cash_breakdown,many=True)
        return JsonResponse({'CashBreakdown':serialize.data},status=200)
    elif request.method == 'POST':
        data_recieve = json.loads(request.body)
        TransID = data_recieve.get('TransID')
        data = data_recieve.get('data')
        dinomination = data.get('dinomination')
        Totaldenominations = data.get('Totaldenominations')
        current_date_ph = GetPHilippineDate()
        cash_breakdown_instances = []
        conversion_rates = {
            'OneThousand': 1000,
            'Fivehundred': 500,
            'Twohundred': 200,
            'Onehundred': 100,
            'Fifty': 50,
            'Twenty': 20,
            'Ten': 10,
            'Five': 5,
            'Peso': 1,
            'Cent25': 0.25,
            'Cent05': 0.05
        }

        # Iterate over the keys in dinomination
        for denomination, quantity in dinomination.items():
            if int(quantity) > 0:
                value = conversion_rates[denomination]
                print((float(value) * int(quantity)))
                breakdown_instance = PosCashBreakdown(
                        login_record=TransID,  # Provide appropriate value
                        date_stamp=current_date_ph,  # Provide appropriate value
                        quantity=quantity,
                        denomination= value,
                        total=float(value) * int(quantity),  # Get the total amount by multiplying quantity with value
                        reviewed_by=0,  # Provide appropriate value
                    )
                breakdown_instance.save()
        return JsonResponse({'message':"This endpoint is for POST requests only."},status=200)
            
