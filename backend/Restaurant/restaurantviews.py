import abc
import decimal
import json
import locale
import os
import pdb
from django.http import JsonResponse,FileResponse
from prompt_toolkit import Application
from rest_framework.response import Response
from backend.models import *
from backend.serializers import *
from rest_framework.decorators import api_view
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import *
from datetime import datetime, timedelta,date
import datetime as dt
from django.utils import timezone
import pytz
from django.db.models import Q
from django.utils import timezone
import pytz
from django.core.exceptions import ObjectDoesNotExist
import time
import logging
from backend.globalFunction import *
from django.db import transaction
from pyprinter import Printer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# from pywinauto.findwindows import ElementNotFoundError
import traceback
from decimal import Decimal
from django.db.models.functions import Concat
from django.db.models import F, CharField, Value, Q, Func, Value, Subquery, OuterRef, DecimalField
from django.db.models.functions import Cast, Coalesce

@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def print_electron(request):
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        try :
            app = Application().connect(title="Print")
            print_dialog = app.window(class_name="#32770")
            print_dialog.print_button.click()
            return JsonResponse({"message": "Print Success"}, status=200)
        
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts}: Print dialog not found. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
    
    print("Failed to connect to the application after maximum attempts.")
    return JsonResponse({"error": "Failed to connect to the application"}, status=404)

     
##********** EXTENDED MONITOR TRANSACTION ********##
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def pos_extended(request):
    if request.method == 'GET':
        data = request.GET.get('data')
        serial_number = getattr(request, "SERIALNO", None)
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        data_list = PosExtended.objects.filter(serial_no = machineInfo.Serial_no)
        serialize = PosExtendedSerializer(data_list,many=True)
        return Response(serialize.data)
    elif request.method == 'PUT':
        try:
                data = request.data.get('data', {})
                print(data)
                serial_number = getattr(request, "SERIALNO", None)
                print(serial_number)

                if not serial_number:
                    return JsonResponse({"success": False, "message": "Serial number missing"}, status=400)

                machine_info = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                if not machine_info:
                    return JsonResponse({"success": False, "message": "Machine not found"}, status=404)

                # Safely get inner data
                TableNo = request.data.get('TableNo') or 0
                OrderType = request.data.get('OrderType')

                quantity = data.get('quantity', 0)
                description = data.get('description', '')
                price = data.get('price', 0)
                total_amount = data.get('totalAmount', 0)
                barcode = data.get('barcode')
                lineno = data.get('lineno')

                # Print each value
                print("TableNo:", TableNo)
                print("OrderType:", OrderType)
                print("quantity:", quantity)
                print("description:", description)
                print("price:", price)
                print("total_amount:", total_amount)
                print("barcode:", barcode)
                print("lineno:", lineno)
                if not barcode or lineno is None:
                    print
                    return JsonResponse({'success': False, 'message': 'Barcode or line number missing'}, status=400)

                # Update existing record
                pos_item = PosExtended.objects.filter(
                    serial_no=serial_number,
                    barcode=barcode,
                    line_no=lineno
                ).first()

                if pos_item:
                    pos_item.qty = float(quantity)
                    pos_item.price = float(str(price).replace(',', ''))
                    pos_item.amount = float(str(total_amount).replace(',', ''))
                    pos_item.save()

                    return JsonResponse({'success': True, 'message': 'Data updated successfully'}, status=200)
                else:
                    return JsonResponse({'success': False, 'message': 'Record not found'}, status=404)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'Invalid data: {str(e)}'}, status=400)
    
    elif request.method == 'POST':
        try:

            data = json.loads(request.body)
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            # data = data['data']
            TableNo = data['TableNo']
            orderType = data['OrderType']
            quantity = data['data']['quantity']
            description = data['data']['description']
            price = data['data']['price']
            total_amount = data['data']['totalAmount']
            barcode = data['data']['barcode']
            lineno = data['data']['lineno']
            if TableNo =='':
                TableNo = 0
            data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number, barcode=barcode)
    
            saveExtended = PosExtended(
                    barcode=barcode,
                    qty=quantity,
                    description=description,
                    price=price,
                    amount=float(str(total_amount).replace(',', '')),
                    serial_no=serial_number,
                    table_no=int(TableNo),
                    order_type=orderType,
                    line_no = lineno

                )
            saveExtended.save()
            return JsonResponse({'success': True, 'message': 'Data received successfully'}, status=200)
        except json.JSONDecodeError:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    elif request.method == 'DELETE':
        try:
    # Parse the JSON data sent in the request body
            data = json.loads(request.body)  # Decode and load JSON data
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            if 'deleteData' in data:
                quantity = data['deleteData']['quantity']
                description = data['deleteData']['description']
                price = data['deleteData']['price']
                total_amount = data['deleteData'].get('totalAmount') if 'deleteData' in data else None
                lineno = data['deleteData'].get('lineno') if 'deleteData' in data else None

                barcode = data['deleteData']['barcode']
                if total_amount is None:
                    PosExtended.objects.filter(serial_no=serial_number).delete()
                    return Response('Delete Successfully')
                    
                # Retrieve the queryset of existing records based on the specified conditions
                data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number, barcode=barcode,line_no = lineno)

                # Check if any records exist in the queryset
                if data_exist_queryset.exists():
                    data_exist_queryset.delete()
                    return Response('Delete Successfully')
            else:
                PosExtended.objects.filter(serial_no=serial_number).delete()
                return Response('Delete Successfully')
        except Exception as e:
            # Handle exceptions here
            print("An error occurred:", e)
   
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def pos_extended_delete_all(request):
    if request.method == 'DELETE':
       
        try:
            # pdb.set_trace()
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            data_exist_queryset = PosExtended.objects.filter(serial_no=serial_number.strip())
            if data_exist_queryset.exists():
                data_exist_queryset.delete()
                return Response('Delete Successfully')
            else:
                return JsonResponse({'Error':'Request Failed'},status=400)

        except Exception as e:
            # Handle exceptions here
            print("An error occurred:", e)


def pos_extended_save_from_listing(request,data,TableNo,QueNO):
    serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
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
@permission_classes([IsAuthenticated])
def get_product_data(request):
    if request.method == 'GET':
        try:
            products = Product.objects.exclude(reg_price=0).exclude(long_desc='')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_per_price_name(request):
    if request.method == 'GET':
        try:
            price_name = request.GET.get('price_name',None)
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            site_code = int(machineInfo.site_no)
        # 1️⃣ Get default price name

            if price_name is None:
                pos_setup = PosPriceTypeSiteSetup.objects.filter(site_code=site_code).first()
                if not pos_setup:
                    return JsonResponse({'data': []})

                price_name = pos_setup.default_pricetype_name

            # 2️⃣ Subquery for Product fields
            products_qs = Product.objects.filter(
                bar_code=OuterRef('bar_code'),
                reg_price__gt=0
            ).exclude(long_desc='')

            # 3️⃣ Fetch multiple prices with Product info in one query
            multiple_price_list = ProductMultiplePrice.objects.filter(
                site_code=site_code,
                price_name=price_name
            ).annotate(
                reg_price=F('amount'),  # rename amount to reg_price
                uom=Subquery(products_qs.values('uom')[:1]),
                item_code=Subquery(products_qs.values('item_code')[:1]),
                category=Subquery(products_qs.values('category')[:1]),
                long_desc=Subquery(products_qs.values('long_desc')[:1]),
                prod_img=Subquery(products_qs.values('prod_img')[:1])
            ).filter(uom__isnull=False)

            # 4️⃣ Serialize to JSON
            data = list(multiple_price_list.values(
                'bar_code', 'reg_price', 'uom', 'item_code', 'category','long_desc','prod_img'
            ))
            return Response(data)
        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_productCategory_data(request):
    # Assuming 'category' is a field in the Product model
    # distinct_categories = Product.objects.values('category').distinct()
        # serializer = ProductCategorySerializer(distinct_categories, many=True)
    try:
        distinct_categories = ProductCategorySetup.objects.filter(pos_category='Y')
        serializer = ProductCategorySetupSerializer(distinct_categories, many=True)


       
        return Response(serializer.data)
    except Exception as e:
        print(e)
        traceback.print_exc()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_by_category(request):
    if request.method == 'GET':
        try:
            
            category = request.GET.get('category')
            print(category)
        # Query the Product model based on the category received in the URL
            if category == 'ALL':
                products = Product.objects.exclude(reg_price='0').exclude(long_desc='')

            # Serialize the products (convert to JSON or any desired format)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            elif category == 'MENU ACCESSORIES':
                products = Product.objects.filter(category=category)

            # Serialize the products (convert to JSON or any desired format)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)               
            else:
                products = Product.objects.filter(category=category).exclude(reg_price='0').exclude(long_desc='')

            # Serialize the products (convert to JSON or any desired format)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def table_list_view(request):
    try:
        serial_number = getattr(request, "SERIALNO", None)
        site_code = request.GET.get('site_code', None)  # Assuming site_code is passed as a query parameter
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        if site_code is None:
            site_code = int(float(machineInfo.site_no))
        tables = PosRestTable.objects.filter(site_code=site_code).order_by('table_start')

        if not tables.exists():
            return Response({"message": f"No tables found for site code: {site_code}"})

        # 1️⃣ Collect all table numbers
        table_numbers = []
        for table in tables:
            table_start = int(table.table_start)
            table_no = int(table.table_no)
            table_numbers.extend(range(table_start + 1, table_no + table_start + 1))

        # 2️⃣ Preload related data (3 queries total)
        suspend_lists = PosSuspendList.objects.filter(
            table_no__in=table_numbers,
            terminal_no=machineInfo.terminal_no,
            site_no=int(machineInfo.site_no)
        ).values_list('table_no', flat=True)

        unpaid_orders = PosSalesOrder.objects.filter(
            table_no__in=table_numbers,
            paid='N',
            active='Y',
            terminal_no=machineInfo.terminal_no,
            site_code=int(machineInfo.site_no)
        )

        dinein_orders = PosSalesOrder.objects.filter(
            table_no__in=table_numbers,
            paid='Y',
            active='Y',
            dinein_order_and_pay='Y',
            terminal_no=machineInfo.terminal_no,
            site_code=int(machineInfo.site_no)
        )

        # 3️⃣ Serialize results (still no extra DB hits)
        unpaid_serializer = PosSalesOrderSerializer(unpaid_orders, many=True)
        dinein_serializer = PosSalesOrderSerializer(dinein_orders, many=True)

        # 4️⃣ Convert to lookup maps for instant access
        suspend_set = set(suspend_lists)
        unpaid_map = {item['table_no']: item['paid'] for item in unpaid_serializer.data}
        dinein_map = {item['table_no']: item['dinein_order_and_pay'] for item in dinein_serializer.data}

        # 5️⃣ Build final table list
        table_list = []
        for table_no in table_numbers:
            table_list.append({
                "table_count": table_no,
                "Paid": unpaid_map.get(table_no, 'Y'),
                "Susppend": 'YES' if table_no in suspend_set else 'NO',
                "dinein_order_and_pay": dinein_map.get(table_no, '')
            })

        return Response({"tables": table_list})
      
        
    except Exception as e:
        print(e)
        traceback.print_exc()


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def table_list_view(request):
#     try:
#         serial_number = getattr(request, "SERIALNO", None)
#         site_code = request.GET.get('site_code', None)  # Assuming site_code is passed as a query parameter
#         machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
#         if site_code is None:
#             site_code = int(float(machineInfo.site_no))
#         tables = PosRestTable.objects.filter(site_code=site_code).order_by('table_start')
        
#         if not tables.exists():
#             return Response({"message": f"No tables found for site code: {site_code}"})

#         table_list = []
#         for table in tables:
#             table_count = 1 + table.table_start
#             while table_count <= table.table_no + table.table_start:
#                 paid_list ='Y'
#                 susppend ='NO'
#                 dinein_order_and_payData = ''
#                 susppend_list = PosSuspendList.objects.filter(table_no=table_count ,terminal_no = machineInfo.terminal_no,site_no = int(machineInfo.site_no))
#                 if susppend_list.exists():
#                     susppend = 'YES'
                    
#                 paid = PosSalesOrder.objects.filter(table_no=table_count ,paid = 'N',active = 'Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
#                 if paid.exists():
#                     serializer = PosSalesOrderSerializer(paid, many=True)
#                     for item in serializer.data:
                    
#                         paid_list = item['paid']  # Assuming 'paid' is the correct field name
#                         # table_list.append({"table_count": table_count, "Paid": paid_list,"Susppend":susppend,'dinein_order_and_pay':''})
               
#                 dinein_orderpay = PosSalesOrder.objects.filter(table_no=table_count ,paid = 'Y',active = 'Y',dinein_order_and_pay = 'Y',
#                                                                     terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
#                 if dinein_orderpay.exists():
#                     serializer1 = PosSalesOrderSerializer(dinein_orderpay, many=True)
#                     for item1 in serializer1.data:
#                         dinein_order_and_payData = item1['dinein_order_and_pay']  # Assuming 'paid' is the correct field name
                    
#                 table_list.append({"table_count": table_count, "Paid": paid_list,"Susppend":susppend,'dinein_order_and_pay':dinein_order_and_payData})
#                 table_count += 1
#         # print(table_list)
#         return Response({"tables": table_list})
#     except Exception as e:
#         print(e)
#         traceback.print_exc()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cleared_table_dinein_order_and_pay(request):
        try:
            recieve_data = json.loads(request.body)
            table_no = recieve_data.get('TableNo')
         
         
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            if table_no:
                clear_table_data = PosSalesOrder.objects.filter(table_no = table_no,paid = 'Y',active = 'Y' ,dinein_order_and_pay = 'Y',
                                                                terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no)).first()
                if clear_table_data:
                    clear_table_data.dinein_order_and_pay = None
                    clear_table_data.save()
                    return Response({"message": "Table Cleared"})

        except Exception as e:
            print(e)
            traceback.print_exc(0)
            return Response({"error": str(e)}, status=500)

        


