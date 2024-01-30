import abc
import json
import locale
from django.http import JsonResponse
from rest_framework.response import Response
from backend.models import (Product,PosRestTable,PosSalesOrder,PosSalesTransDetails,InvRefNo,POS_Terminal,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                            CompanySetup,Customer,PosWaiterList,PosPayor,User,Employee)
from backend.serializers import (ProductSerializer,ProductCategorySerializer,PosSalesOrderSerializer,PosSalesTransDetailsSerializer,PosSalesTransSerializer,
                                 PosSalesInvoiceListing,PosSalesInvoiceList,CustomerSerializer,PosWaiterListSerializer,PosPayorSerializer,PosSalesInvoiceListSerializer,
                                 UserSerializer,EmployeeSetupSerializer,PosRestTableSerializer)
from rest_framework.decorators import api_view
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Q


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

