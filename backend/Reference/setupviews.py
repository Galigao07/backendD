import abc
import base64
import json
import locale
import os
import pdb
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from backend.models import (BankCompany,TSetup,AcctSubsidiary,OtherAccount,Employee,Customer,RCCDetails,CCCDetails,ProductCategorySetup)
from backend.serializers import (BankCompanySerializer,TSetupSerializer,AcctSubsidiarySerializer,OtherAccountSerializer,EmployeeSetupSerializer,
                                 CustomerSerializer,RCCDetailsSerializer,CCCDetailsSerializer,ProductCategorySetupSerializer)
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
from django.db import transaction
from django.db.models import  F, Value
from django.db.models.functions import Concat

@api_view(['GET','POST','DELETE'])
def Setup(request):
    if request.method == 'GET':
        TransType = request.query_params.get('TransType',None)
        Transaction = request.query_params.get('Transaction',None)
        print(TransType,Transaction)
        # pdb.set_trace()
        setupData = []
        if TransType == 'Bank':
            Data = BankCompany.objects.all()

            for item in Data:
                # Filter Setup model based on event_name matching company_description
                setups = TSetup.objects.filter(event_name=item.company_description,status=Transaction)

                if setups:
                     for setup in setups:

                        if setup.acct_title is not None:
                            acctTitle = setup.acct_title
                        else:
                            acctTitle = ''
                        listdata ={
                            'bankcode':item.id_code,
                            'bankname':item.company_description,
                            'accttitle':acctTitle,
                            'slacct':setup.sl_acct,
                            'slid': setup.sl_id,
                            'status':setup.status,
                            'sl_type': setup.sl_type,
                            
                        }

                        setupData.append(listdata)
                else:
                    listdata ={
                            'bankcode':item.id_code,
                            'bankname':item.company_description,
                            'slname': '',
                            'accttitle':'',
                            'slacct':'',
                            'slid': '0',
                            'status':Transaction,
                            'sl_type': '',
                        }
                    setupData.append(listdata)

        else:
            if Transaction == 'Setp-up of Debit account for Sales Transaction':
                dataList = [
                    "Cash Sales (Debit)",
                    "Sales paid through Current Checks (Debit)",
                    "Sales paid through Post Dated Checks (Debit)",
                    "Sales on Account Guest Ledger (Debit)",
                    "Sales on Account Banquet (Debit)",
                    "Sales on Account Regular Customer (Debit)",
                    "Sales paid through Debit Card (Debit)",
                    "Sales paid through Credit Card (Debit)",
                    "Senior citizen discount (Debit)",
                    "PWD discount (Debit)",
                    "FO - Sales on Account Guest Ledger (Debit)",
                    "Service Charge",
                    "FO - Sales on Event Ledger (Debit)",
                    "Senior citizen discount Remarks",
                    "Non - Senior citizen discount Remarks",
                    "Item Discount",
                    "Trade Discount",
                    "Transaction Discount"
                ]

                for item in dataList:
                    setups = TSetup.objects.filter(event_name=item)
                    if setups:
                        for setup in setups:
                            listdata ={
                                    'event':item,
                                    'accttitle':setup.acct_title,
                                    'slacct':setup.sl_acct,
                                    'slid': setup.sl_id,
                                    'sl_type': setup.sl_type,
                                }
                        setupData.append(listdata)
                    else:
                        listdata ={
                            'event':item,
                            'accttitle':'',
                            'slacct':'',
                            'slid': '0',
                            'sl_type': '',
                        }
                        setupData.append(listdata)
            elif Transaction == 'Setp-up of Credit account for Sales Transaction':
                dataList = [
                    "Cash Sales (Credit)",
                    "Sales paid through Current Checks (Credit)",
                    "Sales paid through Post Dated Checks (Credit)",
                    "Sales on Account Guest Ledger (Credit)",
                    "Sales on Account Banquet (Credit)",
                    "Sales on Account Regular Customer (Credit)",
                    "Sales paid through Debit Card (Credit)",
                    "Sales paid through Credit Card (Credit)",
                    "Senior citizen discount (Credit)",
                    "FO - Sales on Account Guest Ledger (Credit)",
                    "FO - Sales on Event Ledger (Credit)"
                        ]
                for item in dataList:
                    setups = TSetup.objects.filter(event_name=item)
                    if setups:
                        for setup in setups:
                            listdata ={
                                    'event':item,
                                    'accttitle':setup.acct_title,
                                    'slacct':setup.sl_acct,
                                    'slid': setup.sl_id,
                                    'sl_type': setup.sl_type,
                                }
                        setupData.append(listdata)
                    else:
                        listdata ={
                            'event':item,
                            'accttitle':'',
                            'slacct':'',
                            'slid': '0',
                            'sl_type': '',
                        }
                        setupData.append(listdata)
        # print(setupData)
        return Response(setupData)
    elif request.method == 'POST':
        return Response('Success')
    
    elif request.method == 'DELETE':
        return Response('Success')