#***************** GET WAITER NAME ************************
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_waiter_name(request):
    if request.method == 'GET':
     
        id = request.GET.get('id')
        # Retrieve the Waiter object with the specified ID
        try:
            waiter = PosWaiterList.objects.get(waiter_id=id)
        except PosWaiterList.DoesNotExist:
            return Response({'error': 'Waiter not found'}, status=404)

        # Serialize the Waiter object
        serializer = PosWaiterListSerializer(waiter)

        # Return serialized data
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def queing_list_view(request):
    if request.method == 'GET':
        site_code = request.GET.get('site_code', None)  # Assuming site_code is passed as a query parameter
        
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        if site_code is None:
            site_code = int(float(machineInfo.site_no))
        que_list=[]        
        paid = PosSalesOrder.objects.filter(
            q_no__isnull=False,
            paid='N',
            active='Y',
            terminal_no=machineInfo.terminal_no,
            site_code=int(machineInfo.site_no)
        ).exclude(q_no=Decimal('0.000'))
        if paid.exists():
            serializer = PosSalesOrderSerializer(paid, many=True)
            for item in serializer.data:
                    
                paid_list = item['paid'] 
                que_list.append({"q_no": item['q_no'] , "Paid": paid_list})
        print(que_list)
        return Response({"que": que_list})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales_order_list(request):
    if request.method == 'GET':
        tableno = request.GET.get('tableno')
        queno = request.GET.get('queno')

        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        if tableno is not None:
            if tableno == 0:
                # serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
                else:
                    return JsonResponse({'Message':'Close'},status=200)
            else:
                # serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =tableno)
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
                else:
                    return JsonResponse({'Message':'Close'},status=200)
        else:
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,q_no = queno)
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                return Response(serializer.data)
            else:
                return JsonResponse({'Message':'Close'},status=200)
                  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales_order_listing(request):
    # document_no = request.GET.get('document_no[]')
    # pdb.set_trace()
    try:

        TableNo = request.GET.get('tableno')
        so_no = request.GET.get('so_no')

        # serial_number = get_serial_number()
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        queno = request.GET.get('queno')
        # pdb.set_trace()
        if TableNo !='':
        
            if so_no:
                # pdb.set_trace()
                pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo,SO_no = so_no)
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
                            'tbl_pos_sales_order.document_no = %s', 'tbl_pos_sales_trans_details.isvoid = %s'
                        ],
                        params=[item.document_no,'NO']  
                    )
                    result.extend(list(matched_records.values()))
                pos_extended_save_from_listing(request,result ,TableNo,queno)   
            else:
                pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo,active ='Y')
                result = []
                # print('pos_sales_order_data',pos_sales_order_data)
                
                for item in pos_sales_order_data:
                    print('item.document_no',item.document_no)
                    matched_records = PosSalesTransDetails.objects.extra(
                        select={
                            'sales_order_document_no': 'tbl_pos_sales_order.document_no',
                            'so_no': 'tbl_pos_sales_order.SO_no'
                        },
                        tables=['tbl_pos_sales_trans_details', 'tbl_pos_sales_order'],
                        where=[
                            'tbl_pos_sales_trans_details.sales_trans_id = tbl_pos_sales_order.document_no',
                            'tbl_pos_sales_order.document_no = %s', 'tbl_pos_sales_trans_details.isvoid = %s'
                        ],
                        params=[item.document_no,'NO']  
                    )
                    result.extend(list(matched_records.values()))
                pos_extended_save_from_listing(request,result ,TableNo,queno)   
        else:
            pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,q_no =queno)
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
                        'tbl_pos_sales_order.document_no = %s', 'tbl_pos_sales_trans_details.isvoid = %s'
                    ],
                    params=[item.document_no,'NO']  
                )
                result.extend(list(matched_records.values()))
                print('result',result)
            pos_extended_save_from_listing(request,result ,TableNo,queno)  
        return Response(result)
    except Exception as e:
        print(e) 
        traceback.print_exc()
    

## **************** CANCELLED SALES ORDER TRANSACTION *****************
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales_order_list_cancelled(request):
    if request.method == 'GET':
        tableno = request.GET.get('tableno')
        queno = request.GET.get('queno')
        print(tableno,queno)
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        if tableno is not None:
            if tableno == 0:
   
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
            else:

                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                paid = PosSalesOrder.objects.filter(paid = 'N',active='N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =tableno)
                if paid.exists():
                    serializer = PosSalesOrderSerializer(paid, many=True)
                    return Response(serializer.data)
        else:

            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            paid = PosSalesOrder.objects.filter(paid = 'N',active='N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
            if paid.exists():
                serializer = PosSalesOrderSerializer(paid, many=True)
                return Response(serializer.data)
                  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales_order_listing_cancelled(request):
    # document_no = request.GET.get('document_no[]')
    # pdb.set_trace()
    TableNo = request.GET.get('tableno')
    so_no = request.GET.get('so_no')

    serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    queno = request.GET.get('queno')
    print('queno',queno)
    # pdb.set_trace()
    if TableNo is not None:
       
        if so_no:
            print('pos_sales_order_dataaaa',int(machineInfo.site_no),machineInfo.terminal_no)
            # pdb.set_trace()
            pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo,SO_no = so_no,active='N')
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
            pos_extended_save_from_listing(request,result ,TableNo,queno)   
        else:
            pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,table_no =TableNo,active ='N')
            result = []
            # print('pos_sales_order_data',pos_sales_order_data)
            
            for item in pos_sales_order_data:
                print('item.document_no',item.document_no)
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
            pos_extended_save_from_listing(request,result ,TableNo,queno)   
    else:

        pos_sales_order_data = PosSalesOrder.objects.filter(paid = 'N',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no) ,active ='N')
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
            print('result',result)
        pos_extended_save_from_listing(request,result ,TableNo,queno)   
    return Response(result)
#*********************** END *******************************************


##***************************** UPDATE ITEM DISCOUNT*****************************************
@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def update_item_discount(request):
    if request.method == 'POST':
        try:
            receive_data = json.loads(request.body)
            serial_number = getattr(request, "SERIALNO", None)
            SelectedItemDiscount = receive_data.get('SelectedItemDiscount')
            line_no = SelectedItemDiscount.get('line_no')
            sales_trans_id = SelectedItemDiscount.get('sales_trans_id')
            desc_rate = receive_data.get('D1')
            desc_amount = receive_data.get('ByAmount')

            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            item_discount = PosSalesTransDetails.objects.filter(
                line_no=line_no,
                sales_trans_id=sales_trans_id,
                terminal_no=machineInfo.terminal_no,
                site_code=int(machineInfo.site_no)
            ).first()
            if item_discount:
                item_discount.desc_rate = float(str(desc_rate).replace(',', ''))
                item_discount.item_disc = float(str(desc_amount).replace(',', ''))
                item_discount.save()
            return JsonResponse({'success': True, 'message': 'Discount updated successfully'}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'Invalid data: {str(e)}'}, status=400)
    elif request.method == 'PUT':
        try:
            receive_data = json.loads(request.body)
            serial_number = getattr(request, "SERIALNO", None)
            SelectedItemDiscount = receive_data.get('SelectedItemDiscount')
            line_no = SelectedItemDiscount.get('line_no')
            sales_trans_id = SelectedItemDiscount.get('sales_trans_id')
            desc_rate = 0
            desc_amount = 0
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first
            item_discount = PosSalesTransDetails.objects.filter(
                line_no=line_no,
                sales_trans_id=sales_trans_id,
                terminal_no=machineInfo.terminal_no,
                site_code=int(machineInfo.site_no)
            ).first()
            if item_discount:
                item_discount.desc_rate = desc_rate
                item_discount.item_disc = desc_amount
                item_discount.save()
            
            return JsonResponse({'success': True, 'message': 'Discount reset successfully'}, status=200)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'Invalid data: {str(e)}'}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_category(request):
    if request.method == 'GET':
        try:
            # receive_data = json.loads(request.body)
            # print(receive_data)
            category_data_list = []
            category = request.GET.get('category')
            print('category',category)
            distinct_categories = Customer.objects.filter().values_list('sl_category', flat=True).distinct().exclude(sl_category = '')
            print(distinct_categories)
            for category_item in distinct_categories:
                    categories_data = SLCategory.objects.filter(category=category_item).first()
                    if categories_data:
                        category_data = {
                            'code': categories_data.code,
                            'category': categories_data.category
                        }
                        category_data_list.append(category_data)

                # Prepare Response
            response_data = {
            'data': category_data_list
            }

            return Response(response_data)
            
        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_with_category(request):
    if request.method == 'GET':
        try:
            name = request.GET.get('name')
            print('name',name)
            customer_list = Customer.objects.filter(trade_name__icontains=name)
            serialize = CustomerSerializer(customer_list,many=True)

            return Response(serialize.data)
            
        except Exception as e:
            print(e)
            traceback.print_exc()



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_add_order_view(request):
    # Query the Product model based on the category received in the URL
    tableNo = request.GET.get('tableNo')
    serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
    machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
    paid = PosSalesOrder.objects.filter(paid = 'N',active='Y',terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no),table_no = tableNo)
    serializer = PosSalesOrderSerializer(paid, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_list(request):
    if request.method == 'GET':
        try:
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
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({"message": "Request Failed"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_company_details(request):
    companyCode = getCompanyData()
    # serial_number = get_serial_number()
    serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
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
@permission_classes([IsAuthenticated])
def get_bank_card(request):
    if request.method =='GET':
        data = BankCard.objects.filter(active='Y')
        serialize = BankCardSerializer(data,many=True)
        return  Response(serialize.data) 
     
     
##*******************GET Bank Company *******************##

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bank_list(request):
    if request.method =='GET':
        data = BankCompany.objects.filter(active='Y')
        serialize = BankCompanySerializer(data,many=True)
        return  Response(serialize.data) 
     
##**********GET TRANSACTION FOR REPRINT ********##
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reprint_transaction(request):
    if request.method == 'GET':
        DateFrom = request.GET.get('datefrom')  # Get the 'datefrom' parameter
        DateTo = request.GET.get('dateto')      # Get the 'dateto' parameter
        TerminalNo = request.GET.get('TerminalNo')

        date_from = datetime.datetime.strptime(DateFrom, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(DateTo, '%Y-%m-%d')     
        
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
@permission_classes([IsAuthenticated])
def get_reprint_transaction_for_receipt(request):
    if request.method == 'GET':
        DocNo = request.GET.get('DocNo')  # Get the 'datefrom' parameter
        DocType = request.GET.get('DocType') 
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        list = PosSalesTransDetails.objects.filter(sales_trans_id=DocNo,terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no))
        listing = PosSalesTransDetailsSerializer(list,many=True).data
        companyCode = getCompanyData()
        
        sales_invoice = PosSalesInvoiceList.objects.filter(doc_no=DocNo,doc_type = DocType, terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no)).first()
        if sales_invoice: 
            print('sales_invoice.customer_name',sales_invoice.customer_name)
            Payor = PosPayor.objects.filter(payor_name=sales_invoice.customer_name).first()
            if Payor:
                customer_code = Payor.id_code
                CustomerName = Payor.payor_name
                CusTIN =Payor.tin
                CusAddress =Payor.address
                CusBusiness = Payor.business_style
                cust_type = "P"
            else:
                customer_code= "8888"
                CustomerName = "Walk-IN"
                cust_type = ""
                CusTIN =""
                CusAddress =""
                CusBusiness =""

                
        else:
            customer_code= "8888"
            CustomerName = "Walk-IN"
            cust_type = ""
            CusTIN =""
            CusAddress =""
            CusBusiness =""
        
        saleTrans = PosSalesTrans.objects.filter(sales_trans_id=DocNo, terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no)).first()
        if saleTrans:
            table_no = saleTrans.table_no
            Guest_Count = saleTrans.guest_count
            QueNo = saleTrans.q_no

        

        cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }

        ReprintPDFReceipt(request,DocNo,DocType,cus_Data)
        return JsonResponse({'Data':listing,'CusData':cus_Data}, status=200)

                
    #     data = []

    #     data = {
    #         'CustomerCompanyName':companyCode.company_name,
    #         'CustomerCompanyAddress':companyCode.company_address,
    #         'CustomerTIN':companyCode.company_TIN,
    #         'CustomerZipCode':companyCode.company_zipcode,
    #         'MachineNo':machineInfo.Machine_no,
    #         'SerialNO':machineInfo.Serial_no,
    #         'CustomerPTU':machineInfo.PTU_no,
    #         'DateIssue':machineInfo.date_issue,
    #         'DateValid':machineInfo.date_valid,
    #         'TelNo':'TEL NOS:785-462',
    #         'OR':DocNo,
    #         'VAT': '{:,.2f}'.format(sales_invoice.vat),
    #         'VATable': '{:,.2f}'.format(sales_invoice.net_vat),
    #         'Discount': '{:,.2f}'.format(sales_invoice.discount),
    #         'VatExempt': '{:,.2f}'.format(sales_invoice.vat_exempted),
    #         'NonVat':'0.00',
    #         'VatZeroRated':'0.00',
    #         'ServiceCharge': '0.00',
    #         # 'customer_code' : customer_code,
    #         # 'CustomerName' :CustomerName,
    #         # 'CusTIN' :CusTIN,
    #         # 'CusAddress' :CusAddress,
    #         # 'CusBusiness' : CusBusiness,
    #         # 'cust_type' : cust_type,
    #         'TerminalNo':machineInfo.terminal_no,
    #         # 'WaiterName':waiterName
    #     }
    
    # return JsonResponse({'Data':listing,'DataInfo':data}, status=200)

##********** TRANSFER TABLE ********##

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_table(request):
    if request.method =='POST':
        try:
            recieve_data = json.loads(request.body)
            TableNOfrom = recieve_data.get('TableFrom')
            TableNOTo = recieve_data.get('TableTo')
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            if TableNOfrom:
                if TableNOTo:
                    print('info ',machineInfo.terminal_no)
                    data = PosSalesOrder.objects.filter(terminal_no=machineInfo.terminal_no, table_no=TableNOfrom ,active = 'Y',paid='N').first()
                    if data:
                        data.table_no = int(TableNOTo)
                        data.save()
                        return Response('Success')
        except Exception as e:
            print(e)
            traceback.print_exc()



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



###***************CHECK QUE NO IF EXIST *******************

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Check_Que_No(request):
    if request.method == 'GET':
        try:
            QueNo = request.GET.get('QueNo')
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            Check_Que_No_if_exist = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(machineInfo.terminal_no),
                    site_code=int(machineInfo.site_no)
                ).first()
            
            if Check_Que_No_if_exist:
                 return Response('Exist')

            else:
                return Response('Not Exist')
           
        except Exception as e:
            print(e)
            traceback.print_exc(0)

###***************ADD SALES ORDER *******************

