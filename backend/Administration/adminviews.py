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
import traceback
from decimal import Decimal
from django.db.models.functions import Concat
from django.db.models import F, CharField, Value, Q, Func, Value, Subquery, OuterRef, DecimalField
from django.db.models.functions import Cast, Coalesce


@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
def other_payment_setup(request):
    if request.method =='GET':
        try:
            data = PosOtherPmtSetup.objects.all()
            serializer = PosOtherPmtSetupSerialize(data,many=True)

            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=404)
    elif request.method == 'POST':
        try:
            print(1)
            data = request.data.get('data',None)
            pmt_code = data.get('pmt_code', 0)
            pmt_desc = data.get('pmt_desc', '')
            acct_code = data.get('acct_code', '')
            acct_title = data.get('acct_title', '')
            pmt_type = data.get('pmt_type', '')
            remarks = data.get('remarks', '')

            obj, created = PosOtherPmtSetup.objects.update_or_create(
            pmt_code=pmt_code,  # lookup field
            defaults={
                'pmt_desc': pmt_desc,
                'acct_code': acct_code,
                'acct_title': acct_title,
                'pmt_type': pmt_type,
                'remarks': remarks
            }
            )
            if created:
                message = "Record created successfully."
            else:
                message = "Record updated successfully."
            return Response({
                'message': message}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
            data = request.data.get('data', {})
            pmt_code = data.get('pmt_code', None)

            if not pmt_code:
                return Response({'error': 'Missing pmt_code'}, status=status.HTTP_400_BAD_REQUEST)

            obj = PosOtherPmtSetup.objects.filter(pmt_code=pmt_code).first()
            if not obj:
                return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

            obj.pmt_desc = data.get('pmt_desc', obj.pmt_desc)
            obj.acct_code = data.get('acct_code', obj.acct_code)
            obj.acct_title = data.get('acct_title', obj.acct_title)
            obj.pmt_type = data.get('pmt_type', obj.pmt_type)
            obj.remarks = data.get('remarks', obj.remarks)
            obj.save()

            return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)

        # ----------------------------
        # DELETE
        # ----------------------------
    elif request.method == 'DELETE':
            pmt_code = request.query_params.get('pmt_code', None)

            if not pmt_code:
                return Response({'error': 'Missing pmt_code'}, status=status.HTTP_400_BAD_REQUEST)

            obj = PosOtherPmtSetup.objects.filter(pmt_code=pmt_code).first()
            if not obj:
                return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

            obj.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)


