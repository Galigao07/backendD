import abc
import base64
import json
import locale
import os
import pdb
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from backend.models import *
from backend.serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime
from django.db.models import Sum
import traceback
import subprocess
import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings
from backend.views import paginate_queryset



# @api_view(['GET'])
# def get_product_profile(request):
#     # 1. Query all products
#     products = Product.objects.all().order_by('-autonum')

#     # 2. Use DRF default pagination
#     paginator_class = api_settings.DEFAULT_PAGINATION_CLASS
#     paginator = paginator_class()
    
#     paginated_products = paginator.paginate_queryset(products, request)
    
#     # 3. Serialize paginated data
#     serializer = Product2Serializer(paginated_products, many=True)
    
#     # 4. Return paginated response
#     return paginator.get_paginated_response(serializer.data)

@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
def get_product_profile(request):
    if request.method =='GET':
        # Query all products ordered by autonum descending
        # products = Product.objects.all().order_by('-autonum')

        description = request.GET.get('Search')
        if description== None:
            products = Product.objects.all().order_by('-autonum')
            return paginate_queryset(request, products, Product2Serializer)
        else:
            products = Product.objects.filter(long_desc__icontains=description).order_by('-autonum')
            return paginate_queryset(request, products, Product2Serializer)

        # Paginate using reusable function
        
    elif request.method =='POST':
        try:
            receive_data = json.loads(request.body)
            form_data = receive_data.get('data')

            img = receive_data.get('image_prod')

            product = Product(
                pos_item = form_data.get("posItem", "YES"),
                weight_scale = form_data.get("weightScale", "N"),
                pos_site_code = form_data.get("posSiteCode", "0"),
                print_cat = form_data.get("printCat", 0),
                item_type = form_data.get("itemType", ""),
                category_id = form_data.get("categoryId", 0),
                category = form_data.get("category", ""),
                brand = form_data.get("brand", ""),
                model = form_data.get("model", ""),
                style = form_data.get("style", ""),
                p_size = form_data.get("pSize", ""),
                color = form_data.get("color", ""),
                qty_onhand = form_data.get("qtyOnhand", 0),
                qty_avl = form_data.get("qtyAvl", 0),
                uom = form_data.get("uom", ""),
                item_code = form_data.get("itemCode", ""),
                bar_code = form_data.get("barCode", ""),
                alternate_code = form_data.get("alternateCode", ""),
                long_desc = form_data.get("longDesc", ""),
                short_desc = form_data.get("shortDesc", ""),
                reg_price = form_data.get("regPrice", 0),
                key_price = form_data.get("keyPrice", 0),
                ws_price = form_data.get("wsPrice", 0),
                ec_price = form_data.get("ecPrice", 0),
                last_purch = form_data.get("lastPurch", 0),
                po_qty_allowance = form_data.get("poQtyAllowance", 0),
                so_qty_allowance = form_data.get("soQtyAllowance", 0),
                standard_price = form_data.get("standardPrice", 0),
                rm_cost = form_data.get("rmCost", 0),
                dl_cost = form_data.get("dlCost", 0),
                oh_cost = form_data.get("dlCost", 0),
                ave_cost = form_data.get("aveCost", 0),
                fifo_cost = form_data.get("fifoCost", 0),
                tax_code = form_data.get("taxCode", ""),
                vat_category_code = form_data.get("vatCategoryCode", ""),
                # add other fields if needed
            )

            product.save()
            if img:
                image_bytes = base64.b64decode(img.split(',')[1])
                # Remove base64 prefix if exists
                # if img.startswith('data:image/png;base64,'):
                #     header, encoded = img.split(',', 1)
                #     image_bytes = base64.b64decode(encoded)  # Decode to bytes
                # elif  "," in img:
                #     img = img.split(",")[1]
                #     image_bytes = base64.b64decode(img)

                if form_data:
                    product = Product.objects.filter(bar_code=form_data.get("barCode")).first()
                    if product:
                        product.prod_img = image_bytes  # save as bytes
                        product.save()    
                return Response('Success') 
        
        
        except Exception as e:
            print(e)
            traceback.print_exc()

    elif request.method == 'PUT':
        try:
            receive_data = json.loads(request.body)
            form_data = receive_data.get('data')
            img = receive_data.get('image_prod')

            # ---- STEP 1: Find existing product ----
            bar_code = form_data.get("barCode")
            product = Product.objects.filter(bar_code=bar_code).first()

            if not product:
                return Response({"error": "Product not found"}, status=404)

            # ---- STEP 2: Update fields ----
            product.pos_item = form_data.get("posItem", "YES")
            product.weight_scale = form_data.get("weightScale", "N")
            product.pos_site_code = form_data.get("posSiteCode", "0")
            product.print_cat = form_data.get("printCat", 0)
            product.item_type = form_data.get("itemType", "")
            product.category_id = form_data.get("categoryId", 0)
            product.category = form_data.get("category", "")
            product.brand = form_data.get("brand", "")
            product.model = form_data.get("model", "")
            product.style = form_data.get("style", "")
            product.p_size = form_data.get("pSize", "")
            product.color = form_data.get("color", "")
            product.qty_onhand = form_data.get("qtyOnhand", 0)
            product.qty_avl = form_data.get("qtyAvl", 0)
            product.uom = form_data.get("uom", "")
            product.item_code = form_data.get("itemCode", "")
            product.alternate_code = form_data.get("alternateCode", "")
            product.long_desc = form_data.get("longDesc", "")
            product.short_desc = form_data.get("shortDesc", "")
            product.reg_price = form_data.get("regPrice", 0)
            product.key_price = form_data.get("keyPrice", 0)
            product.ws_price = form_data.get("wsPrice", 0)
            product.ec_price = form_data.get("ecPrice", 0)
            product.last_purch = form_data.get("lastPurch", 0)
            product.po_qty_allowance = form_data.get("poQtyAllowance", 0)
            product.so_qty_allowance = form_data.get("soQtyAllowance", 0)
            product.standard_price = form_data.get("standardPrice", 0)
            product.rm_cost = form_data.get("rmCost", 0)
            product.dl_cost = form_data.get("dlCost", 0)
            product.oh_cost = form_data.get("ohCost", 0)     # ← FIXED
            product.ave_cost = form_data.get("aveCost", 0)
            product.fifo_cost = form_data.get("fifoCost", 0)
            product.tax_code = form_data.get("taxCode", "")
            product.vat_category_code = form_data.get("vatCategoryCode", "")

            # ---- STEP 3: Save image if provided ----
            if img:
                try:
                    encoded = img.split(",")[1]
                    image_bytes = base64.b64decode(encoded)
                    product.prod_img = image_bytes  # prod_img MUST be BLOB
                except Exception as e:
                    print("Image decode error:", e)

            product.save()

            return Response("Success")

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

    
# @api_view(['GET','POST','PUT'])
# @permission_classes([IsAuthenticated])
# def get_product_profile(request):
#     if request.method == 'GET':
#         print('www')
#         try:
#             description = request.GET.get('Search')
#             if description== None:
#                 product_list = Product.objects.all().order_by('-autonum')
#                 serialize = Product2Serializer(product_list,many=True)
#                 print(1)
#                 return Response(serialize.data)
#             else:
#                 product_list = Product.objects.filter(long_desc__icontains=description)
#                 serialize = Product2Serializer(product_list,many=True)
#                 return Response(serialize.data)
#         except Exception as e:
#             print(e)
#             traceback.print_exc()
#     elif request.method =='POST':
#         try:
#             receive_data = json.loads(request.body)
#             form_data = receive_data.get('data')

