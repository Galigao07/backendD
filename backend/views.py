from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
from backend.models import User,POS_Terminal
from backend.serializers import UserSerializer,POS_TerminalSerializer
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
import json
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
    
import platform
import subprocess



from cryptography.hazmat.primitives import padding

@api_view(['GET'])
def user_login_api(request):
    if request.method == 'GET':
        # body_unicode = request.body
        # body_data = json.loads(body_unicode)
        username = request.GET.get('username')
        password = request.GET.get('password')
            # Extract username and password from the request body
        # username = body_data.get('username')
        # password = body_data.get('password')
        
        # print('user',body_data.get('username'))

        user = User.objects.filter(user_name=username).first()
        if user is not None:
            serial_number = get_serial_number()
            print('serial',serial_number)
            machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
            print('sad',machineInfo)
            infolist ={
                'UserRank': user.user_rank,
                'FullName':user.fullname,
                'UserID':user.id_code,
                'UserName':user.user_name,
                'TerminalNo': machineInfo.terminal_no,
                'SiteCode': machineInfo.site_no,
                'PTU': machineInfo.PTU_no
                
            }
            print('infolist',infolist)
            
            return JsonResponse({'Info':infolist}, status=200)
        else:
            # Login failed
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def decrypt_aes(encrypted_data, key):
    try:
        key = key.encode() if isinstance(key, str) else key
        cipher = AES.new(key, AES.MODE_ECB)  # Use appropriate mode (e.g., CBC) if known
        encrypted_data = base64.b64decode(encrypted_data)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
        return decrypted_data
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