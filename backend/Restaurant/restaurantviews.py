import abc
import json
import locale
from django.http import JsonResponse
from rest_framework.response import Response
from backend.models import (Product,PosRestTable,PosSalesOrder,PosSalesTransDetails,InvRefNo,POS_Terminal,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                            CompanySetup,Customer,PosWaiterList,PosPayor)
from backend.serializers import (ProductSerializer,ProductCategorySerializer,PosSalesOrderSerializer,PosSalesTransDetailsSerializer,PosSalesTransSerializer,
                                 PosSalesInvoiceListing,PosSalesInvoiceList,CustomerSerializer,PosWaiterListSerializer,PosPayorSerializer,PosSalesInvoiceListSerializer)
from rest_framework.decorators import api_view
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime

@api_view(['GET'])
def get_product_data(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_productCategory_data(request):
    # Assuming 'category' is a field in the Product model

    distinct_categories = Product.objects.values('category').distinct()

    serializer = ProductCategorySerializer(distinct_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_by_category(request, category):
    # Query the Product model based on the category received in the URL

    products = Product.objects.filter(category=category).exclude(reg_price='0')

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
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            
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
def get_sales_order_list(request):
    if request.method == 'GET':
        tableno = request.GET.get('tableno')
        
        if tableno == 0:
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                return Response(serializer.data)
        else:
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =tableno)
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                return Response(serializer.data)
            

@api_view(['GET'])
def get_sales_order_listing(request):
    # document_no = request.GET.get('document_no[]')
    TableNo = request.GET.get('tableno')
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()

    if TableNo:
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
    return Response(result)




@api_view(['GET'])
def get_add_order_view(request):
    
    
    # Query the Product model based on the category received in the URL
    tableNo = request.GET.get('tableNo')
    serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
    paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no),table_no = tableNo)
    serializer = PosSalesOrderSerializer(paid, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_customer_list(request):
    customer = request.GET.get('customer')
    print('customer',customer)
    if customer:
        customers = Customer.objects.filter(trade_name__icontains=customer)
        serialized_data = CustomerSerializer(customers, many=True).data

        return Response({"customers": serialized_data})
    else:
        return Response({"message": "No 'str' parameter provided"}, status=400)
    
@api_view(['GET'])
def get_waiter_list(request):
    waiter = request.GET.get('waiter')
    print('waiter',waiter)
    if waiter:
        waiters = PosWaiterList.objects.filter(waiter_name__icontains=waiter)
        serialized_data = PosWaiterListSerializer(waiters, many=True).data

        return Response({"waiter": serialized_data})
    else:
        return Response({"message": "No 'str' parameter provided"}, status=400)
     
     
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
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
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
            'VATable': '{:,.2f}'.format(sales_invoice.sub_total),
            'Discount': '{:,.2f}'.format(sales_invoice.discount),
            'VatExempt': '{:,.2f}'.format(sales_invoice.vat_exempted),
            'NonVat':'0.00',
            'VatZeroRated':'0.00',
            'ServiceCharge': '0.00'
            # 'customer_code' : customer_code,
            # 'CustomerName' :CustomerName,
            # 'CusTIN' :CusTIN,
            # 'CusAddress' :CusAddress,
            # 'CusBusiness' : CusBusiness,
            # 'cust_type' : cust_type,
            # 'TerminalNo':machineInfo.terminal_no,
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
       
       
        current_datetime = timezone.now()
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
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        

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
            
            
        SaveToSalesOrder = PosSalesOrder(
            SO_no = so_no,
            document_no = min_sales_trans_id,
            customer_type = 'W',
            customer_name = customer,
            table_no = table_no,
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
        doc_no = get_sales_transaction_id(TerminalNo,'POS SI')
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        companyCode = getCompanyData()
        
        GetWaiterID = PosSalesOrder.objects.filter(
            table_no=table_no,
            paid='N',
            terminal_no=TerminalNo,
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
        
        print('waiter',waiterID,waiterName)

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
        
        # data = {
        #     'OR':doc_no,
        #     'VAT': total_vat_amt,
        #     'VATable': total_net_total,
        #     'Discount:': total_disc_amt,
        #     'Discount_Rate': total_desc_rate,
        #     'VatExcempt': total_vat_exempt,
        #     'ServiceCharge': 0
        # }
        
        
    return Response({'data':data}, status=200)
        
        
###******************** CANCEL SALES ORDER    ***************************    
@api_view(['POST'])
def cancel_sales_order(request):
    if request.method == 'POST':
        tableno = request.data.get('params', {}).get('tableno')
        
        print('table',tableno)
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()

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
def save_sales_order_takeout(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        table_no = received_data.get('TableNo')
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountTendered = received_data.get('AmountTendered')

        doc_no = get_sales_transaction_id(TerminalNo,'POS SI')
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
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        

        for item in cart_items:
            line_no += 1 
            quantity = item['quantity']
            description = item['description']
            price = item['price']
            barcode = item['barcode']
            
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
            amount_disc = 0,
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