#             img = receive_data.get('image_prod')

#             product = Product(
#                 pos_item = form_data.get("posItem", "YES"),
#                 weight_scale = form_data.get("weightScale", "N"),
#                 pos_site_code = form_data.get("posSiteCode", "0"),
#                 print_cat = form_data.get("printCat", 0),
#                 item_type = form_data.get("itemType", ""),
#                 category_id = form_data.get("categoryId", 0),
#                 category = form_data.get("category", ""),
#                 brand = form_data.get("brand", ""),
#                 model = form_data.get("model", ""),
#                 style = form_data.get("style", ""),
#                 p_size = form_data.get("pSize", ""),
#                 color = form_data.get("color", ""),
#                 qty_onhand = form_data.get("qtyOnhand", 0),
#                 qty_avl = form_data.get("qtyAvl", 0),
#                 uom = form_data.get("uom", ""),
#                 item_code = form_data.get("itemCode", ""),
#                 bar_code = form_data.get("barCode", ""),
#                 alternate_code = form_data.get("alternateCode", ""),
#                 long_desc = form_data.get("longDesc", ""),
#                 short_desc = form_data.get("shortDesc", ""),
#                 reg_price = form_data.get("regPrice", 0),
#                 key_price = form_data.get("keyPrice", 0),
#                 ws_price = form_data.get("wsPrice", 0),
#                 ec_price = form_data.get("ecPrice", 0),
#                 last_purch = form_data.get("lastPurch", 0),
#                 po_qty_allowance = form_data.get("poQtyAllowance", 0),
#                 so_qty_allowance = form_data.get("soQtyAllowance", 0),
#                 standard_price = form_data.get("standardPrice", 0),
#                 rm_cost = form_data.get("rmCost", 0),
#                 dl_cost = form_data.get("dlCost", 0),
#                 oh_cost = form_data.get("dlCost", 0),
#                 ave_cost = form_data.get("aveCost", 0),
#                 fifo_cost = form_data.get("fifoCost", 0),
#                 tax_code = form_data.get("taxCode", ""),
#                 vat_category_code = form_data.get("vatCategoryCode", ""),
#                 # add other fields if needed
#             )

#             product.save()
#             if img:
#                 image_bytes = base64.b64decode(img.split(',')[1])
#                 # Remove base64 prefix if exists
#                 # if img.startswith('data:image/png;base64,'):
#                 #     header, encoded = img.split(',', 1)
#                 #     image_bytes = base64.b64decode(encoded)  # Decode to bytes
#                 # elif  "," in img:
#                 #     img = img.split(",")[1]
#                 #     image_bytes = base64.b64decode(img)