@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_sales_order(request):
    if request.method == 'POST':
        try:
            waiter = ''
            waiterID = 0
            QueNo = 0
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            data_from_modal = received_data.get('data2')
            table_no = received_data.get('TableNo')
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            OrderType = received_data.get('OrderType')
    
            customer = data_from_modal.get('Customer')
            guest_count = data_from_modal.get('GuestCount')
            waiterName = data_from_modal.get('Waiter')
            waiterID = data_from_modal.get('waiterID')
            payment_type = data_from_modal.get('PaymentType')
            QueNo = data_from_modal.get('QueNO',0)
            if QueNo =='' :
                QueNo = 0
            elif QueNo is None:
                QueNo = 0


            if table_no == '':
                table_no = 0
            
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
            # Get current datetime in UTC
            current_datetime_utc = timezone.now()

            # Convert to Asia/Manila
            target_timezone = pytz.timezone("Asia/Manila")
            current_datetime = current_datetime_utc.astimezone(target_timezone)

            # Extract date and time directly (no need to format and parse back)
            formatted_date = current_datetime.date()
            formatted_time = current_datetime.time()

            # If you still want a formatted string
            datetime_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
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

            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            
            #**** PRINT SALES ORDER USING BACKEND***

            printer_setup = GetCompanyConfig('multiple_printer')


            PDFSalesOrderaLL(cart_items,so_no,table_no,QueNo,guest_count,customer,OrderType,cashier_id,'','Cashier')
            if printer_setup == False:
                PDFSalesOrder(cart_items,so_no,table_no,QueNo,guest_count,customer,OrderType,cashier_id,'','Cashier')
            else:
             
                make_print = False
                printer_list = POSProductPrinter.objects.all().exclude(prod_desc='Cashiers')
                list_to_print = []
               
                try:
                    for printer_name in printer_list:
                        itemList = cart_items
                       
                       
                        for category in printer_name.category_desc.split(','):
                            for item in itemList:
                                ProductCat = Product.objects.filter(bar_code=item['barcode']).values('category').first()
                                if ProductCat is not None and 'category' in ProductCat:

                                    if ProductCat['category'] == category.strip():
                                        item['printer_name'] = printer_name.printer_name  # Assuming 'name' is a field in POSProductPrinter
                                        item['matched_category'] = category.strip()
                                        make_print = True
                                        print(f"printer_name: {printer_name.printer_name}")
                                        list_to_print.append(item)

                        if make_print == True:
                           
                            print('list_to_print')
                            PDFSalesOrder(list_to_print,so_no,table_no,QueNo,guest_count,customer,OrderType,cashier_id,printer_name.printer_name,printer_name.prod_desc)
                            print('Printing COmplete')
                            list_to_print=[]
                            make_print = False
                except Exception as e:
                    print(e)
                    traceback.print_exc()

            # print_pdf_salesOrder()
            # *********END HERE************

            for item in cart_items:
                print(item)
                if item.get('line_no') is None:
                    line_no = item.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                else:
                    line_no = item['line_no']
                # line_no = item['lineno']
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
                
            saveCustomer = PosSalesTransCustomer(
               sales_trans_id = min_sales_trans_id,
               name_stamp=customer,
               document_type ='SO',
               terminal_no = machineInfo.terminal_no,
               cashier_id =cashier_id,
            )
            saveCustomer.save()
            # pdb.set_trace()
            # Common fields for both payment_type conditions
            common_fields = {
                'SO_no': so_no,
                'document_no': min_sales_trans_id,
                'customer_type': 'W',
                'customer_name': customer,
                'table_no': table_no,
                'q_no': QueNo,
                'dinein_takeout': OrderType,
                'guest_count': guest_count,
                'waiter_id': int(waiterID),
                'cashier_id': cashier_id,
                'terminal_no': TerminalNo,
                'site_code': int(machineInfo.site_no),
                'date_trans': formatted_date,
                'time_trans': formatted_time,
                'paid': 'N',
                'active': 'Y',
            }

            # Check payment_type to determine additional fields
            if payment_type == 'Order and Pay':
                # Additional fields for payment_type 'Order And Pay'
                common_fields['dinein_order_and_pay'] = 'Y'

            # Create and save PosSalesOrder instance with common and conditional fields
            SaveToSalesOrder = PosSalesOrder(**common_fields)
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
            
      
            Susppend_list = PosSuspendList.objects.filter(table_no=table_no,site_no=int(machineInfo.site_no),terminal_no = machineInfo.terminal_no)
            if Susppend_list.exists():
                Susppend_list.delete()
            Susppend_list2 = PosSuspendListing.objects.filter(table_no=table_no,terminal_no = machineInfo.terminal_no)
            if Susppend_list2.exists():
                Susppend_list2.delete()


            data =[]

            data = {
                'documentno':min_sales_trans_id,
                'SO_NO':so_no,
                'TerminalNo':TerminalNo,
                
                
            }
            # transaction.commit()

            return JsonResponse({'SOdata': data}, status=200)
           
        except Exception as e:
            print(e)
            traceback.print_exc()
        # If any error occurs during the save operations, roll back the transaction
            transaction.rollback()
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    

###***************SUSPPEND TRANSACTIONS *******************

@api_view(['POST','GET'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def suspend_save_sales_order(request):
    if request.method == 'POST':
        try:
            print('suspend_save_sales_order') 
            waiter = ''
            waiterID = 0
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            CustomerData = received_data.get('data2')
            print(CustomerData)
            table_no = received_data.get('TableNo')
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            trans_id =  get_sales_transaction_id(TerminalNo,'POS SUSPPEND')
            QueNo = ''
            CustomerName=CustomerData.get('Customer')
            CustomerAddress=CustomerData.get('CusAddress')
            print(CustomerName,CustomerAddress)
       
            line_no=0
            if table_no == '':
                table_no = 0
            
            if QueNo == '':
                QueNo=0


            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            

            for item in cart_items:
                line_no += 1 
                quantity = item['quantity']
                description = item['description']
                price = item['price']
                barcode = item['barcode']
                
                SaveSusppendListing = PosSuspendListing(
                    trans_id =  int(float(trans_id)),
                    terminal_no = TerminalNo,
                    table_no = table_no,
                    que_no = QueNo,
                    barcode = barcode,
                    description = description,
                    price = price,
                    quantity = quantity,
                )
                
                SaveSusppendListing.save()
                
            
            saveSusppendList = PosSuspendList(
                trans_id =int(float(trans_id)),
                table_no = table_no,
                que_no = QueNo,
                site_no = int(machineInfo.site_no),
                terminal_no = TerminalNo,
                cashier_id=cashier_id,
                customer=CustomerName,
                address = CustomerAddress,
            )
            saveSusppendList.save()
            UpdateINVRef = InvRefNo.objects.filter(description='POS SUSPPEND').first()
            UpdateINVRef.next_no = trans_id
            UpdateINVRef.save()
            return JsonResponse({'message': 'Successfully'}, status=200)
           
        except Exception as e:
            print(e)
            traceback.print_exc(0)

        # If any error occurs during the save operations, roll back the transaction
            transaction.rollback()
    if request.method == 'GET':
        try:

            TableNo = request.GET.get('TableNo')
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            Susppend_list = PosSuspendList.objects.filter(table_no=TableNo,site_no=int(machineInfo.site_no),terminal_no = machineInfo.terminal_no).first()
            Susppend_list2 = PosSuspendList.objects.filter(table_no=TableNo,site_no=int(machineInfo.site_no),terminal_no = machineInfo.terminal_no)
            Susppend_list_serialize = PosSuspendListSerializer(Susppend_list2,many=True)
            if Susppend_list:
                Susppend_listing = PosSuspendListing.objects.filter(trans_id=Susppend_list.trans_id,table_no=TableNo,terminal_no = machineInfo.terminal_no)
                Susppend_listing_serialize = PosSuspendListingSerializer(Susppend_listing,many=True)

                return JsonResponse({'listing':Susppend_listing_serialize.data,'list':Susppend_list_serialize.data})
        except Exception as e:
            print(e)
            traceback.print_exc(0)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
###************ CASH PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_cash_payment(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            data_from_modal = received_data.get('CustomerPaymentData')
            table_no = received_data.get('TableNo')
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            AmountDue = received_data.get('AmountDue')
            CashierName =  received_data.get('CashierName')
            OrderType =  received_data.get('OrderType')
            DiscountDataList = received_data.get('DiscountDataList')
            DiscountType = received_data.get('DiscountType','')
            DiscountData= received_data.get('DiscountData')
            Discounted_by= received_data.get('Discounted_by')
            QueNo= received_data.get('QueNo')
            doctype = received_data.get('doctype')
            ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
           
            doc_no = get_sales_transaction_id(TerminalNo,doctype)
            if table_no =='':
                table_no = 0
            if QueNo =='':
                QueNo = 0
        
            current_datetime = timezone.now()
            datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            # serial_number = get_serial_number()            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
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
            Guest_Count = 0
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
            countxx = 0
             
        
            
            tmp_cart_item_discount = cart_items

            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0

                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                uom = ''
                if productInfo is not None:
                    uom = productInfo.uom
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    if price !=0:
                        if DiscountType == 'SC':
                            SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                            SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                            SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                            SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                            SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                            vatable = 'Es'
                            desc_rate = 20
                            totalItem = quantity * price
                                
                            NetSale =  totalItem / (0.12 + 1 )
                            vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                            disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                            net_total = (totalItem) - (disc_amt + vat_exempt)
                            vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                            Vatable_Amount = SVatSales - SCAmmountCovered
    
                        
                        elif DiscountType =='ITEM':
                            for dis in DiscountData:
                                try:
                                    lineNO = 0
                                    if dis.get('line_no') is None:
                                        lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                                    else:
                                        lineNO = dis['line_no']


                                    if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                        
                                        # for x in tmp_cart_item_discount:
                                        #     if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        #         tmp_cart_item_discount.remove(x)
                                        vatable = 'V'
                                        desc_rate = float(dis['D1'])
                                        totalItem = quantity * price
                                        item_disc = float(dis['D1'])
                                        NetSale =  float(dis['DiscountedPrice'])
                                        vat_exempt =  0
                                        disc_amt  = float(dis['ByAmount'])
                                        net_total = (totalItem - disc_amt)
                                        vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                        unit_cost = (totalItem) 
                                        Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                                except Exception as e:
                                    print(e)
                                    traceback.print_exc()
                        elif DiscountType =='TRANSACTION':

                            for dis in DiscountData:
                                lineNO = 0
                                if dis.get('line_no') is None:
                                    lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                                else:
                                    lineNO = dis['line_no']

                                if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                    desc_rate = float(dis['desc_rate'])
                                    vatable = 'V'
                                    totalItem = quantity * price
                                    item_disc = float(dis['desc_rate'])
                                    vat_exempt =  0
                                    disc_amt  = float(dis['Discount'])
                                    net_total = (totalItem - disc_amt)
                                    vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                    unit_cost = (totalItem) 
                                    Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                        else:
                            if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem !=0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                            else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        vatable = 'N'
                        vat_amt = 0
                        disc_amt = 0
                        net_total = 0

                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                # total_disc_amt = total_disc_amt + float(disc_amt)
                # total_desc_rate= total_desc_rate + desc_rate
                # total_vat_amt = total_vat_amt + vat_amt

                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])

                try:
                    if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                        sales_orders_data = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                            terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(float(machineInfo.site_no))
                        ).first()
                        if sales_orders_data:
                            so_no=sales_orders_data.SO_no
                            so_doc_no=sales_orders_data.document_no
                    
                    else:
                        sales_orders_data = PosSalesOrder.objects.filter(
                            q_no=QueNo,
                            paid='N',
                            active='Y',
                            terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(float(machineInfo.site_no))
                        ).first()
                        if sales_orders_data:
                            so_no=sales_orders_data.SO_no
                            so_doc_no=sales_orders_data.document_no
                    
                    
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
                            rec_uom = uom,
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
                            isvoid = 'NO',
                            unit_cost = unit_cost,
                            vatable = vatable,
                            status = 'A',
                            so_no= so_no,
                            so_doc_no =so_doc_no,
                            sn_bc = '',
                            discounted_by = Discounted_by,  
                            )
                    SaveToPOSSalesInvoiceListing.save()
                except Exception as e:
                    print(e)
                    traceback.print_exc()


            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                total_sub_total = 0
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem !=0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    # total_net_total = total_net_total + net_total
                    # total_vat_exempt = vat_exempt + total_vat_exempt
                    # total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    # total_desc_rate= desc_rate 
                    # total_vat_amt = vat_amt + total_vat_amt
                    # totalQty = totalQty + float(items['quantity'])

            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',',''))
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=456,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
            elif DiscountType == 'ITEM':
   


                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                DiscountType == 'IM'

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"


            total_disc_amt = float(str(total_disc_amt).replace(',', ''))
            total_desc_rate = float(str(total_desc_rate).replace(',', ''))
            total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
                       
   
            if DiscountType == 'ITEM':
                DiscountType = 'IM'
            SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                    company_code = f"{companyCode.autonum:0>4}",
                    ul_code = machineInfo.ul_code,
                    site_code = int(machineInfo.site_no),
                    trans_type = 'Cash Sales',
                    discount_type = DiscountType,
                    doc_no = doc_no,
                    doc_type = 'POS-SI',
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    so_no =tmp_so_no,
                    so_doc_no =tmp_so_doc_no,
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
                    ServiceCharge_TotalAmount = ServiceChargeAmount ,
                    total_cash =  AmountDue_formatted,
                    total_qty = totalQty,
                    discount = float(str(total_disc_amt).replace(',', '')),
                    vat = float(str(total_vat_amt).replace(',', '')),
                    vat_exempted = float(str(vat_exempted).replace(',', '')),
                    net_vat = float(str(net_vat).replace(',', '')),
                    net_discount = float(str(net_discount).replace(',', '')),
                    sub_total = float(str(total_sub_total).replace(',', '')),
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
            

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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

                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                ).first()
                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    table_no = sales_orders_data.table_no
                    QueNo = sales_orders_data.q_no
            
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    pass
            else:

                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                ).first()
                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no


                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'SeniorDiscountDataList':DiscountDataList,
            } 

            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }

            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            # transaction.commit()
            return Response({'data':data}, status=200)     
        except Exception as e:
            print(e)
            traceback.print_exc()
            # If any error occurs during the save operations, roll back the transaction
            transaction.rollback()  
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
        
###******************** CANCEL SALES ORDER    ***************************    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_sales_order(request):
    if request.method == 'POST':
        tableno = request.data.get('params', {}).get('tableno')
        so_no = request.data.get('params', {}).get('so_no')
        
        print('table',tableno)
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()       
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

        if not machineInfo:
            return Response({'message': 'Machine information not found'}, status=404)

        if not tableno:
            return Response({'message': 'Table number is required'}, status=400)

        if so_no:
            paid_orders = PosSalesOrder.objects.filter(table_no=tableno,
                paid='N', active='Y', terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no),SO_no =so_no
            )

            if paid_orders.exists():
                paid_orders.update(active='N')
                return Response({'message': 'Sales orders canceled successfully'}, status=200)
            else:
                return Response({'message': 'No active unpaid orders found'}, status=404)
        else:
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
        
###******************** UNCANCEL SALES ORDER    ***************************    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uncancelled_sales_order(request):
    if request.method == 'POST':
        tableno = request.data.get('params', {}).get('tableno')
        so_no = request.data.get('params', {}).get('so_no')
        
        serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

        if not machineInfo:
            return Response({'message': 'Machine information not found'}, status=404)

        if not tableno:
            return Response({'message': 'Table number is required'}, status=400)

        if so_no:
            paid_orders = PosSalesOrder.objects.filter(table_no=tableno,
                paid='N', active='N', terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no),SO_no =so_no
            )

            if paid_orders.exists():
                paid_orders.update(active='Y')
                return Response({'message': 'Sales orders canceled successfully'}, status=200)
            else:
                return Response({'message': 'No active unpaid orders found'}, status=404)
        else:
            paid_orders = PosSalesOrder.objects.filter(table_no=tableno,
                paid='N', active='N', terminal_no=machineInfo.terminal_no, site_code=int(machineInfo.site_no)
            )

            if paid_orders.exists():
                paid_orders.update(active='Y')
                return Response({'message': 'Sales orders canceled successfully'}, status=200)
            else:
                return Response({'message': 'No active unpaid orders found'}, status=404)
    else:
        return Response({'message': 'Invalid request method'}, status=405)
        

