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
                            CompanySetup,Customer,PosWaiterList,PosPayor,User,Employee)
from backend.serializers import (ProductSerializer,ProductCategorySerializer,PosSalesOrderSerializer,PosSalesTransDetailsSerializer,PosSalesTransSerializer,
                                 PosSalesInvoiceListing,PosSalesInvoiceList,CustomerSerializer,PosWaiterListSerializer,PosPayorSerializer,PosSalesInvoiceListSerializer,
                                 UserSerializer,EmployeeSetupSerializer,PosRestTableSerializer,POS_TerminalSerializer)
from rest_framework.decorators import api_view
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
@api_view(['GET','POST'])
def UploadVideo(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            # Save the file to the media directory
            filename = video_file.name
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            with open(filepath, 'wb') as destination:
                # Read the entire file content at once
                file_content = video_file.read()
                # Write the file content to the destination
                destination.write(file_content)
            
            # Return a response indicating success
            video_url = os.path.join(settings.MEDIA_URL, filename)
            return Response({'message': 'Video uploaded successfully', 'url': video_url}, status=200)
        else:
            return Response({'error': 'No video file provided'}, status=400)
    
    elif request.method == 'GET':

        media_dir = os.path.join(settings.BASE_DIR, 'media')

        # Check if the videos directory exists
        if os.path.isdir(media_dir):
            # List all files in the videos directory
            video_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]

            # Sort files by modification time (latest first)
            video_files.sort(key=lambda x: os.path.getmtime(os.path.join(media_dir, x)), reverse=True)

            # Get the path to the latest video file
            if video_files:
                latest_video_file = os.path.join(media_dir, video_files[0])
                with open(latest_video_file, 'rb') as file:
                    file_content = file.read()

                    # Encode the file content to Base64
                    base64_content = base64.b64encode(file_content).decode()
                    # print(base64_content)
                    # Construct the data URL
                    # data_url = 'data:base64,{base64_content}'

                    data_url = f'data:video/mp4;base64,{base64_content}'
      
                return JsonResponse({'data':data_url})
                # Serve the latest video file
            else:
                return Response({'error': 'No videos found in the media directory'}, status=404)
        else:
            return Response({'error': 'Media directory not found'}, status=404)



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


