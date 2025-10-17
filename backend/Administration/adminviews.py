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