###*************** SAVE SALES ORDER ---TAKE OUT-----*******************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_sales_order_payment(request):
    if request.method == 'POST':
        try:
        # pdb.set_trace()
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            table_no = received_data.get('TableNo','')
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            AmountTendered = received_data.get('AmountTendered')
            DiscountType = received_data.get('DiscountType')
            DiscountData= received_data.get('DiscountData')
            customer_data= received_data.get('customer')
            doctype = received_data.get('doctype')
            PaymentMethod= received_data.get('PaymentType')
            doc_no = get_sales_transaction_id(TerminalNo,doctype)
            current_datetime_utc = timezone.now()
            QueNo = received_data.get('QueNo','')


            # Convert to Asia/Manila
            target_timezone = pytz.timezone("Asia/Manila")
            current_datetime = current_datetime_utc.astimezone(target_timezone)

            # Extract date and time directly (no need to format and parse back)
            formatted_date = current_datetime.date()
            formatted_time = current_datetime.time()
            # If you still want a formatted string
            datetime_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            customername = ''
            guestcount = 0
            waiterid = 0
            waitername = ''
            paymenttype = ''
            document_type = 'SI'

            if PaymentMethod == 'CHARGE':
                document_type = 'CI'

     
            if customer_data:
                customername = customer_data['Customer']
                guestcount = customer_data['GuestCount']
                waiterid = customer_data.get('waiterID', None)  # Use get() to safely access waiterID, providing a default value of None if the key is missing
                waitername = customer_data['Waiter']
                paymenttype = customer_data['PaymentType']

            
            min_details_id = PosSalesTransDetails.objects.aggregate(details_id=Max('details_id'))['details_id'] or 0
            
            min_details_id = min_details_id + 1
            
            line_no = 0 

            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            Amt_Discount = 0
            so_no = ''
            for item in cart_items:
                # line_no += 1              
                if item.get('line_no') is None:
                    line_no = item.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                else:
                    line_no = item['line_no']
                    

                quantity = item['quantity']
                description = item['description']
                price = item['price']
                barcode = item['barcode']
                is_SC = 'NO'
                item_disc = 0
                desc_rate = 0
                vat_ex = 0

                if (paymenttype == 'Sales Order'):
                    if so_no == '':
                        so_no =  str(item['so_no'])
                    else:
                        so_no = str(so_no) + ',' + str(item['so_no'])


   
            
                
                if DiscountType == 'SC':
                    Amt_Discount = DiscountData['SLess20SCDiscount']
                    desc_rate = 20
                    totalItem = float(quantity) * float(price)
                    # print('price',price,'totalItem',totalItem,)
                    # pdb.set_trace()
                    NetSale =  float(totalItem) / float(0.12 + 1)
                    vat_ex =  float(totalItem) - float(NetSale)
                    item_disc  = (float(totalItem) - float(vat_ex) ) * 0.2
                
                SaveOrderToDetails = PosSalesTransDetails(
                    sales_trans_id = int(float(doc_no)),
                    datetime_stamp = datetime_stamp,
                    document_type = document_type,
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
                # pdb.set_trace()
            amountT = str(AmountTendered).replace(',', '')
            SaveToPosSalesTrans = PosSalesTrans(
                login_record = 1,
                sales_trans_id = int(float(doc_no)),
                terminal_no = TerminalNo,
                site_code = int(machineInfo.site_no),
                cashier_id = cashier_id,
                datetime_stamp = datetime_stamp,
                bagger = '',
                amount_tendered = float(str(amountT).replace(',','')),
                document_type = document_type,
                amount_disc = float(str(Amt_Discount).replace(',', '')),
                lvl1_disc = 0,
                lvl2_disc= 0,
                lvl3_disc = 0,
                lvl4_disc = 0,
                lvl5_disc =0,
                vat_stamp =0,
                sales_man = '',
                document_no = so_no,
                isvoid = 'NO',
                issuspend = 'NO',
                isclosed = 'NO',
                trans_type = 1,
                prepared_by = cashier_id,
            )
            
            SaveToPosSalesTrans.save()
            
            
            sales_details = PosSalesTransDetails.objects.filter(sales_trans_id=float(doc_no),  terminal_no = TerminalNo,  site_code =  int(machineInfo.site_no),document_type='SI')
            sales_details_data = PosSalesTransDetailsSerializer(sales_details, many=True).data
            # transaction.commit()
            return JsonResponse({'data':sales_details_data}, status=200)
        except Exception as e:
            print(e)
            traceback.print_exc()  
            # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()  
            # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)

        # return JsonResponse( status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


###************ CREDIT CARD PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_credit_card_payment2(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        cart_items = received_data.get('data', [])
        data_from_modal = received_data.get('CustomerPaymentData')
        table_no = received_data.get('TableNo')
        QueNo = received_data.get('QueNo',0)
        cashier_id = received_data.get('CashierID')
        TerminalNo = received_data.get('TerminalNo')
        AmountDue = received_data.get('AmountDue')
        CashierName =  received_data.get('CashierName')
        OrderType =  received_data.get('OrderType')
        doc_no = get_sales_transaction_id(TerminalNo,'POS SI')
        current_datetime = timezone.now()
        datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        serial_number = getattr(request, "SERIALNO", None)
        ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
            # serial_number = get_serial_number()
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
            
        so_no =0
        so_doc_no =''
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
            disc_amt = 0
            desc_rate= 0
            vat_amt = 0
            vat_exempt = 0
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

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
            
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
        if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
        else:
            sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)

        
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
                so_no =tmp_so_no,
                so_doc_no =tmp_so_doc_no,
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
                ServiceCharge_TotalAmount = ServiceChargeAmount ,
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
        

        if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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
# @transaction.atomic
@permission_classes([IsAuthenticated])
def save_credit_card_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        try:
            received_data = json.loads(request.body)
            try:
                cart_items = received_data.get('data', [])
                data_from_modal = received_data.get('CustomerPaymentData')
                table_no = received_data.get('TableNo')
                QueNo = received_data.get('QueNo',0)
                cashier_id = received_data.get('CashierID')
                TerminalNo = received_data.get('TerminalNo')
                AmountDue = received_data.get('AmountDue')
                CashierName =  received_data.get('CashierName')
                OrderType =  received_data.get('OrderType')
                Discounted_by= received_data.get('Discounted_by')
                DiscountDataList = received_data.get('DiscountDataList')
                DiscountType = received_data.get('DiscountType')
                DiscountData= received_data.get('DiscountData')
                QueNo= received_data.get('QueNo')
                CreditCard = received_data.get('CreditCard')
                doctype = received_data.get('doctype')
                ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
                doc_no = get_sales_transaction_id(TerminalNo,doctype)
            except Exception as e:
                print('Error',e)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            # pdb.set_trace()
            Guest_Count = 0
            if QueNo == '':
                QueNo=0
            bankID = ''
            BankName = ''
            if table_no =='':
                table_no = 0
            try:
                current_datetime = timezone.now()
                datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                serial_number = getattr(request, "SERIALNO", None)
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                companyCode = getCompanyData()
            except Exception as e:
                print('error',e)

            waiterName=''

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


            try:
                credit_card_payments = CreditCard['CreditCardPaymentList']
                for payment in credit_card_payments:

                    card_no = payment['CardNo']
                    acquire_bank = payment['AcquireBank']
                    card_issuer = payment['CardIssuer']
                    card_holder = payment['CardHolder']
                    approval_no = payment['ApprovalNo']
                    expiry_month = int(payment['ExpiryMonth'])
                    expiry_year = int(payment['ExpiryYear'])
                    amount_due = payment['AmountDue']


                    # Format the datetime object as "January 1, 2024"
                    expiry_date = dt.datetime(expiry_year, expiry_month, 1)
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
            except Exception as e:
                print('error',e)
                traceback.print_exc()

            if table_no =='':
                table_no = 0
        
            if QueNo =='':
                QueNo = 0
 
            current_datetime = timezone.now()
            datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
      
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
            countxx = 0

            uom = ''
            tmp_cart_item_discount = cart_items

            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
               
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                uom = ''
                
                if productInfo is not None:
                    uom = productInfo.uom
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    elif DiscountType =='ITEM':
                        
                        for dis in DiscountData:
                           
                            try:
                                lineNO = 0
                                if dis.get('line_no') is None:
                                    lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                                else:
                                    lineNO = dis['line_no']
 

                                if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:

                                    vatable = 'V'
                                    desc_rate = float(dis['D1'])
                                    totalItem = quantity * price
                                    item_disc = float(dis['D1'])
                                    NetSale =  float(dis['DiscountedPrice'])
                                    vat_exempt =  0
                                    disc_amt  = float(dis['ByAmount'])
                                    net_total = (totalItem - disc_amt)
                                    vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                    unit_cost = (totalItem) 
                                    Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                            except Exception as e:
                                print('Error in ITEM discount processing:', e)

                    elif DiscountType =='TRANSACTION':
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                # total_disc_amt = total_disc_amt + float(disc_amt)
                # total_desc_rate= total_desc_rate + desc_rate
                # total_vat_amt = total_vat_amt + vat_amt
   
                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                # if so_no == '':
                #     so_no = items['sales_trans_id']
                # else:
                #     if so_no == items['sales_trans_id']:
                #         so_no = so_no
                #     else:
                #         so_no = so_no + ', ' + items['sales_trans_id']

                try:
                    if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                        sales_orders_data = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                            terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(float(machineInfo.site_no))
                        ).first()
                        if sales_orders_data:
                            so_no=sales_orders_data.SO_no
                            so_doc_no=sales_orders_data.document_no
                    
                    else:
                        sales_orders_data = PosSalesOrder.objects.filter(
                            q_no=QueNo,
                            paid='N',
                            active='Y',
                            terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(float(machineInfo.site_no))
                        ).first()
                        if sales_orders_data:
                            so_no=sales_orders_data.SO_no
                            so_doc_no=sales_orders_data.document_no
                    try:
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
                            rec_uom = uom,
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
                            isvoid = 'NO',
                            unit_cost = unit_cost,
                            vatable = vatable,
                            status = 'A',
                            so_no =so_no,
                            so_doc_no =so_doc_no,
                            sn_bc = '',
                            discounted_by = Discounted_by,
                            
                        )
                        SaveToPOSSalesInvoiceListing.save()
                    except Exception as e:
                        print('error',e)
                        traceback.print_exc()
                except Exception as e:
                    print('error',e)
                    traceback.print_exc()

  
            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                total_sub_total = 0
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    

                    # totalQty = totalQty + float(items['quantity'])
                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =items['sales_trans_id'],
                    #     so_doc_no =items['sales_trans_id'],
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=456,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
                
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                
                
            # else:   
            #     net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
            #     net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)

     
            try:
                total_disc_amt = float(str(total_disc_amt).replace(',', ''))
                total_desc_rate = float(str(total_desc_rate).replace(',', ''))
                total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
                SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                        company_code = f"{companyCode.autonum:0>4}",
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        trans_type = 'Cash Sales',
                        discount_type = DiscountType,
                        doc_no = doc_no,
                        doc_type = 'POS-SI',
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        so_no =tmp_so_no,
                        so_doc_no =tmp_so_doc_no,
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
                        ServiceCharge_TotalAmount = ServiceChargeAmount ,
                        total_credit_card =  AmountDue_formatted,
                        total_qty = totalQty,
                        discount = float(str(total_disc_amt).replace(',', '')),
                        vat = float(str(total_vat_amt).replace(',', '')),
                        vat_exempted = float(str(vat_exempted).replace(',', '')),
                        net_vat = float(str(net_vat).replace(',', '')),
                        net_discount = float(str(net_discount).replace(',', '')),
                        sub_total = float(str(total_sub_total).replace(',', '')),
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
            except Exception as e:
                print('error',e)

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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


                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
            
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass

            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'CreditcardData':credit_card_payments,
                'SeniorDiscountDataList':DiscountDataList,
            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            return Response({'data':data}, status=200)
        except Exception as e:
                # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()
            traceback.print_exc()    
                # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return Response({"message": "An error occurred while saving the sales order"}, status=500)


##************ DEBIT CARD  OR EPS PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_debit_card_payment(request):
    if request.method == 'POST':
        try:
        # pdb.set_trace()
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            data_from_modal = received_data.get('CustomerPaymentData')
            table_no = received_data.get('TableNo')
            QueNo = received_data.get('QueNo',0)
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            AmountDue = received_data.get('AmountDue')
            CashierName =  received_data.get('CashierName')
            OrderType =  received_data.get('OrderType')
            Discounted_by= received_data.get('Discounted_by')
            DiscountDataList = received_data.get('DiscountDataList')
            # doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
            DiscountType = received_data.get('DiscountType')
            DiscountData= received_data.get('DiscountData')
            QueNo= received_data.get('QueNo')
            DebitCard = received_data.get('DebitCard')
            doctype = received_data.get('doctype')
            doc_no = get_sales_transaction_id(TerminalNo,doctype)
            ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            bankID = ''
            BankName = ''
            Guest_Count = 0
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

            Guest_Count = 0
            if QueNo == '':
                QueNo = '0'

            if table_no =='':
                table_no = 0
        
            
            
            current_datetime = timezone.now()
            datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0

                
        
            tmp_cart_item_discount = cart_items
            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        print(DiscountData)
                        print(DiscountData.get('SAmountCovered'))
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    
                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                # for x in tmp_cart_item_discount:
                                #     if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                #         tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        print(DiscountData)
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                         
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                # total_disc_amt = total_disc_amt + float(disc_amt)
                # total_desc_rate= total_desc_rate + desc_rate
                # total_vat_amt = total_vat_amt + vat_amt
          
                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no

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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no =so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()


            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                total_sub_total = 0
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])
                    # if so_no == '':
                    #     so_no = items['sales_trans_id']
                    # else:
                    #     if so_no == items['sales_trans_id']:
                    #         so_no = so_no
                    #     else:
                    #         so_no = so_no + ', ' + items['sales_trans_id']

                    # so_doc_no = so_no
                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =items['sales_trans_id'],
                    #     so_doc_no =items['sales_trans_id'],
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()

            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
        
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=456,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
            
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"


            total_disc_amt = float(total_disc_amt)
            total_desc_rate = float(total_desc_rate)
            total_vat_exempt = float(total_vat_exempt)
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                    company_code = f"{companyCode.autonum:0>4}",
                    ul_code = machineInfo.ul_code,
                    site_code = int(machineInfo.site_no),
                    trans_type = 'Cash Sales',
                    discount_type = DiscountType,
                    doc_no = doc_no,
                    doc_type = 'POS-SI',
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    so_no =tmp_so_no,
                    so_doc_no =tmp_so_doc_no,
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
                    ServiceCharge_TotalAmount = ServiceChargeAmount, 
                    total_eps =  AmountDue_formatted,
                    total_qty = totalQty,
                    discount = float(str(total_disc_amt).replace(',', '')),
                    vat = float(str(total_vat_amt).replace(',', '')),
                    vat_exempted = float(str(vat_exempted).replace(',', '')),
                    net_vat = float(str(net_vat).replace(',', '')),
                    net_discount = float(str(net_discount).replace(',', '')),
                    sub_total = float(str(total_sub_total).replace(',', '')),
                   
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
            

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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
            
                    sales_orders_data = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                             terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        ).first()

                    if sales_orders_data:
                            Guest_Count=sales_orders_data.guest_count
                            QueNo = sales_orders_data.q_no
                            table_no = sales_orders_data.table_no
                    
                    sales_orders_to_update = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                            terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        )

                        # Check if there are any matching objects
                    if sales_orders_to_update.exists():
                            # Update all matching objects to set 'paid' to 'Y'
                            sales_orders_to_update.update(paid='Y')
                            
                            pass
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                            q_no=QueNo,
                            paid='N',
                            active='Y',
                             terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        ).first()

                if sales_orders_data:
                            Guest_Count=sales_orders_data.guest_count
                            QueNo = sales_orders_data.q_no
                            table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                            q_no=QueNo,
                            paid='N',
                            active='Y',
                             terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        )

                        # Check if there are any matching objects
                if sales_orders_to_update.exists():
                            # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                            
                    pass  


            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'SeniorDiscountDataList':DiscountDataList,
            } 

            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)

            # transaction.commit()
            return Response({'data':data}, status=200)
        except Exception as e:
            # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()  
            traceback.print_exc()  
            # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status=500)
     
