import abc
import base64
import json
import locale
import os
import pdb
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from backend.models import (POSSettings,POS_Terminal)
from backend.serializers import (POSSettingsSerializer,POS_TerminalSerializer)
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

@api_view(['GET','POST'])
def systemSettings(request):
    if request.method == 'GET':
        try:
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no)
            serialize = POSSettingsSerializer(pos_settings,many=True)
            # print(serialize)
            return Response(serialize.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error':str(e)})
    if request.method == 'POST':
        try:
            recieve_data = json.loads(request.body)
            data = recieve_data.get('data')
            print('data',data)
            print('data', data['withHotel'])
            serial_number = get_serial_number()
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            # pdb.set_trace()
            pos_settings = POSSettings.objects.filter(terminal_no=machineInfo.terminal_no,site_no = machineInfo.site_no).first()
            if pos_settings:
                pos_settings.withHotel = data['withHotel']
                pos_settings.ProductColPerRows =  data['ProductColPerRows']
                pos_settings.TableColPerRows =  data['TableColPerRows']
                pos_settings.ShowArrowUpAndDown = data['ShowArrowUpAndDown']
                pos_settings.save()
                return Response('Success')
            return Response(serializer.errors)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({'error':str(e)})