
import datetime
import pytz
from .models import POSProductPrinter,POSSettings
from .serializers import POSProductPrinterSerializer

def GetPHilippineDateTime():
    ph_time_zone = pytz.timezone('Asia/Manila')
    current_datetime_ph = datetime.datetime.now(ph_time_zone).strftime('%m/%d/%Y %H:%M:%S %p')
    return current_datetime_ph

def GetPHilippineDate():
    ph_time_zone = pytz.timezone('Asia/Manila')
    current_date_ph = datetime.datetime.now(ph_time_zone).strftime('%Y-%m-%d')
    return current_date_ph

def GetSLnameInOtherAccounts():
    return True

# def GetCompanyConfig(fieldName):
#     result = POSProductPrinter.objects.values_list(fieldName, flat=True).first()
#     print('result',result)
#     return result

def GetCompanyConfig(fieldName):
    result = POSSettings.objects.values_list(fieldName, flat=True).first()
    print('result',result)
    return result


