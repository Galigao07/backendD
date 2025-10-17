"""
ASGI config for backendD project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendD.settings')

# application = get_asgi_application()

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendD.settings')
import django
django.setup()  # ✅ Important: setup Django before importing anything that uses settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# ✅ Configure settings before anything else

# ✅ Now safe to import modules that depend on Django
from backend.middleware import CookieJWTAuthMiddleware
import backend.routing

# ✅ Define application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": CookieJWTAuthMiddleware(
        URLRouter(
            backend.routing.websocket_urlpatterns
        )
    ),
})

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import backend.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendD.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             backend.routing.websocket_urlpatterns
#         )
#     ),
# })