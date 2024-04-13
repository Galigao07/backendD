import abc
import base64
import json
import locale
import os
import pdb
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from backend.models import (Product,PosRestTable,PosSalesOrder,PosSalesTransDetails,InvRefNo,POS_Terminal,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                            CompanySetup,Customer,PosWaiterList,PosPayor,User,Employee,LeadSetup,PosClientSetup,PosCashiersLogin,PosCashBreakdown)
from backend.serializers import (ProductSerializer,ProductCategorySerializer,PosSalesOrderSerializer,PosSalesTransDetailsSerializer,PosSalesTransSerializer,
                                 PosSalesInvoiceListing,PosSalesInvoiceList,CustomerSerializer,PosWaiterListSerializer,PosPayorSerializer,PosSalesInvoiceListSerializer,
                                 UserSerializer,EmployeeSetupSerializer,PosRestTableSerializer,POS_TerminalSerializer,LeadSetupSerializer,PosClientSetupSerializer,
                                 PosCashiersLoginpSerializer,PosCashBreakdownSerializer)
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

@api_view(['GET'])
def get_employee_list(request):
    if request.method == 'GET':
        name = request.GET.get('employee')
        data = Employee.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name),active='Y').order_by('-autonum')
        
        EmployeeList = EmployeeSetupSerializer(data, many=True).data
        return JsonResponse({'EmployeeList': EmployeeList}, status=200)
    



