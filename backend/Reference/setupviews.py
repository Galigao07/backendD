import abc
import base64
import json
import locale
import os
import pdb
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from backend.models import (BankCompany, POS_Terminal,TSetup,AcctSubsidiary,OtherAccount,Employee,Customer,RCCDetails,CCCDetails,ProductCategorySetup,
                            ProductSiteSetup,PosPriceTypeSiteSetup,PosMultiplePriceTypeSiteSetup,ProductCategorySales,PosSetup,AcctList)
from backend.serializers import (BankCompanySerializer,TSetupSerializer,AcctSubsidiarySerializer,OtherAccountSerializer,EmployeeSetupSerializer,
                                 CustomerSerializer,RCCDetailsSerializer,CCCDetailsSerializer,ProductCategorySetupSerializer,ProductSiteSetupSerializer,
                                 PosPriceTypeSiteSetupSerializer,PosMultiplePriceTypeSiteSetupSerializer,ProductCategorySalesSerializer,PosSetupSerializer,
                                 AcctListSerializer)
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
        try:
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

            elif TransType =='PriceType':
                product_setups = ProductSiteSetup.objects.filter(active='Y')

                # Iterate over each item in product_setups
                for product_item in product_setups:
                    # Fetch setups from PosPriceTypeSiteSetup based on site_desc (assuming it's a foreign key or related field)
                    setups = PosPriceTypeSiteSetup.objects.filter(site_name=product_item.site_desc)
                    # Serialize setups using the serializer
                    serialized_setups = PosPriceTypeSiteSetupSerializer(setups, many=True).data
                    
                    # Create a dictionary containing required fields
                    list_data = {
                        'site_code': product_item.site_code,
                        'site_name': product_item.site_desc,  # Assuming site_desc is intended for site name
                        'default_pricetype': serialized_setups[0]['default_pricetype'] if serialized_setups else '',
                        'default_pricetype_name': serialized_setups[0]['default_pricetype_name'] if serialized_setups else ''
                    }

                    setupData.append(list_data)

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
                elif Transaction == 'Setup SL Type Per Terminal':
                        x = 0
                        while x < 10 :
                            x += 1
                            terminal = 'Terminal Number : ' + str(x)

                            data = TSetup.objects.filter(event_name = terminal)
                            if data:
                                for setup in data:
                                    listdata = {
                                        'event': setup.event_name,
                                        'accttitle':setup.acct_title,
                                        'slacct':setup.sl_acct,
                                        'slid': setup.sl_id,
                                        'sl_type': setup.sl_type,
                                    }
                                    setupData.append(listdata)
                            else:
                                listdata = {
                                'event':terminal,
                                'accttitle':'',
                                'slacct':'',
                                'slid': '0',
                                'sl_type': '',
                                }
                                setupData.append(listdata)
                                        
            print(setupData)
            return Response(setupData)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response('Error Happened!')
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
                data = AcctSubsidiary.objects.filter(subsidiary_acct_title__icontains=acct_title)
                serialize = AcctSubsidiarySerializer(data,many=True)
                return Response(serialize.data)
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
            name = request.query_params.get('name',None)
   
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
                    print('sss')
                    data = RCCDetails.objects.filter(description__icontains = name)
                    serialize = RCCDetailsSerializer(data,many=True)
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
                # pdb.set_trace()
                event_name = items['event']
                acct_title = items['accttitle']
                sl_acct = items['slacct']
                sl_id = items['slid']
                sl_type = items['sl_type']
            try:
                t_setup = TSetup.objects.get(event_name=event_name)
                t_setup.acct_title = acct_title
                t_setup.sl_acct = sl_acct
                t_setup.sl_id = sl_id
                t_setup.sl_type = sl_type
                t_setup.save()
            except TSetup.DoesNotExist:
                t_setup = TSetup(
                    event_name=event_name,
                    acct_title=acct_title,
                    sl_acct=sl_acct,
                    sl_id=sl_id,
                    sl_type=sl_type
                )
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

