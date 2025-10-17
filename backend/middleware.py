# backend/middleware.py
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from urllib.parse import parse_qs



@database_sync_to_async
def get_user_from_token(token):
    from rest_framework_simplejwt.exceptions import InvalidToken
    from rest_framework_simplejwt.settings import api_settings
    from .auth.authentication import CookieJWTAuthentication
    try:
        auth = CookieJWTAuthentication()
        validated_token = auth.get_validated_token(token)
        user = auth.get_user(validated_token)
        print('auth', user)
        return user, validated_token
    except InvalidToken:
        return None, None

class CookieJWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate WebSocket using cookies.
    """
    async def __call__(self, scope, receive, send):
        close_old_connections()

        # Get cookies from headers
        headers = dict(scope.get("headers", []))
        cookies = headers.get(b'cookie', b'').decode()
        raw_token = None
        print('token',raw_token)

        # Parse cookies
        for c in cookies.split(";"):
            key, _, value = c.strip().partition("=")
            if key == "access_token":
                raw_token = value
                break
        user = None
        token_data = None
        if raw_token:
            user, token_data = await get_user_from_token(raw_token)

        # Attach user & extra info to scope
        scope["user"] = user if user else AnonymousUser()
        if token_data:
            scope["SERIALNO"] = token_data.get("SERIALNO")
            scope["TERMINALNO"] = token_data.get("TERMINALNO")
            scope["MACHINENO"] = token_data.get("MACHINENO")

        return await super().__call__(scope, receive, send)



# import threading
# from django.utils.deprecation import MiddlewareMixin

# _thread_locals = threading.local()

# def get_current_request_cookie():
#     request = getattr(_thread_locals, "request", None)
#     if not request:
#         return None
#     return request.COOKIES.get("access_token")

# class ThreadLocalMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         _thread_locals.request = request