##************ Multiple PAYMENT ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_multiple_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        try:
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            data_from_modal = received_data.get('CustomerPaymentData')
            table_no = received_data.get('TableNo')
            QueNo = received_data.get('QueNo',0)
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            AmountDue = received_data.get('AmountDue')
            CashierName =  received_data.get('CashierName')
            OrderType =  received_data.get('OrderType')
            OrderType =  received_data.get('OrderType')
            Discounted_by= received_data.get('Discounted_by')
            doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
            DiscountDataList = received_data.get('DiscountDataList')
            DiscountType = received_data.get('DiscountType')
            DiscountData= received_data.get('DiscountData')
            QueNo= received_data.get('QueNo')
            DebitCard = received_data.get('DebitCard')
            CreditCard = received_data.get('CreditCard')
            Online = received_data.get('Online')
            GiftCheck = received_data.get('GiftCheck')
            Other = received_data.get('Other')
            CashAmount = received_data.get('CashAmount') 
            doctype = received_data.get('doctype')
            doc_no = get_sales_transaction_id(TerminalNo,doctype)
            serial_number = getattr(request, "SERIALNO", None)
            ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            companyCode = getCompanyData()
            current_datetime = timezone.now()
            datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            Guest_Count = 0
            bankID = ''
            BankName = ''
            OnlineAmount=0
            OtherAmount =0
            GiftCheckAmount = 0
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
                    expiry_date = dt.datetime(int(expiry_year), int(expiry_month), 1)
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
            
            if GiftCheck:
                try:
                    GiftCheck_payments = GiftCheck['GiftCheckPaymentList']
                    for payment in GiftCheck_payments:

                        gift_check_no = payment['gift_check_no']
                        gift_check_count = payment['gift_check_count']
                        amount_due = payment['amount']
                        isIncome = payment['isIncome']
                        if gift_check_no == '':
                            gift_check_no = 0
                        if gift_check_count == '':
                            gift_check_count = 0

                        GiftCheckAmount += amount_due 
                        save_gift_check = POSSalesTransGiftCheck (
                            sales_trans_id = int(float(doc_no)),
                            ul_code = machineInfo.ul_code,
                            site_code = int(machineInfo.site_no),
                            terminal_no = TerminalNo,
                            cashier_id = cashier_id,
                            doc_type = 'SI',
                            datetime_stamp = datetime_stamp,
                            gift_check_no = gift_check_no,
                            gift_check_count = gift_check_count,
                            amount = amount_due,
                        )

                        save_gift_check.save()
                except Exception as e:
                    print('error',e)
                    traceback.print_exc()
            if Online:
                try:
                    raw = Online.get('OnlinekPaymentList',[])
                    online_payments = [raw] if isinstance(raw, dict) else raw
                    for payment in online_payments:

                        date_credited = payment.get('date_credited', None)
                        acct_title = payment.get('acct_title', '')
                        acct_code = payment.get('acct_code', 0)
                        reference_no = payment.get('reference_no', '')
                        sl_type = payment.get('sl_type', '')
                        sl_name = payment.get('sl_name', '')
                        sl_code = payment.get('sl_code', '')
                        remarks = payment.get('remarks', '')
                        total_amount = payment.get('total_amount', 0)

                        OnlineAmount += float(total_amount) 
                        save_online_payment = POSSalesTransOnlinePayment (
                            sales_trans_id = int(float(doc_no)),
                            ul_code = machineInfo.ul_code,
                            site_code = int(machineInfo.site_no),
                            terminal_no = TerminalNo,
                            cashier_id = cashier_id,
                            date_credited=date_credited,
                            date_stamp = datetime_stamp,
                            acct_code = acct_code,
                            acct_title = acct_title,
                            reference_no=reference_no,
                            sl_code=sl_code,
                            sl_name=sl_name,
                            sl_type=sl_type,
                            remarks=remarks,
                            total_amount = total_amount,
                        )

                        save_online_payment.save()
                except Exception as e:
                    print('error',e)
                    traceback.print_exc()

            if Other:
                try:
                    print('Other',Other)
                    raw = Other.get('OtherPaymentList',[])
                    other_payments = [raw] if isinstance(raw, dict) else raw
                    print('other_payments',other_payments)
                    for payment in other_payments:

                        particular = payment.get('particular', None)
                        sl_type = payment.get('sl_type', '')
                        sl_name = payment.get('sl_name', '')
                        sl_code = payment.get('sl_code', '')
                        remarks = payment.get('remarks', '')
                        total_amount = payment.get('total_amount', 0)

                        OtherAmount += float(total_amount) 
                        save_other_payment = POSSalesTransOtherPayment (
                            sales_trans_id = int(float(doc_no)),
                            ul_code = machineInfo.ul_code,
                            site_code = int(machineInfo.site_no),
                            terminal_no = TerminalNo,
                            cashier_id = cashier_id,
                            particular=particular,
                            date_stamp = datetime_stamp,
                            sl_code=sl_code,
                            sl_name=sl_name,
                            sl_type=sl_type,
                            remarks=remarks,
                            total_amount = total_amount,
                        )

                        save_other_payment.save()
                except Exception as e:
                    print('error',e)
                    traceback.print_exc()

            if table_no =='':
                table_no = 0
        
            
            if QueNo == '':
                QueNo = 0
            
            
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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
                

            tmp_cart_item_discount = cart_items
            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    # pdb.set_trace()
                    if DiscountType == 'SC':
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                for x in tmp_cart_item_discount:
                                    if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        print(DiscountData)
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                          
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem == 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                # total_disc_amt = total_disc_amt + float(disc_amt)
                # total_desc_rate= total_desc_rate + desc_rate
                # total_vat_amt = total_vat_amt + vat_amt

                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no

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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no =so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()


            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                # total_sub_total = 0
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                             
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])
                   
                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =so_no,
                    #     so_doc_no =so_doc_no,
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
            
    
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=456,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
            
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                
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
            if bankID == "":
                bankID = 0
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                    company_code = f"{companyCode.autonum:0>4}",
                    ul_code = machineInfo.ul_code,
                    site_code = int(machineInfo.site_no),
                    trans_type = 'Cash Sales',
                    discount_type = DiscountType,
                    doc_no = doc_no,
                    doc_type = 'POS-SI',
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    so_no =tmp_so_no,
                    so_doc_no =tmp_so_doc_no,
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
                    ServiceCharge_TotalAmount = ServiceChargeAmount ,
                    total_cash = "{:.3f}".format(float(CashAmount)),
                    total_eps = "{:.3f}".format(float(DebitCardAmount)),
                    total_credit_card = "{:.3f}".format(float(CreditCardAmount)),
                    other_payment = "{:.3f}".format(float(OtherAmount)),
                    online_payment = "{:.3f}".format(float(OnlineAmount)),
                    gift_check = "{:.3f}".format(float(GiftCheckAmount)),
                    total_qty = totalQty,
                    other_income = 0,
                    discount = float(str(total_disc_amt).replace(',', '')),
                    vat = float(str(total_vat_amt).replace(',', '')),
                    vat_exempted = float(str(vat_exempted).replace(',', '')),
                    net_vat = float(str(net_vat).replace(',', '')),
                    net_discount = float(str(net_discount).replace(',', '')),
                    sub_total = float(str(total_sub_total).replace(',', '')),
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
            

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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
                sales_orders_data = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                             terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
                    
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass

            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass  




            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'SeniorDiscountDataList':DiscountDataList,

            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            
     
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            # transaction.commit()
            return Response({'data':data}, status=200)
        except Exception as e:
            traceback.print_exc()  
            # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()
            
            # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status=500)
     
##************ CHARGE ----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_charge_payment(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            cart_items = received_data.get('data', [])
            data_from_modal = received_data.get('CustomerPaymentData')
            table_no = received_data.get('TableNo')
            QueNo = received_data.get('QueNo',0)
            cashier_id = received_data.get('CashierID')
            TerminalNo = received_data.get('TerminalNo')
            AmountDue = received_data.get('AmountDue')
            CashierName =  received_data.get('CashierName')
            OrderType =  received_data.get('OrderType')
            DiscountDataList = received_data.get('DiscountDataList')
            # doc_no = get_sales_transaction_id(TerminalNo,'POS CI')
            DiscountType = received_data.get('DiscountType')
            DiscountData= received_data.get('DiscountData')
            Discounted_by= received_data.get('Discounted_by')
            QueNo= received_data.get('QueNo')
            Charge = received_data.get('Charge')
            doctype = received_data.get('doctype')
            ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
            doc_no = get_sales_transaction_id(TerminalNo,doctype)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            Guest_Count = 0

            waiterName=''
            
            CategoryID = '0'
            CustomerID ='0'
            CustomerName = ''
            Terms = ''
            Amount = '0'
            CreditLimit ='0'
            last_details_id = 0
            CusAddress = ''
            CusBusiness = ''
            CusTIN =''
            customer_code = '0'
            cust_type = ''
            
                # Get the last details_id
            try:
                last_record = PosSalesTransCreditSale.objects.latest('id')
                last_details_id = last_record.id
            except PosSalesTransCreditSale.DoesNotExist:
                last_details_id = 0  # Assuming a default starting value if no records exist

            # Generate a new details_id for the next record
            new_details_id = last_details_id + 1
            Charge_payments = Charge.get('ChargeCustomerAccount', [])
        
            if Charge_payments:
                CategoryID = Charge_payments.get('CategoryID')
                Category = Charge_payments.get('Category')
                CustomerID = Charge_payments.get('CustomerID')
                CustomerName = Charge_payments.get('CustomerName')
                Terms = Charge_payments.get('Terms')
                CreditLimit = Charge_payments.get('CreditLimit')
                Amountdue = Charge_payments.get('Amountdue')

                save_Charge = PosSalesTransCreditSale (
                    sales_trans_id = int(float(doc_no)),
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    document_type = 'SI',
                    id = new_details_id,
                    id_code = CustomerID,
                    term = Terms,
                    amount = Amount
                    )

                save_Charge.save()

            
                customer = Customer.objects.filter(id_code=CustomerID).first()
                if customer:
                    customer_code = customer.id_code
                    CustomerName = customer.trade_name
                    cust_type = "C"
                    CusAddress = customer.st_address
                    CusBusiness = customer.business_style
                    CusTIN = customer.tax_id_no

            if table_no =='':
                table_no = 0

            if QueNo =='':
                QueNo = 0
        
            current_datetime = timezone.now()
            datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            companyCode = getCompanyData()
            waiterName=''


            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0

                
            tmp_cart_item_discount = cart_items
            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        print(DiscountData)
                        print(DiscountData.get('SAmountCovered').replace(',',''))
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    
                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                for x in tmp_cart_item_discount:
                                    if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        print(DiscountData)
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                     
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    



                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no

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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no =so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()


            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                # total_sub_total = 0
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                              
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])

                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =so_no,
                    #     so_doc_no =so_doc_no,
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
           
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

                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=456,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no
                        )
                    saveSeniorData.save()
                
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"

            total_disc_amt = float(str(total_disc_amt).replace(',', ''))
            total_desc_rate = float(str(total_desc_rate).replace(',', ''))
            total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                    company_code = f"{companyCode.autonum:0>4}",
                    ul_code = machineInfo.ul_code,
                    site_code = int(machineInfo.site_no),
                    trans_type = 'Credit Sales',
                    discount_type = DiscountType,
                    doc_no = doc_no,
                    doc_type = 'POS-CI',
                    terminal_no = TerminalNo,
                    cashier_id = cashier_id,
                    so_no =tmp_so_no,
                    so_doc_no =tmp_so_doc_no,
                    doc_date = datetime_stamp,
                    customer_code = customer_code,
                    customer_name = CustomerName,
                    customer_address = CusAddress,
                    business_unit = CusBusiness,
                    customer_type = cust_type,
                    salesman_id = '0',
                    salesman = '',
                    collector_id = 0,
                    collector = '',
                    pricing = '',
                    terms = 0,
                    remarks = '',
                    ServiceCharge_TotalAmount = ServiceChargeAmount ,
                    total_eps =  AmountDue_formatted,
                    total_qty = totalQty,
                    discount = float(str(total_disc_amt).replace(',', '')),
                    vat = float(str(total_vat_amt).replace(',', '')),
                    vat_exempted = float(str(vat_exempted).replace(',', '')),
                    net_vat = float(str(net_vat).replace(',', '')),
                    net_discount = float(str(net_discount).replace(',', '')),
                    sub_total = float(str(total_sub_total).replace(',', '')),
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
            

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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
            
                sales_orders_data = PosSalesOrder.objects.filter(
                            table_no=table_no,
                            paid='N',
                            active='Y',
                             terminal_no=int(float(machineInfo.terminal_no)),
                            site_code=int(machineInfo.site_no)
                        ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
                    
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass

            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass  




            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'Charge':Charge_payments,
                'SeniorDiscountDataList':DiscountDataList,
            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }

            PDFChargeReceipt(request,doc_no,'POS-CI',cus_Data)
     

            # transaction.commit()
            return Response({'data':data}, status=200)
        except Exception as e:
            print(e)
            # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()  
            traceback.print_exc()  
            # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status=500)
     