@api_view(['POST','GET'])
@transaction.atomic     
def get_allowed_price_type(request):
    if request.method == 'GET':
        try:
            siteCode = request.query_params.get('site_code',None)
            siteDesc = request.query_params.get('site_desc',None)

            print(siteCode,siteDesc)

            if siteCode:
                product_setup2 = []
                product_setup = ProductSiteSetup.objects.filter(site_code=siteCode,site_desc=siteDesc)
                product_setup_serialize = ProductSiteSetupSerializer(product_setup,many=True)

                multiple_price = PosMultiplePriceTypeSiteSetup.objects.filter(site_code=siteCode, site_name=siteDesc)
                multiple_price_serialize = PosMultiplePriceTypeSiteSetupSerializer(multiple_price,many=True)

                return JsonResponse({'data':multiple_price_serialize.data})
            else:
                product_setup2 = []
                product_setup = ProductSiteSetup.objects.all()
                product_setup_serialize = ProductSiteSetupSerializer(product_setup,many=True)

                for item in product_setup_serialize.data[0]:
                    print('sadadas',product_setup_serialize.data[0])
                    if isinstance(item, dict):
                        site_code = int(item['site_code'])
                        multiple_price = PosMultiplePriceTypeSiteSetup.objects.filter(site_code=site_code, site_name=item['site_name'])
                        product_setup2.append(list(multiple_price))

                return JsonResponse({'data':product_setup_serialize.data})
        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['POST','GET'])