@api_view(['GET'])
def get_account_title(request):
    if request.method == 'GET':
        try:
            acct_title = request.query_params.get('account_title',None)
     

            if acct_title:
                data = AcctSubsidiary.objects.filter(subsidiary_acct_title__icontain=acct_title)
                serialize = AcctSubsidiarySerializer(data,many=True)
                return JsonResponse(serialize.data)
            else:
                data = AcctSubsidiary.objects.all()
                data = AcctSubsidiary.objects.all()
                serializer = AcctSubsidiarySerializer(data, many=True)  # Set safe parameter to False
                return Response(serializer.data)
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return Response({"message": "An error occurred while saving the sales order"}, status=500)
        
@api_view(['GET'])
def get_SL_account(request):
    if request.method == 'GET':
        try:
            sl_type = request.query_params.get('sl_type',None)
            print('sl_type',sl_type)
            # name = request.query_params.get('name',None)
            name = ''
            # pdb.set_trace()
     

            if sl_type =='O':
                if name:
                    data = OtherAccount.objects.filter(sl_name__icontains = name ,acct_title = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)
                else:
                    data = OtherAccount.objects.filter(acct_title__icontains = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)

            elif sl_type =='E':
                if name:
                    data = Employee.objects.annotate(sl_name=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'))
                    serialize = EmployeeSetupSerializer(data,many=True)
                    print(serialize.data)
                    return Response(serialize.data)
                else:
                    data = Employee.objects.all()
                    serialize = EmployeeSetupSerializer(data,many=True)
                    return Response(serialize.data)
            elif sl_type =='C':
                if name:
                    data = OtherAccount.objects.filter(sl_name__icontains = name ,acct_title = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)
                else:
                    data = Customer.objects.all()
                    serialize = CustomerSerializer(data,many=True)
                    return Response(serialize.data)
            elif sl_type =='T':
                if name:
                    data = OtherAccount.objects.filter(sl_name__icontains = name ,acct_title = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)
                else:
                    data = OtherAccount.objects.filter(acct_title = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)
            elif sl_type =='R':
                if name:
                    data = RCCDetails.objects.filter(sl_name__icontains = name ,acct_title = 'Cash in Bank')
                    serialize = OtherAccountSerializer(data,many=True)
                    return Response(serialize.data)
                else:
                    data = RCCDetails.objects.all()
                    serialize = RCCDetailsSerializer(data,many=True)
                    return Response(serialize.data)


        except Exception as e:
            print(e)
            traceback.print_exc()  
            return Response({"message": "An error occurred while saving the sales order"}, status=500)

@api_view(['POST'])
@transaction.atomic
def setup_configure(request):
    if request.method =='POST':
        try:
            received_data = json.loads(request.body)
            data = received_data.get('data', [])
            print(data)
            for items in data:
                event_name = items['event']
                acct_title = items['accttitle']
                sl_acct = items['slacct']
                sl_id = items['slid']
                sl_type = items['sl_type']

                t_setup = TSetup.objects.get(event_name=event_name)

                t_setup.acct_title = acct_title
                t_setup.sl_acct = sl_acct
                t_setup.sl_id = sl_id
                t_setup.sl_type = sl_type
                t_setup.save()
            return Response('Success',status=200)
        except Exception as e:
            print(e)
            traceback.print_exc()
            transaction.rollback()

@api_view(['POST','GET'])
@transaction.atomic
def get_cost_of_sales(request):
    if request.method == 'GET':
        try:
            data = ProductCategorySetup.objects.all()
            serialize = ProductCategorySetupSerializer(data,many=True)

            return Response(serialize.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            transaction.rollback()
        