##************ GIFT CHECK PAYMENT ONLY----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_gift_check_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        try:
            received_data = json.loads(request.body)
            try:
                cart_items = received_data.get('data', [])
                data_from_modal = received_data.get('CustomerPaymentData')
                table_no = received_data.get('TableNo')
                QueNo = received_data.get('QueNo',0)
                cashier_id = received_data.get('CashierID')
                TerminalNo = received_data.get('TerminalNo')
                AmountDue = received_data.get('AmountDue')
                CashierName =  received_data.get('CashierName')
                OrderType =  received_data.get('OrderType')
                Discounted_by= received_data.get('Discounted_by')
                DiscountDataList = received_data.get('DiscountDataList')
                DiscountType = received_data.get('DiscountType')
                DiscountData= received_data.get('DiscountData')
                QueNo= received_data.get('QueNo')
                GiftCheck = received_data.get('GiftCheck')
                doctype = received_data.get('doctype')
                doc_no = get_sales_transaction_id(TerminalNo,doctype)
                ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
                print('GiftCheck',GiftCheck)
            except Exception as e:
                print('Error',e)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            # pdb.set_trace()
            Guest_Count = 0
            total_gift_check = 0
            isIncome  = False
            total_excess = 0
            if QueNo == '':
                QueNo=0
            if table_no =='':
                table_no = 0
            try:
                current_datetime = timezone.now()
                datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                serial_number = getattr(request, "SERIALNO", None)
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                companyCode = getCompanyData()
            except Exception as e:
                print('error',e)

            waiterName=''


            try:
                GiftCheck_payments = GiftCheck['GiftCheckPaymentList']
                for payment in GiftCheck_payments:

                    gift_check_no = payment['gift_check_no']
                    gift_check_count = payment['gift_check_count']
                    amount_due = payment['amount']
                    isIncome = payment['isIncome']
                    if gift_check_no == '':
                        gift_check_no = 0
                    if gift_check_count == '':
                        gift_check_count = 0

                    total_gift_check += amount_due 
                    save_gift_check = POSSalesTransGiftCheck (
                        sales_trans_id = int(float(doc_no)),
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        doc_type = 'SI',
                        datetime_stamp = datetime_stamp,
                        gift_check_no = gift_check_no,
                        gift_check_count = gift_check_count,
                        amount = amount_due,
                    )

                    save_gift_check.save()
            except Exception as e:
                print('error',e)
                traceback.print_exc()

            if table_no =='':
                table_no = 0
            if QueNo =='':
                QueNo = 0
        

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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
            countxx = 0

                
            tmp_cart_item_discount = cart_items
            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                for x in tmp_cart_item_discount:
                                    if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no

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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no = so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()

            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                # total_sub_total = 0 
                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])

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
                        isvoid = 'NO',
                        unit_cost = unit_cost,
                        vatable = vatable,
                        status = 'A',
                        so_no =items['sales_trans_id'],
                        so_doc_no =items['sales_trans_id'],
                        sn_bc = '',
                        discounted_by = Discounted_by,
                        
                    )
                    SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=0,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
                
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                
                
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"
            print('isIncome',isIncome)
            if isIncome == True:
                total_excess = float(total_gift_check) - AmountDue_float
            print('total_excess',total_excess)
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            try:
                total_disc_amt = float(str(total_disc_amt).replace(',', ''))
                total_desc_rate = float(str(total_desc_rate).replace(',', ''))
                total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
                
                SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                        company_code = f"{companyCode.autonum:0>4}",
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        trans_type = 'Cash Sales',
                        discount_type = DiscountType,
                        doc_no = doc_no,
                        doc_type = 'POS-SI',
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        so_no =tmp_so_no,
                        so_doc_no =tmp_so_doc_no,
                        doc_date = datetime_stamp,
                        customer_code = customer_code,
                        customer_name = CustomerName,
                        customer_address = CusAddress,
                        business_unit = CusBusiness,
                        customer_type = cust_type,
                        salesman_id = '0',
                        salesman = '',
                        pricing = '',
                        terms = 0,
                        remarks = '',
                        ServiceCharge_TotalAmount =  ServiceChargeAmount ,
                        other_income = total_excess,
                        gift_check =  AmountDue_formatted,
                        total_qty = totalQty,
                        discount = float(str(total_disc_amt).replace(',', '')),
                        vat = float(str(total_vat_amt).replace(',', '')),
                        vat_exempted = float(str(vat_exempted).replace(',', '')),
                        net_vat = float(str(net_vat).replace(',', '')),
                        net_discount = float(str(net_discount).replace(',', '')),
                        sub_total = float(str(total_sub_total).replace(',', '')),
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
            except Exception as e:
                print('error',e)

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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


                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
            
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass

            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'GiftCheck':GiftCheck,
                'SeniorDiscountDataList':DiscountDataList,
            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            return Response({'data':data}, status=200)
        except Exception as e:
                # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()
            traceback.print_exc()    
                # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return Response({"message": "An error occurred while saving the sales order"}, status=500)



##************ ONLINE PAYMENT ONLY----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_online_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        try:
            received_data = json.loads(request.body)
            try:
                cart_items = received_data.get('data', [])
                data_from_modal = received_data.get('CustomerPaymentData')
                table_no = received_data.get('TableNo')
                QueNo = received_data.get('QueNo',0)
                cashier_id = received_data.get('CashierID')
                TerminalNo = received_data.get('TerminalNo')
                AmountDue = received_data.get('AmountDue')
                CashierName =  received_data.get('CashierName')
                OrderType =  received_data.get('OrderType')
                Discounted_by= received_data.get('Discounted_by')
                DiscountDataList = received_data.get('DiscountDataList')
                DiscountType = received_data.get('DiscountType')
                DiscountData= received_data.get('DiscountData')
                QueNo= received_data.get('QueNo')
                Online = received_data.get('Online')
                doctype = received_data.get('doctype')
                doc_no = get_sales_transaction_id(TerminalNo,doctype)
                ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)

                print('Online',Online)
            except Exception as e:
                print('Error',e)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            # pdb.set_trace()
            Guest_Count = 0
            total_online = 0

            if QueNo == '':
                QueNo=0
            if table_no =='':
                table_no = 0
            try:
                
                current_datetime = timezone.now()
                datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                serial_number = getattr(request, "SERIALNO", None)
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                companyCode = getCompanyData()
            except Exception as e:
                print('error',e)

            waiterName=''


            try:
                raw = Online.get('OnlinekPaymentList',[])
                online_payments = [raw] if isinstance(raw, dict) else raw
                print('online_payments',online_payments)
                for payment in online_payments:

                    date_credited = payment.get('date_credited', None)
                    acct_title = payment.get('acct_title', '')
                    acct_code = payment.get('acct_code', 0)
                    reference_no = payment.get('reference_no', '')
                    sl_type = payment.get('sl_type', '')
                    sl_name = payment.get('sl_name', '')
                    sl_code = payment.get('sl_code', '')
                    remarks = payment.get('remarks', '')
                    total_amount = payment.get('total_amount', 0)

                    total_online += float(total_amount) 
                    save_online_payment = POSSalesTransOnlinePayment (
                        sales_trans_id = int(float(doc_no)),
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        date_credited=date_credited,
                        date_stamp = datetime_stamp,
                        acct_code = acct_code,
                        acct_title = acct_title,
                        reference_no=reference_no,
                        sl_code=sl_code,
                        sl_name=sl_name,
                        sl_type=sl_type,
                        remarks=remarks,
                        total_amount = total_amount,
                    )

                    save_online_payment.save()
            except Exception as e:
                print('error',e)
                traceback.print_exc()

            if table_no =='':
                table_no = 0
        

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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
            countxx = 0

                
            tmp_cart_item_discount = cart_items
            for items in cart_items:
                disc_amt = 0
                desc_rate= 0
                vat_amt = 0
                vat_exempt = 0
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                for x in tmp_cart_item_discount:
                                    if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no

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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no =so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()

            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                # total_sub_total = 0 

                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])
                    # if so_no == '':
                    #     so_no = items['sales_trans_id']
                    # else:
                    #     if so_no == items['sales_trans_id']:
                    #         so_no = so_no
                    #     else:
                    #         so_no = so_no + ', ' + items['sales_trans_id']

                    # so_doc_no = so_no
                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =items['sales_trans_id'],
                    #     so_doc_no =items['sales_trans_id'],
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=0,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
                
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                
                
            
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            try:
                total_disc_amt = float(str(total_disc_amt).replace(',', ''))
                total_desc_rate = float(str(total_desc_rate).replace(',', ''))
                total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
                SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                        company_code = f"{companyCode.autonum:0>4}",
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        trans_type = 'Cash Sales',
                        discount_type = DiscountType,
                        doc_no = doc_no,
                        doc_type = 'POS-SI',
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        so_no =tmp_so_no,
                        so_doc_no =tmp_so_doc_no,
                        doc_date = datetime_stamp,
                        customer_code = customer_code,
                        customer_name = CustomerName,
                        customer_address = CusAddress,
                        business_unit = CusBusiness,
                        customer_type = cust_type,
                        salesman_id = '0',
                        salesman = '',
                        pricing = '',
                        terms = 0,
                        remarks = '',
                        ServiceCharge_TotalAmount = ServiceChargeAmount ,
                        online_payment=total_online,
                        total_qty = totalQty,
                        discount = float(str(total_disc_amt).replace(',', '')),
                        vat = float(str(total_vat_amt).replace(',', '')),
                        vat_exempted = float(str(vat_exempted).replace(',', '')),
                        net_vat = float(str(net_vat).replace(',', '')),
                        net_discount = float(str(net_discount).replace(',', '')),
                        sub_total = float(str(total_sub_total).replace(',', '')),
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
            except Exception as e:
                print('error',e)

            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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


                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
            
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass

            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'Online':Online,
                'SeniorDiscountDataList':DiscountDataList,
            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            return Response({'data':data}, status=200)
        except Exception as e:
                # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()
            traceback.print_exc()    
                # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return Response({"message": "An error occurred while saving the sales order"}, status=500)



