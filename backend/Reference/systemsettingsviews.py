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
from django.db import transaction
from django.db.models import  F, Value
from django.db.models.functions import Concat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def systemSettings(request):
#     if request.method == 'GET':
#         try:
#             serial_number = getattr(request, "SERIALNO", None)
#             # serial_number = get_serial_number()
#             machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
#             pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no)
#             serialize = POSSettingsSerializer(pos_settings,many=True)

#             pos_discount = PosDiscountSetup.objects.all()

#             discount = PosDiscountSetupSerializer(pos_discount,many=True)

#             data = {
#                 'Settings':serialize.data,
#                 'discount':discount.data
#             }
#             return Response(data)
#         except Exception as e:
#             print(e)
#             traceback.print_exc()
#             return Response({'error':str(e)})
#     if request.method == 'POST':
#         try:
#             recieve_data = json.loads(request.body)
#             data = recieve_data.get('data')
#             print(data)
#             serial_number = getattr(request, "SERIALNO", None)
#             # serial_number = get_serial_number()
#             machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
#             # pdb.set_trace()
#             # pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no).first()
#             # if pos_settings:
#             #     pos_settings.withHotel = data['withHotel']
#             #     pos_settings.ProductColPerRows =  data['ProductColPerRows']
#             #     pos_settings.TableColPerRows =  data['TableColPerRows']
#             #     pos_settings.ShowArrowUpAndDown = data['ShowArrowUpAndDown']
#             #     pos_settings.save()
#             # Fields to update/create (excluding discount amounts)
#             fields_to_update = [
#                 'Baggers', 'esc_mode', 'Salesman', 'Checker', 'EPS', 'PO_Charge', 
#                 'void_item', 'void_trans', 'price_override', 'vat_override',
#                 'trade_discount', 'senior_citizen', 'discount', 'product_details_decimals',
#                 'items_selling_price', 'cash', 'checks', 'debit', 'credit', 'PO',
#                 'gift_check', 'gift_check_with_serial_no', 'credit_sales', 'stale',
#                 'bankcard', 'multipleCheck', 'multipleCharge', 'returns', 'cashpullout',
#                 'soCancel', 'regular', 'with_barcode', 'order_type', 'printer_no',
#                 'printer_type', 'printer_name', 'virtual_receipt', 'manual_or',
#                 'change_fund', 'borrowed_fund', 'multiple_printer',
#                 'Allow_SalesOrderReceipt', 'Allow_WholeDay', 'allowed_retail',
#                 'include_servicecharge', 'ServiceCharge_DineIn', 'ServiceCharge_TakeOut',
#                 'ServiceCharge_Room', 'ServiceCharge_Retail', 'allow_duplicate_copy',
#                 'allow_service_charge_printout', 'allow_discount_percent', 'xz_filter',
#                 'showCreditlimit', 'ShowExtendedForm', 'Allow_BilloutBreakDown',
#                 'Allow_Duplicate_SO', 'Allow_cancel_transaction', 'allow_LiveQty',
#                 'CostComputation', 'VisibleAmount_tendered', 'Interchangeable_salesman',
#                 'weight_scale', 'weight_scale_start', 'weight_scale_last_degit_for_Qty',
#                 'BarcodeLenght', 'DecimalPlaces', 'RoundDigits', 'RoundType',
#                 'InputPrimaryMethod', 'item_search', 'item_display', 'Display_UOM',
#                 'Settle_order_only', 'Allow_filter_in_supervisor_cash_count',
#                 'Allow_display_live_qty', 'Allow_crystal_report', 'Allow_consignment_to_display',
#                 'Allow_TakeOut_Direct_Pay', 'withHotel', 'ProductColPerRows',
#                 'naac_discount','pwd_discount',
#                 'TableColPerRows', 'ShowArrowUpAndDown', 'transaction_discount'
#             ]

#             # Prepare dictionary with only allowed fields from `data`
#             defaults = {field: data[field] for field in fields_to_update if field in data}

#             # Update if exists, otherwise create
#             pos_settings, created = POSSettings.objects.update_or_create(
#                 terminal_no=machineInfo.terminal_no,
#                 site_no=machineInfo.site_no,
#                 defaults=defaults
#             )

#             if created:
#                 print("✅ POSSettings created")
#             else:
#                 print("✅ POSSettings updated")

#             SC = data['SCAmount']
#             PWD = data['PWDAmount']
#             NAAC = data['NAACDiscount']

#             PosDiscountSetup.objects.update_or_create(
#                 description = 'SC',
#                 disc_rate = SC
#             )
#             PosDiscountSetup.objects.update_or_create(
#                 description = 'PWD',
#                 disc_rate = PWD
#             )

#             PosDiscountSetup.objects.update_or_create(
#                 description = 'NAAC',
#                 disc_rate = NAAC
#             )



#             return Response('Success')
#         except Exception as e:
#             print(e)
#             traceback.print_exc()
#             return Response({'error':str(e)})