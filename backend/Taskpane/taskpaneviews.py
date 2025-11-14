import abc
import json
import locale
from django.http import JsonResponse
from rest_framework.response import Response
from backend.models import *
from backend.serializers import *
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Min,Max
from django.utils import timezone
from backend.views import get_serial_number
from datetime import datetime, timedelta
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime
import traceback
from backend.views import *


####* **************************** Get Cashiers Login For the Day ****************************
    
@api_view(['GET','POST'])
def get_cahiers_login(request):
    if request.method == 'GET':
        DateFrom = request.query_params.get("DateFrom")
        DateTo = request.query_params.get("DateTo")

        current_date_ph = GetPHilippineDate()
        if DateFrom and DateTo:
            data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES', islogout='YES',isxread='NO')
            list_data = []
            if data:
                for item in data:
                    reviewed = 'NO'  # Default value
                    login_record = '0'
                    login_record = item.trans_id

                    cash_breakdown_data = PosCashBreakdown.objects.filter(login_record=item.trans_id)

                    if cash_breakdown_data.exists():
                       
                        # Iterate over each PosCashBreakdown object in the queryset
                        for breakdown_item in cash_breakdown_data:
                            if breakdown_item.reviewed_by not in ['', '0',0]:
                                reviewed = 'YES'
                                break
                    cashiers_data = {
                        'idcode': item.id_code,
                        'fullname': item.name_stamp,
                        'status': reviewed,
                        'login_record':login_record
                        }
                    list_data.append(cashiers_data)

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
@permission_classes([IsAuthenticated])
def get_cash_count_cash_breakdown(request):
    if request.method == 'GET':
        # pdb.set_trace()
        login_record = request.query_params.get('login_record')
        cashBreakdown = PosCashBreakdown.objects.filter(login_record=login_record)
        serialize = PosCashBreakdownSerializer(cashBreakdown,many=True)
        return Response(serialize.data)
    elif request.method == 'POST':
        # pdb.set_trace()
        data_recieve = json.loads(request.body)
        login_record = data_recieve.get('login_record')
        UserID = data_recieve.get('UserID')


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

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def approved_cash_breakdown(request):
    if request.method =='POST':
        try:
            login_record = request.data.get('login_record')
            cashier_name = request.data.get('cashier_name')
            approve_by = request.user.id_code

            PosCashBreakdown.objects.filter(login_record=login_record).update(
                reviewed_by = approve_by
            )

            # PosCashiersLogin.objects.filter(trans_id=login_record).update(
            #     isxread='YES'
            # )
            PDFCashBreakDownApproved(request,login_record,cashier_name)
            return Response('Successfully Approved',status=200)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response(e,status=401)



####* **************************** Get Cashiers Login For XREADING ****************************
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_cahiers_login_for_xread(request):
    if request.method == 'GET':
        DateFrom = request.GET.get("DateFrom")
        DateTo = request.GET.get("DateTo")
        if DateFrom and DateTo:
            try:
                list_data =[]
                data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES',islogout='YES',isxread='NO')
                if data:
                    for item in data:
                        
                        login_record = '0'
                        login_record = item.trans_id

                        cash_breakdown_data = PosCashBreakdown.objects.filter(login_record=item.trans_id)

                        if cash_breakdown_data.exists():
                        
                            # Iterate over each PosCashBreakdown object in the queryset
                            for breakdown_item in cash_breakdown_data:
                                if breakdown_item.reviewed_by not in ['', '0',0]:
                                    list_data.append(item)
                                    break

                        # serialize = PosCashiersLoginpSerializer(data, many=True)  # Corrected typo in "PosCashiersLoginpSerializer"
                if list_data:
                    serializer = PosCashiersLoginpSerializer(list_data, many=True)
                    return Response(serializer.data)
                else:
                    return Response({'message':'No Data Found'},status=401)

            except Exception as e:
                print(e)
                traceback.print_exc()
    
    elif request.method == 'POST':
        try:
            # pdb.set_trace()
            login_record = request.data.get('login_record')
            id_code = request.data.get('id_code')
            Cashiername = request.data.get('Cashiername')
            data = PosCashiersLogin.objects.filter(trans_id=login_record,id_code=id_code).first()
            if data:
                data.isxread = 'YES'
                data.save()

                PrintXread(request,login_record,Cashiername)
                

                return JsonResponse({'message':'Xreading Successfully'},status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)



####* **************************** Get Cashiers Login For XREADING ****************************
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_cahiers_login_done_xread(request):
    if request.method == 'GET':
        DateFrom = request.GET.get("DateFrom")
        DateTo = request.GET.get("DateTo")
 
        if DateFrom and DateTo:
            data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES',islogout='YES',isxread='NO')
            if data:
                return JsonResponse({'message':'Data Found'},status=200)
            else: 
                data = PosCashiersLogin.objects.filter(date_stamp__range=[DateFrom, DateTo], isshift_end='YES',islogout='YES',isxread='YES')
                if data:
                    list_data = []
                    for item in data:
                        trans_id = item.trans_id

                        list_ = TblPosDailyRecords.objects.filter(id=trans_id,iszread='NO')

                        if list_:
                            print('1',item)
                            list_data.append(item)

                if list_data:
                    serialize = PosCashiersLoginpSerializer(list_data, many=True)  # Corrected typo in "PosCashiersLoginpSerializer"
                    return Response(serialize.data)
                else:
                    print('no data')
                    return JsonResponse({'meeasge':'No Record Found'},status=500)



####* **************************** Generate Data For XREADING ****************************
@api_view(['GET','POST'])       
def generate_data_xread(request):
    if request.method =='GET':
        DateFrom = request.query_params.get("DateFrom")
        DateTo = request.query_params.get("DateTo")
        serial_number = getattr(request, "SERIALNO", None)
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
    

####* **************************** GET LATEST ZREAD ****************************
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def latest_zread(request):
    if request.method =='GET':
        try:
            latest_ = PosZReading.objects.order_by('-zread_no').first()

            serializers = PosZReadingSerializer(latest_,many=False)

            return Response(serializers.data)
        except Exception as e:
            print(e)
            traceback.print_exc()

####* **************************** GET LATEST ZREAD ****************************
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_zread_no(request):
    if request.method =='GET':
        try:
      

            dateFrom = request.GET.get('dateFrom')
            dateTo =  request.GET.get('dateTo')
            terminalNo =  request.GET.get('TerminalNo')
            siteNo =  request.GET.get('siteNo')

            _data = PosZReading.objects.filter(date_trans__range=(dateFrom,dateTo),terminal_no = terminalNo,site_code=siteNo)

            serializers = PosZReadingSerializer(_data,many=True)

            return Response(serializers.data)
        except Exception as e:
            print(e)
            traceback.print_exc()


    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_cashier_zread_no(request):
    if request.method =='GET':
        try:
            dateFrom = request.GET.get('dateFrom')
            dateTo =  request.GET.get('dateTo')
            terminalNo =  request.GET.get('TerminalNo')
            siteNo =  request.GET.get('siteNo')

            data = PosCashiersLogin.objects.filter(date_stamp__range=[dateFrom, dateTo], isshift_end='YES',islogout='YES',isxread='YES',user_rank='Cashier')
            serializers = PosCashiersLoginpSerializer(data,many=True)

            return Response(serializers.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