#                 if form_data:
#                     product = Product.objects.filter(bar_code=form_data.get("barCode")).first()
#                     if product:
#                         product.prod_img = image_bytes  # save as bytes
#                         product.save()    
#                 return Response('Success') 
        
        
#         except Exception as e:
#             print(e)
#             traceback.print_exc()

#     elif request.method == 'PUT':
#         try:
#             receive_data = json.loads(request.body)
#             form_data = receive_data.get('data')
#             img = receive_data.get('image_prod')

#             # ---- STEP 1: Find existing product ----
#             bar_code = form_data.get("barCode")
#             product = Product.objects.filter(bar_code=bar_code).first()

#             if not product:
#                 return Response({"error": "Product not found"}, status=404)

#             # ---- STEP 2: Update fields ----
#             product.pos_item = form_data.get("posItem", "YES")
#             product.weight_scale = form_data.get("weightScale", "N")
#             product.pos_site_code = form_data.get("posSiteCode", "0")
#             product.print_cat = form_data.get("printCat", 0)
#             product.item_type = form_data.get("itemType", "")
#             product.category_id = form_data.get("categoryId", 0)
#             product.category = form_data.get("category", "")
#             product.brand = form_data.get("brand", "")
#             product.model = form_data.get("model", "")
#             product.style = form_data.get("style", "")
#             product.p_size = form_data.get("pSize", "")
#             product.color = form_data.get("color", "")
#             product.qty_onhand = form_data.get("qtyOnhand", 0)
#             product.qty_avl = form_data.get("qtyAvl", 0)
#             product.uom = form_data.get("uom", "")
#             product.item_code = form_data.get("itemCode", "")
#             product.alternate_code = form_data.get("alternateCode", "")
#             product.long_desc = form_data.get("longDesc", "")
#             product.short_desc = form_data.get("shortDesc", "")
#             product.reg_price = form_data.get("regPrice", 0)
#             product.key_price = form_data.get("keyPrice", 0)
#             product.ws_price = form_data.get("wsPrice", 0)
#             product.ec_price = form_data.get("ecPrice", 0)
#             product.last_purch = form_data.get("lastPurch", 0)
#             product.po_qty_allowance = form_data.get("poQtyAllowance", 0)
#             product.so_qty_allowance = form_data.get("soQtyAllowance", 0)
#             product.standard_price = form_data.get("standardPrice", 0)
#             product.rm_cost = form_data.get("rmCost", 0)
#             product.dl_cost = form_data.get("dlCost", 0)
#             product.oh_cost = form_data.get("ohCost", 0)     # ← FIXED
#             product.ave_cost = form_data.get("aveCost", 0)
#             product.fifo_cost = form_data.get("fifoCost", 0)
#             product.tax_code = form_data.get("taxCode", "")
#             product.vat_category_code = form_data.get("vatCategoryCode", "")

#             # ---- STEP 3: Save image if provided ----
#             if img:
#                 try:
#                     encoded = img.split(",")[1]
#                     image_bytes = base64.b64decode(encoded)
#                     product.prod_img = image_bytes  # prod_img MUST be BLOB
#                 except Exception as e:
#                     print("Image decode error:", e)

#             product.save()

#             return Response("Success")

#         except Exception as e:
#             print("Error:", e)
#             traceback.print_exc()
#             return Response({"error": str(e)}, status=500)