@transaction.atomic  
def get_tagging_category_list(request):
    if request.method == 'GET':
        try:
            type = request.query_params.get('type',None)
            data = ProductCategorySales.objects.all()
            serialize = ProductCategorySalesSerializer(data,many=True)
            return Response(serialize.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method == 'POST':
        try:
            receive_data = json.loads(request.body)
            data = receive_data.get('data')
            vat_type = receive_data.get('vat_type')
            for item in data:
                data2 = ProductCategorySales.objects.filter(
                    category_desc=item['category_desc'],
                    ).first()
                if data2:
                    if vat_type == 'VAT':
                        vat_code = AcctList.objects.filter(acct_title =item['vat_title']).first()
                        acct_code = AcctList.objects.filter(acct_title =item['acct_title2']).first()
                        if vat_code:
                            if acct_code:
                                data2.vat_code = vat_code.code
                                data2.vat_title = item['vat_title']
                                data2.acct_code2 = acct_code.code
                                data2.acct_title2 = item['acct_title2']
                                data2.save()
                            else:
                                data2.vat_code = vat_code.code
                                data2.vat_title = item['vat_title']
                                data2.acct_code2 =0
                                data2.acct_title2 = ''
                                data2.save()
                    elif vat_type == 'Non VAT':
                        nonvat_code = AcctList.objects.filter(acct_title =item['nonvat_title']).first()
                        acct_code = AcctList.objects.filter(acct_title =item['acct_title3']).first()
                        if nonvat_code:
                            if acct_code:
                                data2.nonvat_code = nonvat_code.code
                                data2.nonvat_title = item['nonvat_title']
                                data2.acct_code3 = acct_code.code
                                data2.acct_title3 = item['acct_title3']
                                data2.save()
                            else:
                                data2.nonvat_code = nonvat_code.code
                                data2.nonvat_title = item['nonvat_title']
                                data2.acct_code3 = 0
                                data2.acct_title3 = ''
                                data2.save()

                    elif vat_type == 'Zero Rated':
                        zerorated_code = AcctList.objects.filter(acct_title =item['zerorated_title']).first()
                        acct_code = AcctList.objects.filter(acct_title =item['acct_title4']).first()
                        if zerorated_code:
                            if acct_code:
                                data2.zerorated_code = zerorated_code.code
                                data2.zerorated_title = item['zerorated_title']
                                data2.acct_code4 = acct_code.code
                                data2.acct_title4 = item['acct_title4']
                                data2.save()
                            else:
                                data2.zerorated_code = zerorated_code.code
                                data2.zerorated_title = item['zerorated_title']
                                data2.acct_code4 = 0
                                data2.acct_title4 = ''
                                data2.save()

                    elif vat_type == 'VAT Excempt':
                        vatex_code = AcctList.objects.filter(acct_title =item['vatex_title']).first()
                        acct_code = AcctList.objects.filter(acct_title =item['acct_title5']).first()
                        if vatex_code:
                            if acct_code:
                                data2.vatex_code = vatex_code.code
                                data2.vatex_title = item['vatex_title']
                                data2.acct_code5 = acct_code.code
                                data2.acct_title5 = item['acct_title5']
                                data2.save()
                            else:
                                data2.vatex_code = vatex_code.code
                                data2.vatex_title = item['vatex_title']
                                data2.acct_code5 = 0
                                data2.acct_title5 = ''
                                data2.save()

                    
            return Response('Success')
        except Exception as e:
            print(e)
            traceback.print_exc()

@api_view(['POST','GET'])
@transaction.atomic 
def get_tagging_per_terminal(request):
    if request.method =='GET':
        try:
            dataList = []
            dataListFinal = []
            machineInfo = POS_Terminal.objects.all()

            for items in machineInfo:
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Cash Sales (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales paid through Current Checks (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales paid through Post Dated Checks (Debit)',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales on Account Guest Ledger (Debit)',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales on Account Banquet (Debit)',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales on Account Regular Customer (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales paid through Debit Card (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Sales paid through Credit Card (Debit)',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Senior citizen discount (Debit))',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'PWD discount (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'FO - Sales on Account Guest Ledger (Debit)',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Service Charge',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'FO - Sales on Event Ledger (Debit)',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Senior citizen discount Remarks',
                'acct_code':'0',
               'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Non - Senior citizen discount Remarks',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)


                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Item Discount',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Trade Discount',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)

                dataInfo = {
                'ul_code':items.ul_code,
                'site_code':int(items.site_no),
                'terminal_no':items.terminal_no,
                'event_name':'Transaction Discount',
                'acct_code':'0',
                'account_title':'',
                'subsidiary_code':'0',
                'subsidiary_account':'',
                'sl_type':''
                }
                dataList.append(dataInfo)
       

            for item in dataList:
                data = PosSetup.objects.filter(
                    ul_code=item['ul_code'],
                    site_code=item['site_code'],
                    terminal_no=item['terminal_no'],
                    event_name=item['event_name']
                ).first()

                if data:
                    # If data already exists, update it
                    item['account_title'] = data.account_title
                    item['subsidiary_account'] = data.subsidiary_account
                    item['acct_code'] = data.acct_code
                    item['subsidiary_code'] = data.subsidiary_code

                    SL_type_data = AcctSubsidiary.objects.filter(subsidiary_acct_title__icontains=data.account_title).first()
                    if SL_type_data:
                        item['sl_type'] = SL_type_data.sl_type


                else:
                    # If data doesn't exist, create a new entry
                    PosSetup.objects.create(**item)
            print(dataList)
            return Response(dataList)
        except Exception as e:
            print(e)
            traceback.print_exc()
    elif request.method =='POST':
        try:
            received_data = json.loads(request.body)
            data = received_data.get('data')

            for item in data:
                data2 = PosSetup.objects.filter(
                    ul_code=item['ul_code'],
                    site_code= int(item['site_code']),
                    terminal_no=item['terminal_no'],
                    event_name=item['event_name']
                ).first()

                if data2:
                    # pdb.set_trace()
                    data2.acct_code= item['acct_code'] 
                    data2.subsidiary_code = item['subsidiary_code'] 
                    data2.account_title = item['account_title']
                    data2.subsidiary_account = item['subsidiary_account']
                    data2.save()
                
                    print('success',data)
            return Response('Success')

        except Exception as e:
            print(e)
            traceback.print_exc()






