
import datetime
import pytz

def GetPHilippineDateTime():
    ph_time_zone = pytz.timezone('Asia/Manila')
    current_datetime_ph = datetime.datetime.now(ph_time_zone).strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime_ph

def GetPHilippineDate():
    ph_time_zone = pytz.timezone('Asia/Manila')
    current_date_ph = datetime.datetime.now(ph_time_zone).strftime('%Y-%m-%d')
    return current_date_ph