###* **************************** WAITER *******************************
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_waiter(request):
    if request.method == 'GET':
        data = PosWaiterList.objects.all().order_by('-autonum')
        userList = PosWaiterListSerializer(data, many=True).data
        return JsonResponse({'userList': userList}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_waiter(request):
    if request.method == 'POST':
        try:
       
            received_data = json.loads(request.body)
            waiter_id = received_data.get('waiter_id')
            waiter_name = received_data.get('waiter_name')
            
            existing_waiter = PosWaiterList.objects.filter(waiter_id=waiter_id).first()
            
            if existing_waiter:
                return JsonResponse({'message': 'Duplication is Not Allowed'}, status=500)

            else:
                if waiter_id:
                        # Create a new User instance and save it to the database
                        new_waiter = PosWaiterList(waiter_id=waiter_id,waiter_name=waiter_name)
                        new_waiter.save()

                        return JsonResponse({'message': 'Waiter created successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'All fields are required'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_waiter(request):
    if request.method == 'POST':
        received_data = request.data
        waiter_id = received_data.get('waiter_id')
        waiter_name = received_data.get('waiter_name')

        if all(waiter_id):
            # Check if the user already exists based on some identifier like username
            existing_waiter = PosWaiterList.objects.filter(waiter_id=waiter_id).first()
            if existing_waiter:
                # Update existing user data
                existing_waiter.waiter_id = waiter_id
                existing_waiter.waiter_name = waiter_name
                existing_waiter.save()
                return JsonResponse({'message': 'Waiter updated successfully'}, status=200)
            else:
                # Create a new User instance and save it to the database
                new_waiter = PosWaiterList.objects.create(
                    waiter_id=waiter_id,
                    waiter_name=waiter_name,
                )
                return JsonResponse({'message': 'Waiter created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'All fields are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@api_view(['DELETE'])  
@permission_classes([IsAuthenticated])
def delete_waiter(request):
    if request.method == 'DELETE':
        received_data = json.loads(request.body.decode('utf-8'))  # Decode and load JSON data
        
        waiter_data = received_data.get('user')  # Assuming the data is under 'user' key
        if waiter_data:
            waiter_id = waiter_data.get('waiter_id')
            waiter_name = waiter_data.get('waiter_name')

            if waiter_data:
                try:
                    waiter = PosWaiterList.objects.get(waiter_id=waiter_id,waiter_name=waiter_name)
                    waiter.delete()
                    return JsonResponse({'message': 'Waiter deleted successfully'}, status=200)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Waiter does not exist'}, status=404)
            else:
                return JsonResponse({'error': 'All fields are required'}, status=400)
        else:
            return JsonResponse({'error': 'Waiter data not provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



####* **************************** TABLE NO *******************************

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_table(request):
    if request.method == 'GET':
        data = PosRestTable.objects.all().order_by('-details_id')
        userList = PosRestTableSerializer(data, many=True).data
        return JsonResponse({'userList': userList}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_table(request):
    if request.method == 'POST':
        try:
       
            received_data = json.loads(request.body)
            details_id = received_data.get('details_id')
            table_no = received_data.get('table_no')
            table_start = received_data.get('table_start')
            site_code = received_data.get('site_code')

            if details_id and table_no and table_start and site_code:
                  
                new_table = PosRestTable(details_id=details_id,table_no=table_no, table_start=table_start, site_code=site_code)
                new_table.save()

                return JsonResponse({'message': 'Table created successfully'}, status=200)
            else:
                return JsonResponse({'error': 'All fields are required'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_table(request):
    if request.method == 'POST':
       
        received_data = json.loads(request.body)
        details_id = received_data.get('details_id')
        table_no = received_data.get('table_no')
        table_start = received_data.get('table_start')
        site_code = received_data.get('site_code')
        


        if details_id and table_no and table_start and site_code:
            # Check if the user already exists based on some identifier like username
            existing_table = PosRestTable.objects.filter(site_code=site_code,details_id=details_id).first()
            if existing_table:
                # Update existing user data
                existing_table.details_id = details_id
                existing_table.table_no = table_no
                existing_table.table_start = table_start
                existing_table.site_code = site_code
                existing_table.save()
                return JsonResponse({'message': 'Table updated successfully'}, status=200)
            else:
                # Create a new User instance and save it to the database
                new_user = User.objects.create(
                    details_id=details_id,
                    table_no=table_no,
                    table_start=table_start,
                    site_code=site_code
                )
                return JsonResponse({'message': 'Table created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'All fields are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['DELETE'])  
@permission_classes([IsAuthenticated])
def delete_table(request):
    if request.method == 'DELETE':
        received_data = json.loads(request.body.decode('utf-8'))  # Decode and load JSON data
        
        table_data = received_data.get('user')  # Assuming the data is under 'user' key
        if table_data:
            details_id = table_data.get('details_id')
            table_no = table_data.get('table_no')
            table_start = table_data.get('table_start')
            site_code = table_data.get('site_code')


            if table_data:
                try:
                    table = PosRestTable.objects.get(details_id=details_id,site_code=site_code)
                    table.delete()
                    return JsonResponse({'message': 'User deleted successfully'}, status=200)
                except PosRestTable.DoesNotExist:
                    return JsonResponse({'error': 'User does not exist'}, status=404)
            else:
                return JsonResponse({'error': 'All fields are required'}, status=400)
        else:
            return JsonResponse({'error': 'User data not provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UploadVideo(request):
    if request.method == 'POST':
        try:
            video_file = request.FILES.get('video')
            if not video_file:
                return Response({'error': 'No video file provided'}, status=400)

            # Get serial number and machine info
            serial_number = getattr(request, "SERIALNO", None) or request.POST.get('serialNo')
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            if not machineInfo:
                return Response({'error': 'Machine not found'}, status=404)

            # Save file in MEDIA_ROOT
            filename = video_file.name
            save_path = os.path.join(settings.MEDIA_ROOT, filename)
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(save_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Save DB record
            SaveVideo = PosVideo(
                filepath=save_path,
                filename=filename,
                serial_no=machineInfo.Serial_no
            )
            SaveVideo.save()

            # Return absolute URL
            video_url = request.build_absolute_uri(settings.MEDIA_URL + filename)


            return Response({'message': 'Video uploaded successfully', 'url': video_url}, status=200)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    elif request.method == 'GET':
        try:
       
            serial_number = getattr(request, "SERIALNO", None) or request.GET.get('serialNo')
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
            if not machineInfo:
                return JsonResponse({'error': 'Machine not found'}, status=404)

            video_record = PosVideo.objects.filter(serial_no=machineInfo.Serial_no).order_by('-autonum').first()
            if not video_record or not video_record.filename:
             
                return JsonResponse({'error': 'No videos found'}, status=404)
            video_url = request.build_absolute_uri(settings.MEDIA_URL + video_record.filename)
            # video_url = request.build_absolute_uri(settings.MEDIA_URL + video_record.filename)

            if not settings.DEBUG:
                if video_url.startswith('http://'):
                    video_url = video_url.replace('http://', 'https://', 1)
            print(video_url)
            return JsonResponse({'data': video_url})

        except Exception as e:
            print(2)
            print(e)
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def UploadVideo(request):
#     if request.method == 'POST':
#         try:
#             video_file = request.FILES.get('video')
#             if video_file:
#                 # pdb.set_trace()
#                 # Get the desktop path
#                 username = os.getlogin()
#                 desktop_path = os.path.join('C:/Users', username, 'Desktop')
#                 serial_number = getattr(request, "SERIALNO", None)
#                 machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
#                 # Save the file to the desktop
#                 filename = video_file.name
#                 filepath = os.path.join(desktop_path, filename)
#                 SaveVideo = PosVideo(
#                     filepath = desktop_path,
#                     filename = filename,
#                     serial_no = machineInfo.Serial_no,
#                 )
#                 SaveVideo.save()

#                 with open(filepath, 'wb') as destination:
#                     # Write the file content to the destination
#                     for chunk in video_file.chunks():
#                         destination.write(chunk)

#                 # Return a response indicating success
#                 video_url = filepath
#                 return Response({'message': 'Video uploaded successfully', 'url': video_url}, status=200)
#             else:
#                 return Response({'error': 'No video file provided'}, status=400)
#         except Exception as e:
#             print(e)
#             traceback.print_exc()
#     elif request.method == 'GET':
#         try:
#             # desktop_path = os.path.join('C:/Users', os.getlogin(), 'Desktop')
#             print('getvideo')
#             serial_number = getattr(request, "SERIALNO", None)
#             if serial_number is None:
#                 serial_number = request.GET.get('serialNo')  # <-- get from query string
#             machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
#             print(serial_number)
#             if machineInfo:
#                 print(1)
#                 path = PosVideo.objects.filter(serial_no=machineInfo.Serial_no).first()
#                 try:
#                     if path and path.filepath:
#                         # pdb.set_trace()
#                         desktop_path = path.filepath
#                         desktop_path = os.path.normpath(desktop_path)
#                         filename = path.filename  # Assuming filename is a field in PosVideo model
#                         print(2)
#                         print('directory',desktop_path)
#                         try:
#                             if os.path.isdir(desktop_path):
                                
#                                 # List all files on the desktop
#                                 video_files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
                                
#                                 # Filter video files by filename (if specified)
#                                 if filename:
#                                     video_files = [f for f in video_files if f.lower() == filename.lower()]
                                
#                                 # Sort files by modification time (latest first)
#                                 video_files.sort(key=lambda x: os.path.getmtime(os.path.join(desktop_path, x)), reverse=True)
#                                 print(3)
#                                 # Get the path to the latest video file on the desktop
#                                 if video_files:
#                                     latest_video_file = os.path.join(desktop_path, video_files[0])
                                    
#                                     with open(latest_video_file, 'rb') as file:
#                                         file_content = file.read()
                                        
#                                         # Encode the file content to Base64
#                                         base64_content = base64.b64encode(file_content).decode()
                                        
#                                         # Construct the data URL
#                                         data_url = f'data:video/mp4;base64,{base64_content}'
#                                         print('data_url',data_url)
                                        
#                                         return JsonResponse({'data': data_url})
#                         except Exception as e:
#                             print(e)
#                             traceback.print_exc()
#                 except Exception as e:
#                     print(e)
#                     traceback.print_exc()
#         except Exception as e:
#             print(e)
#             traceback.print_exc()



####* **************************** Customer Details *******************************

@api_view(['GET','POST','PUT'])   
def CustomerDetails(request):
        if request.method == 'GET':
            trade_name = request.GET.get('trade_name', '')

            if trade_name == '':
                all_customers = Customer.objects.all()
                latest_customer = Customer.objects.order_by('-id_code').first()
                serializer_all_customers =CustomerSerializer(all_customers, many=True)
                serializer_latest_customer = CustomerSerializer(latest_customer)
                response_data = {
                    'all_customers': serializer_all_customers.data,
                    'latest_customer': serializer_latest_customer.data
                }
                return Response(response_data)
            else:
                customers = Customer.objects.filter(trade_name__icontains=trade_name).values('id_code', 'trade_name')
                return JsonResponse(list(customers), safe=False)
        elif request.method == 'POST':
            try:
                data = request.data
                # pdb.set_trace()
                base64_image = data.get('image')
                if base64_image:
                    image = base64.b64decode(base64_image.split(',')[1])
                
                SaveCustomer = Customer(
                    id_code = data['ID_Code'],
                    trade_name = data['Tradename'],
                    last_name = data['Lname'],
                    first_name = data['Fname'],
                    middle_name = data['MI'],
                    business_phone_no = data['Phone'],
                    mobile_no = data['Mobile'],
                    fax_no = data['Fax'],
                    st_address = data['Address'],
                    city_address = data['City'],
                    zip_code = data['ZipCode'],
                    vat = data['Vat'],
                    tax_id_no = data['Tax'],
                    group_name = data['Group'],
                    area_name = data['Area'],
                    agent_name = data['Agent'],
                    collector_name = data['Collector'],
                    kob_name = data['KOB'],
                    remarks = data['Remarks'],
                )
                if base64_image:
                    SaveCustomer.customer_image = image

                SaveCustomer.save()
                return Response({'mesage':'Customer Successfully Added'})
            except Exception as e:
                print(e)
                traceback.print_exc()
    
        elif request.method == 'PUT':
            data = request.data
            try:
                cutomerDetails = Customer.objects.get(id_code=data['ID_Code'])
                cutomerDetails.id_code = data.get('ID_Code', cutomerDetails.id_code)
                cutomerDetails.trade_name = data.get('Tradename', cutomerDetails.trade_name)
                cutomerDetails.last_name = data.get('Lname', cutomerDetails.last_name)
                cutomerDetails.first_name = data.get('Fname', cutomerDetails.first_name)
                cutomerDetails.middle_name = data.get('MI', cutomerDetails.middle_name)
                cutomerDetails.business_phone_no = data.get('Phone', cutomerDetails.business_phone_no)
                cutomerDetails.mobile_no = data.get('Mobile', cutomerDetails.mobile_no)
                cutomerDetails.fax_no = data.get('Fax', cutomerDetails.fax_no)
                cutomerDetails.st_address = data.get('Address', cutomerDetails.st_address)
                cutomerDetails.city_address = data.get('City', cutomerDetails.city_address)
                cutomerDetails.province = data.get('Province', cutomerDetails.province)
                cutomerDetails.zip_code = data.get('ZipCode', cutomerDetails.zip_code)
                cutomerDetails.vat = data.get('Vat', cutomerDetails.vat)
                cutomerDetails.tax_id_no = data.get('Tax', cutomerDetails.tax_id_no)
                cutomerDetails.active = data.get('Status', cutomerDetails.active)
                cutomerDetails.group_name = data.get('Group', cutomerDetails.group_name)
                cutomerDetails.area_name = data.get('Area', cutomerDetails.area_name)
                cutomerDetails.agent_name = data.get('Agent', cutomerDetails.agent_name)
                cutomerDetails.collector_name = data.get('Collector', cutomerDetails.collector_name)
                cutomerDetails.kob_name = data.get('KOB', cutomerDetails.kob_name)
                cutomerDetails.sl_sub_category_description = data.get('sl', cutomerDetails.sl_sub_category_description)
                cutomerDetails.remarks = data.get('Remarks', cutomerDetails.remarks)
                base64_image = data.get('image')

                if base64_image:
                    image = base64.b64decode(base64_image.split(',')[1])
                    cutomerDetails.customer_image = image
                cutomerDetails.save()

                return Response({"message": "UnitLocation updated successfully"}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=500)

@api_view(['GET','POST','DELETE'])   
def CustomerSearchResults(request):
        if request.method =='GET':
            trade_name = request.GET.get('trade_name', '')        
            latest_customers = Customer.objects.filter(trade_name__icontains=trade_name)
            serializer = CustomerSerializer(latest_customers, many=True)  # Use many=True for multiple instances

            return JsonResponse({'customersSearch': serializer.data})
        elif request.method =='DELETE':
            id_code = request.GET.get('id_code', '')   
            Customer.objects.filter(id_code=id_code).delete()
            return Response({'message': 'Location Successfully Deleted'})
####* **************************** Supplier Details *******************************
        

class SupplierDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        trade_name = request.GET.get('trade_name', '')
        if trade_name == '':
            all_customers = Supplier.objects.all()
            latest_customer = Supplier.objects.order_by('-id_code').first()
            serializer_all_customers = SupplierSerializer(all_customers, many=True)
            serializer_latest_customer = SupplierSerializer(latest_customer)
            response_data = {
                'all_customers': serializer_all_customers.data,
                'latest_customer': serializer_latest_customer.data
            }
            return Response(response_data)
        else:
            customers = MainRefCustomer.objects.filter(trade_name__contains=trade_name).values('id_code', 'trade_name')
            return JsonResponse(list(customers), safe=False)
    def post(self,request):
        data = request.data
        base64_image = data.get('supplier_image')
        if base64_image:
            image = base64.b64decode(base64_image.split(',')[1])
          
        SaveCustomer = Supplier(
            id_code = data['ID_Code'],
            trade_name = data['Tradename'],
            last_name = data['Lname'],
            first_name = data['Fname'],
            middle_name = data['MI'],
            business_phone_no = data['Phone'],
            mobile_no = data['Mobile'],
            fax_no = data['Fax'],
            st_address = data['Address'],
            city_address = data['City'],
            zip_code = data['ZipCode'],
            tax_id_no = data['Tax'],
            group_name = data['Group'],
            remarks = data['Remarks'],
            
        )
        if base64_image:
            SaveCustomer.supplier_image = image
        SaveCustomer.save()
        return Response({'mesage':'Customer Successfully Added'})
    
    def put(self, request, args, *kwargs):
        data = request.data
        try:
            cutomerDetails = Supplier.objects.get(id_code=data['ID_Code'])
            cutomerDetails.id_code = data.get('ID_Code', cutomerDetails.id_code)
            cutomerDetails.trade_name = data.get('Tradename', cutomerDetails.trade_name)
            cutomerDetails.last_name = data.get('Lname', cutomerDetails.last_name)
            cutomerDetails.first_name = data.get('Fname', cutomerDetails.first_name)
            cutomerDetails.middle_name = data.get('MI', cutomerDetails.middle_name)
            cutomerDetails.business_phone_no = data.get('Phone', cutomerDetails.business_phone_no)
            cutomerDetails.mobile_no = data.get('Mobile', cutomerDetails.mobile_no)
            cutomerDetails.fax_no = data.get('Fax', cutomerDetails.fax_no)
            cutomerDetails.st_address = data.get('Address', cutomerDetails.st_address)
            cutomerDetails.zip_code = data.get('ZipCode', cutomerDetails.zip_code)
            cutomerDetails.tax_id_no = data.get('Tax', cutomerDetails.tax_id_no)
            cutomerDetails.active = data.get('Status', cutomerDetails.active)
            cutomerDetails.group_name = data.get('Group', cutomerDetails.group_name)
            cutomerDetails.remarks = data.get('Remarks', cutomerDetails.remarks)
            base64_image = data.get('image')

            if base64_image:
                image = base64.b64decode(base64_image.split(',')[1])
                cutomerDetails.supplier_image = image
            cutomerDetails.save()

            return Response({"message": "UnitLocation updated successfully"}, status=status.HTTP_200_OK)
        except UnitLocation.DoesNotExist:
            return Response({"error": "UnitLocation not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
        try:
            id_code = request.GET.get('id_code', '')   
            Supplier.objects.filter(id_code=id_code).delete()
            return Response({'message': 'Location Successfully Deleted'})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    




@api_view(['GET','POST','DELETE'])
def product_printer_category(request):
    if request.method == 'GET':
        try:
            product_printer_category_list= POSProductPrinter.objects.all()

            serialize = POSProductPrinterSerializer(product_printer_category_list,many=True)
            return JsonResponse(serialize.data,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'POST':
        try:
            data_receiver = json.loads(request.body)

            data_receive = data_receiver.get('data')

            prod_code = data_receive.get('prod_code')
            prod_desc = data_receive.get('prod_desc')
            printer_name = data_receive.get('printer_name')
            category_desc = data_receive.get('category_desc')

            check_data = POSProductPrinter.objects.filter(prod_code=prod_code).first()

            if check_data:
                check_data.prod_desc = prod_desc
                check_data.printer_name = printer_name
                check_data.category_desc = category_desc
                check_data.save()

            else:
                savePrinterCat = POSProductPrinter (
                    prod_code = prod_code,
                    prod_desc = prod_desc,
                    printer_name = printer_name,
                    category_desc = category_desc
                )
                savePrinterCat.save()



            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'DELETE':
        try:
            prod_code = request.GET.get('prod_code')
     
            POSProductPrinter.objects.filter(prod_code=prod_code).delete()
            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def printer_list(request):
    if request.method == 'GET':
        try:
            list_data = []
            data =subprocess.check_output(['wmic','printer','list','brief']).decode('utf-8').split('\r\r\n')
            data = data[1:]
            for line in data:
                for printername in line.split("   "):
                    if printername !="":
                        match = re.search(r'Device\s+([\w\s-]+)', printername)
                        if match:
                            list = {
                                "printer_name":match.group(1).lstrip()
                            }
                        else:
                            list = {
                                "printer_name":printername.lstrip()
                            }
                        list_data.append(list)
                        break
            return Response(list_data,status=200)


        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['GET'])
def get_product_Category_setup(request):
    if request.method =='GET':
        try:
            category_setup = ProductCategorySetup.objects.filter(pos_category='Y')

            serialize = ProductCategorySetupSerializer(category_setup,many=True)
            return Response(serialize.data,status=200)
            
        except Exception as e:
            print(e)
            traceback.print_exc()


####* **************************** GIFT CHECK SERIES ****************************

@api_view(['GET','POST','DELETE'])
def Gift_Check_series(request):
    if request.method == 'GET':
        try:
            gift_Check_series= POSGiftCheckSeries.objects.all()

            serialize = POSGiftCheckSeriesSerializer(gift_Check_series,many=True)
            return JsonResponse(serialize.data,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'POST':
        try:
            # data_receiver = json.loads(request.body)
            data_receive = request.data.get('data','')

            # data_receive = data_receiver.get('data')
            trans_no = data_receive.get('trans_no')
            SeriesFrom = data_receive.get('series_from')
            SeriesTo = data_receive.get('series_to')
            DateFrom = data_receive.get('validity_date_from')
            DateTo = data_receive.get('validity_date_to')
            Amount = data_receive.get('amount')
            serial_number = getattr(request, "SERIALNO", None)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            check_data = POSGiftCheckSeries.objects.filter(trans_no=trans_no).first()

            errors = {}

            # 1️⃣ Convert series to integers
            try:
                series_from_int = int(SeriesFrom)
                series_to_int = int(SeriesTo)
                if series_from_int > series_to_int:
                    errors['series'] = "Series From cannot be greater than Series To."

                   
            except ValueError:
                errors['series'] = "Series From and Series To must be valid integers."

            # 2️⃣ Convert dates
            try:
                date_from_obj = DateFrom if isinstance(DateFrom, datetime) else datetime.strptime(DateFrom, "%Y-%m-%d")
                date_to_obj = DateTo if isinstance(DateTo, datetime) else datetime.strptime(DateTo, "%Y-%m-%d")
                if date_from_obj > date_to_obj:
                    errors['dates'] = "Validity start date cannot be after end date."
            except Exception:
                errors['dates'] = "Validity dates must be valid date strings (YYYY-MM-DD)."

            # 3️⃣ Check for overlapping series (no PK check)
            overlapping = POSGiftCheckSeries.objects.filter(
                Q(series_from__lte=series_to_int, series_to__gte=series_from_int) &
                Q(validity_date_from__lte=date_to_obj, validity_date_to__gte=date_from_obj)
            )

            if overlapping.exists():
                errors['series'] = "Series numbers overlap with existing GiftCheck entries."

            # 4️⃣ Raise error if any validation fails
            if errors:
                return Response({"success": False, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)


            if check_data:
                check_data.site_code = machineInfo.site_no
                check_data.ul_code = machineInfo.ul_code
                check_data.trans_no = trans_no
                check_data.series_from = SeriesFrom
                check_data.series_to = SeriesTo
                check_data.validity_date_from = DateFrom
                check_data.validity_date_to = DateTo
                check_data.amount = Amount
                check_data.save()

            else:
                savePrinterCat = POSGiftCheckSeries (
                    site_code = machineInfo.site_no,
                    ul_code = machineInfo.ul_code,
                    trans_no = trans_no,
                    series_from = SeriesFrom,
                    series_to = SeriesTo,
                    validity_date_from = DateFrom,
                    validity_date_to = DateTo,
                    amount = Amount,
                )
                savePrinterCat.save()
            return Response('Success')

        except Exception as e:
            print('errors',e)
            traceback.print_exc()
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
            
    elif request.method == 'DELETE':
        try:
            # data_receiver = json.loads(request.body)
            trans_no = request.GET.get('trans_no')
            POSGiftCheckSeries.objects.filter(trans_no=trans_no).delete()
            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()



####* **************************** GIFT CHECK DENOMINATION ****************************

@api_view(['GET','POST','DELETE'])
def Gift_Check_Denomination(request):

    if request.method == 'GET':
     
        try:
            gift_Check_Denomination= POSGiftCheckDenomination.objects.all()
            serialize = POSGiftCheckDenominationSerializer(gift_Check_Denomination,many=True)
            return JsonResponse(serialize.data,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'POST':
        try:
            data_receiver = json.loads(request.body)
            data_receive = data_receiver.get('data')
            code = data_receive.get('code')
            denomination = data_receive.get('denomination_amount')

  

            check_data = POSGiftCheckDenomination.objects.filter(code=code).first()

            if check_data:
                check_data.code = code
                check_data.denomination_amount = denomination
                check_data.save()

            else:
                savePrinterCat = POSGiftCheckDenomination (
                code = code,
                denomination_amount = denomination,
                )
                savePrinterCat.save()
            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'DELETE':
        try:

            code = request.GET.get('code','0')

            POSGiftCheckDenomination.objects.filter(code=code).delete()
            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def item_type_view(request):
    if request.method =='GET':
        try:
            data = TblProductType.objects.all()

            serializer = TblProductTypeSerializer(data,many=True)

            return Response(serializer.data)
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({'message':'Failed Request',},status=500)
        
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def category_all_view(request):
    if request.method =='GET':
        try:
            main = ProductCategorySetup.objects.all()
            mainCat = ProductCategorySetupSerializer(main,many=True)

            sub1 =ProductSubCategory1.objects.all()
            subCat1 = ProductSubCategory1Serializer(sub1,many=True)

            sub2 = ProductSubCategory2.objects.all()
            subCat2 = ProductSubCategory2Serializer(sub2,many=True)

            sub3 = ProductSubCategory3.objects.all()
            subCat3 = ProductSubCategory3Serializer(sub3,many=True)

            data = {
                'maincat': mainCat.data,
                'subcat1': subCat1.data if subCat1.data is not None else [],
                'subcat2': subCat2.data if subCat2.data is not None else [],
                'subcat3': subCat3.data if subCat3.data is not None else [],
                }


            return Response(data)
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({'message':'Failed Request',},status=500)