####* **************************** USER *******************************
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def view_user(request):
    if request.method == 'GET':
        try:
            data = User.objects.filter(sys_type ='POS').exclude(fullname='Super Admin').order_by('-autonum')
            userList = UserSerializer(data, many=True).data
            return JsonResponse({'userList': userList}, status=200)
        except Exception as e:
            print(e)
            traceback.print_exc()
        
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_list(request):
    if request.method == 'GET':
        name = request.GET.get('employee','')
        if name == '':
            data = Employee.objects.filter(active='Y').order_by('-autonum')
        else:
            data = Employee.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name),active='Y').order_by('-autonum')
        
        EmployeeList = EmployeeSetupSerializer(data, many=True).data
        return JsonResponse({'EmployeeList': EmployeeList}, status=200)
    


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def systemSettings(request):
    if request.method == 'GET':
        try:
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no)
            serialize = POSSettingsSerializer(pos_settings,many=True)

            pos_discount = PosDiscountSetup.objects.all()

            discount = PosDiscountSetupSerializer(pos_discount,many=True)

            data = {
                'Settings':serialize.data,
                'discount':discount.data
            }
            return Response(data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error':str(e)})
    if request.method == 'POST':
        try:
            recieve_data = json.loads(request.body)
            data = recieve_data.get('data')
            print(data)
            serial_number = getattr(request, "SERIALNO", None)
            # serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            # pdb.set_trace()
            # pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no).first()
            # if pos_settings:
            #     pos_settings.withHotel = data['withHotel']
            #     pos_settings.ProductColPerRows =  data['ProductColPerRows']
            #     pos_settings.TableColPerRows =  data['TableColPerRows']
            #     pos_settings.ShowArrowUpAndDown = data['ShowArrowUpAndDown']
            #     pos_settings.save()
            # Fields to update/create (excluding discount amounts)
            fields_to_update = [
                'Baggers', 'esc_mode', 'Salesman', 'Checker', 'EPS', 'PO_Charge', 
                'void_item', 'void_trans', 'price_override', 'vat_override',
                'trade_discount', 'senior_citizen', 'discount', 'product_details_decimals',
                'items_selling_price', 'cash', 'checks', 'debit', 'credit', 'PO',
                'gift_check', 'gift_check_with_serial_no', 'credit_sales', 'stale',
                'bankcard', 'multipleCheck', 'multipleCharge', 'returns', 'cashpullout',
                'soCancel', 'regular', 'with_barcode', 'order_type', 'printer_no',
                'printer_type', 'printer_name', 'virtual_receipt', 'manual_or',
                'change_fund', 'borrowed_fund', 'multiple_printer',
                'Allow_SalesOrderReceipt', 'Allow_WholeDay', 'allowed_retail',
                'include_servicecharge', 'ServiceCharge_DineIn', 'ServiceCharge_TakeOut',
                'ServiceCharge_Room', 'ServiceCharge_Retail', 'allow_duplicate_copy',
                'allow_service_charge_printout', 'allow_discount_percent', 'xz_filter',
                'showCreditlimit', 'ShowExtendedForm', 'Allow_BilloutBreakDown',
                'Allow_Duplicate_SO', 'Allow_cancel_transaction', 'allow_LiveQty',
                'CostComputation', 'VisibleAmount_tendered', 'Interchangeable_salesman',
                'weight_scale', 'weight_scale_start', 'weight_scale_last_degit_for_Qty',
                'BarcodeLenght', 'DecimalPlaces', 'RoundDigits', 'RoundType',
                'InputPrimaryMethod', 'item_search', 'item_display', 'Display_UOM',
                'Settle_order_only', 'Allow_filter_in_supervisor_cash_count',
                'Allow_display_live_qty', 'Allow_crystal_report', 'Allow_consignment_to_display',
                'Allow_TakeOut_Direct_Pay', 'withHotel', 'ProductColPerRows',
                'naac_discount','pwd_discount',
                'TableColPerRows', 'ShowArrowUpAndDown', 'transaction_discount'
            ]

            # Prepare dictionary with only allowed fields from `data`
            defaults = {field: data[field] for field in fields_to_update if field in data}

            # Update if exists, otherwise create
            pos_settings, created = POSSettings.objects.update_or_create(
                terminal_no=machineInfo.terminal_no,
                site_no=machineInfo.site_no,
                defaults=defaults
            )

            if created:
                print("✅ POSSettings created")
            else:
                print("✅ POSSettings updated")

            SC = data['SCAmount']
            PWD = data['PWDAmount']
            NAAC = data['NAACDiscount']

            PosDiscountSetup.objects.update_or_create(
                description = 'SC',
                disc_rate = SC
            )
            PosDiscountSetup.objects.update_or_create(
                description = 'PWD',
                disc_rate = PWD
            )

            PosDiscountSetup.objects.update_or_create(
                description = 'NAAC',
                disc_rate = NAAC
            )



            return Response('Success')
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error':str(e)})



####* **************************** Lead/Supplier Setup *******************************
@api_view(['GET','POST'])   
def lead_setup(request):
    if request.method == 'GET':
        data = LeadSetup.objects.all()
        
        serializer = LeadSetupSerializer(data,many=True).data
        return JsonResponse({'data': serializer}, status=200)
    
    elif request.method == 'POST':

        try:
            received_data = json.loads(request.body)

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
            if autonum == '':
                autonum = 0
            CheckDtata = LeadSetup.objects.filter(autonum=autonum).first()
            
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
        except Exception as e:
            print(e)
            traceback.print_exc()

####* **************************** Client Setup *******************************
@api_view(['GET','POST'])   
def Client_setup(request):
    if request.method == 'GET':
        data = PosClientSetup.objects.all()
        
        serializer = PosClientSetupSerializer(data,many=True)

        return JsonResponse({'data': serializer.data}, status=200)
    
    elif request.method == 'POST':

        received_data = json.loads(request.body)


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



####* **************************** Terminal Setup *******************************
@api_view(['GET','POST'])       
def terminal_setup(request):
    if request.method == 'GET':
        data = POS_Terminal.objects.all()
        
        serializer = POS_TerminalSerializer(data,many=True).data
        return JsonResponse({'data': serializer}, status=200)
    
    elif request.method == 'POST':
    
        received_data = json.loads(request.body)
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
        
        if autonum == '':
            autonum = 0

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