####* **************************** USER *******************************
@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        try:
       
            received_data = json.loads(request.body)
            id_code = received_data.get('id_code')
            full_name = received_data.get('fullName')
            username = received_data.get('username')
            password = received_data.get('password')
            rank = received_data.get('rank')
            hashed_password = make_password(password)
            print(full_name,username,password,rank,received_data)

            if full_name and username and hashed_password and rank:
                if User.objects.filter(user_name=username).exists():
                    return JsonResponse({'error': 'Username already exists'}, status=400)
                else:
                    new_user = User(id_code=id_code,fullname=full_name, user_name=username, password=hashed_password, user_rank=rank,sys_type='POS')
                    new_user.save()
                    return JsonResponse({'message': 'User created successfully'}, status=200)
            else:
                return JsonResponse({'error': 'All fields are required'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['GET'])
def view_user(request):
    if request.method == 'GET':
        data = User.objects.filter(sys_type ='POS').order_by('-autonum')
        userList = UserSerializer(data, many=True).data
        return JsonResponse({'userList': userList}, status=200)
    
    
@api_view(['POST'])
def update_user(request):
    if request.method == 'POST':
        received_data = request.data
        id_code = received_data.get('id_code')
        full_name = received_data.get('fullName')
        username = received_data.get('username')
        password = received_data.get('password')
        rank = received_data.get('rank')
        
        hashed_password = make_password(password)

        if all([full_name, username, hashed_password, rank]):
            # Check if the user already exists based on some identifier like username
            existing_user = User.objects.filter(id_code=id_code).first()
            if existing_user:
                # Update existing user data
                existing_user.fullname = full_name
                existing_user.password = hashed_password
                existing_user.user_rank = rank
                existing_user.user_name = username
                existing_user.sys_type = 'POS'
                existing_user.save()
                return JsonResponse({'message': 'User updated successfully'}, status=200)
            else:
                # Create a new User instance and save it to the database
                new_user = User.objects.create(
                    username=username,
                    fullname=full_name,
                    password=hashed_password,
                    user_rank=rank
                )
                return JsonResponse({'message': 'User created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'All fields are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['DELETE'])  
def delete_user(request):
    if request.method == 'DELETE':
        received_data = json.loads(request.body.decode('utf-8'))  # Decode and load JSON data
        
        user_data = received_data.get('user')  # Assuming the data is under 'user' key
        if user_data:
            id_code = user_data.get('id_code')
            full_name = user_data.get('fullName')
            username = user_data.get('username')
            password = user_data.get('password')
            rank = user_data.get('rank')
            print(id_code,full_name,username,rank)

            if user_data:
                try:
                    user = User.objects.get(id_code=id_code,user_name=username)
                    user.delete()
                    return JsonResponse({'message': 'User deleted successfully'}, status=200)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User does not exist'}, status=404)
            else:
                return JsonResponse({'error': 'All fields are required'}, status=400)
        else:
            return JsonResponse({'error': 'User data not provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


####* **************************** WAITER *******************************
@api_view(['GET'])
def view_waiter(request):
    if request.method == 'GET':
        data = PosWaiterList.objects.all().order_by('-autonum')
        userList = PosWaiterListSerializer(data, many=True).data
        return JsonResponse({'userList': userList}, status=200)


@api_view(['POST'])
def add_waiter(request):
    if request.method == 'POST':
        try:
       
            received_data = json.loads(request.body)
            waiter_id = received_data.get('waiter_id')
            waiter_name = received_data.get('waiter_name')
            
            existing_waiter = PosWaiterList.objects.filter(waiter_id=waiter_id).first()
            
            if existing_waiter:
                print('Waiter ID already exists:', existing_waiter.waiter_id)
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
def view_table(request):
    if request.method == 'GET':
        data = PosRestTable.objects.all().order_by('-details_id')
        userList = PosRestTableSerializer(data, many=True).data
        return JsonResponse({'userList': userList}, status=200)

@api_view(['POST'])
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


####* **************************** VIDEO *******************************
# @api_view(['GET','POST'])
# def UploadVideo(request):
#     if request.method == 'POST':
#         video_file = request.FILES.get('video')
#         if video_file:
#             # Save the file to the media directory
#             filename = video_file.name
#             filepath = os.path.join(settings.MEDIA_ROOT, filename)
#             with open(filepath, 'wb') as destination:
#                 # Read the entire file content at once
#                 file_content = video_file.read()
#                 # Write the file content to the destination
#                 destination.write(file_content)
            
#             # Return a response indicating success
#             video_url = os.path.join(settings.MEDIA_URL, filename)
#             return Response({'message': 'Video uploaded successfully', 'url': video_url}, status=200)
#         else:
#             return Response({'error': 'No video file provided'}, status=400)
    
#     elif request.method == 'GET':

#         media_dir = os.path.join(settings.BASE_DIR, 'media')

#         # Check if the videos directory exists
#         if os.path.isdir(media_dir):
#             # List all files in the videos directory
#             video_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]

#             # Sort files by modification time (latest first)
#             video_files.sort(key=lambda x: os.path.getmtime(os.path.join(media_dir, x)), reverse=True)

#             # Get the path to the latest video file
#             if video_files:
#                 latest_video_file = os.path.join(media_dir, video_files[0])
#                 with open(latest_video_file, 'rb') as file:
#                     file_content = file.read()

#                     # Encode the file content to Base64
#                     base64_content = base64.b64encode(file_content).decode()
#                     # print(base64_content)
#                     # Construct the data URL
#                     # data_url = 'data:base64,{base64_content}'

#                     data_url = f'data:video/mp4;base64,{base64_content}'
      
#                 return JsonResponse({'data':data_url})
#                 # Serve the latest video file
#             else:
#                 return Response({'error': 'No videos found in the media directory'}, status=404)
#         else:
#             return Response({'error': 'Media directory not found'}, status=404)



@api_view(['GET', 'POST'])
def UploadVideo(request):
    if request.method == 'POST':
        try:
            video_file = request.FILES.get('video')
            if video_file:
                # Get the desktop path
                username = os.getlogin()
                desktop_path = os.path.join('C:/Users', username, 'Desktop')

                # Save the file to the desktop
                filename = video_file.name
                filepath = os.path.join(desktop_path, filename)
                with open(filepath, 'wb') as destination:
                    # Write the file content to the destination
                    for chunk in video_file.chunks():
                        destination.write(chunk)

                # Return a response indicating success
                video_url = filepath
                return Response({'message': 'Video uploaded successfully', 'url': video_url}, status=200)
            else:
                return Response({'error': 'No video file provided'}, status=400)
        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'GET':
        try:
            desktop_path = os.path.join('C:/Users', os.getlogin(), 'Desktop')
            # Check if the desktop directory exists
            if os.path.isdir(desktop_path):
                # List all files on the desktop
                video_files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]

                # Sort files by modification time (latest first)
                video_files.sort(key=lambda x: os.path.getmtime(os.path.join(desktop_path, x)), reverse=True)

                # Get the path to the latest video file on the desktop
                if video_files:
                    latest_video_file = os.path.join(desktop_path, video_files[0])
                    with open(latest_video_file, 'rb') as file:
                        file_content = file.read()

                        # Encode the file content to Base64
                        base64_content = base64.b64encode(file_content).decode()

                        # Construct the data URL
                        data_url = f'data:video/mp4;base64,{base64_content}'
                    # print(data_url)
                    return JsonResponse({'data': data_url})
                    # Serve the latest video file
                else:
                    return Response({'error': 'No videos found on the desktop'}, status=404)
            else:
                return Response({'error': 'Desktop directory not found'}, status=404)
        except Exception as e:
            print(e)
            traceback.print_exc()

####* **************************** Terminal Setup *******************************
@api_view(['GET','POST'])       
def terminal_setup(request):
    if request.method == 'GET':
        data = POS_Terminal.objects.all()
        
        serializer = POS_TerminalSerializer(data,many=True).data
        return JsonResponse({'data': serializer}, status=200)
    
    elif request.method == 'POST':
    
        received_data = json.loads(request.body)
        print('received_data',received_data)
        autonum = received_data.get('autonum')
        ulcode = received_data.get('ulcode')
        terminalno = received_data.get('terminalno')
        description = received_data.get('description')
        siteno = received_data.get('siteno')
        serialno = received_data.get('serialno')
        machineno = received_data.get('machineno')
        modelno = received_data.get('modelno')
        ptu = received_data.get('ptu')
        dateissue = received_data.get('dateissue')
        datevalid = received_data.get('datevalid')

        CheckDtata = POS_Terminal.objects.filter(autonum=autonum).first()
        # pdb.set_trace()
        if CheckDtata:
                CheckDtata.ul_code = ulcode
                CheckDtata.terminal_no = terminalno
                CheckDtata.description= description
                CheckDtata.site_no = siteno
                CheckDtata.Serial_no = serialno
                CheckDtata.Machine_no = machineno
                CheckDtata.Model_no = modelno
                CheckDtata.PTU_no = ptu
                CheckDtata.date_issue =dateissue
                CheckDtata.date_valid = datevalid
                CheckDtata.save()
                return JsonResponse({'data':'Terminal Successfully Update'},status=200)

        else:    
            SaveTerminalSetup = POS_Terminal (
                ul_code = ulcode,
                terminal_no = terminalno,
                description= description,
                site_no = siteno,
                Serial_no = serialno,
                Machine_no = machineno,
                Model_no = modelno,
                PTU_no = ptu,
                date_issue =dateissue,
                date_valid = datevalid,
            )

            SaveTerminalSetup.save()

            return JsonResponse({'data':'Terminal Successfully Added'},status=200)


####* **************************** Lead/Supplier Setup *******************************
@api_view(['GET','POST'])   
def lead_setup(request):
    if request.method == 'GET':
        data = LeadSetup.objects.all()
        
        serializer = LeadSetupSerializer(data,many=True).data
        return JsonResponse({'data': serializer}, status=200)
    
    elif request.method == 'POST':
        print('sfsdfsdf')
        received_data = json.loads(request.body)
        print('received_data',received_data)
        autonum = received_data.get('autonum')
        company_code = received_data.get('companycode')
        company_name = received_data.get('companyname')
        company_name2 = received_data.get('companyname2')
        company_address = received_data.get('companyaddress')
        company_address2 = received_data.get('companyaddress2')
        tin = received_data.get('tin')
        accreditation_no = received_data.get('accreditation')
        date_issued = received_data.get('dateissued')
        date_valid = received_data.get('datevalid')

        CheckDtata = LeadSetup.objects.filter(autonum=autonum).first()
        # pdb.set_trace()
        if CheckDtata:
                CheckDtata.company_code = company_code
                CheckDtata.company_name = company_name
                CheckDtata.company_name2= company_name2
                CheckDtata.company_address = company_address
                CheckDtata.company_address2 = company_address2
                CheckDtata.tin = tin
                CheckDtata.accreditation_no = accreditation_no
                CheckDtata.date_issued = date_issued
                CheckDtata.date_valid =date_valid
                CheckDtata.save()
                return JsonResponse({'data':'Terminal Successfully Update'},status=200)

        else:    
            lead_setup = LeadSetup(
                autonum=autonum,
                company_code=company_code,
                company_name=company_name,
                company_name2=company_name2,
                company_address=company_address,
                company_address2=company_address2,
                tin=tin,
                accreditation_no=accreditation_no,
                date_issued=date_issued,
                date_valid=date_valid
            )

            lead_setup.save()
            return JsonResponse({'data':'Terminal Successfully Added'},status=200)

####* **************************** Client Setup *******************************
@api_view(['GET','POST'])   
def Client_setup(request):
    if request.method == 'GET':
        data = PosClientSetup.objects.all()
        
        serializer = PosClientSetup(data,many=True).data
        return JsonResponse({'data': serializer}, status=200)
    
    elif request.method == 'POST':
        print('sfsdfsdf')
        received_data = json.loads(request.body)
        print('received_data',received_data)

        autonum = received_data.get('autonum')
        company_code = received_data.get('companycode')
        company_name = received_data.get('companyname')
        company_name2 = received_data.get('companyname2')
        company_address = received_data.get('companyaddress')
        company_address2 = received_data.get('companyaddress2')
        company_address3 = received_data.get('companyaddress3')
        tin = received_data.get('tin')
        tel_no = received_data.get('telno')
        remarks = received_data.get('remarks')
        remarks2 = received_data.get('remarks2')
        remarks3 = received_data.get('remarks3')

        if autonum == '':
            autonum=0
        CheckDtata = PosClientSetup.objects.filter(autonum=autonum).first()
        # pdb.set_trace()
        if CheckDtata:
                CheckDtata.company_code = company_code
                CheckDtata.company_name = company_name
                CheckDtata.company_name2= company_name2
                CheckDtata.company_address = company_address
                CheckDtata.company_address2 = company_address2
                CheckDtata.company_address3 = company_address3
                CheckDtata.tin = tin
                CheckDtata.tel_no = tel_no
                CheckDtata.remarks = remarks
                CheckDtata.remarks2 =remarks2
                CheckDtata.remarks3 =remarks3
                CheckDtata.save()
                return JsonResponse({'data':'Terminal Successfully Update'},status=200)

        else:   
            # pdb.set_trace()
            lead_setup = PosClientSetup(
                company_code=company_code,
                company_name=company_name,
                company_name2=company_name2,
                company_address=company_address,
                company_address2=company_address2,
                company_address3 = company_address3,
                tin=tin,
                tel_no = tel_no,
                remarks = remarks,
                remarks2 =remarks2,
                remarks3 =remarks3

            )

            lead_setup.save()
            return JsonResponse({'data':'Terminal Successfully Added'},status=200)

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
            data = request.data
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
                # address = data['Address'],
                # city_municipality = data['City'],
                province = data['Province'],
                zip_code = data['ZipCode'],
                vat = data['Vat'],
                                # vat_registration_type = data['Vat'],
                tax_id_no = data['Tax'],
                group_name = data['Group'],
                area_name = data['Area'],
                agent_name = data['Agent'],
                collector_name = data['Collector'],
                kob_name = data['KOB'],
                sl_sub_category_description = data['sl'],
                remarks = data['Remarks'],
                customer_image = image,
            )
            SaveCustomer.save()
            return Response({'mesage':'Customer Successfully Added'})
    
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
            print(serializer.data)
            return JsonResponse({'customersSearch': serializer.data})
        elif request.method =='DELETE':
            id_code = request.GET.get('id_code', '')   
            Customer.objects.filter(id_code=id_code).delete()
            return Response({'message': 'Location Successfully Deleted'})
####* **************************** Supplier Details *******************************
        
class SupplierDetails(APIView):
    def get(self,request,args,*kwargs):    
        return Response('OK')
    # def get(self, request, args, *kw):
    #     trade_name = request.GET.get('trade_name', '')
    #     if trade_name == '':
    #         all_customers = MainRefSlSupplier.objects.all()
    #         latest_customer = MainRefSlSupplier.objects.order_by('-id_code').first()
    #         serializer_all_customers = MainRefSLSupplierSerializer(all_customers, many=True)
    #         serializer_latest_customer = MainRefSLSupplierSerializer(latest_customer)
    #         response_data = {
    #             'all_customers': serializer_all_customers.data,
    #             'latest_customer': serializer_latest_customer.data
    #         }
    #         return Response(response_data)
    #     else:
    #         customers = MainRefCustomer.objects.filter(trade_name__contains=trade_name).values('id_code', 'trade_name')
    #         return JsonResponse(list(customers), safe=False)
    # def post(self,request, args, *kw):
    #     data = self.request.data
        
    #     base64_image = data.get('supplier_image')
    #     if base64_image:
    #         image = base64.b64decode(base64_image.split(',')[1])
          
    #     SaveCustomer = MainRefSlSupplier(
    #         id_code = data['ID_Code'],
    #         trade_name = data['Tradename'],
    #         last_name = data['Lname'],
    #         first_name = data['Fname'],
    #         middle_name = data['MI'],
    #         business_phone_no = data['Phone'],
    #         mobile_no = data['Mobile'],
    #         fax_no = data['Fax'],
    #         address = data['Address'],
    #         city_municipality = data['City'],
    #         province = data['Province'],
    #         zip_code = data['ZipCode'],
    #         vat_registration_type = data['Vat'],
    #         tax_id_no = data['Tax'],
    #         group_name = data['Group'],
    #         # area_name = data['Area'],
    #         # agent_name = data['Agent'],
    #         # collector_name = data['Collector'],
    #         # kob_name = data['KOB'],
    #         sl_sub_category_description = data['sl'],
    #         remarks = data['Remarks'],
    #         supplier_image = image,
    #     )
    #     SaveCustomer.save()
    #     return Response({'mesage':'Customer Successfully Added'})
    
    # def put(self, request, args, *kwargs):
    #     data = request.data
    #     try:
    #         cutomerDetails = MainRefSlSupplier.objects.get(id_code=data['ID_Code'])
    #         cutomerDetails.id_code = data.get('ID_Code', cutomerDetails.id_code)
    #         cutomerDetails.trade_name = data.get('Tradename', cutomerDetails.trade_name)
    #         cutomerDetails.last_name = data.get('Lname', cutomerDetails.last_name)
    #         cutomerDetails.first_name = data.get('Fname', cutomerDetails.first_name)
    #         cutomerDetails.middle_name = data.get('MI', cutomerDetails.middle_name)
    #         cutomerDetails.business_phone_no = data.get('Phone', cutomerDetails.business_phone_no)
    #         cutomerDetails.mobile_no = data.get('Mobile', cutomerDetails.mobile_no)
    #         cutomerDetails.fax_no = data.get('Fax', cutomerDetails.fax_no)
    #         cutomerDetails.address = data.get('Address', cutomerDetails.address)
    #         cutomerDetails.city_municipality = data.get('City', cutomerDetails.city_municipality)
    #         cutomerDetails.province = data.get('Province', cutomerDetails.province)
    #         cutomerDetails.zip_code = data.get('ZipCode', cutomerDetails.zip_code)
    #         cutomerDetails.vat_registration_type = data.get('Vat', cutomerDetails.vat_registration_type)
    #         cutomerDetails.tax_id_no = data.get('Tax', cutomerDetails.tax_id_no)
    #         cutomerDetails.active_status = data.get('Status', cutomerDetails.active_status)
    #         cutomerDetails.group_name = data.get('Group', cutomerDetails.group_name)
    #         # cutomerDetails.area_name = data.get('Area', cutomerDetails.area_name)
    #         # cutomerDetails.agent_name = data.get('Agent', cutomerDetails.agent_name)
    #         # cutomerDetails.collector_name = data.get('Collector', cutomerDetails.collector_name)
    #         # cutomerDetails.kob_name = data.get('KOB', cutomerDetails.kob_name)
    #         cutomerDetails.sl_sub_category_description = data.get('sl', cutomerDetails.sl_sub_category_description)
    #         cutomerDetails.remarks = data.get('Remarks', cutomerDetails.remarks)
    #         base64_image = data.get('image')

    #         if base64_image:
    #             image = base64.b64decode(base64_image.split(',')[1])
    #             cutomerDetails.supplier_image = image
    #         cutomerDetails.save()

    #         return Response({"message": "UnitLocation updated successfully"}, status=status.HTTP_200_OK)
    #     except UnitLocation.DoesNotExist:
    #         return Response({"error": "UnitLocation not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


####* **************************** Get Cashiers Login For the Day ****************************
    
@api_view(['GET','POST'])
def get_cahiers_login(request):
    if request.method == 'GET':
        DateFrom = request.query_params.get("DateFrom")
        DateTo = request.query_params.get("DateTo")
        # filterDate = json.loads(request.body)
        print(DateFrom,DateTo)
        # pdb.set_trace()
        # dateFrom = filterDate.GET.get('DateFrom')  # Corrected typo in ".Get"
        # dateTo = filterDate.GET.get('DateTo') 
        current_date_ph = GetPHilippineDate()
        if DateFrom and DateTo:
            data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES', islogout='YES',isxread='NO')
            list_data = []
            if data:
                for item in data:
                    reviewed = 'NO'  # Default value
                    login_record = '0'
                    login_record = item.trans_id
                    # print(item.trans_id)
                    cash_breakdown_data = PosCashBreakdown.objects.filter(login_record=item.trans_id)

                    if cash_breakdown_data.exists():
                       
                        # Iterate over each PosCashBreakdown object in the queryset
                        for breakdown_item in cash_breakdown_data:
                            if breakdown_item.reviewed_by not in ['', '0']:
                                reviewed = 'YES'
                                break
                    cashiers_data = {
                            'idcode': item.id_code,
                            'fullname': item.name_stamp,
                            'status': reviewed,
                            'login_record':login_record
                            }
                    list_data.append(cashiers_data)
                print(list_data)
                return Response(list_data)
            else: 
                return JsonResponse({'message':'No Data Found'})

        else:
            # pdb.set_trace()
            data = PosCashiersLogin.objects.filter(date_stamp=current_date_ph, isshift_end='YES')
            
            if data:

                serialize = PosCashiersLoginpSerializer(data, many=True)  # Corrected typo in "PosCashiersLoginpSerializer"
                return JsonResponse(serialize.data)
            else: 
                return JsonResponse({'message':'No Data Found'})
    
    elif request.method == 'POST':
        try:
            cashierData = json.loads(request.body)
            TransID = cashierData['TransID']
            Fullname = cashierData['Fullname']
            data = PosCashBreakdown.objects.filter(login_record=TransID)
            if data:
                data.reviewed_by = Fullname
                data.save()
                return JsonResponse({'message':'Reviewed Successfully'},status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
@api_view(['GET','POST'])
def get_cash_count_cash_breakdown(request):
    if request.method == 'GET':
        # pdb.set_trace()
        login_record = request.query_params.get('login_record')
        # DateFrom = request.query_params.get("DateFrom")
        print('login_record',login_record)
        cashBreakdown = PosCashBreakdown.objects.filter(login_record=login_record)
        serialize = PosCashBreakdownSerializer(cashBreakdown,many=True)
        print(cashBreakdown)
        print(serialize.data)
        return Response(serialize.data)
    elif request.method == 'POST':
        # pdb.set_trace()
        data_recieve = json.loads(request.body)
        login_record = data_recieve.get('login_record')
        UserID = data_recieve.get('UserID')
        print('login_record',login_record)

        data = data_recieve.get('data')
        dinomination = data.get('dinomination')
        Totaldenominations = data.get('Totaldenominations')
        current_date_ph = GetPHilippineDate()
        cash_breakdown_instances = []
        conversion_rates = {
            'OneThousand': 1000,
            'FiveHundred': 500,
            'TwoHundred': 200,
            'OneHundred': 100,
            'Fifty': 50,
            'Twenty': 20,
            'Ten': 10,
            'Five': 5,
            'Peso': 1,
            'Cent25': 0.25,
            'Cent05': 0.05
        }
        # pdb.set_trace()
        # Iterate over the keys in dinomination
        for denomination, quantity in dinomination.items():
            if int(quantity) > 0:
                value = conversion_rates[denomination]
                breakdown_instance = PosCashBreakdown.objects.filter(login_record=login_record,denomination=value).first()

                if breakdown_instance:
                    breakdown_instance.reviewed_by = UserID
                    breakdown_instance.quantity = quantity
                    breakdown_instance.total = float(value) * int(quantity)
                    breakdown_instance.save()
                else:
                    breakdown_instance = PosCashBreakdown(
                            reviewed_by = UserID,
                            login_record=login_record,  # Provide appropriate value
                            date_stamp=current_date_ph,  # Provide appropriate value
                            quantity=quantity,
                            denomination= value,
                            total=float(value) * int(quantity),  # Get the total amount by multiplying quantity with value
                        )
                    breakdown_instance.save()
        return JsonResponse({'message':"This endpoint is for POST requests only."},status=200)



####* **************************** Get Cashiers Login For XREADING ****************************
    
@api_view(['GET','POST'])
def get_cahiers_login_for_xread(request):
    if request.method == 'GET':
        DateFrom = request.query_params.get("DateFrom")
        DateTo = request.query_params.get("DateTo")
        # filterDate = json.loads(request.body)
        print(DateFrom,DateTo)
        # pdb.set_trace()
        # dateFrom = filterDate.GET.get('DateFrom')  # Corrected typo in ".Get"
        # dateTo = filterDate.GET.get('DateTo') 
        current_date_ph = GetPHilippineDate()
        if DateFrom and DateTo:
            data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES',islogout='YES',isxread='NO')
            if data:

                serialize = PosCashiersLoginpSerializer(data, many=True)  # Corrected typo in "PosCashiersLoginpSerializer"
                return Response(serialize.data)
            else: 
                return JsonResponse({'message':'No Data Found'})

        else:
            # pdb.set_trace()
            data = PosCashiersLogin.objects.filter(date_stamp=current_date_ph, isshift_end='YES')
            
            if data:

                serialize = PosCashiersLoginpSerializer(data, many=True)  # Corrected typo in "PosCashiersLoginpSerializer"
                return JsonResponse(serialize.data)
            else: 
                return JsonResponse({'message':'No Data Found'})
    
    elif request.method == 'POST':
        try:
            # pdb.set_trace()
            cashierData = json.loads(request.body)
            login_record = cashierData.get('login_record')
            id_code = cashierData.get('id_code')
            Cashiername = cashierData.get('Cashiername')
            data = PosCashiersLogin.objects.filter(trans_id=login_record,id_code=id_code).first()
            if data:
                data.isxread = 'YES'
                data.save()
                return JsonResponse({'message':'Xreading Successfully'},status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


####* **************************** Generate Data For XREADING ****************************
@api_view(['GET','POST'])       
def generate_data_xread(request):
    if request.method =='GET':
        DateFrom = request.query_params.get("DateFrom")
        DateTo = request.query_params.get("DateTo")
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        
        sales_invoices_listing = PosSalesInvoiceListing.objects.filter(
            doc_date__range=(DateFrom, DateTo),
            isvoid='NO',
            terminal_no=machineInfo.terminal_no,
            ).exclude(status__in=['A', 'N']).order_by('doc_date')
        print(sales_invoices_listing)

        sales_data = PosSalesInvoiceList.objects.filter(
            doc_date__range=(DateFrom, DateTo),
            terminal_no=machineInfo.terminal_no,
            doc_type__in=['POS-SI', 'POS-CI'],
            ).exclude(status__in=['A', 'N']).aggregate(
            total_cash=Sum('total_cash'),
            total_check=Sum('total_check'),
            total_pdc=Sum('total_pdc'),
            total_eps=Sum('total_eps'),
            total_credit_card=Sum('total_credit_card'),
            total_credit_sales=Sum('total_credit_sales'),
            discount=Sum('discount'),
            ServiceCharge_TotalAmount=Sum('ServiceCharge_TotalAmount'),
            sub_total=Sum('sub_total'),
            vat=Sum('vat'),
            vat_exempt=Sum('vat_exempt'),
            vat_exempted=Sum('vat_exempted'),
            net_vat=Sum('net_vat')
        )
        
        total_cash = sales_data['total_cash'] or 0
        total_check = sales_data['total_check'] or 0
        total_pdc = sales_data['total_pdc'] or 0
        total_eps = sales_data['total_eps'] or 0
        total_credit_card = sales_data['total_credit_card'] or 0
        total_credit_sales = sales_data['total_credit_sales'] or 0
        discount = sales_data['discount'] or 0
        service_charge_total_amount = sales_data['ServiceCharge_TotalAmount'] or 0
        sub_total = sales_data['sub_total'] or 0
        vat = sales_data['vat'] or 0
        vat_exempt = sales_data['vat_exempt'] or 0
        vat_exempted = sales_data['vat_exempted'] or 0
        net_vat = sales_data['net_vat'] or 0
    
        response_data = {
        'SerialNo':machineInfo.Serial_no,
        'terminalNo':machineInfo.terminal_no,
        'total_cash': total_cash,
        'total_check': total_check,
        'total_pdc': total_pdc,
        'total_eps': total_eps,
        'total_credit_card': total_credit_card,
        'total_credit_sales': total_credit_sales,
        'discount': discount,
        'service_charge_total_amount': service_charge_total_amount,
        'sub_total': sub_total,
        'vat': vat,
        'vat_exempt': vat_exempt,
        'vat_exempted': vat_exempted,
        'net_vat': net_vat
}

        return JsonResponse(response_data)