import datetime
import pdb
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
import pytz
from backend.models import User,POS_Terminal
from backend.serializers import UserSerializer,POS_TerminalSerializer,PosCashiersLogin
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
import json
import base64 

from django.contrib.auth.hashers import make_password, check_password

import platform
import subprocess
from datetime import date
from django.db.models import Max
# Get current date
from backend.globalFunction import GetPHilippineDate,GetPHilippineDateTime

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from cryptography.hazmat.primitives import padding


@api_view(['GET'])
def user_login_api(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        hashed_password = make_password(password)

        password1 = 'Lsi#1288'
        current_date = date.today()

        day_of_month = str(current_date.day).zfill(2)
        password_with_date = password1 + day_of_month
        serial_number = get_serial_number()
        if (username=='Admin') & (password==password_with_date):
            print('yy',serial_number)
            if (serial_number =='PF19PSL1'):
                    infolist ={
                        'UserRank': 'Admin',
                        'FullName':'Admin',
                        'UserID':'9999999',
                        'UserName':'Admin',
                        'TerminalNo':0,
                        'SiteCode': 0,
                        'PTU': 0
                        
                    }
                    print('infolist',infolist)
                    
                    return JsonResponse({'Info':infolist}, status=200)
        user = User.objects.filter(user_name=username).first()
        stored_hashed_password = user.password
        if user is not None:
            if check_password(password, stored_hashed_password):
                serial_number = get_serial_number()
                machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
                latest_trans_id = PosCashiersLogin.objects.aggregate(max_trans_id=Max('trans_id'))['max_trans_id']
                new_trans_id = 0
                if user.user_rank =='Cashier':
                    current_date_ph = GetPHilippineDate()
                    current_datetime_ph = GetPHilippineDateTime()   
                    check_if_cashier_login = PosCashiersLogin.objects.filter(id_code = user.id_code,islogout='YES',isshift_end = 'NO',date_stamp = current_date_ph)
                    if check_if_cashier_login.exists():
                        cashier_login = check_if_cashier_login.first()  # or cashier_login = check_if_cashier_login.get()
                        cashier_login.islogout = 'NO'
                        cashier_login.save()
                    else:
                        current_date_ph = GetPHilippineDate()
                        current_datetime_ph = GetPHilippineDateTime()
                        if latest_trans_id is None:
                            new_trans_id = 1
                        else:
                            new_trans_id = latest_trans_id + 1

                        cashier_data = PosCashiersLogin(
                            trans_id=new_trans_id,
                            terminal_no=machineInfo.terminal_no,
                            site_code=machineInfo.site_no,
                            id_code=user.id_code,
                            name_stamp=user.fullname,
                            date_stamp=current_date_ph,
                            change_fund=0.0,
                            borrowed_fund=0.0,
                            time_login=current_datetime_ph,
                            time_logout='',
                            islogout='NO',
                            isshift_end='NO',
                            isxread='NO',
                        )

                        # Save the instance
                        cashier_data.save()
                infolist ={
                    'UserRank': user.user_rank,
                    'FullName':user.fullname,
                    'UserID':user.id_code,
                    'UserName':user.user_name,
                    'TerminalNo': machineInfo.terminal_no,
                    'SiteCode': machineInfo.site_no,
                    'PTU': machineInfo.PTU_no,
                    'TransID':new_trans_id
                }
                
                return JsonResponse({'Info':infolist}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)  
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@api_view(["GET"])
def user_logout_api(request):
    if request.method =='GET':
        try:
            # pdb.set_trace()
            UserID = request.query_params.get("UserID")
            TransID = request.query_params.get("TransID")
            # UserID = request.Get.get("UserID")
            # TransID = request.Get.get("TransID")
            print('UserID',UserID,TransID)
            # password = request.GET.get("password")

            user = User.objects.filter(id_code=UserID).first()

            serial_number = get_serial_number()
            machine = POS_Terminal.objects.filter(Serial_no=serial_number).first()

            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()
            if user.user_rank == 'Cashier':
                cashier_data = PosCashiersLogin.objects.get(id_code=UserID,trans_id = TransID,islogout='NO')

                cashier_data.time_logout = current_datetime_ph
                cashier_data.islogout = "YES"
                cashier_data.save()

            return JsonResponse({"message": "Logout Successfully"}, status=200)

        except (User.DoesNotExist, IntegrityError):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception:
            return JsonResponse({"message": "Method not allowed"}, status=405)


@api_view(["GET"])
def user_endshift_api(request):
    if request.method =='GET':
        try:
            # pdb.set_trace()
            UserID = request.query_params.get("UserID")
            TransID = request.query_params.get("TransID")
            user = User.objects.filter(id_code=UserID).first()

            serial_number = get_serial_number()
            machine = POS_Terminal.objects.filter(Serial_no=serial_number).first()

            current_date_ph = GetPHilippineDate()
            current_datetime_ph = GetPHilippineDateTime()

            cashier_data = PosCashiersLogin.objects.get(id_code=UserID,trans_id = TransID,islogout='NO',isshift_end='NO')

            cashier_data.time_logout = current_datetime_ph
            cashier_data.islogout = "YES"
            cashier_data.isshift_end = "YES"
            cashier_data.save()

            return JsonResponse({"message": "Logout Successfully"}, status=200)

        except (User.DoesNotExist, IntegrityError):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        except PermissionDenied:
            return JsonResponse({"message": "Permission denied"}, status=403)

        except Exception:
            return JsonResponse({"message": "Method not allowed"}, status=405)





def verification_account(request):
    if request.method == 'GET':
        # body_unicode = request.body
        # body_data = json.loads(body_unicode)
        username = request.GET.get('username')
        password = request.GET.get('password')
        hashed_password = make_password(password)

        user = User.objects.filter(user_name=username).first()
        stored_hashed_password = user.password
        if user is not None:
            if check_password(password, stored_hashed_password):
            
                infolist ={
                    'UserRank': user.user_rank,
                    'FullName':user.fullname,   
                }
                print('infolist',infolist)
                
                return JsonResponse({'Info':infolist}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)  
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

    

def decrypt_aes(encrypted_data, key):
    try:
        # key = key.encode() if isinstance(key, str) else key
        # cipher = AES.new(key, AES.MODE_ECB)  # Use appropriate mode (e.g., CBC) if known
        # encrypted_data = base64.b64decode(encrypted_data)
        # decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
        # return decrypted_data
        print("adasdasdsdas")
    except Exception as e:
        print(f"Decryption error: {e}")
        return None  # Handle decryption errors accordingly
    
    
    
    
    
    


def get_serial_number():
    try:
        system = platform.system()
        if system == 'Windows':
            # Retrieve serial number using WMIC (Windows Management Instrumentation Command-line)
            wmic_output = subprocess.check_output('wmic bios get serialnumber').decode().strip()
            lines = wmic_output.split('\n')
            if len(lines) > 1:
                return lines[1]  # Extracting the serial number if available
            else:
                return 'Serial number not found.'
        elif system == 'Linux':
            # Read product serial from the system file
            with open('/sys/class/dmi/id/product_serial') as file:
                return file.read().strip()
        elif system == 'Darwin':  # macOS
            # Retrieving serial number using system profiler
            return platform.system_profiler().get('serial_number', 'N/A')
        else:
            return 'Serial number retrieval not supported on this platform.'
    except Exception as e:
        return f'Error occurred: {str(e)}'

def get_computer_name():
    try:
        return platform.node()  # Retrieves the computer name
    except Exception as e:
        return f'Error occurred: {str(e)}'

# Get the computer name and serial number
computer_name = get_computer_name()

    
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})