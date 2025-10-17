
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.exceptions import ObjectDoesNotExist
from backend.models import User  # your custom Users model


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        request.SERIALNO = validated_token.get("SERIALNO")
        request.TERMINALNO = validated_token.get("TERMINALNO")
        request.MACHINENO = validated_token.get("MACHINENO")
        request.TRANSID = validated_token.get("trans_id")
        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        try:
            id_code = validated_token["id_code"]   # or username
        except KeyError:
            raise InvalidToken("Token missing db_name or id_code")
        try:
            user = User.objects.get(autonum=id_code)
            return user
        except User.DoesNotExist:
            raise InvalidToken("User not found")
        

    #    def get_user(self, validated_token):
    #     try:
    #         id_code = validated_token["id_code"]   # or username
    #     except KeyError:
    #         raise InvalidToken("Token missing db_name or id_code")
    #     try:
    #         user = User.objects.get(id_code=id_code)
    #         return user
    #     except User.DoesNotExist:
    #         raise InvalidToken("User not found")  
 