##************ OTHER PAYMENT ONLY----DINE IN---- SAVE TO TBL_POS_SALES_INVOICE_LIST AND LISTING**********************
@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def save_other_payment(request):
    if request.method == 'POST':
        # pdb.set_trace()
        try:
            received_data = json.loads(request.body)
            try:
                cart_items = received_data.get('data', [])
                data_from_modal = received_data.get('CustomerPaymentData')
                table_no = received_data.get('TableNo')
                QueNo = received_data.get('QueNo',0)
                cashier_id = received_data.get('CashierID')
                TerminalNo = received_data.get('TerminalNo')
                AmountDue = received_data.get('AmountDue')
                CashierName =  received_data.get('CashierName')
                OrderType =  received_data.get('OrderType')
                Discounted_by= received_data.get('Discounted_by')
                DiscountDataList = received_data.get('DiscountDataList')
                DiscountType = received_data.get('DiscountType')
                DiscountData= received_data.get('DiscountData')
                QueNo= received_data.get('QueNo')
                Other = received_data.get('Other')
                doctype = received_data.get('doctype')
                doc_no = get_sales_transaction_id(TerminalNo,doctype)
                ServiceChargeAmount = received_data.get('ServiceChargeAmountD',0)
                print('Other',Other)
            except Exception as e:
                print('Error',e)
            # CreditCardPaymentListData = CreditCard.get("CreditCardPaymentList")
            # pdb.set_trace()
            Guest_Count = 0
            total_other = 0

            if QueNo == '':
                QueNo=0
            if table_no =='':
                table_no = 0
            try:
                current_datetime = timezone.now()
                datetime_stamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                serial_number = getattr(request, "SERIALNO", None)
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                companyCode = getCompanyData()
            except Exception as e:
                print('error',e)

            waiterName=''


            try:
                raw = Other.get('OtherPaymentList',[])
                other_payments = [raw] if isinstance(raw, dict) else raw
                print('online_payments',other_payments)
                for payment in other_payments:

                    particular = payment.get('particular', None)
                    sl_type = payment.get('sl_type', '')
                    sl_name = payment.get('sl_name', '')
                    sl_code = payment.get('sl_code', '')
                    remarks = payment.get('remarks', '')
                    total_amount = payment.get('total_amount', 0)

                    total_other += float(total_amount) 
                    save_other_payment = POSSalesTransOtherPayment (
                        sales_trans_id = int(float(doc_no)),
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        particular=particular,
                        date_stamp = datetime_stamp,
                        sl_code=sl_code,
                        sl_name=sl_name,
                        sl_type=sl_type,
                        remarks=remarks,
                        total_amount = total_amount,
                    )

                    save_other_payment.save()
            except Exception as e:
                print('error',e)
                traceback.print_exc()

            if table_no =='':
                table_no = 0
            if QueNo =='':
                QueNo = 0

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
            tmp_so_no = ''
            tmp_so_doc_no = ''
            so_no = 0
            so_doc_no = ''
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
            unit_cost = 0
            Vatable_Amount = 0
            countxx = 0

                
            tmp_cart_item_discount = cart_items
            for items in cart_items:
                productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                

                if productInfo is not None:
                    quantity = float(items['quantity'])
                    price = float(items['price'])
                    item_disc = float(items['item_disc'])
                    total_sub_total = total_sub_total + (quantity * price)
                    
                    if DiscountType == 'SC':
                        SCAmmountCovered = float(DiscountData.get('SAmountCovered').replace(',',''))
                        SLess20SCDiscount = float(DiscountData.get('SLess20SCDiscount').replace(',',''))
                        SLessVat12 =  float(DiscountData.get('SLessVat12').replace(',',''))
                        SNetOfVat =  float(DiscountData.get('SNetOfVat').replace(',',''))
                        SVatSales =  float(DiscountData.get('SVatSales').replace(',',''))
                        vatable = 'Es'
                        desc_rate = 20
                        totalItem = quantity * price
                            
                        NetSale =  totalItem / (0.12 + 1 )
                        vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                        disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                        net_total = (totalItem) - (disc_amt + vat_exempt)
                        vat_amt =(totalItem / (0.12 + 1 ) * 0.12) * (SVatSales -SCAmmountCovered) / SVatSales
                        Vatable_Amount = SVatSales - SCAmmountCovered

                    elif DiscountType =='ITEM':
                        for dis in DiscountData:

                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('LineNo', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['Barcode'] == items['barcode'] and lineNO == items['line_no']:
                                
                                for x in tmp_cart_item_discount:
                                    if x['barcode'] == items['barcode'] and x['line_no'] == items['line_no']:
                                        tmp_cart_item_discount.remove(x)
                                vatable = 'V'
                                desc_rate = float(dis['D1'])
                                totalItem = quantity * price
                                item_disc = float(dis['D1'])
                                NetSale =  float(dis['DiscountedPrice'])
                                vat_exempt =  0
                                disc_amt  = float(dis['ByAmount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt
                    elif DiscountType =='TRANSACTION':
                        for dis in DiscountData:
                            lineNO = 0
                            if dis.get('line_no') is None:
                                lineNO = dis.get('lineno', 0)  # Use 'lineno' with a default value of 0 if 'line_no' is None
                            else:
                                lineNO = dis['line_no']

                            if dis['barcode'] == items['barcode'] and lineNO == items['line_no']:
                                desc_rate = float(dis['desc_rate'])
                                vatable = 'V'
                                totalItem = quantity * price
                                item_disc = float(dis['desc_rate'])
                                vat_exempt =  0
                                disc_amt  = float(dis['Discount'])
                                net_total = (totalItem - disc_amt)
                                vat_amt = ((totalItem - disc_amt) / 1.12) * 0.12
                                unit_cost = (totalItem) 
                                Vatable_Amount = (totalItem + Vatable_Amount) - disc_amt

                    else:
                        if productInfo.tax_code == 'VAT':
                            vatable = 'V'
                            totalItem = quantity * price
                            if totalItem != 0:
                                
                                desc_rate = item_disc / (totalItem) * 100
                                vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                disc_amt = item_disc
                                net_total = (totalItem - item_disc)
                                Vatable_Amount = (totalItem + Vatable_Amount)
                                unit_cost = totalItem
                        else:
                            vatable = 'N'
                            vat_amt = 0
                            disc_amt = item_disc
                            net_total = (quantity * price) - disc_amt
                else:
                    # Handle case where productInfo is None (no product found for the barcode)
                    pass  # You might want to log this or handle it according to your logic
                    

                if DiscountType == 'SC':
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) +float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                else:
                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                
                # pdb.set_trace()
                totalQty = totalQty + float(items['quantity'])
                if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        table_no=table_no,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
                
                else:
                    sales_orders_data = PosSalesOrder.objects.filter(
                        q_no=QueNo,
                        paid='N',
                        active='Y',
                        terminal_no=int(float(machineInfo.terminal_no)),
                        site_code=int(float(machineInfo.site_no))
                    ).first()
                    if sales_orders_data:
                        so_no=sales_orders_data.SO_no
                        so_doc_no=sales_orders_data.document_no
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
                    isvoid = 'NO',
                    unit_cost = unit_cost,
                    vatable = vatable,
                    status = 'A',
                    so_no =so_no,
                    so_doc_no =so_doc_no,
                    sn_bc = '',
                    discounted_by = Discounted_by,
                    
                )
                SaveToPOSSalesInvoiceListing.save()

            if DiscountType == 'ITEM' or DiscountType == 'TRANSACTION':
                # total_sub_total = 0

                for items in tmp_cart_item_discount:
                    productInfo = Product.objects.filter(bar_code=items['barcode']).first()
                    if productInfo is not None:
                        quantity = float(items['quantity'])
                        price = float(items['price'])
                        item_disc = float(items['item_disc'])
                        total_sub_total = total_sub_total + (quantity * price)
                        if productInfo.tax_code == 'VAT':
                               
                                vatable = 'V'
                                totalItem = quantity * price
                                if totalItem != 0:
                                    desc_rate = item_disc / (totalItem) * 100
                                    vat_amt = ((totalItem - item_disc) / 1.12) * 0.12
                                    disc_amt = item_disc
                                    net_total = (totalItem - item_disc)
                                    Vatable_Amount = (totalItem + Vatable_Amount)
                                    unit_cost = totalItem
                        else:
                                vatable = 'N'
                                vat_amt = 0
                                disc_amt = item_disc
                                net_total = (quantity * price) - disc_amt
                    else:
                        # Handle case where productInfo is None (no product found for the barcode)
                        pass  # You might want to log this or handle it according to your logic
                        

                    total_net_total = total_net_total + net_total
                    total_vat_exempt = vat_exempt + total_vat_exempt
                    total_disc_amt = float(disc_amt) + float(total_disc_amt)
                    total_desc_rate= desc_rate 
                    total_vat_amt = vat_amt + total_vat_amt
                    
                    # pdb.set_trace()
                    # totalQty = totalQty + float(items['quantity'])
   
                    # SaveToPOSSalesInvoiceListing = PosSalesInvoiceListing(
                    #     company_code = f"{companyCode.autonum:0>4}",
                    #     ul_code = machineInfo.ul_code,
                    #     terminal_no = TerminalNo,
                    #     site_code = int(machineInfo.site_no),
                    #     cashier_id = cashier_id,
                    #     doc_date = datetime_stamp,
                    #     doc_no = doc_no,
                    #     doc_type = 'POS-SI',
                    #     line_number = items['line_no'],
                    #     bar_code =items['barcode'],
                    #     alternate_code = 0,
                    #     item_code = items['barcode'],
                    #     rec_qty = items['quantity'],
                    #     rec_uom = productInfo.uom,
                    #     description = items['description'],
                    #     unit_price = items['price'],
                    #     sub_total = float(items['quantity']) * float(items['price']),
                    #     pc_price =  items['price'],
                    #     qtyperuom = 1,
                    #     disc_amt = f"{disc_amt:.3f}",
                    #     desc_rate =f"{desc_rate:.3f}",
                    #     vat_amt =  f"{vat_amt:.3f}",
                    #     vat_exempt = f"{vat_exempt:.3f}",
                    #     net_total =  f"{net_total:.3f}",
                    #     isvoid = 'NO',
                    #     unit_cost = unit_cost,
                    #     vatable = vatable,
                    #     status = 'A',
                    #     so_no =so_no,
                    #     so_doc_no =so_doc_no,
                    #     sn_bc = '',
                    #     discounted_by = Discounted_by,
                        
                    # )
                    # SaveToPOSSalesInvoiceListing.save()


            Vatable_Amount = float(Vatable_Amount) - float(total_vat_amt)
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
                count = len(DiscountDataList)
                # SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) * int(count)
                SCAmmountCovered =  float(str(DiscountData['SAmountCovered']).replace(',','')) 
                for item in DiscountDataList:
                    saveSeniorData  = PosSalesTransSeniorCitizenDiscount(
                            sales_trans_id=int(float(doc_no)),
                            terminal_no=TerminalNo,
                            cashier_id=cashier_id,
                            document_type=doctype,
                            details_id=0,
                            id_no=item['SID'],
                            senior_member_name=item['SName'],
                            id=0,
                            tin_no=item['STIN'],
                            so_no=so_no,
                            amount_covered=SCAmmountCovered
                        )
                    saveSeniorData.save()
                
            elif DiscountType == 'ITEM':
                DiscountType='IM'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)

            elif DiscountType == 'TRANSACTION':
                DiscountType='TRSD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            elif DiscountType == 'TRADE':
                DiscountType='TRD'
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
            else:   
                net_vat = total_sub_total - (total_disc_amt + total_vat_amt + total_vat_exempt)
                net_discount = total_sub_total - (total_disc_amt + total_vat_exempt)
                
                
            AmountDue_without_comma = AmountDue.replace(',', '')
            # Convert the modified string to a float
            AmountDue_float = float(AmountDue_without_comma)
            
            AmountDue_float = float(AmountDue_float)       
            AmountDue_formatted = f"{AmountDue_float:.3f}"
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no))
                 )
                    
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(float(machineInfo.site_no)))
            if sales_orders_data.exists():
                for so_data in sales_orders_data:
                    if tmp_so_no == '':
                        tmp_so_no = so_data.SO_no
                        tmp_so_doc_no = so_data.document_no
                    else:
                        tmp_so_no = str(tmp_so_no) + ',' + str(so_data.SO_no)
                        tmp_so_doc_no = str(tmp_so_doc_no) + ',' + str(so_data.document_no)
            try:
                total_disc_amt = float(str(total_disc_amt).replace(',', ''))
                total_desc_rate = float(str(total_desc_rate).replace(',', ''))
                total_vat_exempt = float(str(total_vat_exempt).replace(',', ''))
                SaveToPOSSalesInvoiceList = PosSalesInvoiceList (
                        company_code = f"{companyCode.autonum:0>4}",
                        ul_code = machineInfo.ul_code,
                        site_code = int(machineInfo.site_no),
                        trans_type = 'Cash Sales',
                        discount_type = DiscountType,
                        doc_no = doc_no,
                        doc_type = 'POS-SI',
                        terminal_no = TerminalNo,
                        cashier_id = cashier_id,
                        so_no =tmp_so_no,
                        so_doc_no =tmp_so_doc_no,
                        doc_date = datetime_stamp,
                        customer_code = customer_code,
                        customer_name = CustomerName,
                        customer_address = CusAddress,
                        business_unit = CusBusiness,
                        customer_type = cust_type,
                        salesman_id = '0',
                        salesman = '',
                        pricing = '',
                        terms = 0,
                        remarks = '',
                        ServiceCharge_TotalAmount = ServiceChargeAmount ,
                        other_payment=total_other,
                        total_qty = totalQty,
                        discount = float(str(total_disc_amt).replace(',', '')),
                        vat = float(str(total_vat_amt).replace(',', '')),
                        vat_exempted = float(str(vat_exempted).replace(',', '')),
                        net_vat = float(str(net_vat).replace(',', '')),
                        net_discount = float(str(net_discount).replace(',', '')),
                        sub_total = float(str(total_sub_total).replace(',', '')),
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
            except Exception as e:
                print('error',e)
            print(2)
            if OrderType == 'DINE IN' and table_no != 0 and QueNo == 0:
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


                sales_orders_data = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()
                print(3)
                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no
            
                sales_orders_to_update = PosSalesOrder.objects.filter(
                    table_no=table_no,
                    paid='N',
                    active='Y',
                    terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass
            else:
                sales_orders_data = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                ).first()

                if sales_orders_data:
                    Guest_Count=sales_orders_data.guest_count
                    QueNo = sales_orders_data.q_no
                    table_no = sales_orders_data.table_no

                sales_orders_to_update = PosSalesOrder.objects.filter(
                    q_no=QueNo,
                    paid='N',
                    active='Y',
                     terminal_no=int(float(machineInfo.terminal_no)),
                    site_code=int(machineInfo.site_no)
                )

                # Check if there are any matching objects
                if sales_orders_to_update.exists():
                    # Update all matching objects to set 'paid' to 'Y'
                    sales_orders_to_update.update(paid='Y')
                    
                    pass
            print(4)
            UpdateINVRef = InvRefNo.objects.filter(description=doctype,terminalno=TerminalNo).first()
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
                'VATable': '{:,.2f}'.format(Vatable_Amount),
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
                'Other':Other,
                'SeniorDiscountDataList':DiscountDataList,
            } 
            cus_Data = {
                'CustomerName' :CustomerName,
                'CusTIN' :CusTIN,
                'CusAddress' :CusAddress,
                'CusBusiness' : CusBusiness,
                'TableNo':table_no,
                'Guest_Count':Guest_Count,
                'QueNo':QueNo
                }
            # transaction.commit()
            PDFReceipt(request,doc_no,'POS-SI',cus_Data)
            return Response({'data':data}, status=200)
        except Exception as e:
                # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()
            traceback.print_exc()    
                # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
    else:
        return Response({"message": "An error occurred while saving the sales order"}, status=500)









