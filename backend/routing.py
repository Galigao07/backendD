from django.urls import re_path
from backend.consumer import CountConsumer, POSextended

websocket_urlpatterns = [
    re_path(r'ws/count/$', CountConsumer.as_asgi()),
    re_path(r'ws/group_name/$', POSextended.as_asgi()),
    #  re_path(r'ws/group_name/(?P<extended_group>[^/]+)/$', POSextended.as_asgi()),
]

