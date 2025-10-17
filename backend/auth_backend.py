# app/auth_backend.py

from django.contrib.auth.backends import BaseBackend
from backend.models import User  # Adjust to your actual app name
from django.contrib.auth.hashers import check_password

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Authenticating: username={username}, password={password}")
        try:
            user = User.objects.get(user_name=username, sys_type='POS')
            print(f"Found user: {user.fullname}, active={user.active}")
            if user.active != 'Y':
                print("User not active")
                return None
            if check_password(password, user.password):
                print("Password correct")
                print(user)
                return user
            else:
                print("Password incorrect")
                return None
        except User.DoesNotExist:
            print("User does not exist")
            return None

    # def get_user(self, user_id):
    #     try:
    #         return Users.objects.get(pk=user_id)
    #     except Users.DoesNotExist:
    #         return None