###*************** SAVE AFTER CASH COUNT END SHIFT-----*******************
@api_view(['GET','POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
def cash_breakdown(request):
    if request.method == 'GET':
        cash_breakdown = PosCashBreakdown.objects.filter(login_record='1')
        serialize = PosCashBreakdownSerializer(cash_breakdown,many=True)
        return JsonResponse({'CashBreakdown':serialize.data},status=200)
    elif request.method == 'POST':
        # pdb.set_trace()
        try:
            data_recieve = json.loads(request.body)
            TransID = data_recieve.get('TransID')
            data = data_recieve.get('data')
            Type = data_recieve.get('Type')
            CashierID = data_recieve.get('CashierID')
            FullName = data_recieve.get('FullName')
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
            if Type == 'END SHIFT':
                # Create a new instance of the PosCashBreakdown model for each key-value pair
                for denomination, quantity in dinomination.items():
                    if int(quantity) > 0:
                        trans_id = 0
                        value = conversion_rates[denomination]
                        
                        try:
                            last_record = PosCashBreakdown.objects.latest('trans_id')
                            trans_id = last_record.trans_id + 1
                        except PosCashBreakdown.DoesNotExist:
                            trans_id = 1
                        breakdown_instance = PosCashBreakdown(
                                trans_id=trans_id,
                                login_record=TransID,  # Provide appropriate value
                                date_stamp=current_date_ph,  # Provide appropriate value
                                quantity=quantity,
                                denomination = f'Php {float(value):,.2f}',
                                total=float(value) * int(quantity),  # Get the total amount by multiplying quantity with value
                                reviewed_by=0,  # Provide appropriate value
                            )
                        breakdown_instance.save()
            elif Type == 'CASH PULL OUT':
                trans_id = 0
                login_record = 0
                pullout_by = ''
                pullout_name = ''
                verify_by = ''
                serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
                date_stamp = GetPHilippineDateTime()
                try:
                    last_record = PosCashiersLogin.objects.latest('trans_id')
                    login_record = last_record.trans_id
                except PosCashPullout.DoesNotExist:
                    trans_id = 1
                try:
                    last_record = PosCashPullout.objects.latest('trans_id')
                    trans_id = last_record.trans_id + 1
                except PosCashPullout.DoesNotExist:
                    trans_id = 1
                for denomination, quantity in dinomination.items():
                    if int(quantity) > 0:
                        value = conversion_rates[denomination]
                        
                        details_id = 0
                        try:
                            last_record = PosCashPulloutDetails.objects.latest('details_id')
                            details_id = last_record.details_id + 1
                        except PosCashPulloutDetails.DoesNotExist:
                            details_id = 1  # Return None if no records exist in the table

                        save_cash_pullout_details = PosCashPulloutDetails(
                                trans_id=trans_id,  # Provide appropriate value
                                details_id=details_id,  # Provide appropriate value
                                quantity=quantity,
                                denomination = f'Php {float(value):,.2f}',
                                total=float(value) * int(quantity),  # Get the total amount by multiplying quantity with value
                            )
                        save_cash_pullout_details.save()
                save_cash_pullout = PosCashPullout(
                    trans_id = trans_id,
                    login_record = login_record,
                    terminal_no = machineInfo.terminal_no,
                    datetime_stamp = date_stamp,
                    pullout_by = CashierID,
                    pullout_name = FullName,
                    verified_by = verify_by,
                )
                save_cash_pullout.save()

                    # transaction.commit()

            PDFCashBreakDown(request,TransID)
            return JsonResponse({'message':"This endpoint is for POST requests only."},status=200)      
        except Exception as e:
            print(e)
            traceback.print_exc()
            # If any error occurs during the save operations, rollback the transaction
            transaction.rollback()  
            # Optionally, log the error or handle it in some way
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
        

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_sales_list_of_transaction(request):
    if request.method =='GET':
        try:

            DateFrom = request.GET.get('DateFrom')
            DateTo = request.GET.get('DateTo')
            DocType = request.GET.get('DocType')
            DocNo = request.GET.get('DocNo')
            sales_list=[]
            if DateFrom and DateTo:
                DateFrom1 = datetime.strptime(DateFrom, '%Y-%m-%d')  # Example start date
                DateTo1 = datetime.strptime(DateTo, '%Y-%m-%d')    # Example end date

                DateTo_datetime = DateTo1.replace(hour=23, minute=59, second=59)

            
                if DocNo and DateFrom and DocType:
                    sales_list = PosSalesInvoiceList.objects.filter(doc_date__range=(DateFrom1,DateTo_datetime),doc_type =DocType,doc_no=DocNo)
                else:
                    sales_list = PosSalesInvoiceList.objects.filter(doc_date__range=(DateFrom1,DateTo_datetime),doc_type =DocType)

                serialize = PosSalesInvoiceListSerializer(sales_list,many=True)
                return Response(serialize.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'POST':
        try:
            receive_data = json.loads(request.body)
            data = receive_data.get('data')
            verify_data = receive_data.get('verify')

            verify_id = verify_data.get('Veriusername')
            verify_name = verify_data.get('VeriFullname')
            currentDate = GetPHilippineDateTime()

            if data:
                doc_no = data.get('doc_no')
                terminal_no = data.get('terminal_no')
                site_code =  data.get('site_code')
                doc_type =  data.get('doc_type')

                

                sales_list = PosSalesInvoiceList.objects.filter(
                    doc_no=doc_no,
                    terminal_no=terminal_no,
                    site_code=site_code,
                    doc_type=doc_type,
                    status = 'S',
                ).first()

                if sales_list:
                    sales_list.status = 'N'
                    sales_list.cancel_by= verify_name
                    sales_list.cancel_date = currentDate
                    sales_list.save()
            return Response('Success')
        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_gift_check(request):
    try:
        gift_check_no = request.GET.get("gift_check_no")  # or POST if needed

        if not gift_check_no:
            return JsonResponse({"success": False, "message": "Gift Check number is required"}, status=400)

        # 1️⃣ Check if already used
        if POSSalesTransGiftCheck.objects.filter(gift_check_no=gift_check_no).exists():
            return JsonResponse({
                "success": False,
                "message": "Gift Check already used!"
            }, status=400)

        # 2️⃣ Check if exists in series
        gift_check = POSGiftCheckSeries.objects.filter(
            series_from__lte=gift_check_no,
            series_to__gte=gift_check_no
        ).first()

        if not gift_check:
            return JsonResponse({
                "success": False,
                "message": "Gift Check is not on the list!"
            }, status=400)

        now = timezone.now().date()
        validity_date_from = dt.datetime.strptime(gift_check.validity_date_from, "%Y-%m-%d").date()
        validity_date_to = dt.datetime.strptime(gift_check.validity_date_to, "%Y-%m-%d").date()

        # 3️⃣ Check validity dates
        if now < validity_date_from:
            return JsonResponse({
                "success": False,
                "message": f"Gift Check validity starts on {gift_check.validity_date_from.strftime('%B %d, %Y')}!"
            }, status=400)

        if now > validity_date_to:
            return JsonResponse({
                "success": False,
                "message": "Gift Check has expired!"
            }, status=400)

        # ✅ Valid
        return JsonResponse({
            "success": True,
            "message": "Gift Check is valid",
            "amount": float(gift_check.amount)
        })
    except Exception as e:
        print('error',e)
        traceback.print_exc()
        return JsonResponse({
                "success": False,
                "message": "Request failed"
            }, status=501)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_denomination(request):
    try:
        deno = POSGiftCheckDenomination.objects.all()
        serialize = POSGiftCheckDenominationSerializer(deno,many=True)
        return Response(serialize.data)
    except Exception as e:
        print('error',e)
        traceback.print_exc()
        return JsonResponse({
                "success": False,
                "message": "Request failed"
            }, status=501)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_acct_title(request):
    try:
        _list = AcctSubsidiary.objects.all().order_by('subsidiary_acct_title')
        serialize = AcctSubsidiaryTitleSerializer(_list,many=True)
        return Response(serialize.data)

    except Exception as e:
        print('error',e)
        traceback.print_exc()



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSLname(request):

        try:
            SLType = request.GET.get('sl_type')
            sl_name =  request.GET.get('sl_name')
            print('xxxx',SLType)
            # SLType = data.get('st_type', '')
            if SLType == 'S':
                output =  MainRefSlSupplier.objects.annotate(concat_address=Concat(Cast(models.F('address'), CharField()), Value(', '),
                                                                                    Cast(models.F('city_municipality'), CharField()), Value(', '),
                                                                                    Cast(models.F('province'), CharField()), Value(', '),
                                                                                    Cast(models.F('zip_code'), CharField()))
                                                        ).filter( active='Y'
                                                        ).values('concat_address',name=models.F('trade_name'),idcode=models.F('id_code')).order_by('trade_name')
                return Response(output)
            elif SLType == 'C':
                    try:
                        print(11)
                        output =  MainRefCustomer.objects.annotate(concat_address=Concat(Cast(models.F('st_address'), CharField()), Value(', '),
                                                                                        Cast(models.F('city_address'), CharField()), Value(''))
                                                        ).filter(active='Y'
                                                        ).values('concat_address',name=models.F('trade_name'),idcode=models.F('id_code')).order_by('trade_name')
                        print('output',output)
                        return Response(output)
                    except Exception as e:
                        print('error',e) 
                    
            elif SLType == 'E':
                    output =  Employee.objects.annotate(name=Concat(Cast(models.F('last_name'), CharField()),Value(', '),
                                                                                Cast(models.F('first_name'), CharField()),Value(' '),
                                                                                Cast(models.F('middle_name'), CharField())),
                                                                    concat_address=Concat(Cast(models.F('address'), CharField()), Value(', '),
                                                                                    Cast(models.F('city_municipality'), CharField()), Value(', '),
                                                                                    Cast(models.F('province'), CharField()), Value(', '),
                                                                                    Cast(models.F('zip_code'), CharField()))
                                                    ).filter(active_status='Y'
                                                    ).values('concat_address','name',idcode=models.F('id_code')).order_by('name')
                    return Response(output)
                                       
            elif SLType == 'P':
                    output =  MainRefSlSupplier.objects.annotate(concat_address=Concat(Cast(models.F('address'), CharField()), Value(', '),
                                                                                    Cast(models.F('city_municipality'), CharField()), Value(', '),
                                                                                    Cast(models.F('province'), CharField()), Value(', '),
                                                                                    Cast(models.F('country'), CharField()), Value(', '),
                                                                                    Cast(models.F('zip_code'), CharField()))
                                                        ).filter(active_status='Y').values('concat_address',name=models.F('trade_name'),idcode=models.F('id_code')).order_by('trade_name')
                    return Response(output)                   
            elif SLType == 'O':
                    output =  OtherAccount.objects.filter(active='Y',acct_title__icontains= sl_name
                                                    ).values(concat_address=Value(''),name=models.F('sl_name'),idcode=models.F('id_code')).order_by('sl_name')
                    return Response(output)
                
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_other_payment_setup(request):
    try:
        _list = PosOtherPmtSetup.objects.all().order_by('pmt_desc')
        serialize = PosOtherPmtSetupPaymentSerializer(_list,many=True)
        return Response(serialize.data)

    except Exception as e:
        print('error',e)
        traceback.print_exc()


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def tmp_sc_discount(request):
    if request.method =='GET':
        try:
            terminal_no = request.GET.get('terminal_no')
            so_no = request.GET.get('so_no')
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()

            summary = TmpPosWebScDiscountList.objects.filter(
                so_no=so_no,
                terminal_no=terminal_no,
                site_no=machineInfo.site_no
            ).values('SeniorCount','SGuestCount','SAmountCovered',
                     'SVatSales','SLessVat12','SNetOfVat',
                     'SLess20SCDiscount','SDiscountedPrice')
            

            if summary.exists():
            # Fetch the per-senior details (Listing)
                details = TmpPosWebScDiscountListing.objects.filter(
                    so_no=so_no,
                    terminal_no=terminal_no,
                    site_no=machineInfo.site_no
                ).values(
                    'SID',
                    'STIN',
                    SName=F('SNAME'),  # Rename SNAME to SName
                )
                response = {
                    "summary": summary,
                    "details": details  # array of seniors
                }
                return Response(response)
            else:
                return JsonResponse({"status": "error", "message": "No records found"}, status=404)

        except Exception as e:
            print(e)
            traceback.print_exc()

    elif request.method == "POST":
        try:
           
            _list = request.data.get('list',None)
            listing_data = request.data.get("listing", [])
            so_no = request.data.get('so_no',0)
            sales_trans_id = request.data.get('sales_trans_id',0)

            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            cashier_id = request.user.id_code
            
            TmpPosWebScDiscountList.objects.filter(so_no=so_no,terminal_no=machineInfo.terminal_no,site_no=machineInfo.site_no).delete()
            TmpPosWebScDiscountListing.objects.filter(so_no=so_no,terminal_no=machineInfo.terminal_no,site_no=machineInfo.site_no).delete()


            # Create TmpPosWebScDiscountList entry
            discount_list = TmpPosWebScDiscountList(
                terminal_no=machineInfo.terminal_no, 
                site_no=machineInfo.site_no,
                cashier_id=cashier_id,
                so_no=so_no,
                SeniorCount=_list.get("SeniorCount", 0),
                SGuestCount=_list.get("SGuestCount", 0),
                SAmountCovered=_list.get("SAmountCovered", 0.000),
                SVatSales=_list.get("SVatSales", 0.000),
                SLessVat12=_list.get("SLessVat12", 0.000),
                SNetOfVat=_list.get("SNetOfVat", 0.000),
                SLess20SCDiscount=_list.get("SLess20SCDiscount", 0.000),
                SDiscountedPrice=_list.get("SDiscountedPrice", 0.000),
            )

            discount_list.save()

            pos_details_listing = PosSalesTransDetails.objects.filter(sales_trans_id=sales_trans_id,
                                                                      terminal_no=int(machineInfo.terminal_no),
                                                                      site_code=int(machineInfo.site_no)) 
            if pos_details_listing.exists():

                for items in pos_details_listing:
                    quantity = items.quantity
                    price = items.price
                    barcode = items.barcode
                    line_no = items.line_no
               
                    SeniorCount = float(_list.get('SeniorCount'))
                    SGuestCount = float(_list.get('SGuestCount'))
                    SCAmmountCovered = float(_list.get('SAmountCovered').replace(',',''))
                    SLess20SCDiscount = float(_list.get('SLess20SCDiscount').replace(',',''))
                    SLessVat12 =  float(_list.get('SLessVat12').replace(',',''))
                    SNetOfVat =  float(_list.get('SNetOfVat').replace(',',''))
                    SVatSales =  float(_list.get('SVatSales').replace(',',''))

                    
                    
                    total = quantity * price  
                    
                    if SeniorCount == SGuestCount:
                        totalItem = total
                    
                    else:
                        total = total / SGuestCount
                        totalItem = total * SeniorCount


                    vat_exempt =  (totalItem / (0.12 + 1 ) * 0.12) * (SCAmmountCovered / SVatSales)
                    disc_amt  = (totalItem / (0.12 + 1 ) * 0.2) * (SCAmmountCovered / SVatSales)
                    print('vat Exempt',vat_exempt)
                    print('dis_amt',disc_amt)

                    update = PosSalesTransDetails.objects.filter(sales_trans_id=sales_trans_id,
                                                                      terminal_no=int(machineInfo.terminal_no),
                                                                      site_code=int(machineInfo.site_no),
                                                                      line_no=line_no,barcode=barcode).first()
                    if update:
                        update.item_disc = disc_amt
                        update.vat_ex = vat_exempt
                        update.desc_rate = SLess20SCDiscount

                        update.save()

           
            listing_objects = []
            for item in listing_data:
                listing_objects.append(
                    TmpPosWebScDiscountListing(
                        terminal_no=machineInfo.terminal_no, 
                        site_no=machineInfo.site_no,
                        cashier_id=cashier_id,
                        so_no=so_no,
                        SID=item.get("SID", 0),
                        SNAME=item.get("SName", ""),
                        STIN=item.get("STIN", ""),
                    )
                )
            TmpPosWebScDiscountListing.objects.bulk_create(listing_objects)

            return JsonResponse({"status": "success", "message": "Discount entries created successfully."})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)})

    traceback.print_exc()
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@api_view(['GET'])
@transaction.atomic     
@permission_classes([IsAuthenticated])
def get_price_type_list(request):
    if request.method == 'GET':
        try:
            serial_number = getattr(request,'SERIALNO',None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            product_setup = PosMultiplePriceTypeSiteSetup.objects.filter(site_code=int(machineInfo.site_no))
            serialize = PosMultiplePriceTypeSiteSetupSerializer(product_setup,many=True)

            return Response(serialize.data)
        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['POST'])
@transaction.atomic  
@permission_classes([IsAuthenticated])
def void_so_listing(request):
    if request.method =='POST':
        try:
            _list = request.data.get('list',[])
            serial_number = getattr(request,'SERIALNO',None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            terminal_no = int(machineInfo.terminal_no)
            site_no = int(machineInfo.site_no)
            if _list:
                bar_code = _list.get('barcode')
                sales_trans_id = _list.get('sales_trans_id')
                line_no = _list.get('line_no')

                PosSalesTransDetails.objects.filter(
                    sales_trans_id=sales_trans_id,
                    barcode=bar_code,
                    line_no=line_no,
                    site_code = site_no,
                    terminal_no=terminal_no
                ).update(isvoid='YES')

            updated2 = PosSalesTransDetails.objects.filter(
                sales_trans_id=sales_trans_id,
                isvoid='NO',
                site_code = site_no,
                terminal_no=terminal_no
            )

            if not updated2.exists():
                PosSalesOrder.objects.filter(document_no=sales_trans_id,
                    site_code = site_no,
                    terminal_no=terminal_no).update(active='N')
                PosSalesTrans.objects.filter(sales_trans_id=sales_trans_id,
                    document_type='SO',
                    site_code = site_no,
                    terminal_no=terminal_no).update(isvoid='YES')
            return Response('Successfully Update')
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({'Error':'Request Failed'},status=400)
            
@api_view(['POST'])
@transaction.atomic  
def void_so(request):
    if request.method =='POST':
        try:
            _list = request.data.get('list',[])
            serial_number = getattr(request,'SERIALNO',None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            terminal_no = int(machineInfo.terminal_no)
            site_no = int(machineInfo.site_no)
            if _list:
                sales_trans_id = _list.get('document_no')
                PosSalesTransDetails.objects.filter(
                    sales_trans_id=sales_trans_id,
                    site_code = site_no,
                    terminal_no=terminal_no
                ).update(isvoid='YES')

                updated2 = PosSalesTransDetails.objects.filter(
                    sales_trans_id=sales_trans_id,
                    isvoid='NO',
                    site_code = site_no,
                    terminal_no=terminal_no
                )

                if not updated2.exists():
                    PosSalesOrder.objects.filter(document_no=sales_trans_id,
                        site_code = site_no,
                        terminal_no=terminal_no).update(active='N')
                    PosSalesTrans.objects.filter(sales_trans_id=sales_trans_id,
                        document_type='SO',
                        site_code = site_no,
                        terminal_no=terminal_no).update(isvoid='YES')
            return Response('Successfully Update')
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({'Error':'Request Failed'},status=400)
           

          


